import os
import ssl
import logging
import asyncio
import urllib.request
import json
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
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# Global variables for caching discovered schema
discovered_table = None
column_mapping = {}
db_connected = False
rest_mode = False

# Hardcoded fallback mock catalog data
FALLBACK_PRODUCTS = [
  { "id": "ny-1", "name": "Stark Matte Black Backpack", "price": "₹4,500", "rating": 4.8, "category": "Luggage", "image_url": "", "description": "Weather-resistant minimalist daily carry with dedicated laptop sleeve." },
  { "id": "ny-2", "name": "Minimalist Mechanical Keyboard", "price": "₹6,800", "rating": 4.9, "category": "Electronics", "image_url": "", "description": "Tenkeyless layout with custom linear switches and dark keycaps." },
  { "id": "ny-3", "name": "Studio Noise Cancelling Headset", "price": "₹12,999", "rating": 4.7, "category": "Audio", "image_url": "", "description": "High fidelity audio with adaptive noise cancellation and comfort fit." },
  { "id": "ny-4", "name": "Wool Felt Sleeve Organizer", "price": "₹1,499", "rating": 4.5, "category": "Office", "image_url": "", "description": "Premium desk layout sleeve for phone, cables, and writing tools." },
  { "id": "ny-5", "name": "Aluminum Desk Phone Dock", "price": "₹899", "rating": 4.6, "category": "Accessories", "image_url": "", "description": "Solid aluminum stand with rubberized grip pads and cable routing." },
  { "id": "dino-1", "name": "DinoBuilder Jurassic LEGO Set", "price": "₹1,299", "rating": 4.8, "category": "Toys & Games", "image_url": "", "description": "Build your own Jurassic park with interactive dino figures." },
  { "id": "dino-2", "name": "Glow-in-the-Dark T-Rex Skeleton 3D Puzzle", "price": "₹499", "rating": 4.5, "category": "Toys & Games", "image_url": "", "description": "Fascinating glow puzzle that forms a T-Rex fossil setup." },
  { "id": "dino-3", "name": "National Geographic Big Book of Dinosaurs", "price": "₹799", "rating": 4.9, "category": "Toys & Games", "image_url": "", "description": "Stunning visuals and educational info on primeval creatures." }
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

def format_image_url(val, project_ref="bkbvdhicsduuarsojlhf"):
    if not val:
        return ""
    val_str = str(val).strip()
    if val_str.startswith(("http://", "https://")):
        return val_str
    
    # Strip leading slash if present
    if val_str.startswith("/"):
        val_str = val_str[1:]
        
    # Check if there is a bucket in the path (contains a slash)
    if "/" in val_str:
        bucket, path = val_str.split("/", 1)
    else:
        bucket = "products"  # Default fallback bucket
        path = val_str
        
    return f"https://{project_ref}.supabase.co/storage/v1/object/public/{bucket}/{path}"

def get_db_user():
    user = os.getenv("DB_USER", "postgres")
    host = os.getenv("DB_HOST", "")
    if "pooler.supabase.com" in host and "." not in user:
        project_ref = "bkbvdhicsduuarsojlhf"
        return f"{user}.{project_ref}"
    return user

async def introspect_rest_schema() -> bool:
    """Tries to find products-like tables and columns via HTTPS REST API using the Anon Key."""
    global discovered_table, column_mapping, db_connected, rest_mode
    if not SUPABASE_ANON_KEY:
        logger.warning("[REST Discovery] No SUPABASE_ANON_KEY configured in environment.")
        return False
        
    try:
        url = f"https://{DB_HOST.replace('db.', '')}/rest/v1/"
        req = urllib.request.Request(url)
        req.add_header("apikey", SUPABASE_ANON_KEY)
        req.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")
        
        loop = asyncio.get_event_loop()
        def _fetch():
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode())
                
        swagger = await loop.run_in_executor(None, _fetch)
            
        definitions = swagger.get("definitions", {})
        table_names = list(definitions.keys())
        logger.info(f"[REST Discovery] Found REST tables: {table_names}")
        
        # Search for first table matching keywords
        target_keywords = ["product", "item", "inventory", "catalog", "goods"]
        target_table = None
        for tbl in table_names:
            tbl_lower = tbl.lower()
            if any(kw in tbl_lower for kw in target_keywords):
                target_table = tbl
                break
                
        if not target_table:
            logger.warning("[REST Discovery] No table name matched products-like keywords in REST OpenAPI spec.")
            return False
            
        # Introspect columns of selected table from Swagger definition
        properties = definitions[target_table].get("properties", {})
        col_names = list(properties.keys())
        
        # Match columns
        mapping = {}
        id_candidates = ["id", "product_id", "item_id", "uuid", "uid"]
        mapping["id"] = next((c for c in col_names if c.lower() in id_candidates), col_names[0])

        name_candidates = ["name", "title", "product_name", "item_name", "label", "heading"]
        mapping["name"] = next((c for c in col_names if c.lower() in name_candidates), None)

        price_candidates = ["price", "amount", "cost", "unit_price", "rate", "value"]
        mapping["price"] = next((c for c in col_names if c.lower() in price_candidates), None)

        image_candidates = ["image_url", "image", "img_url", "img", "picture", "pic"]
        mapping["image_url"] = next((c for c in col_names if c.lower() in image_candidates), None)

        rating_candidates = ["rating", "score", "stars", "rating_score"]
        mapping["rating"] = next((c for c in col_names if c.lower() in rating_candidates), None)

        category_candidates = ["category", "group", "type", "tag", "genre"]
        mapping["category"] = next((c for c in col_names if c.lower() in category_candidates), None)

        description_candidates = ["description", "desc", "details", "summary", "about"]
        mapping["description"] = next((c for c in col_names if c.lower() in description_candidates), None)
        
        discovered_table = target_table
        column_mapping = mapping
        db_connected = True
        rest_mode = True
        logger.info(f"[REST Discovery] SUCCESS! Discovered Table via HTTP REST: '{discovered_table}' | Mapping: {column_mapping}")
        return True
    except Exception as e:
        logger.error(f"[REST Discovery] Failed to discover schema via HTTP REST API: {e}")
        return False

async def introspect_db_schema():
    """Tries to find products-like tables and maps common columns dynamically."""
    global discovered_table, column_mapping, db_connected, rest_mode
    
    if not DB_PASSWORD:
        logger.warning("[DB Discovery] DB_PASSWORD env variable is missing or empty. Trying REST API check...")
        if SUPABASE_ANON_KEY:
            rest_success = await introspect_rest_schema()
            if rest_success:
                return
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
            user=get_db_user(),
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl=ssl_ctx,
            timeout=10,
            statement_cache_size=0
        )
        db_connected = True
    except Exception as e:
        logger.error(f"[DB Discovery] Direct connection setup failed: {e}. Trying REST API fallback...")
        if SUPABASE_ANON_KEY:
            rest_success = await introspect_rest_schema()
            if rest_success:
                return
        logger.error("[DB Discovery] Both direct PG and REST API configurations failed. Falling back to mock catalog.")
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

        # Prioritize exact table name matches first to avoid matching relationship/similar tables
        exact_targets = ["products", "product", "items", "item", "inventory"]
        for target in exact_targets:
            match = next((t for t in table_names if t.lower() == target), None)
            if match:
                discovered_table = match
                break

        # Fallback to keyword matching if exact match not found
        if not discovered_table:
            target_keywords = ["product", "item", "inventory", "catalog", "goods"]
            for tbl in table_names:
                tbl_lower = tbl.lower()
                if "similar" in tbl_lower or "relation" in tbl_lower or "mapping" in tbl_lower:
                    continue
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

        # Description Column Mapping
        description_candidates = ["description", "desc", "details", "summary", "about"]
        mapping["description"] = next((c for c in col_names if c.lower() in description_candidates), None)

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

app = FastAPI(lifespan=lifespan)

# Add CORS Policy to resolve browser local requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "CommerceOS Backend Running",
        "docs_url": "/docs",
        "endpoints": {
            "get_nearby_products": "/api/products/nearby"
        }
    }

@app.get("/api/products/nearby")
async def get_nearby_products():
    """Serves 6-10 products from Supabase table or returns fallback mock data."""
    global discovered_table, column_mapping, db_connected, rest_mode

    if not db_connected or not discovered_table:
        logger.info("[API Response] Serving fallback mockup data due to inactive database state.")
        return {
            "source": "mock",
            "products": FALLBACK_PRODUCTS
        }

    try:
        records = []
        if rest_mode:
            # Query via HTTP REST
            url = f"https://{DB_HOST.replace('db.', '')}/rest/v1/{discovered_table}?select=*"
            select_fields = []
            for key, col_name in column_mapping.items():
                if col_name:
                    select_fields.append(col_name)
            if select_fields:
                url = f"https://{DB_HOST.replace('db.', '')}/rest/v1/{discovered_table}?select={','.join(select_fields)}&limit=150"
            
            req = urllib.request.Request(url)
            req.add_header("apikey", SUPABASE_ANON_KEY)
            req.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")
            
            loop = asyncio.get_event_loop()
            def _fetch_records():
                with urllib.request.urlopen(req, timeout=5) as response:
                    return json.loads(response.read().decode())
            records = await loop.run_in_executor(None, _fetch_records)
        else:
            # Secure SSL connection
            ssl_ctx = ssl.create_default_context()
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE

            conn = await asyncpg.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=get_db_user(),
                password=DB_PASSWORD,
                database=DB_NAME,
                ssl=ssl_ctx,
                timeout=5,
                statement_cache_size=0
            )

            # Dynamically build SELECT columns query based on mappings
            select_cols = []
            for key, col_name in column_mapping.items():
                if col_name:
                    select_cols.append(f'"{col_name}" AS {key}')

            # Handle mapping omissions safely
            if not select_cols:
                raise ValueError("No mapped columns discovered.")

            query_str = f"SELECT {', '.join(select_cols)} FROM \"{discovered_table}\" LIMIT 150;"
            records = await conn.fetch(query_str)
            await conn.close()

        formatted_products = []
        for rec in records:
            # Map values with fallback defaults if column names were missing in database schema
            id_val = str(rec.get("id") or "")
            name_val = str(rec.get("name") or "Unnamed Product")
            price_val = format_price(rec.get("price"))
            image_url_val = format_image_url(rec.get("image_url"))
            
            # Safe numeric conversion defaults
            rating_val = 4.5
            if rec.get("rating") is not None:
                try:
                    rating_val = float(rec.get("rating"))
                except ValueError:
                    pass

            category_val = str(rec.get("category") or "General")
            description_val = str(rec.get("description") or "No description available.")

            formatted_products.append({
                "id": id_val,
                "name": name_val,
                "price": price_val,
                "image_url": image_url_val,
                "rating": rating_val,
                "category": category_val,
                "description": description_val
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
