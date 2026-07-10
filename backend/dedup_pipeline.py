import pandas as pd
import numpy as np
from pathlib import Path
from thefuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import time

def compute_completeness(row):
    score = 0
    cols_to_check = [
        ['product title', 'product_name', 'name', 'title'],
        ['brand'],
        ['bb category', 'category', 'product_category_tree'],
        ['product description', 'description'],
        ['product_specifications', 'specifications'],
        ['price', 'retail_price', 'discounted_price', 'mrp'],
        ['rating', 'product_rating', 'overall_rating'],
        ['review count', 'review_count'],
        ['image url', 'image'],
        ['url', 'product_url']
    ]
    
    row_idx_lower = {str(k).lower(): k for k in row.index}
    
    for col_list in cols_to_check:
        for col in col_list:
            if col in row_idx_lower:
                actual_col = row_idx_lower[col]
                val = row[actual_col]
                if pd.notna(val) and str(val).strip() != '':
                    score += 1
                    break
    return score

def find_fuzzy_pairs(series, threshold):
    series = series.dropna()
    series = series[series.str.strip() != '']
    if len(series) < 2:
        return []
        
    texts = series.astype(str).tolist()
    indices = series.index.tolist()
    
    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 4), min_df=1)
    tfidf = vectorizer.fit_transform(texts)
    
    pairs = []
    visited = set()
    
    batch_size = 2000
    n = len(texts)
    
    for i in range(0, n, batch_size):
        end = min(i + batch_size, n)
        sim = cosine_similarity(tfidf[i:end], tfidf)
        
        margin = 0.15
        tf_thresh = max(0.1, (threshold / 100.0) - margin)
        
        rows, cols = np.where(sim > tf_thresh)
        
        for r, c in zip(rows, cols):
            idx1 = i + r
            idx2 = c
            if idx1 >= idx2: continue
            
            orig_idx1 = indices[idx1]
            orig_idx2 = indices[idx2]
            
            if orig_idx1 in visited or orig_idx2 in visited:
                continue
                
            score = fuzz.ratio(texts[idx1], texts[idx2])
            if score >= threshold:
                pairs.append([orig_idx1, orig_idx2])
                visited.add(orig_idx1)
                visited.add(orig_idx2)
                
    return pairs

def get_col(df, possible_names):
    cols_lower = {str(c).lower(): c for c in df.columns}
    for n in possible_names:
        if n in cols_lower:
            return cols_lower[n]
    return None

def process_dataset(filepath, dataset_index):
    print(f"Processing {filepath.name}...")
    df = pd.read_csv(filepath, on_bad_lines='skip', engine='python')
    
    initial_rows = len(df)
    initial_cols = len(df.columns)
    
    print("Computing completeness scores...")
    scores = df.apply(compute_completeness, axis=1)
    
    removed_records = []
    
    active_df = df.copy()
    
    name_col = get_col(active_df, ['product title', 'product_name', 'name', 'title'])
    brand_col = get_col(active_df, ['brand'])
    cat_col = get_col(active_df, ['bb category', 'category', 'product_category_tree'])
    
    def resolve_groups(groups, strategy, reason_prefix):
        nonlocal active_df
        to_remove = []
        for g_name, indices in groups.items():
            if len(indices) > 1:
                best_idx = indices[0]
                best_score = -1
                for idx in indices:
                    if scores[idx] > best_score:
                        best_score = scores[idx]
                        best_idx = idx
                
                b_name = active_df.loc[best_idx, name_col] if name_col else "Unknown"
                b_brand = active_df.loc[best_idx, brand_col] if brand_col else "Unknown"
                b_cat = active_df.loc[best_idx, cat_col] if cat_col else "Unknown"
                
                for idx in indices:
                    if idx != best_idx:
                        to_remove.append(idx)
                        removed_records.append({
                            'Original Row Index': best_idx,
                            'Duplicate Row Index': idx,
                            'Reason for Removal': f"{reason_prefix} ({g_name})",
                            'Matching Strategy': strategy,
                            'Completeness Score of Kept Record': scores[best_idx],
                            'Completeness Score of Removed Record': scores[idx],
                            'Product Name': str(b_name),
                            'Brand': str(b_brand),
                            'Category': str(b_cat)
                        })
        if to_remove:
            active_df = active_df.drop(index=to_remove)
            print(f"[{strategy}] Removed {len(to_remove)} rows.")

    print("Level 1: Exact duplicate rows")
    # Exclude empty rows from creating massive groups
    groups = active_df.groupby(active_df.columns.tolist(), dropna=False).groups
    resolve_groups(groups, "Level 1: Exact", "Exact match across all columns")
    
    print("Level 2: Duplicate URLs")
    url_col = get_col(active_df, ['url', 'product_url'])
    if url_col:
        groups = active_df.groupby(url_col, dropna=True).groups
        resolve_groups(groups, "Level 2: URL", "Matching Product URL")
        
    print("Level 3: Duplicate Image URLs")
    img_col = get_col(active_df, ['image url', 'image', 'image_url'])
    if img_col:
        groups = active_df.groupby(img_col, dropna=True).groups
        resolve_groups(groups, "Level 3: Image URL", "Matching Image URL")
        
    print("Level 4: Name + Brand")
    if name_col and brand_col:
        groups = active_df.groupby([name_col, brand_col], dropna=True).groups
        resolve_groups(groups, "Level 4: Name + Brand", "Matching Name and Brand")
        
    print("Level 5: Name + Price")
    price_col = get_col(active_df, ['price', 'retail_price', 'discounted_price', 'mrp'])
    if name_col and price_col:
        groups = active_df.groupby([name_col, price_col], dropna=True).groups
        resolve_groups(groups, "Level 5: Name + Price", "Matching Name and Price")
        
    print("Level 6: Fuzzy Name >= 95%")
    if name_col:
        pairs = find_fuzzy_pairs(active_df[name_col], 95)
        to_remove = []
        for idx1, idx2 in pairs:
            if scores[idx1] >= scores[idx2]:
                kept, rem = idx1, idx2
            else:
                kept, rem = idx2, idx1
                
            b_name = active_df.loc[kept, name_col] if name_col else "Unknown"
            b_brand = active_df.loc[kept, brand_col] if brand_col else "Unknown"
            b_cat = active_df.loc[kept, cat_col] if cat_col else "Unknown"
            
            to_remove.append(rem)
            removed_records.append({
                'Original Row Index': kept,
                'Duplicate Row Index': rem,
                'Reason for Removal': f"Fuzzy Name match >= 95%",
                'Matching Strategy': "Level 6: Fuzzy Name",
                'Completeness Score of Kept Record': scores[kept],
                'Completeness Score of Removed Record': scores[rem],
                'Product Name': str(b_name),
                'Brand': str(b_brand),
                'Category': str(b_cat)
            })
        if to_remove:
            active_df = active_df.drop(index=to_remove)
            print(f"[Level 6: Fuzzy Name] Removed {len(to_remove)} rows.")

    print("Level 7: Fuzzy Description >= 98%")
    desc_col = get_col(active_df, ['product description', 'description'])
    if desc_col:
        pairs = find_fuzzy_pairs(active_df[desc_col], 98)
        to_remove = []
        for idx1, idx2 in pairs:
            if scores[idx1] >= scores[idx2]:
                kept, rem = idx1, idx2
            else:
                kept, rem = idx2, idx1
                
            b_name = active_df.loc[kept, name_col] if name_col else "Unknown"
            b_brand = active_df.loc[kept, brand_col] if brand_col else "Unknown"
            b_cat = active_df.loc[kept, cat_col] if cat_col else "Unknown"
            
            to_remove.append(rem)
            removed_records.append({
                'Original Row Index': kept,
                'Duplicate Row Index': rem,
                'Reason for Removal': f"Fuzzy Description match >= 98%",
                'Matching Strategy': "Level 7: Fuzzy Description",
                'Completeness Score of Kept Record': scores[kept],
                'Completeness Score of Removed Record': scores[rem],
                'Product Name': str(b_name),
                'Brand': str(b_brand),
                'Category': str(b_cat)
            })
        if to_remove:
            active_df = active_df.drop(index=to_remove)
            print(f"[Level 7: Fuzzy Description] Removed {len(to_remove)} rows.")

    final_rows = len(active_df)
    
    out_file = f"dataset{dataset_index}_deduplicated.csv"
    active_df.to_csv(out_file, index=False)
    
    stats = {
        'initial_rows': initial_rows,
        'final_rows': final_rows,
        'removed_rows': initial_rows - final_rows,
        'cols': initial_cols,
        'col_names': df.columns.tolist()
    }
    
    return removed_records, stats, out_file, df

def generate_report(all_stats, all_removed, out_files):
    report_lines = []
    report_lines.append("# Duplicate Detection and Removal Report")
    report_lines.append("")
    
    for i, (stats, out_file) in enumerate(zip(all_stats, out_files)):
        report_lines.append(f"## Dataset {i+1}")
        report_lines.append(f"- **Initial Rows**: {stats['initial_rows']}")
        report_lines.append(f"- **Final Rows**: {stats['final_rows']}")
        report_lines.append(f"- **Rows Removed**: {stats['removed_rows']}")
        dup_pct = (stats['removed_rows'] / stats['initial_rows'] * 100) if stats['initial_rows'] > 0 else 0
        report_lines.append(f"- **Duplicate Percentage**: {dup_pct:.2f}%")
        report_lines.append(f"- **Total Unique Products**: {stats['final_rows']}")
        report_lines.append("")
    
    report_lines.append("## Duplicate Analysis")
    if all_removed:
        df_removed = pd.DataFrame(all_removed)
        report_lines.append("### Removal Reasons (Strategies)")
        reasons = df_removed['Matching Strategy'].value_counts()
        for strategy, count in reasons.items():
            report_lines.append(f"- **{strategy}**: {count}")
            
        report_lines.append("")
        report_lines.append("### Most Duplicated Brands")
        brands = df_removed[df_removed['Brand'] != 'Unknown']['Brand'].value_counts().head(5)
        for brand, count in brands.items():
            report_lines.append(f"- **{brand}**: {count}")
            
        report_lines.append("")
        report_lines.append("### Most Duplicated Categories")
        cats = df_removed[df_removed['Category'] != 'Unknown']['Category'].value_counts().head(5)
        for cat, count in cats.items():
            report_lines.append(f"- **{cat}**: {count}")
            
        report_lines.append("")
        report_lines.append("### Most Duplicated Products")
        prods = df_removed[df_removed['Product Name'] != 'Unknown']['Product Name'].value_counts().head(5)
        for prod, count in prods.items():
            report_lines.append(f"- **{prod}**: {count}")
    else:
        report_lines.append("No duplicates found.")
        
    report_lines.append("")
    
    with open("duplicate_report.md", "w") as f:
        f.write("\n".join(report_lines))

if __name__ == "__main__":
    base_dir = Path(r"c:\Users\srika\OneDrive\projects\DigitalIndia")
    
    csv_files = [
        Path(r"c:\Users\srika\OneDrive\projects\DigitalIndia\Dataset\archive (1)\home\sdf\marketing_sample_for_flipkart_com-ecommerce__20191101_20191130__15k_data.csv"),
        Path(r"c:\Users\srika\OneDrive\projects\DigitalIndia\Dataset\extracted\dataset.csv")
    ]
    # Keep it simple, just test these two files
    
    if not csv_files:
        print("No datasets found.")
        sys.exit(0)
        
    print(f"Found {len(csv_files)} datasets.")
    
    all_removed = []
    all_stats = []
    out_files = []
    
    for i, p in enumerate(csv_files):
        rem, stats, out_f, df = process_dataset(p, i+1)
        all_removed.extend(rem)
        all_stats.append(stats)
        out_files.append(out_f)
        
    if all_removed:
        df_out = pd.DataFrame(all_removed)
        # Drop columns we used internally for report
        df_out = df_out.drop(columns=['Product Name', 'Brand', 'Category'])
        df_out.to_csv("duplicates_removed.csv", index=False)
    else:
        pd.DataFrame(columns=['Original Row Index', 'Duplicate Row Index', 'Reason for Removal', 'Matching Strategy', 'Completeness Score of Kept Record', 'Completeness Score of Removed Record']).to_csv("duplicates_removed.csv", index=False)
        
    generate_report(all_stats, all_removed, out_files)
    
    print("\n--- Summary ---")
    for i, stats in enumerate(all_stats):
        print(f"Dataset {i+1}:")
        print(f"Rows Before: {stats['initial_rows']}")
        print(f"Rows After: {stats['final_rows']}")
        print(f"Duplicates Removed: {stats['removed_rows']}\n")
    
    print("Files Generated:")
    for out_f in out_files:
        print(f"- {out_f}")
    print("- duplicates_removed.csv")
    print("- duplicate_report.md")
