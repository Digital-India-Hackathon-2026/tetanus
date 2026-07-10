# Database + Neo4j Package

This document lists the required project files for the Database and Neo4j Graph generation package, as well as the files that should be excluded.

## Dataset Files

### master_products.csv
* **Status:** ✅ REQUIRED
* **Purpose:** The complete, merged, and cleaned dataset before the 150-product filtering.
* **Open:** [master_products.csv](file:///C:/Users/srika/OneDrive/projects/DigitalIndia/master_products.csv)
* **Absolute Path:** `C:\Users\srika\OneDrive\projects\DigitalIndia\master_products.csv`
* **Relative Path:** `master_products.csv`
* **File Size:** 12.49 MB
* **Last Modified:** 2026-07-10 12:21:20

### products_final_150.csv
* **Status:** ✅ REQUIRED
* **Purpose:** Final curated catalog of 150 perfectly balanced products.
* **Open:** [products_final_150.csv](file:///C:/Users/srika/OneDrive/projects/DigitalIndia/products_final_150.csv)
* **Absolute Path:** `C:\Users\srika\OneDrive\projects\DigitalIndia\products_final_150.csv`
* **Relative Path:** `products_final_150.csv`
* **File Size:** 220.50 KB
* **Last Modified:** 2026-07-10 12:21:20

### inventory.csv
* **Status:** ✅ REQUIRED
* **Purpose:** Current stock levels and status for the 150 curated products.
* **Open:** [inventory.csv](file:///C:/Users/srika/OneDrive/projects/DigitalIndia/inventory.csv)
* **Absolute Path:** `C:\Users\srika\OneDrive\projects\DigitalIndia\inventory.csv`
* **Relative Path:** `inventory.csv`
* **File Size:** 11.73 KB
* **Last Modified:** 2026-07-10 12:21:20

### similar_products.csv
* **Status:** ✅ REQUIRED
* **Purpose:** Weighted edges representing similarity relationships between products.
* **Open:** [similar_products.csv](file:///C:/Users/srika/OneDrive/projects/DigitalIndia/similar_products.csv)
* **Absolute Path:** `C:\Users\srika\OneDrive\projects\DigitalIndia\similar_products.csv`
* **Relative Path:** `similar_products.csv`
* **File Size:** 42.97 KB
* **Last Modified:** 2026-07-10 12:21:20

### ProductMissionMapping.csv
* **Status:** ✅ REQUIRED
* **Purpose:** Maps the 150 products to specific lifestyle missions.
* **Open:** [ProductMissionMapping.csv](file:///C:/Users/srika/OneDrive/projects/DigitalIndia/ProductMissionMapping.csv)
* **Absolute Path:** `C:\Users\srika\OneDrive\projects\DigitalIndia\ProductMissionMapping.csv`
* **Relative Path:** `ProductMissionMapping.csv`
* **File Size:** 14.18 KB
* **Last Modified:** 2026-07-10 12:21:20

### mission_bundles.csv
* **Status:** ✅ REQUIRED
* **Purpose:** Curated bundles of products targeted towards specific missions.
* **Open:** [mission_bundles.csv](file:///C:/Users/srika/OneDrive/projects/DigitalIndia/mission_bundles.csv)
* **Absolute Path:** `C:\Users\srika\OneDrive\projects\DigitalIndia\mission_bundles.csv`
* **Relative Path:** `mission_bundles.csv`
* **File Size:** 2.04 KB
* **Last Modified:** 2026-07-10 12:21:20

### recommendation_seed.csv
* **Status:** ✅ REQUIRED
* **Purpose:** Synthetic user interaction events (views, carts, purchases) mapped to missions.
* **Open:** [recommendation_seed.csv](file:///C:/Users/srika/OneDrive/projects/DigitalIndia/recommendation_seed.csv)
* **Absolute Path:** `C:\Users\srika\OneDrive\projects\DigitalIndia\recommendation_seed.csv`
* **Relative Path:** `recommendation_seed.csv`
* **File Size:** 18.74 KB
* **Last Modified:** 2026-07-10 12:21:20

### events.csv
* **Status:** ✅ REQUIRED
* **Purpose:** System-level price and inventory fluctuation events for graph simulation.
* **Open:** [events.csv](file:///C:/Users/srika/OneDrive/projects/DigitalIndia/events.csv)
* **Absolute Path:** `C:\Users\srika\OneDrive\projects\DigitalIndia\events.csv`
* **Relative Path:** `events.csv`
* **File Size:** 7.65 KB
* **Last Modified:** 2026-07-10 12:21:20

### category_mapping.csv
* **Status:** ✅ REQUIRED
* **Purpose:** Mapping of canonical categories and brands.
* **Open:** [category_mapping.csv](file:///C:/Users/srika/OneDrive/projects/DigitalIndia/category_mapping.csv)
* **Absolute Path:** `C:\Users\srika\OneDrive\projects\DigitalIndia\category_mapping.csv`
* **Relative Path:** `category_mapping.csv`
* **File Size:** 1.23 KB
* **Last Modified:** 2026-07-10 12:21:18

### product_quality_scores.csv
* **Status:** ✅ REQUIRED
* **Purpose:** Exhaustive quality scoring metrics for the entire catalog.
* **Open:** [product_quality_scores.csv](file:///C:/Users/srika/OneDrive/projects/DigitalIndia/product_quality_scores.csv)
* **Absolute Path:** `C:\Users\srika\OneDrive\projects\DigitalIndia\product_quality_scores.csv`
* **Relative Path:** `product_quality_scores.csv`
* **File Size:** 1.87 MB
* **Last Modified:** 2026-07-10 12:21:19


---

## FILES NOT REQUIRED

The following files are pipeline artifacts, raw datasets, intermediate reports, or codebase files that **should NOT** be shared with the database teammate.

* `anomaly_report.csv`
* `curation_pipeline.py`
* `dataset1_deduplicated.csv`
* `dataset2_deduplicated.csv`
* `dedup_pipeline.py`
* `duplicate_report.md`
* `duplicates_removed.csv`
* `image_validation_report.csv`
* `missing_value_report.csv`
* `pipeline_summary.md`
* `qa_report.json`
* `qa_script.py`

---

## Folder Tree

```text
database_package/
├── ProductMissionMapping.csv
├── category_mapping.csv
├── events.csv
├── inventory.csv
├── master_products.csv
├── mission_bundles.csv
├── product_quality_scores.csv
├── products_final_150.csv
├── recommendation_seed.csv
└── similar_products.csv
```

*(Note: SQL Scripts, Architecture Documents, and Neo4j Designs were not found in the directory and are therefore omitted from the tree).*

---

## Final Checklist

### Database Teammate Package
- [x] Products Dataset
- [x] Inventory Dataset
- [x] Category Mapping
- [x] Similar Products
- [x] Mission Mapping
- [x] Mission Bundles
- [x] Recommendation Seed
- [x] Events
- [x] Product Quality Scores
- [ ] PostgreSQL Schema *(Not found in directory)*
- [ ] SQL Scripts *(Not found in directory)*
- [ ] Architecture Document *(Not found in directory)*
- [ ] Neo4j Design *(Not found in directory)*
- [ ] README *(Not found in directory)*
