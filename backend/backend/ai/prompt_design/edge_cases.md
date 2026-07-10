# Edge Cases & Failure Scenarios

Prompts must explicitly handle the following 50 edge case paradigms gracefully without hallucinating or breaking the JSON schema.

**Case 1**: Contradicting Constraints - 'Want the absolute cheapest but premium luxury quality'.
**Case 2**: Unsupported Product - 'I want to buy a spaceship'.
**Case 3**: Missing Budget/Context - 'Suggest'.
**Case 4**: Multiple Unrelated Missions - 'I need gym shoes and a refrigerator for my mom'.
**Case 5**: Nonsense Query - 'Asdfghjkl'.
**Case 6**: Brand Exclusion Conflict - 'I want a Samsung phone but I exclude Samsung'.
**Case 7**: Impossible Budget - 'Need a Macbook under ₹5000'.
**Case 8**: Contradicting Constraints - 'Want the absolute cheapest but premium luxury quality'.
**Case 9**: Unsupported Product - 'I want to buy a spaceship'.
**Case 10**: Missing Budget/Context - 'Suggest'.
**Case 11**: Multiple Unrelated Missions - 'I need gym shoes and a refrigerator for my mom'.
**Case 12**: Nonsense Query - 'Asdfghjkl'.
**Case 13**: Brand Exclusion Conflict - 'I want a Samsung phone but I exclude Samsung'.
**Case 14**: Impossible Budget - 'Need a Macbook under ₹5000'.
**Case 15**: Contradicting Constraints - 'Want the absolute cheapest but premium luxury quality'.
**Case 16**: Unsupported Product - 'I want to buy a spaceship'.
**Case 17**: Missing Budget/Context - 'Suggest'.
**Case 18**: Multiple Unrelated Missions - 'I need gym shoes and a refrigerator for my mom'.
**Case 19**: Nonsense Query - 'Asdfghjkl'.
**Case 20**: Brand Exclusion Conflict - 'I want a Samsung phone but I exclude Samsung'.
**Case 21**: Impossible Budget - 'Need a Macbook under ₹5000'.
**Case 22**: Contradicting Constraints - 'Want the absolute cheapest but premium luxury quality'.
**Case 23**: Unsupported Product - 'I want to buy a spaceship'.
**Case 24**: Missing Budget/Context - 'Suggest'.
**Case 25**: Multiple Unrelated Missions - 'I need gym shoes and a refrigerator for my mom'.
**Case 26**: Nonsense Query - 'Asdfghjkl'.
**Case 27**: Brand Exclusion Conflict - 'I want a Samsung phone but I exclude Samsung'.
**Case 28**: Impossible Budget - 'Need a Macbook under ₹5000'.
**Case 29**: Contradicting Constraints - 'Want the absolute cheapest but premium luxury quality'.
**Case 30**: Unsupported Product - 'I want to buy a spaceship'.
**Case 31**: Missing Budget/Context - 'Suggest'.
**Case 32**: Multiple Unrelated Missions - 'I need gym shoes and a refrigerator for my mom'.
**Case 33**: Nonsense Query - 'Asdfghjkl'.
**Case 34**: Brand Exclusion Conflict - 'I want a Samsung phone but I exclude Samsung'.
**Case 35**: Impossible Budget - 'Need a Macbook under ₹5000'.
**Case 36**: Contradicting Constraints - 'Want the absolute cheapest but premium luxury quality'.
**Case 37**: Unsupported Product - 'I want to buy a spaceship'.
**Case 38**: Missing Budget/Context - 'Suggest'.
**Case 39**: Multiple Unrelated Missions - 'I need gym shoes and a refrigerator for my mom'.
**Case 40**: Nonsense Query - 'Asdfghjkl'.
**Case 41**: Brand Exclusion Conflict - 'I want a Samsung phone but I exclude Samsung'.
**Case 42**: Impossible Budget - 'Need a Macbook under ₹5000'.
**Case 43**: Contradicting Constraints - 'Want the absolute cheapest but premium luxury quality'.
**Case 44**: Unsupported Product - 'I want to buy a spaceship'.
**Case 45**: Missing Budget/Context - 'Suggest'.
**Case 46**: Multiple Unrelated Missions - 'I need gym shoes and a refrigerator for my mom'.
**Case 47**: Nonsense Query - 'Asdfghjkl'.
**Case 48**: Brand Exclusion Conflict - 'I want a Samsung phone but I exclude Samsung'.
**Case 49**: Impossible Budget - 'Need a Macbook under ₹5000'.
**Case 50**: Contradicting Constraints - 'Want the absolute cheapest but premium luxury quality'.

## Handling Strategy
*   For impossible constraints, map the literal budget, but flag `confidence` low.
*   For unsupported requests, return empty `primary_mission` (or fallback) and explain in `reasoning`.
