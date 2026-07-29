import json

with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Count all dates
date_counts = {}
for item in data:
    d = item.get('date', 'NO_DATE')
    date_counts[d] = date_counts.get(d, 0) + 1

print("=== All dates ===")
for d in sorted(date_counts.keys(), reverse=True):
    print(f"  {d}: {date_counts[d]} items")

# Check July 29
july29 = [item for item in data if item.get('date') == '2026-07-29']
print(f"\n=== 2026-07-29 ({len(july29)} items) ===")
cats = {}
for item in july29:
    c = item.get('category', 'unknown')
    cats[c] = cats.get(c, 0) + 1
for c, n in sorted(cats.items()):
    print(f"  {c}: {n}")

papers = [item for item in july29 if item.get('category') == 'academic_paper']
print(f"\nPapers: {len(papers)}")
for p in papers[:3]:
    print(f"  - {p.get('title', 'N/A')[:80]}")
