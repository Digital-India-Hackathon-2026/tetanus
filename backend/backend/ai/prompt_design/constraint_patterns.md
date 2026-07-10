# Constraint Extraction

This document outlines how the Intent prompt should extract filtering constraints into the `Constraint` schema.

## 1. Brand Preferences & Exclusions
*   **Positive**: "I only want Samsung", "Sony or LG" -> `preferred_brands: ["Samsung"]`.
*   **Negative**: "No Apple", "Avoid cheap brands" -> `excluded_brands: ["Apple"]`.

## 2. Urgency & Delivery
*   "Need it today", "Urgent" -> `maximum_delivery_days: 1`.
*   "By this weekend" -> `maximum_delivery_days: 3`.

## 3. Quality & Ratings
*   "Highly rated", "Good reviews" -> `minimum_rating: 4.0`.
*   "Best rated" -> `minimum_rating: 4.5`.

## 4. Specific Features (Must Have vs Nice to Have)
*   **Must Have**: "Must have 16GB RAM", "Required in black" -> `must_have: ["16GB RAM", "black"]`.
*   **Nice to Have**: "Preferably with a case", "RGB if possible" -> `nice_to_have: ["case", "RGB"]`.

## 5. Inventory Constraints
*   "I can wait", "Preorder is fine" -> `inventory_required: "PREORDER"`.
*   "Need it now" -> `inventory_required: "IN_STOCK"`.
