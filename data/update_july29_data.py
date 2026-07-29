import json

# 读取 all_inspiration.json
with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 读取灵感文件获取完整信息
with open('inspiration_2026-07-29.json', 'r', encoding='utf-8') as f:
    inspiration = json.load(f)

# 找出 7.29 的旧格式记录（缺少 url/keywords 等字段）
july29_records = [r for r in data if r.get('date') == '2026-07-29']
print(f"找到 {len(july29_records)} 条 7.29 记录")
print("\n旧格式记录（缺少 url）：")
for r in july29_records:
    if not r.get('url'):
        print(f"  - {r.get('title', 'N/A')}")

# 更新这些记录
updated_count = 0
for record in data:
    if record.get('date') == '2026-07-29' and not record.get('url'):
        # 查找对应的灵感记录
        for insp in inspiration['records']:
            if record.get('title') == insp.get('title'):
                # 更新字段
                if insp.get('url'):
                    record['url'] = insp['url']
                if insp.get('source'):
                    record['source'] = insp['source']
                if insp.get('keywords'):
                    record['keywords'] = insp['keywords']
                if insp.get('id'):
                    record['id'] = insp['id']
                updated_count += 1
                print(f"✓ 更新: {record.get('title')[:50]}")
                break

# 保存
with open('all_inspiration.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✓ 共更新 {updated_count} 条记录")
