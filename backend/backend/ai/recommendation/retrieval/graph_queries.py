GET_PRODUCT_BY_ID = """
MATCH (p:Product {id: $product_id})
OPTIONAL MATCH (c:Category)-[:HAS_PRODUCT]->(p)
OPTIONAL MATCH (b:Brand)-[:MANUFACTURES]->(p)
RETURN p.id AS product_id, p.name AS name, b.name AS brand, c.name AS category, 
       p.price AS price, p.mrp AS mrp, p.rating AS rating, p.review_count AS review_count, 
       p.description AS description, p.image_url AS image_url, p.product_url AS product_url, 
       p.quality_score AS quality_score
"""

GET_PRODUCTS_BY_CATEGORY = """
MATCH (c:Category)-[:HAS_PRODUCT]->(p:Product)
WHERE c.name IN $categories
OPTIONAL MATCH (b:Brand)-[:MANUFACTURES]->(p)
RETURN p.id AS product_id, p.name AS name, b.name AS brand, c.name AS category, 
       p.price AS price, p.mrp AS mrp, p.rating AS rating, p.review_count AS review_count, 
       p.description AS description, p.image_url AS image_url, p.product_url AS product_url, 
       p.quality_score AS quality_score
LIMIT $limit
"""

GET_PRODUCTS_BY_BRAND = """
MATCH (b:Brand)-[:MANUFACTURES]->(p:Product)
WHERE b.name IN $brands
OPTIONAL MATCH (c:Category)-[:HAS_PRODUCT]->(p)
RETURN p.id AS product_id, p.name AS name, b.name AS brand, c.name AS category, 
       p.price AS price, p.mrp AS mrp, p.rating AS rating, p.review_count AS review_count, 
       p.description AS description, p.image_url AS image_url, p.product_url AS product_url, 
       p.quality_score AS quality_score
LIMIT $limit
"""

GET_PRODUCTS = """
MATCH (p:Product)
OPTIONAL MATCH (c:Category)-[:HAS_PRODUCT]->(p)
OPTIONAL MATCH (b:Brand)-[:MANUFACTURES]->(p)
WITH p, c, b
WHERE ($categories IS NULL OR size($categories) = 0 OR c.name IN $categories)
  AND ($brands IS NULL OR size($brands) = 0 OR b.name IN $brands)
RETURN p.id AS product_id, p.name AS name, b.name AS brand, c.name AS category, 
       p.price AS price, p.mrp AS mrp, p.rating AS rating, p.review_count AS review_count, 
       p.description AS description, p.image_url AS image_url, p.product_url AS product_url, 
       p.quality_score AS quality_score
"""

SEARCH_PRODUCTS = """
MATCH (p:Product)
WHERE toLower(p.name) CONTAINS toLower($keyword)
OPTIONAL MATCH (c:Category)-[:HAS_PRODUCT]->(p)
OPTIONAL MATCH (b:Brand)-[:MANUFACTURES]->(p)
RETURN p.id AS product_id, p.name AS name, b.name AS brand, c.name AS category, 
       p.price AS price, p.mrp AS mrp, p.rating AS rating, p.review_count AS review_count, 
       p.description AS description, p.image_url AS image_url, p.product_url AS product_url, 
       p.quality_score AS quality_score
"""

GET_PRODUCT_CONTEXT = """
MATCH (p:Product {id: $product_id})
OPTIONAL MATCH (c:Category)-[:HAS_PRODUCT]->(p)
OPTIONAL MATCH (b:Brand)-[:MANUFACTURES]->(p)
RETURN p.id AS product_id, p.name AS name, b.name AS brand, c.name AS category, 
       p.price AS price, p.mrp AS mrp, p.rating AS rating, p.review_count AS review_count, 
       p.description AS description, p.image_url AS image_url, p.product_url AS product_url, 
       p.quality_score AS quality_score
"""
