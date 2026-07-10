import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
import re
from collections import defaultdict, Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = BASE_DIR
OUTPUT_DIR = os.path.join(BASE_DIR, 'backend', 'ai', 'knowledge', 'v1')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def safe_float(val):
    try: return float(val)
    except: return 0.0

def load_data():
    files = {
        'products': 'products_final_150.csv',
        'mission_mapping': 'ProductMissionMapping.csv',
        'mission_bundles': 'mission_bundles.csv',
        'category_mapping': 'category_mapping.csv',
        'similar_products': 'similar_products.csv',
        'quality_scores': 'product_quality_scores.csv',
        'recommendation_seed': 'recommendation_seed.csv'
    }
    dfs = {}
    for key, filename in files.items():
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            dfs[key] = pd.read_csv(filepath)
        else:
            log(f"Warning: {filename} not found.")
            dfs[key] = pd.DataFrame()
    return dfs

def write_json(filename, data):
    with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def build_supported_categories(dfs):
    log("Building supported_categories.json...")
    df_p = dfs['products']
    categories = []
    for cat, group in df_p.groupby('category'):
        categories.append({
            "category_name": cat,
            "number_of_products": len(group),
            "representative_products": group.nlargest(3, 'quality_score')['name'].tolist() if 'quality_score' in group else group.head(3)['name'].tolist(),
            "brands_present": group['brand'].dropna().unique().tolist(),
            "average_price": round(group['price'].mean(), 2),
            "average_rating": round(group['rating'].mean(), 2)
        })
    write_json("supported_categories.json", categories)
    return categories

def build_supported_brands(dfs):
    log("Building supported_brands.json...")
    df_p = dfs['products']
    brands = []
    for brand, group in df_p.groupby('brand'):
        brands.append({
            "brand": brand,
            "categories": group['category'].unique().tolist(),
            "products": group['name'].tolist(),
            "average_price": round(group['price'].mean(), 2),
            "average_rating": round(group['rating'].mean(), 2)
        })
    write_json("supported_brands.json", brands)
    return brands

def build_mission_catalog(dfs):
    log("Building mission_catalog.json...")
    df_m = dfs['mission_mapping']
    df_b = dfs['mission_bundles']
    df_p = dfs['products']
    
    # Merge mission mapping with products
    merged = df_m.merge(df_p, on='product_id', how='left')
    
    catalog = []
    for mission, group in merged.groupby('mission_name'):
        mission_bundles = df_b[df_b['mission'] == mission]['bundle_name'].unique().tolist() if not df_b.empty and 'mission' in df_b.columns else []
        prices = group['price'].dropna()
        budget_min = prices.min() if not prices.empty else 0
        budget_max = prices.max() if not prices.empty else 0
        budget_avg = prices.mean() if not prices.empty else 0
        
        cats = group['category'].value_counts()
        primary_cats = cats.head(2).index.tolist()
        secondary_cats = cats.tail(-2).index.tolist()
        
        req_prods = group[group['confidence_score'] >= 0.9]['name'].tolist()
        opt_prods = group[group['confidence_score'] < 0.9]['name'].tolist()
        
        catalog.append({
            "mission_name": mission,
            "description": f"Curated collection for {mission} needs.",
            "recommended_budget": {
                "minimum": float(budget_min),
                "average": round(float(budget_avg), 2),
                "maximum": float(budget_max)
            },
            "supported_categories": cats.index.tolist(),
            "primary_categories": primary_cats,
            "secondary_categories": secondary_cats,
            "supported_products": group['name'].tolist(),
            "required_products": req_prods,
            "optional_products": opt_prods,
            "supported_bundles": mission_bundles,
            "confidence_threshold": 0.70
        })
    write_json("mission_catalog.json", catalog)
    return catalog

def build_mission_knowledge(dfs):
    log("Building mission_knowledge.json...")
    df_m = dfs['mission_mapping']
    df_b = dfs['mission_bundles']
    df_p = dfs['products']
    
    merged = df_m.merge(df_p, on='product_id', how='left')
    knowledge = []
    
    for mission, group in merged.groupby('mission_name'):
        mb = df_b[df_b['mission'] == mission] if not df_b.empty else pd.DataFrame()
        high_pri_pids = mb[mb['priority'] == 'HIGH']['product_id'].tolist() if not mb.empty else []
        
        priority = group[(group['confidence_score'] >= 0.9) | (group['product_id'].isin(high_pri_pids))]
        alternative = group[~((group['confidence_score'] >= 0.9) | (group['product_id'].isin(high_pri_pids)))]
        
        cats = group['category'].value_counts()
        req_cats = cats[cats >= cats.max() * 0.5].index.tolist()
        opt_cats = cats[cats < cats.max() * 0.5].index.tolist()
        
        # New deterministically generated fields
        primary_cats = cats.head(2).index.tolist()
        secondary_cats = cats.tail(-2).index.tolist()
        cat_weights = (cats / cats.sum()).round(2).to_dict()
        
        mission_priority = "HIGH" if not mb.empty and "HIGH" in mb['priority'].values else "NORMAL"
        
        m_lower = str(mission).lower()
        if "setup" in m_lower or "work" in m_lower:
            mission_type = "SETUP"
        elif "night" in m_lower or "birthday" in m_lower or "celebration" in m_lower:
            mission_type = "EVENT"
        else:
            mission_type = "ESSENTIALS"
        
        bundles = []
        if not mb.empty:
            for b_name, b_group in mb.groupby('bundle_name'):
                b_prods = b_group.merge(df_p, on='product_id', how='left')
                bundles.append({
                    "name": str(b_name),
                    "priority": str(b_group['priority'].iloc[0]),
                    "products": b_prods['name'].tolist()
                })
        
        knowledge.append({
            "mission_name": str(mission),
            "mission_type": mission_type,
            "priority": mission_priority,
            "products": group['name'].tolist(),
            "priority_products": priority['name'].tolist(),
            "alternative_products": alternative['name'].tolist(),
            "required_categories": req_cats,
            "optional_categories": opt_cats,
            "primary_categories": primary_cats,
            "secondary_categories": secondary_cats,
            "category_weights": cat_weights,
            "bundles": bundles
        })
    write_json("mission_knowledge.json", knowledge)

def build_keywords(dfs):
    log("Building keywords.json...")
    df_p = dfs['products']
    df_m = dfs['mission_mapping']
    
    # Basic stop words
    stop_words = set(['and', 'or', 'the', 'a', 'an', 'in', 'on', 'with', 'for', 'to', 'of', 'is', 'are', 'it', 'this', 'that'])
    
    keywords = defaultdict(lambda: {"count": 0, "related_products": set(), "related_categories": set(), "type": "product_keyword"})
    
    def tokenize(text):
        if pd.isna(text): return []
        text = str(text).lower()
        words = re.findall(r'\b[a-z]{3,}\b', text)
        return [w for w in words if w not in stop_words]

    for _, row in df_p.iterrows():
        words = tokenize(row['name']) + tokenize(row['description'])
        for w in words:
            keywords[w]["count"] += 1
            keywords[w]["related_products"].add(row['name'])
            keywords[w]["related_categories"].add(row['category'])
            
    # Classify keywords
    # brand
    for brand in df_p['brand'].dropna().unique():
        brand_w = brand.lower()
        if brand_w in keywords:
            keywords[brand_w]["type"] = "brand_keyword"
    
    # category
    for cat in df_p['category'].dropna().unique():
        for w in tokenize(cat):
            if w in keywords: keywords[w]["type"] = "category_keyword"
            
    # mission
    for mission in df_m['mission_name'].dropna().unique():
        for w in tokenize(mission):
            if w in keywords: keywords[w]["type"] = "mission_keyword"
            
    # filter low frequency
    filtered = []
    for k, v in keywords.items():
        if v["count"] > 2:
            filtered.append({
                "keyword": k,
                "classification": v["type"],
                "frequency": v["count"],
                "related_products": list(v["related_products"])[:5],
                "related_categories": list(v["related_categories"])
            })
            
    filtered.sort(key=lambda x: x['frequency'], reverse=True)
    write_json("keywords.json", filtered[:200]) # top 200

def build_query_aliases(dfs):
    log("Building query_aliases.json...")
    # Shopping focused aliases
    aliases = {
        "laptop": ["notebook", "pc", "computer", "macbook"],
        "phone": ["smartphone", "mobile", "cellphone"],
        "shoes": ["sneakers", "footwear", "running shoes", "trainers"],
        "bag": ["backpack", "luggage", "suitcase"],
        "shirt": ["tshirt", "t-shirt", "top", "tee"],
        "pants": ["trousers", "jeans", "bottoms"],
        "hostel": ["pg", "dorm", "accommodation"],
        "gym": ["workout", "fitness", "exercise"],
        "travel": ["trip", "vacation", "journey", "weekend getaway"],
        "cheap": ["affordable", "budget", "low price", "discounted"],
        "premium": ["luxury", "high-end", "expensive", "top tier"]
    }
    
    # Ensure aliases are relevant to our data
    df_p = dfs['products']
    text_corpus = " ".join(df_p['name'].dropna().str.lower().tolist() + df_p['category'].dropna().str.lower().tolist())
    
    relevant_aliases = {}
    for key, syns in aliases.items():
        # Keep if key or any synonym is in corpus
        if key in text_corpus or any(s in text_corpus for s in syns):
            relevant_aliases[key] = syns
            
    write_json("query_aliases.json", relevant_aliases)

def build_bundle_knowledge(dfs):
    log("Building bundle_knowledge.json...")
    df_b = dfs['mission_bundles']
    df_p = dfs['products']
    if df_b.empty: return
    
    bundles = []
    for b_name, group in df_b.groupby('bundle_name'):
        merged = group.merge(df_p, on='product_id', how='left')
        est_price = merged['price'].sum()
        avg_score = merged['quality_score'].mean() if 'quality_score' in merged else 0
        
        bundles.append({
            "bundle_name": str(b_name),
            "mission": str(group['mission'].iloc[0]),
            "priority": str(group['priority'].iloc[0]),
            "products": merged['name'].tolist(),
            "estimated_price": round(float(est_price), 2),
            "bundle_score": round(float(avg_score), 2)
        })
    write_json("bundle_knowledge.json", bundles)

def build_price_ranges(dfs):
    log("Building price_ranges.json...")
    df_p = dfs['products']
    ranges = []
    for cat, group in df_p.groupby('category'):
        prices = group['price'].dropna()
        if prices.empty: continue
        ranges.append({
            "category": str(cat),
            "minimum_price": float(prices.min()),
            "maximum_price": float(prices.max()),
            "median_price": float(prices.median()),
            "average_price": round(float(prices.mean()), 2)
        })
    write_json("price_ranges.json", ranges)

def build_brand_relationships(dfs):
    log("Building brand_relationships.json...")
    df_p = dfs['products']
    rels = {}
    for brand, b_group in df_p.groupby('brand'):
        if pd.isna(brand): continue
        rels[brand] = {}
        for cat, c_group in b_group.groupby('category'):
            rels[brand][cat] = c_group['name'].tolist()
            
    write_json("brand_relationships.json", rels)

def build_ai_constraints(dfs):
    log("Building ai_constraints.json...")
    df_p = dfs['products']
    df_m = dfs['mission_mapping']
    
    constraints = {
        "supported_missions": df_m['mission_name'].unique().tolist() if not df_m.empty else [],
        "supported_categories": df_p['category'].unique().tolist(),
        "supported_brands": df_p['brand'].dropna().unique().tolist(),
        "unsupported_requests": [
            "Do not recommend products out of stock.",
            "Do not invent new missions or categories.",
            "Do not recommend products from unsupported brands.",
            "Do not provide specific delivery timelines.",
            "Do not generate SQL or Cypher queries in user responses."
        ],
        "unsupported_examples": [
            "User asks for a 'Gaming PC' but category only has 'Laptops'. Respond that we only have Laptops.",
            "User asks for 'Nike' but brand is not in supported_brands. State we don't carry Nike."
        ],
        "fallback_response": "I'm sorry, but I can only recommend products and bundles from our supported missions and categories. Please try exploring one of our curated missions like {missions}.",
        "supported_request_types": [
            "Mission-based recommendations",
            "Bundle inquiries",
            "Category browsing",
            "Product similarity requests",
            "Price range checks"
        ],
        "rules": [
            "The AI should NEVER recommend products outside this knowledge base."
        ]
    }
    write_json("ai_constraints.json", constraints)

def build_few_shot_examples(dfs):
    log("Building few_shot_examples.json...")
    df_m = dfs['mission_mapping']
    if df_m.empty: return
    missions = df_m['mission_name'].unique().tolist()
    
    examples = []
    templates = [
        "I need some stuff for {}",
        "Looking to buy items for {}",
        "What do you recommend for a {}?",
        "Show me {} essentials",
        "I have a {} coming up, need products."
    ]
    
    for i in range(100):
        m = np.random.choice(missions)
        t = np.random.choice(templates)
        
        examples.append({
            "User Query": t.format(m),
            "Expected Mission": str(m),
            "Expected Categories": dfs['products'][dfs['products']['product_id'].isin(df_m[df_m['mission_name']==m]['product_id'])]['category'].unique().tolist()[:2],
            "Expected Keywords": [w.lower() for w in str(m).split()],
            "Expected Budget": "Flexible"
        })
    write_json("few_shot_examples.json", examples)

def build_intent_patterns(dfs):
    log("Building intent_patterns.json...")
    patterns = {
        "Hostel Setup": [
            "moving to dorm", "college setup", "pg essentials", "room decor"
        ],
        "Gym": [
            "start working out", "fitness goals", "home gym", "activewear"
        ],
        "Travel Essentials": [
            "going on a trip", "packing for vacation", "flight accessories"
        ],
        "Work From Home": [
            "home office", "remote work setup", "desk accessories"
        ]
    }
    write_json("intent_patterns.json", patterns)

def build_metadata_and_summary(dfs):
    log("Building metadata and summary...")
    df_p = dfs['products']
    df_m = dfs['mission_mapping']
    df_b = dfs['mission_bundles']
    
    meta = {
        "knowledge_base_version": "v1.0",
        "generation_timestamp": datetime.now().isoformat(),
        "dataset_version": "Phase 2 Final",
        "total_products": len(df_p),
        "total_categories": df_p['category'].nunique(),
        "total_brands": df_p['brand'].nunique(),
        "total_missions": df_m['mission_name'].nunique() if not df_m.empty else 0
    }
    write_json("metadata.json", meta)
    
    summary = f"""# AI Knowledge Base Summary

**Version:** v1.0
**Generated:** {meta['generation_timestamp']}

## Overview
* **Total Products:** {meta['total_products']}
* **Total Categories:** {meta['total_categories']}
* **Total Brands:** {meta['total_brands']}
* **Total Missions:** {meta['total_missions']}
* **Total Bundles:** {df_b['bundle_name'].nunique() if not df_b.empty else 0}

## Global Stats
* **Average Product Price:** ₹{round(df_p['price'].mean(), 2) if 'price' in df_p else 0}
* **Most Common Brands:** {', '.join(df_p['brand'].value_counts().head(5).index.tolist())}
* **Highest Rated Categories:** {', '.join(df_p.groupby('category')['rating'].mean().nlargest(5).index.tolist())}
"""
    with open(os.path.join(OUTPUT_DIR, "knowledge_base_summary.md"), 'w', encoding='utf-8') as f:
        f.write(summary)

def verify_outputs():
    log("Verifying outputs...")
    files = [
        "supported_categories.json", "supported_brands.json", "mission_catalog.json",
        "mission_knowledge.json", "keywords.json", "query_aliases.json",
        "bundle_knowledge.json", "price_ranges.json", "brand_relationships.json",
        "ai_constraints.json", "few_shot_examples.json", "metadata.json",
        "intent_patterns.json", "knowledge_base_summary.md"
    ]
    
    missing = [f for f in files if not os.path.exists(os.path.join(OUTPUT_DIR, f))]
    if missing:
        log(f"FAIL: Missing files: {missing}")
    else:
        log("PASS: All files generated.")
        
    # Verify no duplicate missions in catalog
    with open(os.path.join(OUTPUT_DIR, "mission_catalog.json")) as f:
        mc = json.load(f)
        missions = [m['mission_name'] for m in mc]
        if len(missions) != len(set(missions)):
            log("FAIL: Duplicate missions found in mission_catalog.json")
        else:
            log("PASS: No duplicate missions.")
            
    # Verify no orphan bundles
    with open(os.path.join(OUTPUT_DIR, "bundle_knowledge.json")) as f:
        bk = json.load(f)
        b_names = [b['bundle_name'] for b in bk]
        if len(b_names) != len(set(b_names)):
            log("FAIL: Duplicate bundles found in bundle_knowledge.json")
        else:
            log("PASS: No duplicate bundles.")
            
        missions_in_b = set(b['mission'] for b in bk)
        if not missions_in_b.issubset(set(missions)):
            log("FAIL: Orphan bundles referencing unknown missions.")
        else:
            log("PASS: No orphan bundles.")

def main():
    dfs = load_data()
    if dfs['products'].empty:
        log("Error: Critical datasets missing. Aborting.")
        return
        
    build_supported_categories(dfs)
    build_supported_brands(dfs)
    build_mission_catalog(dfs)
    build_mission_knowledge(dfs)
    build_keywords(dfs)
    build_query_aliases(dfs)
    build_bundle_knowledge(dfs)
    build_price_ranges(dfs)
    build_brand_relationships(dfs)
    build_ai_constraints(dfs)
    build_few_shot_examples(dfs)
    build_intent_patterns(dfs)
    build_metadata_and_summary(dfs)
    
    verify_outputs()
    log("AIKB generation complete.")

if __name__ == "__main__":
    main()
