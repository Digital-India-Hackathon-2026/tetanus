# Language Patterns & Normalization

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
