import json

with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 统计有无 date 字段的条目数
with_date = 0
without_date = 0
date_fields = []

for item in data:
    if 'date' in item:
        with_date += 1
        date_fields.append(item['date'])
    else:
        without_date += 1
        # 打印第一条没有 date 字段的条目结构
        if without_date == 1:
            print("示例：缺少 date 字段的条目结构")
            print(json.dumps(item, ensure_ascii=False, indent=2))

print(f"\n=== 统计 ===")
print(f"有 date 字段：{with_date} 条")
print(f"无 date 字段：{without_date} 条")

# 按日期统计
date_counts = {}
for d in date_fields:
    date_counts[d] = date_counts.get(d, 0) + 1

print(f"\n=== 日期分布（前10）===")
for d in sorted(date_counts.keys(), reverse=True)[:10]:
    print(f"{d}: {date_counts[d]} 条")

# 检查 7.29 的数据
july29 = [item for item in data if item.get('date') == '2026-07-29']
print(f"\n=== 2026-07-29 数据 ({len(july29)} 条) ===")
for item in july29[:3]:
    print(f"- {item.get('title', 'N/A')[:60]}")
