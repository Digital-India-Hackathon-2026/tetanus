import os
import ssl
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CommerceOS-Backend")

# Load local environment parameters
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "db.bkbvdhicsduuarsojlhf.supabase.co")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Global variables for caching discovered schema
discovered_table = None
column_mapping = {}
db_connected = False

# Hardcoded fallback mock catalog data
FALLBACK_PRODUCTS = [
  { "id": "ny-1", "name": "Stark Matte Black Backpack", "price": "₹4,500", "rating": 4.8, "category": "Luggage", "image_url": "" },
  { "id": "ny-2", "name": "Minimalist Mechanical Keyboard", "price": "₹6,800", "rating": 4.9, "category": "Electronics", "image_url": "" },
  { "id": "ny-3", "name": "Studio Noise Cancelling Headset", "price": "₹12,999", "rating": 4.7, "category": "Audio", "image_url": "" },
  { "id": "ny-4", "name": "Wool Felt Sleeve Organizer", "price": "₹1,499", "rating": 4.5, "category": "Office", "image_url": "" },
  { "id": "ny-5", "name": "Aluminum Desk Phone Dock", "price": "₹899", "rating": 4.6, "category": "Accessories", "image_url": "" },
  { "id": "dino-1", "name": "DinoBuilder Jurassic LEGO Set", "price": "₹1,299", "rating": 4.8, "category": "Toys & Games", "image_url": "" },
  { "id": "dino-2", "name": "Glow-in-the-Dark T-Rex Skeleton 3D Puzzle", "price": "₹499", "rating": 4.5, "category": "Toys & Games", "image_url": "" },
  { "id": "dino-3", "name": "National Geographic Big Book of Dinosaurs", "price": "₹799", "rating": 4.9, "category": "Toys & Games", "image_url": "" }
]

def format_price(value):
    """Helper to convert numeric database price representation to currency layout."""
    if value is None:
        return "₹0"
    try:
        if isinstance(value, (int, float)):
            return f"₹{value:,.0f}"
        val_str = str(value).strip()
        if not val_str.startswith("₹"):
            return f"₹{val_str}"
        return val_str
    except Exception:
        return str(value)

async def introspect_db_schema():
    """Tries to find products-like tables and maps common columns dynamically."""
    global discovered_table, column_mapping, db_connected
    
    if not DB_PASSWORD:
        logger.warning("[DB Discovery] DB_PASSWORD env variable is missing or empty. Startup fallback active.")
        db_connected = False
        return

    try:
        # Secure SSL Context setup for Supabase
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl=ssl_ctx,
            timeout=10
        )
        db_connected = True
    except Exception as e:
        logger.error(f"[DB Discovery] Connection setup failed: {e}. Falling back to mock catalog.")
        db_connected = False
        return

    try:
        # 1. Fetch tables in public schema
        tables = await conn.fetch(
            """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
              AND table_type = 'BASE TABLE';
            """
        )
        
        table_names = [r["table_name"] for r in tables]
        logger.info(f"[DB Discovery] Found public tables: {table_names}")

        # Search for first table matching keyword catalog indicators
        target_keywords = ["product", "item", "inventory", "catalog", "goods"]
        for tbl in table_names:
            tbl_lower = tbl.lower()
            if any(kw in tbl_lower for kw in target_keywords):
                discovered_table = tbl
                break

        if not discovered_table:
            logger.warning("[DB Discovery] No table name matched products-like keywords. Falling back to mock mode.")
            await conn.close()
            db_connected = False
            return

        # 2. Introspect columns of selected table
        columns = await conn.fetch(
            """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
              AND table_name = $1;
            """,
            discovered_table
        )
        col_names = [r["column_name"] for r in columns]
        logger.info(f"[DB Discovery] Found columns for '{discovered_table}': {col_names}")

        # Match columns against key product attributes
        mapping = {}
        
        # ID Column Mapping
        id_candidates = ["id", "product_id", "item_id", "uuid", "uid"]
        mapping["id"] = next((c for c in col_names if c.lower() in id_candidates), col_names[0])

        # Name Column Mapping
        name_candidates = ["name", "title", "product_name", "item_name", "label", "heading"]
        mapping["name"] = next((c for c in col_names if c.lower() in name_candidates), None)

        # Price Column Mapping
        price_candidates = ["price", "amount", "cost", "unit_price", "rate", "value"]
        mapping["price"] = next((c for c in col_names if c.lower() in price_candidates), None)

        # Image URL Column Mapping
        image_candidates = ["image_url", "image", "img_url", "img", "picture", "pic"]
        mapping["image_url"] = next((c for c in col_names if c.lower() in image_candidates), None)

        # Rating Column Mapping
        rating_candidates = ["rating", "score", "stars", "rating_score"]
        mapping["rating"] = next((c for c in col_names if c.lower() in rating_candidates), None)

        # Category Column Mapping
        category_candidates = ["category", "group", "type", "tag", "genre"]
        mapping["category"] = next((c for c in col_names if c.lower() in category_candidates), None)

        # Stock Column Mapping
        stock_candidates = ["stock", "quantity", "inventory", "units", "count"]
        mapping["stock"] = next((c for c in col_names if c.lower() in stock_candidates), None)

        column_mapping = mapping
        logger.info(f"[DB Discovery] SUCCESS! Discovered Table: '{discovered_table}' | Mapping: {column_mapping}")

    except Exception as e:
        logger.error(f"[DB Discovery] Introspection error: {e}. Falling back to mock catalog.")
        db_connected = False
    finally:
        await conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute database schema discover mappings on startup
    await introspect_db_schema()
    yield
    # Cleanup operations here on shutdown if necessary

app = FastAPI(lifespan=lifespan)

# Add CORS Policy to resolve browser local requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/products/nearby")
async def get_nearby_products():
    """Serves 6-10 products from Supabase table or returns fallback mock data."""
    global discovered_table, column_mapping, db_connected

    if not db_connected or not discovered_table:
        logger.info("[API Response] Serving fallback mockup data due to inactive database state.")
        return {
            "source": "mock",
            "products": FALLBACK_PRODUCTS
        }

    try:
        # Secure SSL connection
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl=ssl_ctx,
            timeout=5
        )

        # Dynamically build SELECT columns query based on mappings
        select_cols = []
        for key, col_name in column_mapping.items():
            if col_name:
                select_cols.append(f'"{col_name}" AS {key}')

        # Handle mapping omissions safely
        if not select_cols:
            raise ValueError("No mapped columns discovered.")

        query_str = f"SELECT {', '.join(select_cols)} FROM \"{discovered_table}\" LIMIT 8;"
        records = await conn.fetch(query_str)
        await conn.close()

        formatted_products = []
        for rec in records:
            # Map values with fallback defaults if column names were missing in database schema
            id_val = str(rec.get("id") or "")
            name_val = str(rec.get("name") or "Unnamed Product")
            price_val = format_price(rec.get("price"))
            image_url_val = str(rec.get("image_url") or "")
            
            # Safe numeric conversion defaults
            rating_val = 4.5
            if rec.get("rating") is not None:
                try:
                    rating_val = float(rec.get("rating"))
                except ValueError:
                    pass

            category_val = str(rec.get("category") or "General")

            formatted_products.append({
                "id": id_val,
                "name": name_val,
                "price": price_val,
                "image_url": image_url_val,
                "rating": rating_val,
                "category": category_val
            })

        logger.info(f"[API Response] Served {len(formatted_products)} items from Supabase database table.")
        return {
            "source": "database",
            "products": formatted_products
        }

    except Exception as e:
        logger.error(f"[API Response] Query execution error: {e}. Serving mock catalog fallback.")
        return {
            "source": "mock",
            "products": FALLBACK_PRODUCTS
        }
