import json

# 读取 all_inspiration.json
with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 读取灵感文件获取完整信息
with open('inspiration_2026-07-29.json', 'r', encoding='utf-8') as f:
    inspiration = json.load(f)

# 更新 all_inspiration.json 中的 7.29 记录
updated_count = 0
for record in data:
    if record.get('date') == '2026-07-29':
        # 查找对应的灵感记录
        for insp in inspiration['records']:
            if record.get('title') == insp.get('title') or \
               (record.get('id') and record.get('id') == insp.get('id')):
                # 更新 keywords
                if 'keywords' not in record and 'keywords' in insp:
                    record['keywords'] = insp['keywords']
                    updated_count += 1
                break

# 保存
with open('all_inspiration.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✓ 更新了 {updated_count} 条 7.29 记录的 keywords 字段")
