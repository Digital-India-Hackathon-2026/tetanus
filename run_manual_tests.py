import requests
import time
import json

missions = [
    "I'm moving into my first hostel",
    "I'm moving into my first apartment",
    "I want to start running",
    "I want to improve my fitness",
    "Weekly grocery shopping",
    "Monthly grocery shopping",
    "I need study essentials",
    "I need electronics for my home",
    "I want to organize my room",
    "I need cleaning essentials",
    "I need skincare essentials",
    "I need hair care products",
    "I want to set up a work from home office",
    "I need a birthday gift",
    "I'm hosting a Diwali party",
    "I need protein supplements",
    "I need clothes for college",
    "I need sportswear",
    "I want to buy gadgets",
    "I need a home office setup",
    "I want to buy a motorcycle"
]

results_markdown = ""

for index, mission in enumerate(missions):
    start = time.time()
    try:
        response = requests.post("http://localhost:8000/mission", json={"mission": mission})
        duration = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            cats = data.get("mission", {}).get("categories", [])
            recs = len(data.get("recommendations", []))
            bundle_score = data.get("bundle", {}).get("readiness_score", 0)
            has_summary = bool(data.get("summary"))
            has_tips = len(data.get("shopping_tips", [])) > 0
            
            # Formatting as a markdown table row
            status = "✅ PASS"
            
            results_markdown += f"| {index+1} | {mission} | {cats} | {recs} | {bundle_score}% | {has_summary} | {has_tips} | {duration:.2f}s | {status} |\n"
        else:
            results_markdown += f"| {index+1} | {mission} | N/A | N/A | N/A | False | False | {duration:.2f}s | ❌ FAIL ({response.status_code}) |\n"
            
    except Exception as e:
        results_markdown += f"| {index+1} | {mission} | N/A | N/A | N/A | False | False | N/A | ❌ ERROR ({str(e)}) |\n"

with open("test_results.md", "w", encoding="utf-8") as f:
    f.write(results_markdown)
