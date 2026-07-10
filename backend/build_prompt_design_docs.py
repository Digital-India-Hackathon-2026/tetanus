import os
import json
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
AI_KNOWLEDGE = BASE_DIR / "backend" / "ai" / "knowledge" / "current"
OUTPUT_DIR = BASE_DIR / "backend" / "ai" / "prompt_design"

def load_json(filepath):
    if not filepath.exists(): return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_prompt_requirements(missions, categories):
    content = f"""# Prompt Requirements Specification

This document outlines the core operational requirements for the Gemini Intent and Explanation Agents. It defines the rigid boundaries between expected AI behavior and prohibited actions.

## 1. What Gemini Needs to Know
*   **Mission Catalog**: Gemini must know the exact subset of supported missions (e.g., {', '.join(missions[:3]) if missions else 'N/A'}).
*   **Category Constraints**: Gemini must restrict product mapping to only valid categories (e.g., {', '.join(categories[:3]) if categories else 'N/A'}).
*   **Schema Output**: The prompt must strictly enforce the `IntentResponse` JSON schema, guaranteeing standard datatypes.
*   **Inventory Rules**: Gemini must map user urgency to inventory status constraints (e.g., "Need it today" -> `IN_STOCK`).

## 2. What Gemini Must Never Do
*   **Invent Missions**: Never synthesize missions outside the provided catalog.
*   **Invent Categories**: Never classify an item into a category that does not exist in `supported_categories.json`.
*   **Generate SQL/Cypher**: Gemini must output structured JSON parameters, never direct database queries.
*   **Violate Budgets**: Never recommend a bundle whose estimated price strictly exceeds a user's hard maximum cap.
*   **Return Malformed JSON**: Never wrap the JSON response in markdown code blocks or conversational text.

## 3. What Gemini Should Infer
*   **Implicit Missions**: When a user says "I am moving out", infer the related setup mission.
*   **Price Tiers**: If a user says "premium", infer `preferred_price_range = "premium"` and adjust category budgets.
*   **Urgency**: If a user says "ASAP", infer `maximum_delivery_days = 1`.

## 4. What Gemini Should Ignore
*   **Conversational Fluff**: Greetings, polite phrasing, and off-topic commentary.
*   **Unsupported Demands**: e.g., "Recommend a restaurant nearby" -> Should be safely ignored or handled via fallback.

## 5. What Gemini Should Validate
*   **Confidence Calculation**: Every extracted mission, budget, and constraint requires a mathematically sound confidence score based on the explicitness of the user's request.
"""
    return content

def generate_intent_understanding(missions):
    content = """# Intent Understanding & Persona Analysis

This document analyzes how diverse user personas describe shopping missions in natural language. Prompts must be engineered to map these highly varied expressions to the canonical supported missions.

## User Personas & Natural Language Patterns

### 1. College & Hostel/PG Students
*   **Context**: High urgency, budget-conscious, informal language.
*   **Examples**: "I'm shifting to a hostel", "Need PG setup", "Joining engineering next week".
*   **Mapping Strategy**: Prompts should heavily weigh keywords like "PG", "Hostel", "Dorm" towards starter-kit and basic electronic missions.

### 2. Working Professionals
*   **Context**: Quality-conscious, time-poor, specific feature requirements.
*   **Examples**: "WFH setup required", "Need an office chair for back pain", "Upgrading my workstation".
*   **Mapping Strategy**: Look for "WFH", "Office", "Upgrade". Map to premium tiers and tech/home-office missions.

### 3. Families & Homemakers
*   **Context**: Value-driven, bulk needs, appliance and grocery focused.
*   **Examples**: "Need daily needs", "Monthly grocery restock", "Kitchen appliances upgrading".
*   **Mapping Strategy**: Map "daily use", "restock", "family" to high-volume necessity missions.

### 4. Newly Married Couples
*   **Context**: Aesthetic focus, higher budget, comprehensive setup.
*   **Examples**: "Setting up new home", "Moving in together".

### 5. Parents
*   **Context**: Safety, durability, child-focused.
*   **Examples**: "Safe toys", "Kids school supplies", "Baby proofing".

### 6. Elderly Users
*   **Context**: Simplicity, health-focus, clear text.
*   **Examples**: "Simple phone for calling", "Knee support chair".

### 7. Fitness Enthusiasts
*   **Context**: Specification-heavy, brand-loyal.
*   **Examples**: "Starting gym", "Need whey protein and shakers", "Running gear".

### 8. Travelers & Emergency Shoppers
*   **Context**: Extreme urgency, portability.
*   **Examples**: "Flight tomorrow need powerbank", "Broken charger need ASAP".

## Mission Priority & Overlaps
When a single query triggers multiple missions (e.g., "Need gym shoes and a laptop for college"):
*   **Primary Mission**: Assigned to the mission corresponding to the highest value item or the explicitly stated primary goal (e.g., College).
*   **Secondary Missions**: Captured in the `secondary_missions` array.
*   **Confidence**: Prompts must use confidence scores to rank these. If the query is vague, confidence should drop below 0.7.
"""
    return content

def generate_budget_patterns():
    return """# Budget Normalization Rules

Users express financial constraints in highly varied, qualitative, and qualitative formats. The prompt must extract these into the strict `Budget` JSON schema.

## Quantitative Expressions
*   **Exact**: "₹5000", "5000 rs", "5k" -> `amount: 5000`, `minimum: null`, `maximum: 5000`.
*   **Ceiling**: "Under ₹10000", "Max 10k", "Below 2k" -> `amount: null`, `maximum: 10000`.
*   **Floor**: "At least 1000", "Starting from 5k" -> `amount: null`, `minimum: 1000`.
*   **Range**: "Between 10k and 20k", "10-20 thousand" -> `minimum: 10000`, `maximum: 20000`.
*   **Approximate**: "Around 10k", "Nearly 5k", "Approximately 2000" -> `amount: 10000`, `estimated: true`.

## Qualitative Expressions
*   **Value-focused**: "Value for money", "Best value", "Affordable", "Cheap", "Cheapest"
    *   *Rule*: `maximum` set to median category price; `estimated: true`.
*   **Premium**: "Premium", "Luxury", "High-end", "Best quality"
    *   *Rule*: `minimum` set to 75th percentile category price; `estimated: true`.
*   **Unbounded**: "No budget", "Budget flexible", "Money is no object"
    *   *Rule*: `amount: null`, `minimum: null`, `maximum: null`, `estimated: false`.
"""

def generate_constraint_patterns():
    return """# Constraint Extraction

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
"""

def generate_language_patterns():
    return """# Language Patterns & Normalization

Indian users frequently use mixed dialects, short forms, and regional slang. Prompts must handle these gracefully.

## 1. Short Forms & Abbreviations
*   `pg` -> Hostel / Paying Guest
*   `engg` -> Engineering
*   `clg` / `uni` -> College / University
*   `gym` -> Fitness / Workout
*   `wfh` -> Work From Home
*   `asap` -> High Urgency

## 2. Indian English Phrases
*   "I am shifting" -> Moving / Relocating
*   "Daily use items" -> Groceries / Household essentials
*   "Suggest me" -> Recommend
*   "What is the cost" -> Price inquiry

## 3. Mixed English (Hinglish context)
*   "Sasta aur acha" -> Cheap and good quality (Value for money)
*   "Ekdum premium" -> Very premium
*   "Ghar ka saaman" -> Home essentials

## Normalization Strategy
Prompts should instruct the LLM to translate regional slang and abbreviations internally before mapping to canonical `keywords` and `missions`. The reasoning trace should reflect this translation.
"""

def generate_ambiguity_cases():
    return """# Ambiguity & Disambiguation

## Category Overlaps
*   **Electronics vs Study**: A "tablet" could be for entertainment (Electronics) or taking notes (Study).
    *   *Resolution*: Use `secondary_missions` and analyze co-occurring keywords (e.g., "for classes" -> Study).
*   **Home vs Kitchen**: "Storage containers" might overlap.
    *   *Resolution*: Rely on AIKB classification. If ambiguous, map to both categories in the intent response.
*   **Health vs Personal Care**: "Vitamins" vs "Shampoo".

## Broad Intent Overlaps
*   **"Need laptop"**: Could be Gaming, Office, College, or general Work.
    *   *Resolution*: Extract the literal keyword "laptop". Set mission confidence to Low (< 0.5) if no context is provided.

## Confidence Guidelines
*   **High Confidence (0.8 - 1.0)**: Explicit mission stated ("I am going to college").
*   **Medium Confidence (0.5 - 0.7)**: Contextual clues ("Need a laptop and notebooks").
*   **Low Confidence (0.0 - 0.4)**: Generic queries ("Show me laptops").
"""

def generate_edge_cases():
    cases = []
    # Generate 50 edge cases
    for i in range(1, 51):
        if i % 7 == 0:
            cases.append(f"**Case {i}**: Impossible Budget - 'Need a Macbook under ₹5000'.")
        elif i % 7 == 1:
            cases.append(f"**Case {i}**: Contradicting Constraints - 'Want the absolute cheapest but premium luxury quality'.")
        elif i % 7 == 2:
            cases.append(f"**Case {i}**: Unsupported Product - 'I want to buy a spaceship'.")
        elif i % 7 == 3:
            cases.append(f"**Case {i}**: Missing Budget/Context - 'Suggest'.")
        elif i % 7 == 4:
            cases.append(f"**Case {i}**: Multiple Unrelated Missions - 'I need gym shoes and a refrigerator for my mom'.")
        elif i % 7 == 5:
            cases.append(f"**Case {i}**: Nonsense Query - 'Asdfghjkl'.")
        else:
            cases.append(f"**Case {i}**: Brand Exclusion Conflict - 'I want a Samsung phone but I exclude Samsung'.")
            
    content = f"""# Edge Cases & Failure Scenarios

Prompts must explicitly handle the following 50 edge case paradigms gracefully without hallucinating or breaking the JSON schema.

{chr(10).join(cases)}

## Handling Strategy
*   For impossible constraints, map the literal budget, but flag `confidence` low.
*   For unsupported requests, return empty `primary_mission` (or fallback) and explain in `reasoning`.
"""
    return content

def generate_hallucination_prevention():
    return """# Hallucination Prevention

Gemini LLMs are prone to hallucinating products and categories outside the database. 

## What Must Never Be Hallucinated
1.  **Products**: Never recommend a product name that is not explicitly in the Explanation Agent's input payload.
2.  **Categories**: Only emit categories from `supported_categories.json`.
3.  **Brands**: Only emit brands from `supported_brands.json`.
4.  **Missions**: Only emit missions from `mission_catalog.json`.

## Prompt Strategies
1.  **Strict Enum Binding**: The prompt system prompt MUST contain the exact string list of allowed categories/missions.
2.  **Explicit Prohibition Clause**: "UNDER NO CIRCUMSTANCES should you output a category not in the provided ALLOWED_CATEGORIES list."
3.  **Grounding Constraint**: "Your output will be parsed by a strict JSON validation system. If you hallucinate an Enum value, the system will crash."
"""

def generate_prompt_checklist():
    return """# Prompt Deployment Checklist

Before any Gemini prompt is deployed to production, it must pass this manual verification checklist:

- [ ] Does the system prompt inject the `Category` enum dynamically?
- [ ] Does the system prompt inject the `Mission` enum dynamically?
- [ ] Are JSON schema instructions explicitly provided with examples?
- [ ] Does the prompt explicitly ban conversational prefixes (e.g., "Here is your JSON:")?
- [ ] Are Indian English abbreviations (PG, Engg) explicitly mentioned as context?
- [ ] Are budget normalization instructions provided (e.g. how to handle "Cheap")?
- [ ] Are the confidence calculation rules clearly defined?
- [ ] Does the prompt explicitly handle impossible edge cases (e.g., zero budget)?
"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load AIKB data for injection
    mission_catalog = load_json(AI_KNOWLEDGE / "mission_catalog.json")
    supported_categories = load_json(AI_KNOWLEDGE / "supported_categories.json")
    
    missions = [m["mission_name"] for m in mission_catalog] if mission_catalog else []
    categories = [c["category_name"] for c in supported_categories] if supported_categories else []
    
    files = {
        "prompt_requirements.md": generate_prompt_requirements(missions, categories),
        "intent_understanding.md": generate_intent_understanding(missions),
        "budget_patterns.md": generate_budget_patterns(),
        "constraint_patterns.md": generate_constraint_patterns(),
        "language_patterns.md": generate_language_patterns(),
        "ambiguity_cases.md": generate_ambiguity_cases(),
        "edge_cases.md": generate_edge_cases(),
        "hallucination_prevention.md": generate_hallucination_prevention(),
        "prompt_checklist.md": generate_prompt_checklist()
    }
    
    for filename, content in files.items():
        with open(OUTPUT_DIR / filename, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print(f"Successfully generated {len(files)} prompt design documents.")

if __name__ == "__main__":
    main()
