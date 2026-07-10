import pandas as pd
import numpy as np
import uuid
import json
import re
import html
import random
from datetime import datetime, timedelta
from rapidfuzz import fuzz
from pathlib import Path
import time
import math

# --- Configuration ---
DATASET1_PATH = "dataset1_deduplicated.csv"
DATASET2_PATH = "dataset2_deduplicated.csv"
OUTPUT_DIR = Path(".")

# Canonical categories
CANONICAL_CATEGORIES = [
    "Electronics", "Fashion", "Beauty", "Home", "Kitchen", 
    "Groceries", "Sports", "Books", "Health", "Office", 
    "Automotive", "Pet Supplies", "Other"
]

# Quotas for balanced selection (Total 150)
CATEGORY_QUOTAS = {
    "Electronics": 25,
    "Fashion": 25,
    "Beauty": 15,
    "Home": 15,
    "Kitchen": 15,
    "Groceries": 15,
    "Sports": 10,
    "Books": 5,
    "Health": 10,
    "Office": 5,
    "Automotive": 5,
    "Pet Supplies": 5,
    "Other": 0
}

# Missions
MISSIONS = [
    "Hostel Setup", "Birthday", "Gym", "Work From Home", 
    "Weekly Prep", "Movie Night", "Travel Essentials"
]

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def safe_float(val):
    try:
        # Extract digits and dots
        v = str(val).replace(',', '')
        matches = re.findall(r'[\d\.]+', v)
        if matches:
            return float(matches[0])
        return np.nan
    except:
        return np.nan

def clean_text(text):
    if pd.isna(text): return np.nan
    text = str(text)
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', ' ', text) # remove html
    text = text.encode('utf-8', 'ignore').decode('utf-8')
    text = re.sub(r'\s+', ' ', text).strip() # replace multiple spaces
    return text if text else np.nan

def map_category(raw_cat):
    if pd.isna(raw_cat): return "Other"
    rc = str(raw_cat).lower()
    if any(x in rc for x in ["mobile", "laptop", "computer", "smartwatch", "electronics", "audio", "camera", "tablet"]): return "Electronics"
    if any(x in rc for x in ["clothing", "wear", "shoes", "fashion", "apparel", "jewellery", "watch"]): return "Fashion"
    if any(x in rc for x in ["makeup", "skin", "hair", "perfume", "beauty", "cosmetic", "soap", "cream", "lotion"]): return "Beauty"
    if any(x in rc for x in ["furniture", "decor", "home", "bedding", "bath"]): return "Home"
    if any(x in rc for x in ["kitchen", "cookware", "appliance", "dining"]): return "Kitchen"
    if any(x in rc for x in ["food", "grocery", "snack", "beverage", "chocolate", "spice", "masala"]): return "Groceries"
    if any(x in rc for x in ["sport", "fitness", "exercise", "outdoor"]): return "Sports"
    if any(x in rc for x in ["book", "novel", "literature", "education"]): return "Books"
    if any(x in rc for x in ["health", "supplement", "vitamin", "medical", "nutrition"]): return "Health"
    if any(x in rc for x in ["office", "stationery", "pen", "paper"]): return "Office"
    if any(x in rc for x in ["auto", "car", "bike", "vehicle"]): return "Automotive"
    if any(x in rc for x in ["pet", "dog", "cat", "animal"]): return "Pet Supplies"
    return "Other"

def parse_specs(text):
    if pd.isna(text): return "{}"
    specs = {}
    parts = re.split(r'[,|;]', str(text))
    for p in parts:
        kv = p.split(':')
        if len(kv) >= 2:
            specs[kv[0].strip()[:50]] = ':'.join(kv[1:]).strip()[:100]
        else:
            if len(p.strip()) > 3 and len(p.strip()) < 50:
                specs["Detail"] = p.strip()
    return json.dumps(specs)

def is_valid_url(url):
    if pd.isna(url): return False
    return bool(re.match(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', str(url)))

def process():
    start_time = time.time()
    
    # ----------------------------------------------------
    # STEP 1 & 2: Load and Standardize
    # ----------------------------------------------------
    log("Loading and standardizing datasets...")
    df1 = pd.read_csv(DATASET1_PATH, on_bad_lines='skip', engine='python')
    df2 = pd.read_csv(DATASET2_PATH, on_bad_lines='skip', engine='python')
    
    # DF1 Mapping
    d1 = pd.DataFrame()
    d1['name'] = df1['Product Title']
    d1['category_raw'] = df1['Bb Category']
    d1['description'] = df1['Product Description']
    d1['brand'] = df1['Brand']
    d1['price'] = df1['Price'].apply(safe_float)
    d1['mrp'] = df1['Mrp'].apply(safe_float)
    d1['image_url'] = df1['Image Url']
    d1['product_url'] = df1['Url']
    d1['specifications_raw'] = df1['Quantity Or Pack Size']
    d1['rating'] = np.nan
    d1['review_count'] = np.nan
    d1['seller'] = np.nan
    d1['source'] = 'DF1'
    
    # DF2 Mapping
    d2 = pd.DataFrame()
    d2['name'] = df2['title']
    d2['category_raw'] = df2['category_1'].fillna(df2['category_2']).fillna(df2['category_3'])
    d2['description'] = df2['description']
    d2['brand'] = np.nan  # Try to extract later if needed
    d2['price'] = df2['selling_price'].apply(safe_float)
    d2['mrp'] = df2['mrp'].apply(safe_float)
    d2['image_url'] = df2['image_links']
    d2['product_url'] = np.nan
    d2['specifications_raw'] = df2['highlights']
    d2['rating'] = df2['product_rating'].apply(safe_float)
    d2['review_count'] = np.nan
    d2['seller'] = df2['seller_name']
    d2['source'] = 'DF2'
    
    log(f"DF1 loaded: {len(d1)} rows")
    log(f"DF2 loaded: {len(d2)} rows")
    
    # Merge datasets intelligently (Simple concat then dedup by exact name for speed, then combine info)
    log("Merging datasets...")
    df = pd.concat([d1, d2], ignore_index=True)
    
    # Group by exact name (lowercased) and take the best non-null value
    df['name_lower'] = df['name'].astype(str).str.lower().str.strip()
    # Sort to ensure richest row is first (count non-nulls)
    df['non_null_count'] = df.notna().sum(axis=1)
    df = df.sort_values('non_null_count', ascending=False)
    
    df_merged = df.groupby('name_lower').first().reset_index()
    log(f"Merged dataset rows: {len(df_merged)}")
    
    # ----------------------------------------------------
    # STEP 3: Text Cleaning
    # ----------------------------------------------------
    log("Cleaning text...")
    for col in ['name', 'brand', 'category_raw']:
        df_merged[col] = df_merged[col].apply(lambda x: str(x).title().strip() if pd.notna(x) else x)
    df_merged['description'] = df_merged['description'].apply(clean_text)
    
    # ----------------------------------------------------
    # STEP 4: Handle Missing Values
    # ----------------------------------------------------
    log("Handling missing values...")
    # Attempt to recover price from mrp if missing
    df_merged['price'] = df_merged['price'].fillna(df_merged['mrp'])
    # Filter critical missing
    missing_critical = df_merged[df_merged[['name', 'price']].isna().any(axis=1)]
    missing_critical.to_csv(OUTPUT_DIR / 'missing_value_report.csv', index=False)
    df_merged = df_merged.dropna(subset=['name', 'price'])
    # Fill description if missing
    df_merged['description'] = df_merged['description'].fillna(df_merged['name'] + " - High quality product.")
    df_merged['brand'] = df_merged['brand'].fillna("Generic")
    df_merged['rating'] = df_merged['rating'].fillna(random.uniform(3.5, 4.8)) # Synthetic fallback
    
    # Synthetic review counts
    def gen_rc(row):
        # Base it on rating and some randomness
        base = max(0, (row['rating'] - 3) * 50)
        return int(base + random.randint(1, 500))
    df_merged['review_count'] = df_merged['review_count'].fillna(df_merged.apply(gen_rc, axis=1)).astype(int)
    
    log(f"Rows after missing value drop: {len(df_merged)}")
    
    # ----------------------------------------------------
    # STEP 5: Category Hierarchy
    # ----------------------------------------------------
    log("Normalizing categories...")
    df_merged['category'] = df_merged['category_raw'].apply(map_category)
    cat_mapping = df_merged[['category_raw', 'category']].drop_duplicates()
    cat_mapping.to_csv(OUTPUT_DIR / 'category_mapping.csv', index=False)
    
    # ----------------------------------------------------
    # STEP 6: Specification Parser
    # ----------------------------------------------------
    log("Parsing specifications...")
    df_merged['specifications'] = df_merged['specifications_raw'].apply(parse_specs)
    
    # ----------------------------------------------------
    # STEP 7: Image Validation
    # ----------------------------------------------------
    log("Validating images (Structural)...")
    df_merged['image_valid'] = df_merged['image_url'].apply(is_valid_url)
    img_report = df_merged[['name', 'image_url', 'image_valid']]
    img_report.to_csv(OUTPUT_DIR / 'image_validation_report.csv', index=False)
    
    # ----------------------------------------------------
    # STEP 8: Product Validation
    # ----------------------------------------------------
    log("Validating products (Anomalies)...")
    anomalies = []
    
    def validate_row(row):
        is_anom = False
        reasons = []
        if pd.isna(row['price']) or row['price'] <= 0:
            is_anom = True; reasons.append("Invalid Price")
        if pd.notna(row['rating']) and (row['rating'] < 0 or row['rating'] > 5):
            is_anom = True; reasons.append("Invalid Rating")
        if pd.isna(row['description']) or len(str(row['description'])) < 20:
            is_anom = True; reasons.append("Description too short")
        if not row['image_valid']:
            is_anom = True; reasons.append("Invalid Image URL")
            
        if is_anom:
            anom_dict = row.to_dict()
            anom_dict['anomaly_reason'] = "; ".join(reasons)
            anomalies.append(anom_dict)
        return not is_anom

    valid_mask = df_merged.apply(validate_row, axis=1)
    df_anomalies = pd.DataFrame(anomalies)
    if not df_anomalies.empty:
        df_anomalies.to_csv(OUTPUT_DIR / 'anomaly_report.csv', index=False)
    
    df_merged = df_merged[valid_mask].copy()
    log(f"Rows after anomaly filter: {len(df_merged)}")
    
    # Assign UUIDs
    df_merged['product_id'] = [str(uuid.uuid4()) for _ in range(len(df_merged))]
    
    # ----------------------------------------------------
    # STEP 9: Product Quality Score
    # ----------------------------------------------------
    log("Computing Product Quality Scores...")
    def compute_score(row):
        score = 0
        # 25% Info completeness
        cols = ['name', 'category', 'price', 'description', 'brand', 'rating', 'specifications', 'image_url', 'product_url']
        comp = sum([1 for c in cols if pd.notna(row[c]) and row[c] != '']) / len(cols)
        score += comp * 25
        
        # 20% Description Quality (len > 100 gets max)
        desc_len = len(str(row['description']))
        score += min(20, (desc_len / 150) * 20)
        
        # 15% Spec Richness
        try:
            specs_count = len(json.loads(row['specifications']).keys())
            score += min(15, (specs_count / 3) * 15)
        except:
            pass
            
        # 10% Rating
        score += (row['rating'] / 5.0) * 10
        
        # 10% Review Count (synthetic)
        score += min(10, random.uniform(2, 10))
        
        # 10% Brand
        if str(row['brand']).lower() != "generic": score += 10
        
        # 5% Image
        if row['image_valid']: score += 5
        
        # 5% URL
        if is_valid_url(row['product_url']): score += 5
            
        return score
        
    df_merged['quality_score'] = df_merged.apply(compute_score, axis=1)
    df_merged[['product_id', 'name', 'quality_score']].to_csv(OUTPUT_DIR / 'product_quality_scores.csv', index=False)
    
    # ----------------------------------------------------
    # STEP 10: Balanced Product Selection
    # ----------------------------------------------------
    log("Selecting 150 balanced products...")
    final_150 = []
    
    for cat, quota in CATEGORY_QUOTAS.items():
        cat_df = df_merged[df_merged['category'] == cat].sort_values('quality_score', ascending=False)
        selected = cat_df.head(quota)
        final_150.append(selected)
        
    df_150 = pd.concat(final_150)
    
    # If we don't have exactly 150 due to missing categories, fill the rest from the top overall
    if len(df_150) < 150:
        remaining = 150 - len(df_150)
        used_ids = df_150['product_id'].tolist()
        pool = df_merged[~df_merged['product_id'].isin(used_ids)].sort_values('quality_score', ascending=False)
        df_150 = pd.concat([df_150, pool.head(remaining)])
        
    # Strictly limit to 150
    df_150 = df_150.head(150)
    log(f"Final catalog size: {len(df_150)}")
    
    # Clean up columns for master
    master_cols = ['product_id', 'name', 'brand', 'category', 'price', 'mrp', 'description', 'specifications', 'rating', 'review_count', 'image_url', 'product_url', 'quality_score']
    df_master = df_merged[master_cols]
    df_150_clean = df_150[master_cols]
    
    df_master.to_csv(OUTPUT_DIR / 'master_products.csv', index=False)
    df_150_clean.to_csv(OUTPUT_DIR / 'products_final_150.csv', index=False)
    
    # ----------------------------------------------------
    # STEP 11: Generate Inventory
    # ----------------------------------------------------
    log("Generating inventory...")
    inv_data = []
    for pid in df_150_clean['product_id']:
        stock = random.choices([0, random.randint(1, 10), random.randint(11, 500)], weights=[0.1, 0.2, 0.7])[0]
        status = "OUT_OF_STOCK" if stock == 0 else "LOW_STOCK" if stock <= 10 else "IN_STOCK"
        inv_data.append({
            "product_id": pid,
            "stock_count": stock,
            "status": status,
            "updated_at": datetime.now().isoformat()
        })
    pd.DataFrame(inv_data).to_csv(OUTPUT_DIR / 'inventory.csv', index=False)
    
    # ----------------------------------------------------
    # STEP 12: Generate Similar Products
    # ----------------------------------------------------
    log("Generating similar products...")
    similar_data = []
    # Using df_150 for this inner cross join equivalent
    for idx, row in df_150_clean.iterrows():
        # Find candidates in same category
        candidates = df_150_clean[(df_150_clean['category'] == row['category']) & (df_150_clean['product_id'] != row['product_id'])].copy()
        
        if len(candidates) > 0:
            # Score similarity
            def sim_score(cand):
                score = 0
                if cand['brand'] == row['brand']: score += 30
                # Price diff
                p_diff = abs(cand['price'] - row['price']) / max(row['price'], 1)
                score += max(0, 40 - (p_diff * 40))
                # Rating proximity
                score += 10 - abs(cand['rating'] - row['rating']) * 2
                # Quality score adds a tiny boost
                score += cand['quality_score'] * 0.1
                return score
                
            candidates['sim'] = candidates.apply(sim_score, axis=1)
            best = candidates.sort_values('sim', ascending=False).head(random.randint(2, 5))
            
            for _, b in best.iterrows():
                similar_data.append({
                    "product_id": row['product_id'],
                    "similar_product_id": b['product_id'],
                    "similarity_score": round(b['sim'] / 100, 4)
                })
    pd.DataFrame(similar_data).to_csv(OUTPUT_DIR / 'similar_products.csv', index=False)
    
    # ----------------------------------------------------
    # STEP 13: Generate ProductMissionMapping & Bundles
    # ----------------------------------------------------
    log("Generating ProductMissionMapping & Bundles...")
    mission_mapping = []
    mission_bundles = []
    
    # Predefined mission catalog
    MISSION_CATALOG = {
        "Hostel Setup": ["Home", "Kitchen", "Electronics"],
        "Birthday": ["Fashion", "Beauty", "Books", "Other"],
        "Gym": ["Sports", "Health", "Fashion"],
        "Work From Home": ["Electronics", "Office", "Home"],
        "Weekly Prep": ["Groceries", "Kitchen", "Pet Supplies"],
        "Movie Night": ["Groceries", "Electronics", "Home"],
        "Travel Essentials": ["Beauty", "Fashion", "Automotive", "Health"]
    }
    
    # Ensure every product has at least one mission
    for pid, cat in zip(df_150_clean['product_id'], df_150_clean['category']):
        # Find missions matching this category, or default to a random mission
        suitable_missions = [m for m, cats in MISSION_CATALOG.items() if cat in cats]
        if not suitable_missions:
            suitable_missions = list(MISSION_CATALOG.keys())
            
        # Assign 1 to 3 missions to each product
        num_missions = random.randint(1, 3)
        assigned = random.sample(suitable_missions, min(num_missions, len(suitable_missions)))
        
        for m in assigned:
            conf = round(random.uniform(0.70, 1.00), 2)
            mission_mapping.append({
                "mission_name": m,
                "product_id": pid,
                "confidence_score": conf
            })

    pd.DataFrame(mission_mapping).to_csv(OUTPUT_DIR / 'ProductMissionMapping.csv', index=False)
    
    # Generate Mission Bundles
    # Schema: bundle_name, mission, priority, product_id
    bundle_names = {
        "Hostel Setup": "Dorm Starter Kit",
        "Birthday": "Birthday Gift Box",
        "Gym": "Ultimate Fitness Pack",
        "Work From Home": "WFH Essentials",
        "Weekly Prep": "Sunday Meal Prep",
        "Movie Night": "Snack & Watch",
        "Travel Essentials": "Weekend Getaway"
    }
    
    priorities = ["HIGH", "MEDIUM", "LOW"]
    
    for mission in MISSION_CATALOG.keys():
        # Get products mapped to this mission
        mission_products = [item['product_id'] for item in mission_mapping if item['mission_name'] == mission]
        if not mission_products: continue
            
        # Create a bundle with 3 to 6 products
        bundle_size = min(len(mission_products), random.randint(3, 6))
        selected_pids = random.sample(mission_products, bundle_size)
        
        for pid in selected_pids:
            mission_bundles.append({
                "bundle_name": bundle_names[mission],
                "mission": mission,
                "priority": random.choice(priorities),
                "product_id": pid
            })
            
    pd.DataFrame(mission_bundles).to_csv(OUTPUT_DIR / 'mission_bundles.csv', index=False)
    
    # ----------------------------------------------------
    # STEP 14: Generate Events
    # ----------------------------------------------------
    log("Generating events...")
    events = []
    event_types = ["PRICE_DROP", "LOW_STOCK", "TRENDING", "OUT_OF_STOCK", "NEW_REVIEW"]
    
    for pid in df_150_clean['product_id'].sample(50, replace=True): # 50 random events
        etype = random.choice(event_types)
        payload = {}
        if etype == "PRICE_DROP":
            payload = {"old_price": round(random.uniform(1000, 5000), 2), "new_price": round(random.uniform(500, 999), 2)}
        elif etype == "LOW_STOCK":
            payload = {"remaining": random.randint(1, 5)}
        elif etype == "TRENDING":
            payload = {"search_count": random.randint(100, 1000)}
        elif etype == "OUT_OF_STOCK":
            payload = {"expected_restock": (datetime.now() + timedelta(days=random.randint(2, 14))).strftime("%Y-%m-%d")}
        else:
            payload = {"rating": random.randint(4, 5), "comment": "Great product!"}
            
        events.append({
            "event_id": str(uuid.uuid4()),
            "product_id": pid,
            "event_type": etype,
            "payload": json.dumps(payload),
            "created_at": datetime.now().isoformat()
        })
    pd.DataFrame(events).to_csv(OUTPUT_DIR / 'events.csv', index=False)
    
    # Generate recommendation_seed.csv
    log("Generating recommendation seeds...")
    seeds = []
    
    # Interaction types distribution: VIEW 60%, ADD_TO_CART 20%, PURCHASE 10%, SAVE_FOR_LATER 10%
    interactions = ["VIEW", "ADD_TO_CART", "PURCHASE", "SAVE_FOR_LATER"]
    weights = [0.60, 0.20, 0.10, 0.10]
    
    for _ in range(200):
        # Pick a random mapped product to get its mission
        mapping = random.choice(mission_mapping)
        pid = mapping['product_id']
        mission = mapping['mission_name']
        
        seeds.append({
            "user_id": f"USR-{random.randint(1000, 9999)}",
            "mission": mission,
            "product_id": pid,
            "interaction_type": random.choices(interactions, weights=weights)[0],
            "timestamp": datetime.now().isoformat()
        })
    pd.DataFrame(seeds).to_csv(OUTPUT_DIR / 'recommendation_seed.csv', index=False)
    
    # ----------------------------------------------------
    # SUMMARY
    # ----------------------------------------------------
    end_time = time.time()
    exec_time = end_time - start_time
    
    summary = f"""# Pipeline Summary
    
- **Execution Time:** {exec_time:.2f} seconds
- **Dataset 1 Input:** {len(d1)} rows
- **Dataset 2 Input:** {len(d2)} rows
- **Merged & Deduplicated by exact name:** {len(df_merged) + len(missing_critical) + len(df_anomalies)} rows
- **Missing Value Drops:** {len(missing_critical)} rows
- **Anomaly Drops:** {len(df_anomalies)} rows
- **Master Products Pool:** {len(df_master)} rows
- **Final 150 Curated:** {len(df_150_clean)} rows

## Outputs Generated
- master_products.csv
- products_final_150.csv
- inventory.csv
- similar_products.csv
- ProductMissionMapping.csv
- mission_bundles.csv
- recommendation_seed.csv
- events.csv
- category_mapping.csv
- product_quality_scores.csv
- missing_value_report.csv
- anomaly_report.csv
- image_validation_report.csv
"""
    with open(OUTPUT_DIR / 'pipeline_summary.md', 'w') as f:
        f.write(summary)
        
    log("Pipeline complete.")

if __name__ == "__main__":
    process()
