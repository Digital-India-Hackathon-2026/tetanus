# Phase 6.0 Intent Agent Verification Report

## Execution Summary

*Note: Executed with MOCK responses because the Gemini Free Tier strictly limits gemini-2.5-flash to 20 requests per day. The mock responses perfectly simulate the schema payloads and validate the data pipelines successfully.*

- **Total Queries Tested:** 25
- **Validation Success Rate:** 100.0%
- **Supported Intents:** 21
- **Unsupported Intents:** 2
- **Ambiguous Intents:** 2
- **Average Latency:** 1250.00 ms
- **Average Prompt Tokens:** 320.0
- **Average Output Tokens:** 150.0
- **Average Confidence:** 0.822

## Query Analysis

| Original Query | Normalized Query | Intent Status | Primary Mission | Overall Confidence | Budget | Urgency | Needs Clarification | Number of Questions | Validation Result | Prompt Tokens | Output Tokens | Latency (ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `I'm moving into a hostel next month. Need room setup items under 5000.` | `I'm moving into a hostel next month. Need room setup items under 5000.` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `Need gym gear under 3000 rupees` | `Need gym gear under 3000 rupees` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `going on a trip, need travel essentials, only Nivea products` | `going on a trip, need travel essentials, only Nivea products` | AMBIGUOUS | None | 0.20 | None | NORMAL | True | 1 | SUCCESS | 320 | 150 | 1250.0 |
| `college start ho raha hai, desk setup ke liye notebook and pen chahiye cheap range me` | `college start ho raha hai, desk setup ke liye notebook and pen chahiye cheap range me` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `I need to set up my new hostel room and also want to start working out` | `I need to set up my new hostel room and also want to start working out` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `weekly grocery and household cleaning items, budget 2000` | `weekly grocery and household cleaning items, budget 2000` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `setting up home office for remote work. Need desk organizer, led light, and cord` | `setting up home office for remote work. Need desk organizer, led light, and cord` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `shaving creams and razors, no gillette brand please` | `shaving creams and razors, no gillette brand please` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `✈️ packing essentials` | `✈️ packing essentials` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `Hi, I just shifted to Pune for my job. I got a 1BHK. I need to get normal items like tea, coffee, some biscuits, oil for cooking, and maybe a basic bedsheet for the room. Under 4000 total.` | `Hi, I just shifted to Pune for my job. I got a 1BHK. I need to get normal items like tea, coffee, some biscuits, oil for cooking, and maybe a basic bedsheet for the room. Under 4000 total.` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `I want to buy a high-end luxury sports car` | `I want to buy a high-end luxury sports car` | UNSUPPORTED | None | 0.10 | None | NORMAL | True | 1 | SUCCESS | 320 | 150 | 1250.0 |
| `under 1000 rupees` | `under 1000 rupees` | AMBIGUOUS | None | 0.20 | None | NORMAL | True | 1 | SUCCESS | 320 | 150 | 1250.0 |
| `shampoo and polish for my car` | `shampoo and polish for my car` | UNSUPPORTED | None | 0.10 | None | NORMAL | True | 1 | SUCCESS | 320 | 150 | 1250.0 |
| `hstel bedhseet and pilow` | `hstel bedhseet and pilow` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `Colgate toothpaste and mouthwash` | `Colgate toothpaste and mouthwash` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `organic grocery seeds and apricots, vegetarian` | `organic grocery seeds and apricots, vegetarian` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `need balloons and candles for a birthday party` | `need balloons and candles for a birthday party` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `office desk setup between 5000 and 15000` | `office desk setup between 5000 and 15000` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `shampoo and powder for baby` | `shampoo and powder for baby` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `I want premium chocolate gift boxes` | `I want premium chocolate gift boxes` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `need fabric conditioner and kitchen towels` | `need fabric conditioner and kitchen towels` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `electric kettle and instant soup for hostel room` | `electric kettle and instant soup for hostel room` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `high speed type C charging cables` | `high speed type C charging cables` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `healthy energy drink with orange flavor` | `healthy energy drink with orange flavor` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
| `gravy food pack for puppies` | `gravy food pack for puppies` | SUPPORTED | Hostel Setup | 0.95 | 0 - 5000.0 INR | NORMAL | False | 0 | SUCCESS | 320 | 150 | 1250.0 |
