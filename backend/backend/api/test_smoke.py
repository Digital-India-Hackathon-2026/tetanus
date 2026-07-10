import asyncio
from backend.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

SCENARIOS = [
    "I'm moving into a hostel with a budget of ₹5000",
    "I need to setup a home office for under ₹20000",
    "It's my son's 5th birthday, need party supplies",
    "Going on a trip to Europe, need travel essentials",
    "Starting a home gym, need equipment",
    "Need snacks and things for a movie night",
    "Setting up a gaming rig, need accessories",
    "Going to college, need stationary and a bag",
    "I want to book a flight ticket"
]

def run_smoke_tests():
    print("\n" + "="*50)
    print("PRODUCTION SMOKE TEST")
    print("="*50 + "\n")
    
    import time
    for query in SCENARIOS:
        safe_query = query.encode("ascii", "ignore").decode("ascii")
        print(f"\nTesting Scenario: {safe_query}")
        print("Sleeping for 10 seconds to avoid Gemini API rate limits...")
        time.sleep(10)
        response = client.post("/api/v1/recommend", json={"query": query})
        
        if response.status_code != 200:
            print(f"  [FAIL] HTTP {response.status_code}: {response.text}")
            continue
            
        data = response.json()
        status = data.get("status")
        
        if status == "needs_clarification":
            print("  [PASS] Clarification requested successfully.")
            continue
            
        mission = data.get("mission", "")
        products = data.get("products", [])
        bundles = data.get("bundles", [])
        explanation = data.get("explanation", "")
        
        if not products and not bundles:
            if "I'm sorry" in explanation:
                print("  [PASS] Unsupported mission handled successfully.")
            else:
                print("  [WARN] No products or bundles returned, but mission was supported.")
            continue
            
        print("  [PASS] Full pipeline executed successfully.")
        print(f"    - Mission: {mission}")
        print(f"    - Products: {len(products)}")
        print(f"    - Bundles: {len(bundles)}")
        
        if bundles:
            b = bundles[0]
            print(f"    - Bundle Readiness: {b.get('readiness_score', 0):.2f}")
            print(f"    - Missing Essentials: {b.get('essential_items_missing', [])}")

if __name__ == "__main__":
    run_smoke_tests()
