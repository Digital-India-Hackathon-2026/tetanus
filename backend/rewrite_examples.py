import json
import re
import os

with open('backend/ai/prompts/intent/examples.md', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to parse each example and update its JSON.
blocks = re.split(r'(## Example \d+: .+?\nUser: ".+?"\nOutput:\n)', content)

out_content = "# FEW-SHOT EXAMPLES\n\n"

for i in range(1, len(blocks), 2):
    header_user = blocks[i]
    json_str = blocks[i+1].strip()
    
    # parse JSON
    try:
        data = json.loads(json_str)
        
        # apply changes
        if 'reasoning' in data:
            del data['reasoning']
        
        # update confidence -> overall_confidence
        if 'confidence' in data:
            data['overall_confidence'] = data.pop('confidence')
            
        if 'constraints' in data:
            data['constraints']['urgency'] = "NORMAL"
            
        data['intent_status'] = "SUPPORTED" if data.get('primary_mission') else ("AMBIGUOUS" if data.get('needs_clarification') else "UNSUPPORTED")
        if data['overall_confidence'] < 0.2:
            data['intent_status'] = "UNSUPPORTED"
            
        # questions id update
        for q in data.get('questions', []):
            if q['id'] in ['purpose', 'budget_preference', 'unsupported_product']:
                q['id'] = 'Q_USAGE_CONTEXT' if q['id'] == 'purpose' else ('Q_BUDGET' if q['id'] == 'budget_preference' else 'Q_MISSING_CATEGORY')

        # re-order fields roughly
        new_data = {
            "intent_status": data['intent_status'],
            "primary_mission": data.get("primary_mission"),
            "secondary_missions": data.get("secondary_missions", []),
            "overall_confidence": data.get("overall_confidence", 0.0),
            "categories": data.get("categories", []),
            "keywords": data.get("keywords", []),
            "budget": data.get("budget", {}),
            "constraints": data.get("constraints", {}),
            "reasoning_summary": data.get("reasoning_summary", ""),
            "needs_clarification": data.get("needs_clarification", False),
            "questions": data.get("questions", [])
        }
        
        # For compact examples (> 10), we can just remove empty arrays/nulls to make it compact
        is_compact = (i // 2) >= 10
        if is_compact:
            compact_data = {}
            for k, v in new_data.items():
                if v or isinstance(v, bool) or isinstance(v, float) or isinstance(v, int):
                    compact_data[k] = v
            # compact budget/constraints
            if 'budget' in compact_data:
                compact_data['budget'] = {k: v for k, v in compact_data['budget'].items() if v}
            if 'constraints' in compact_data:
                compact_data['constraints'] = {k: v for k, v in compact_data['constraints'].items() if v}
            new_data = compact_data

        new_json_str = json.dumps(new_data, indent=2)
        out_content += header_user + new_json_str + "\n\n"
        
    except Exception as e:
        print(f"Error parsing JSON in block {i}: {e}")
        out_content += header_user + json_str + "\n\n"

with open('backend/ai/prompts/intent/examples.md', 'w', encoding='utf-8') as f:
    f.write(out_content.strip() + "\n")

print("Rewritten examples.md")
