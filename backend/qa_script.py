import pandas as pd
import json
import re
import math

def log_fail(check, message):
    print(f"[FAIL] {check}: {message}")
    
def log_pass(check):
    print(f"[PASS] {check}")

def is_valid_json(val):
    try:
        json.loads(val)
        return True
    except:
        return False

def run_qa():
    print("Starting QA Validation...\n")
    report = []
    
    # Load Data
    try:
        df_150 = pd.read_csv("products_final_150.csv")
        df_inv = pd.read_csv("inventory.csv")
        df_sim = pd.read_csv("similar_products.csv")
        df_pm = pd.read_csv("ProductMissionMapping.csv")
        df_mb = pd.read_csv("mission_bundles.csv")
        df_rec = pd.read_csv("recommendation_seed.csv")
        df_events = pd.read_csv("events.csv")
        df_cat = pd.read_csv("category_mapping.csv")
    except Exception as e:
        print(f"Error loading files: {e}")
        return
        
    product_ids = set(df_150['product_id'].astype(str))
    
    # CHECK 1: Verify products_final_150.csv
    c1_issues = []
    if len(df_150) != 150: c1_issues.append(f"Row count is {len(df_150)}, expected 150")
    if len(df_150['name'].unique()) != len(df_150): c1_issues.append("Duplicate product names found")
    if len(df_150['product_id'].unique()) != len(df_150): c1_issues.append("Duplicate product IDs found")
    
    expected_cols = ['product_id', 'name', 'brand', 'category', 'price', 'mrp', 'description', 'specifications', 'rating', 'review_count', 'image_url', 'product_url', 'quality_score']
    
    if not set(expected_cols).issubset(df_150.columns):
        c1_issues.append("Missing expected columns in products_final_150")
        
    req_fields = ['product_id', 'name', 'category', 'price', 'description']
    for f in req_fields:
        if f in df_150.columns and df_150[f].isna().any(): c1_issues.append(f"Missing required field: {f}")
        
    if 'price' in df_150.columns and (df_150['price'] < 0).any(): c1_issues.append("Negative prices found")
    
    if len(df_150) != 150: c1_issues.append(f"Expected 150 products, got {len(df_150)}")
    
    # Review count checks
    if 'review_count' in df_150.columns:
        if df_150['review_count'].isna().any():
            c1_issues.append("Missing values in review_count")
        
        if not pd.api.types.is_integer_dtype(df_150['review_count']):
            # Try to convert to int if it's float without decimals
            try:
                df_150['review_count'] = df_150['review_count'].astype(int)
            except:
                c1_issues.append("review_count is not an integer")
                
        if (df_150['review_count'] < 0).any():
            c1_issues.append("review_count contains negative values")
    if ((df_150['rating'] < 0) | (df_150['rating'] > 5)).any(): c1_issues.append("Ratings outside 0-5")
    if ((df_150['quality_score'] < 0) | (df_150['quality_score'] > 100)).any(): c1_issues.append("Quality score outside 0-100")
    
    invalid_specs = df_150[~df_150['specifications'].apply(is_valid_json)]
    if not invalid_specs.empty: c1_issues.append(f"{len(invalid_specs)} invalid JSON specifications")
    
    url_regex = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    invalid_img = df_150[~df_150['image_url'].astype(str).str.match(url_regex)]
    # Allow nan images if not strict, but check structural if present
    if not df_150['image_url'].isna().all() and len(invalid_img[df_150['image_url'].notna()]) > 0: 
        c1_issues.append(f"{len(invalid_img)} structurally invalid image URLs")
        
    if not c1_issues: log_pass("CHECK 1: products_final_150.csv")
    else: log_fail("CHECK 1", "; ".join(c1_issues))
    report.append({"check": "CHECK 1: products_final_150", "status": "FAIL" if c1_issues else "PASS", "issues": c1_issues})

    # CHECK 2: Verify inventory.csv
    c2_issues = []
    if not set(df_inv['product_id'].astype(str)).issubset(product_ids): c2_issues.append("Unknown product_id in inventory")
    if len(df_inv['product_id'].unique()) != len(df_inv): c2_issues.append("Duplicate product IDs in inventory")
    
    bad_status = df_inv[
        ((df_inv['stock_count'] == 0) & (df_inv['status'] != 'OUT_OF_STOCK')) |
        ((df_inv['stock_count'] > 0) & (df_inv['stock_count'] <= 10) & (df_inv['status'] != 'LOW_STOCK')) |
        ((df_inv['stock_count'] > 10) & (df_inv['status'] != 'IN_STOCK'))
    ]
    if not bad_status.empty: c2_issues.append(f"{len(bad_status)} records have mismatched stock_count and status")
    
    if not c2_issues: log_pass("CHECK 2: inventory.csv")
    else: log_fail("CHECK 2", "; ".join(c2_issues))
    report.append({"check": "CHECK 2: inventory.csv", "status": "FAIL" if c2_issues else "PASS", "issues": c2_issues})

    # CHECK 3: Verify similar_products.csv
    c3_issues = []
    if not set(df_sim['product_id'].astype(str)).issubset(product_ids): c3_issues.append("Unknown product_id")
    if not set(df_sim['similar_product_id'].astype(str)).issubset(product_ids): c3_issues.append("Unknown similar_product_id")
    if (df_sim['product_id'] == df_sim['similar_product_id']).any(): c3_issues.append("Self references found")
    if df_sim.duplicated(subset=['product_id', 'similar_product_id']).any(): c3_issues.append("Duplicate mappings")
    if (df_sim['similarity_score'] < 0).any() or (df_sim['similarity_score'] > 1).any(): c3_issues.append("Similarity out of bounds")

    if not c3_issues: log_pass("CHECK 3: similar_products.csv")
    else: log_fail("CHECK 3", "; ".join(c3_issues))
    report.append({"check": "CHECK 3: similar_products", "status": "FAIL" if c3_issues else "PASS", "issues": c3_issues})

    # CHECK 4: Verify ProductMissionMapping.csv
    c4_issues = []
    if len(df_pm['mission_name'].unique()) == 0: c4_issues.append("No missions found")
    # The requirement says "Every product belongs to at least one mission", but our synthetic generation didn't guarantee *every* product got a mission, just a random subset. 
    missing_prods = len(product_ids - set(df_pm['product_id'].astype(str)))
    if missing_prods > 0: c4_issues.append(f"{missing_prods} products are not assigned to any mission")
    if ((df_pm['confidence_score'] < 0) | (df_pm['confidence_score'] > 1)).any(): c4_issues.append("Confidence scores outside 0-1")
    
    if not c4_issues: log_pass("CHECK 4: ProductMissionMapping.csv")
    else: log_fail("CHECK 4", "; ".join(c4_issues))
    report.append({"check": "CHECK 4: ProductMissionMapping", "status": "FAIL" if c4_issues else "PASS", "issues": c4_issues})

    # CHECK 5: Verify mission_bundles.csv
    c5_issues = []
    # bundle_name, mission, priority, product_id
    if not set(['bundle_name', 'mission', 'priority', 'product_id']).issubset(df_mb.columns):
        c5_issues.append("Missing required columns in mission_bundles")
    else:
        if not set(df_mb['product_id'].astype(str)).issubset(product_ids): c5_issues.append("Unknown products in bundles")
        
        valid_priorities = {"HIGH", "MEDIUM", "LOW"}
        invalid_priorities = set(df_mb['priority']) - valid_priorities
        if invalid_priorities: c5_issues.append(f"Invalid priorities found: {invalid_priorities}")
            
    if not c5_issues: log_pass("CHECK 5: mission_bundles.csv")
    else: log_fail("CHECK 5", "; ".join(c5_issues))
    report.append({"check": "CHECK 5: mission_bundles", "status": "FAIL" if c5_issues else "PASS", "issues": c5_issues})

    # CHECK 6: Verify recommendation_seed.csv
    c6_issues = []
    if not set(df_rec['product_id'].astype(str)).issubset(product_ids): c6_issues.append("Unknown product_id in recommendations")
    if 'mission' in df_rec.columns:
        if df_rec['mission'].isna().any(): c6_issues.append("Missing mission in recommendations")
    else:
        c6_issues.append("Column 'mission' does not exist in recommendation_seed.csv (Note: this was not in the generation prompt)")
        
    if not c6_issues: log_pass("CHECK 6: recommendation_seed.csv")
    else: log_fail("CHECK 6", "; ".join(c6_issues))
    report.append({"check": "CHECK 6: recommendation_seed", "status": "FAIL" if c6_issues else "PASS", "issues": c6_issues})

    # CHECK 7: Verify events.csv
    c7_issues = []
    invalid_payloads = df_events[~df_events['payload'].apply(is_valid_json)]
    if not invalid_payloads.empty: c7_issues.append(f"{len(invalid_payloads)} events have invalid JSON payloads")
    if not set(df_events['product_id'].astype(str)).issubset(product_ids): c7_issues.append("Unknown product_id in events")
    
    valid_events = {"PRICE_DROP", "LOW_STOCK", "OUT_OF_STOCK", "TRENDING", "FLASH_SALE", "NEW_PRODUCT", "NEW_REVIEW"}
    invalid_types = set(df_events['event_type']) - valid_events
    if invalid_types: c7_issues.append(f"Invalid event types found: {invalid_types}")
    
    if not c7_issues: log_pass("CHECK 7: events.csv")
    else: log_fail("CHECK 7", "; ".join(c7_issues))
    report.append({"check": "CHECK 7: events", "status": "FAIL" if c7_issues else "PASS", "issues": c7_issues})

    # CHECK 8: Verify category_mapping.csv
    c8_issues = []
    if df_cat.duplicated(subset=['category_raw']).any(): c8_issues.append("Duplicate raw category mappings")
    # All canonical categories used in df_150 should exist
    cat_used = set(df_150['category'])
    cat_mapped = set(df_cat['category'])
    if not cat_used.issubset(cat_mapped): c8_issues.append("Some categories in final dataset are missing from mapping")
    
    if not c8_issues: log_pass("CHECK 8: category_mapping.csv")
    else: log_fail("CHECK 8", "; ".join(c8_issues))
    report.append({"check": "CHECK 8: category_mapping", "status": "FAIL" if c8_issues else "PASS", "issues": c8_issues})

    # CHECK 9: Cross File Integrity
    c9_issues = []
    all_referenced_pids = set()
    all_referenced_pids.update(df_inv['product_id'].astype(str))
    all_referenced_pids.update(df_sim['product_id'].astype(str))
    all_referenced_pids.update(df_sim['similar_product_id'].astype(str))
    all_referenced_pids.update(df_pm['product_id'].astype(str))
    all_referenced_pids.update(df_rec['product_id'].astype(str))
    all_referenced_pids.update(df_events['product_id'].astype(str))
    
    if not all_referenced_pids.issubset(product_ids):
        c9_issues.append("Orphan references found! Products referenced in sub-tables do not exist in master")
        
    if not c9_issues: log_pass("CHECK 9: Cross File Integrity")
    else: log_fail("CHECK 9", "; ".join(c9_issues))
    report.append({"check": "CHECK 9: Cross File Integrity", "status": "FAIL" if c9_issues else "PASS", "issues": c9_issues})

    # ----------------------------------------------------
    # GENERATE QA REPORT
    # ----------------------------------------------------
    passed = sum(1 for r in report if r["status"] == "PASS")
    total = len(report)
    score = (passed / total) * 100
    
    with open("qa_report.json", "w") as f:
        json.dump({"score": score, "details": report}, f)

if __name__ == "__main__":
    run_qa()
