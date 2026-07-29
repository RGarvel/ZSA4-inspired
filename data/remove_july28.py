import json

# 读取 all_inspiration.json
with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 统计7.28的数据
july28 = [item for item in data if item.get('date') == '2026-07-28']
print("=== 7.28 数据 ===")
for item in july28:
    print(json.dumps(item, ensure_ascii=False, indent=2))

# 删除7.28的数据
original_count = len(data)
data = [item for item in data if item.get('date') != '2026-07-28']
new_count = len(data)

print(f"\n删除前：{original_count} 条")
print(f"删除后：{new_count} 条")
print(f"删除了：{original_count - new_count} 条")

# 保存
with open('all_inspiration.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✓ 已删除7.28数据并保存")
