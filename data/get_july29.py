import json

with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

july29 = [item for item in data if item.get('date') == '2026-07-29']
print(f"7.29 共 {len(july29)} 条\n")
for i, item in enumerate(july29):
    print(f"--- [{i+1}] ---")
    print(json.dumps(item, ensure_ascii=False, indent=2))
