# Intent Understanding & Persona Analysis

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
