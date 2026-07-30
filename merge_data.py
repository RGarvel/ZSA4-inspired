import json
import os

# Paths
base = r"C:\Users\阮家威\AppData\Local\hermes\data\inspiration"
all_file = os.path.join(base, "all_inspiration.json")
new_file = os.path.join(base, "temp_new_items.json")

# Load existing
with open(all_file, 'r', encoding='utf-8') as f:
    existing = json.load(f)

existing_titles = {item['title'].lower() for item in existing}

# Load new items
with open(new_file, 'r', encoding='utf-8') as f:
    new_items = json.load(f)

# Deduplicate and add
added = []
for item in new_items:
    if item['title'].lower() not in existing_titles:
        existing.append(item)
        existing_titles.add(item['title'].lower())
        added.append(item['title'])

# Save back
with open(all_file, 'w', encoding='utf-8') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f'Added {len(added)} new items')
print(f'Total now: {len(existing)}')

# Count today
today = [i for i in existing if i['date'] == '2026-07-30']
print(f'Today items: {len(today)}')
cats = {}
for i in today:
    c = i.get('category', 'unknown')
    cats[c] = cats.get(c, 0) + 1
print(f'Categories: {cats}')
major = [i for i in today if i.get('is_major_event')]
print(f'Major events: {len(major)}')
