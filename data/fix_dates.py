import json

with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_count = 0
date_2029_count = 0

for item in data:
    if 'date' not in item:
        if 'date_added' in item:
            item['date'] = item['date_added']
            fixed_count += 1
        elif 'published' in item:
            item['date'] = item['published']
            fixed_count += 1

with open('all_inspiration.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 验证
with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)

for item in data2:
    if item.get('date') == '2026-07-29':
        date_2029_count += 1

print(f"修复条目数: {fixed_count}")
print(f"2026-07-29 条目数: {date_2029_count}")
