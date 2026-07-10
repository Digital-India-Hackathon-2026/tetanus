# FEW-SHOT EXAMPLES

## Example 1: Clear Hostel Setup with Budget
User: "I'm moving into a hostel next month. Need room setup items under 5000."
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Hostel Setup",
  "secondary_missions": [],
  "overall_confidence": 0.95,
  "categories": [
    "Home",
    "Office"
  ],
  "keywords": [
    "hostel",
    "room setup"
  ],
  "budget": {
    "amount": null,
    "currency": "INR",
    "minimum": null,
    "maximum": 5000.0,
    "estimated": false,
    "confidence": 0.95
  },
  "constraints": {
    "preferred_brands": [],
    "excluded_brands": [],
    "preferred_categories": [],
    "must_have": [],
    "nice_to_have": [],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User needs hostel room setup essentials under 5000 INR.",
  "needs_clarification": false,
  "questions": []
}

## Example 2: Ambiguous Request needing Clarification
User: "I want to buy some products."
Output:
{
  "intent_status": "UNSUPPORTED",
  "primary_mission": null,
  "secondary_missions": [],
  "overall_confidence": 0.15,
  "categories": [],
  "keywords": [
    "products"
  ],
  "budget": {
    "amount": null,
    "currency": "INR",
    "minimum": null,
    "maximum": null,
    "estimated": false,
    "confidence": 0.0
  },
  "constraints": {
    "preferred_brands": [],
    "excluded_brands": [],
    "preferred_categories": [],
    "must_have": [],
    "nice_to_have": [],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User requested generic products without context.",
  "needs_clarification": true,
  "questions": [
    {
      "id": "ASK_USAGE_CONTEXT",
      "question": "What kind of items are you looking for today?",
      "type": "SINGLE_SELECT",
      "options": [
        "Hostel Setup",
        "Gym Starter",
        "Weekly Grocery",
        "Office Setup",
        "Snacks"
      ]
    }
  ]
}

## Example 3: Gym Setup under Budget
User: "Need gym gear under 3000 rupees"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Gym Starter",
  "secondary_missions": [],
  "overall_confidence": 0.95,
  "categories": [
    "Sports",
    "Beauty"
  ],
  "keywords": [
    "gym",
    "gear"
  ],
  "budget": {
    "amount": null,
    "currency": "INR",
    "minimum": null,
    "maximum": 3000.0,
    "estimated": false,
    "confidence": 0.95
  },
  "constraints": {
    "preferred_brands": [],
    "excluded_brands": [],
    "preferred_categories": [],
    "must_have": [],
    "nice_to_have": [],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants workout/gym gear with a budget limit of 3000 INR.",
  "needs_clarification": false,
  "questions": []
}

## Example 4: Travel Packing with specific brand
User: "going on a trip, need travel essentials, only Nivea products"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Travel Packing Essentials",
  "secondary_missions": [],
  "overall_confidence": 0.92,
  "categories": [
    "Beauty",
    "Other"
  ],
  "keywords": [
    "trip",
    "travel"
  ],
  "budget": {
    "amount": null,
    "currency": "INR",
    "minimum": null,
    "maximum": null,
    "estimated": false,
    "confidence": 0.0
  },
  "constraints": {
    "preferred_brands": [
      "Nivea"
    ],
    "excluded_brands": [],
    "preferred_categories": [],
    "must_have": [],
    "nice_to_have": [],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants travel toiletries, restricted specifically to the brand Nivea.",
  "needs_clarification": false,
  "questions": []
}

## Example 5: Hinglish Query (College Setup)
User: "college start ho raha hai, desk setup ke liye notebook and pen chahiye cheap range me"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Office/Study Desk Setup",
  "secondary_missions": [],
  "overall_confidence": 0.9,
  "categories": [
    "Office"
  ],
  "keywords": [
    "college",
    "desk",
    "notebook",
    "pen"
  ],
  "budget": {
    "amount": null,
    "currency": "INR",
    "minimum": null,
    "maximum": null,
    "estimated": false,
    "confidence": 0.0
  },
  "constraints": {
    "preferred_brands": [],
    "excluded_brands": [],
    "preferred_categories": [],
    "must_have": [],
    "nice_to_have": [],
    "preferred_price_range": "cheap",
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User requires budget study stationary for a college desk setup.",
  "needs_clarification": false,
  "questions": []
}

## Example 6: Double Mission
User: "I need to set up my new hostel room and also want to start working out"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Hostel Setup",
  "secondary_missions": [
    "Gym Starter"
  ],
  "overall_confidence": 0.88,
  "categories": [
    "Home",
    "Sports",
    "Office"
  ],
  "keywords": [
    "hostel",
    "room",
    "workout"
  ],
  "budget": {
    "amount": null,
    "currency": "INR",
    "minimum": null,
    "maximum": null,
    "estimated": false,
    "confidence": 0.0
  },
  "constraints": {
    "preferred_brands": [],
    "excluded_brands": [],
    "preferred_categories": [],
    "must_have": [],
    "nice_to_have": [],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User needs items for both hostel room setup and beginning workout routines.",
  "needs_clarification": true,
  "questions": [
    {
      "id": "ASK_BUDGET",
      "question": "What is your combined budget for both setups?",
      "type": "NUMBER",
      "options": []
    }
  ]
}

## Example 7: Monthly Grocery (Unambiguous)
User: "weekly grocery and household cleaning items, budget 2000"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Weekly Grocery",
  "secondary_missions": [
    "Home Cleaning & Sanitation"
  ],
  "overall_confidence": 0.94,
  "categories": [
    "Groceries",
    "Other"
  ],
  "keywords": [
    "grocery",
    "cleaning"
  ],
  "budget": {
    "amount": 2000.0,
    "currency": "INR",
    "minimum": null,
    "maximum": 2000.0,
    "estimated": false,
    "confidence": 0.95
  },
  "constraints": {
    "preferred_brands": [],
    "excluded_brands": [],
    "preferred_categories": [],
    "must_have": [],
    "nice_to_have": [],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User requires home groceries and cleaning supplies for 2000 INR.",
  "needs_clarification": false,
  "questions": []
}

## Example 8: Work From Home Setup
User: "setting up home office for remote work. Need desk organizer, led light, and cord"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Office/Study Desk Setup",
  "secondary_missions": [
    "Freelancer Remote Setup"
  ],
  "overall_confidence": 0.91,
  "categories": [
    "Office",
    "Electronics",
    "Home"
  ],
  "keywords": [
    "home office",
    "remote",
    "desk"
  ],
  "budget": {
    "amount": null,
    "currency": "INR",
    "minimum": null,
    "maximum": null,
    "estimated": false,
    "confidence": 0.0
  },
  "constraints": {
    "preferred_brands": [],
    "excluded_brands": [],
    "preferred_categories": [],
    "must_have": [],
    "nice_to_have": [],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User requires study desk and remote freelancer setup items.",
  "needs_clarification": false,
  "questions": []
}

## Example 9: Personal Care with constraints
User: "shaving creams and razors, no gillette brand please"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Men's Shaving Ritual",
  "secondary_missions": [],
  "overall_confidence": 0.95,
  "categories": [
    "Beauty",
    "Other"
  ],
  "keywords": [
    "shaving",
    "razors"
  ],
  "budget": {
    "amount": null,
    "currency": "INR",
    "minimum": null,
    "maximum": null,
    "estimated": false,
    "confidence": 0.0
  },
  "constraints": {
    "preferred_brands": [],
    "excluded_brands": [
      "Gillette"
    ],
    "preferred_categories": [],
    "must_have": [],
    "nice_to_have": [],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants shaving items but explicitly excludes Gillette.",
  "needs_clarification": false,
  "questions": []
}

## Example 10: Emoji and Short Input
User: "✈️ packing essentials"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Travel Packing Essentials",
  "secondary_missions": [],
  "overall_confidence": 0.92,
  "categories": [
    "Other"
  ],
  "keywords": [
    "packing",
    "travel"
  ],
  "budget": {
    "amount": null,
    "currency": "INR",
    "minimum": null,
    "maximum": null,
    "estimated": false,
    "confidence": 0.0
  },
  "constraints": {
    "preferred_brands": [],
    "excluded_brands": [],
    "preferred_categories": [],
    "must_have": [],
    "nice_to_have": [],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User requires travel packing essentials.",
  "needs_clarification": false,
  "questions": []
}

## Example 11: Long Conversational Query
User: "Hi, I just shifted to Pune for my job. I got a 1BHK. I need to get normal items like tea, coffee, some biscuits, oil for cooking, and maybe a basic bedsheet for the room. Under 4000 total."
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Weekly Grocery",
  "secondary_missions": [
    "Hostel Setup"
  ],
  "overall_confidence": 0.91,
  "categories": [
    "Groceries",
    "Home"
  ],
  "keywords": [
    "shifted",
    "tea",
    "coffee",
    "biscuits",
    "oil",
    "bedsheet"
  ],
  "budget": {
    "currency": "INR",
    "maximum": 4000.0,
    "confidence": 0.95
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User shifted to Pune and needs groceries and basic bedding under 4000 INR.",
  "needs_clarification": false
}

## Example 12: Unsupported Request (Hallucination Prevention)
User: "I want to buy a high-end luxury sports car"
Output:
{
  "intent_status": "UNSUPPORTED",
  "overall_confidence": 0.1,
  "keywords": [
    "sports car"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User is searching for products unsupported by our catalog.",
  "needs_clarification": true,
  "questions": [
    {
      "id": "ASK_MISSING_CATEGORY",
      "question": "We specialize in daily household, gym, study, grocery, and travel items. Would you like to shop in one of these areas instead?",
      "type": "SINGLE_SELECT",
      "options": [
        "Hostel Setup",
        "Gym Starter",
        "Weekly Grocery",
        "Office Setup",
        "Snacks"
      ]
    }
  ]
}

## Example 13: Budget-only Query
User: "under 1000 rupees"
Output:
{
  "intent_status": "AMBIGUOUS",
  "overall_confidence": 0.2,
  "keywords": [
    "under 1000"
  ],
  "budget": {
    "currency": "INR",
    "maximum": 1000.0,
    "confidence": 0.95
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User entered a budget constraint without specifying product interest.",
  "needs_clarification": true,
  "questions": [
    {
      "id": "ASK_USAGE_CONTEXT",
      "question": "What items are you planning to buy with your 1000 INR budget?",
      "type": "SINGLE_SELECT",
      "options": [
        "Hostel Setup",
        "Gym Starter",
        "Weekly Grocery",
        "Office Setup",
        "Snacks"
      ]
    }
  ]
}

## Example 14: Car Grooming
User: "shampoo and polish for my car"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Car Care Maintenance",
  "overall_confidence": 0.96,
  "categories": [
    "Automotive"
  ],
  "keywords": [
    "car",
    "polish",
    "shampoo"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants car maintenance products (polish and shampoo).",
  "needs_clarification": false
}

## Example 15: Typo-heavy Input
User: "hstel bedhseet and pilow"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Hostel Setup",
  "overall_confidence": 0.92,
  "categories": [
    "Home"
  ],
  "keywords": [
    "hostel",
    "bedsheet",
    "pillow"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants bedding setup for a hostel room.",
  "needs_clarification": false
}

## Example 16: Oral Care with Brand Preference
User: "Colgate toothpaste and mouthwash"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Oral Care Deep Clean",
  "overall_confidence": 0.95,
  "categories": [
    "Automotive"
  ],
  "keywords": [
    "toothpaste",
    "mouthwash"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "preferred_brands": [
      "Colgate"
    ],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User requires Colgate oral care essentials.",
  "needs_clarification": false
}

## Example 17: Organic Food Preferences
User: "organic grocery seeds and apricots, vegetarian"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Weekly Grocery",
  "overall_confidence": 0.91,
  "categories": [
    "Groceries"
  ],
  "keywords": [
    "organic",
    "seeds",
    "apricots"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "must_have": [
      "organic",
      "vegetarian"
    ],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User requires vegetarian organic groceries (seeds and apricots).",
  "needs_clarification": false
}

## Example 18: Birthday Party Accessories
User: "need balloons and candles for a birthday party"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Birthday Party Prep",
  "overall_confidence": 0.96,
  "categories": [
    "Other"
  ],
  "keywords": [
    "balloons",
    "candles",
    "birthday"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants birthday party accessories.",
  "needs_clarification": false
}

## Example 19: Extreme Budget Range
User: "office desk setup between 5000 and 15000"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Office/Study Desk Setup",
  "overall_confidence": 0.94,
  "categories": [
    "Office",
    "Home"
  ],
  "keywords": [
    "office",
    "desk"
  ],
  "budget": {
    "currency": "INR",
    "minimum": 5000.0,
    "maximum": 15000.0,
    "confidence": 0.95
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants office desk setup with budget between 5000 and 15000 INR.",
  "needs_clarification": false
}

## Example 20: Baby Care with specific need
User: "shampoo and powder for baby"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Baby Care Essentials",
  "secondary_missions": [
    "Newborn Baby Care"
  ],
  "overall_confidence": 0.93,
  "categories": [
    "Beauty",
    "Other"
  ],
  "keywords": [
    "shampoo",
    "powder",
    "baby"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants baby care toiletries (shampoo and powder).",
  "needs_clarification": false
}

## Example 21: High-end Premium Request
User: "I want premium chocolate gift boxes"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Birthday Party Prep",
  "overall_confidence": 0.89,
  "categories": [
    "Other"
  ],
  "keywords": [
    "premium",
    "chocolate",
    "gift"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "must_have": [
      "premium"
    ],
    "preferred_price_range": "premium",
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User requires premium chocolate gift boxes.",
  "needs_clarification": false
}

## Example 22: Home Sanitation & Detergents
User: "need fabric conditioner and kitchen towels"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Home Cleaning & Sanitation",
  "secondary_missions": [
    "Hostel Room Cleaning"
  ],
  "overall_confidence": 0.93,
  "categories": [
    "Other",
    "Office"
  ],
  "keywords": [
    "conditioner",
    "towels"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User requires household cleaning supplies and fabric conditioner.",
  "needs_clarification": false
}

## Example 23: Dorm Cooking
User: "electric kettle and instant soup for hostel room"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Dorm Cooking Essentials",
  "secondary_missions": [
    "Hostel Setup"
  ],
  "overall_confidence": 0.94,
  "categories": [
    "Groceries",
    "Home",
    "Electronics"
  ],
  "keywords": [
    "electric kettle",
    "instant soup",
    "hostel"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User needs quick-cooking dorm essentials (kettle and soup).",
  "needs_clarification": false
}

## Example 24: High-performance Tech
User: "high speed type C charging cables"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Freelancer Remote Setup",
  "secondary_missions": [
    "Movie Night"
  ],
  "overall_confidence": 0.88,
  "categories": [
    "Electronics"
  ],
  "keywords": [
    "high speed",
    "type C"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "must_have": [
      "high speed"
    ],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User requires high-speed Type-C cords.",
  "needs_clarification": false
}

## Example 25: Fitness Health drinks
User: "healthy energy drink with orange flavor"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Summer Hydration Kit",
  "secondary_missions": [
    "First Aid & Wellness"
  ],
  "overall_confidence": 0.9,
  "categories": [
    "Other"
  ],
  "keywords": [
    "energy drink",
    "orange"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "must_have": [
      "orange flavor"
    ],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants an orange-flavored energy/hydration drink.",
  "needs_clarification": false
}

## Example 26: Dog Food
User: "gravy food pack for puppies"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Pet Grooming Essentials",
  "secondary_missions": [
    "Dorm Cooking Essentials"
  ],
  "overall_confidence": 0.87,
  "categories": [
    "Other"
  ],
  "keywords": [
    "gravy food",
    "puppy"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "must_have": [
      "puppy"
    ],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants wet puppy food packets.",
  "needs_clarification": false
}

## Example 27: Evening Cookies
User: "cookies and coffee powder"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Evening Tea/Coffee Break",
  "secondary_missions": [
    "Weekly Grocery"
  ],
  "overall_confidence": 0.94,
  "categories": [
    "Groceries"
  ],
  "keywords": [
    "cookies",
    "coffee"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants coffee and cookies for a tea break.",
  "needs_clarification": false
}

## Example 28: Emergency Lighting
User: "rechargeable bulb and torch"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Emergency Power & Lighting",
  "overall_confidence": 0.96,
  "categories": [
    "Electronics",
    "Home"
  ],
  "keywords": [
    "rechargeable",
    "bulb",
    "torch"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User needs emergency backup lighting (rechargeable bulb and torch).",
  "needs_clarification": false
}

## Example 29: Skin Protection
User: "shampoo for dandruff and face wash"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Car Care Maintenance",
  "secondary_missions": [
    "Gym Starter"
  ],
  "overall_confidence": 0.88,
  "categories": [
    "Beauty"
  ],
  "keywords": [
    "dandruff",
    "shampoo",
    "face wash"
  ],
  "budget": {
    "currency": "INR"
  },
  "constraints": {
    "must_have": [
      "dandruff protection"
    ],
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants anti-dandruff shampoo and face wash.",
  "needs_clarification": false
}

## Example 30: Healthy Snacks
User: "pumpkin seeds and almonds under 1500"
Output:
{
  "intent_status": "SUPPORTED",
  "primary_mission": "Healthy Snacking",
  "overall_confidence": 0.94,
  "categories": [
    "Groceries"
  ],
  "keywords": [
    "pumpkin seeds",
    "almonds"
  ],
  "budget": {
    "currency": "INR",
    "maximum": 1500.0,
    "confidence": 0.95
  },
  "constraints": {
    "urgency": "NORMAL"
  },
  "reasoning_summary": "User wants healthy seeds and nuts under 1500 INR.",
  "needs_clarification": false
}
