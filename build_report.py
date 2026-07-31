import json

# Read today's data
with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

today = '2026-07-31'
today_items = [i for i in all_data if i.get('date') == today]
major_events = [i for i in today_items if i.get('is_major_event')]

# Count by category
cats = {}
for i in today_items:
    c = i.get('category', 'unknown')
    cats[c] = cats.get(c, 0) + 1

# Read insights
with open('data/inspiration_2026-07-31.json', 'r', encoding='utf-8') as f:
    insights_data = json.load(f)

insights = insights_data.get('insights', [])

# Print summary for report building
print(f"Total new: {len(today_items)}")
print(f"Major events: {len(major_events)}")
for cat, count in sorted(cats.items()):
    print(f"  {cat}: {count}")
print()
print("Major events (top 5):")
for item in major_events[:5]:
    print(f"  [{item['importance']}] {item['title']}")
    print(f"      {item['summary'][:80]}...")
print()
print("Insights:")
for ins in insights:
    print(f"  [{ins['type']}] {ins['title']}")
    print(f"    {ins.get('summary','') or ins.get('body','')[:100]}")
