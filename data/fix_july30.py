import json
from pathlib import Path

# 读取 all_inspiration.json
all_data_file = Path(r'C:\Users\阮家威\AppData\Local\hermes\data\inspiration\data\all_inspiration.json')
with open(all_data_file, 'r', encoding='utf-8') as f:
    all_data = json.load(f)

# 筛选 2026-07-30 的数据
july_30_data = [item for item in all_data if item.get('date') == '2026-07-30']
print(f"找到 {len(july_30_data)} 条 7.30 的数据")

# 读取 inspiration_2026-07-30.json
inspiration_file = Path(r'C:\Users\阮家威\AppData\Local\hermes\data\inspiration\data\inspiration_2026-07-30.json')
with open(inspiration_file, 'r', encoding='utf-8') as f:
    inspiration_data = json.load(f)

# 更新 records 字段
inspiration_data['records'] = july_30_data

# 写回文件
with open(inspiration_file, 'w', encoding='utf-8') as f:
    json.dump(inspiration_data, f, ensure_ascii=False, indent=2)

print("✓ 已更新 inspiration_2026-07-30.json")
