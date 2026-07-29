"""
AI Model Price Dashboard - Value Score Calculation Fix

问题分析：
1. 当前公式: value = (quality - 30) / price
   - 当quality < 30时得分为0，过于严苛
   - 价格敏感度过高，$1和$2的模型差距过大
   - 没有考虑free tier模型

2. 改进方案：
   - 使用log缩放平衡价格差异
   - 降低质量阈值到20
   - 引入quality^1.2权重，让高质量模型获得更大优势
   - 归一化到0-100范围
"""

import json
import math

DATA_PATH = r"C:\Users\阮家威\AppData\Local\hermes\data\inspiration\project\ai-model-price-dashboard\data\models.json"

def calc_value_score_improved(model, task_type='chat'):
    """
    改进的性价比计算公式
    
    公式: value_score = 100 * log(1 + quality_factor) / log(1 + price_factor)
    
    其中:
    - quality_factor = quality^1.2 / 100 (高质量模型获得更大权重)
    - price_factor = price / min_price (相对价格)
    """
    ip = float(model.get('input_price_per_1m', 0) or 0)
    op = float(model.get('output_price_per_1m', 0) or 0)
    
    # 根据任务类型选择质量和价格
    if task_type == 'image':
        quality = float(model.get('score_image', 0) or 0)
        pg = model.get('image_generation_price')
        price = float(pg) if pg and pg != '/' and float(pg) > 0 else 0
        if price == 0:
            return None
    elif task_type == 'coding':
        quality = float(model.get('score_coding', 0) or model.get('composite_score', 0) or 0)
        price = op if op > 0 else (ip if ip > 0 else 0)
    elif task_type == 'reasoning':
        quality = float(model.get('score_reasoning', 0) or model.get('composite_score', 0) or 0)
        price = op if op > 0 else (ip if ip > 0 else 0)
    else:  # chat
        quality = float(model.get('score_chat', 0) or model.get('composite_score', 0) or 0)
        price = op if op > 0 else (ip if ip > 0 else 0)
    
    # 免费模型：性价比为0
    if price <= 0:
        return 0
    
    # 改进的公式
    # 1. 质量权重：quality^1.2，让高质量模型获得更大优势
    quality_weighted = (quality / 100) ** 1.2
    
    # 2. 价格因子：log缩放，减少价格敏感度
    # 假设最低价格$0.1作为基准
    min_price = 0.1
    price_factor = price / min_price
    price_penalty = math.log(1 + price_factor) / math.log(1 + 10)  # log(11)/log(11) = 1 when price=$1
    
    # 3. 最终得分：质量优势 vs 价格劣势
    # 归一化到0-100
    raw_score = (quality_weighted / price_penalty) * 100
    
    # 4. 限制范围
    return min(100, max(0, raw_score))


def update_models_json():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    models = data['models']
    
    print("=" * 80)
    print("重新计算性价比评分（归一化0-100，最高=100，免费=0）")
    print("=" * 80)
    
    # Step 1: 计算原始分数
    raw_scores = {}  # {model_id: {task: raw_score}}
    for model in models:
        mid = model['model_id']
        raw_scores[mid] = {}
        for task in ['chat', 'coding', 'reasoning', 'image']:
            raw = calc_value_score_improved(model, task)
            raw_scores[mid][task] = raw
    
    # Step 2: 每个任务类型找最大值
    task_max = {}
    for task in ['chat', 'coding', 'reasoning', 'image']:
        vals = [raw_scores[mid][task] for mid in raw_scores if raw_scores[mid][task] is not None and raw_scores[mid][task] > 0]
        task_max[task] = max(vals) if vals else 1
        print(f"  {task} 最大值: {task_max[task]:.1f}")
    
    # Step 3: Softmax压缩，减少差距
    # 先收集所有正数原始分数
    task_scores = {}
    for task in ['chat', 'coding', 'reasoning', 'image']:
        task_scores[task] = [(mid, raw_scores[mid][task]) for mid in raw_scores
                             if raw_scores[mid][task] is not None and raw_scores[mid][task] > 0]
    
    # 对每个任务类型应用softmax压缩
    # softmax_i = exp(score_i / T) / sum(exp(score_j / T)) * 100
    # 温度T越高，分数越压缩；T越低，分数差距越大
    T = 50.0  # 提高温度参数，减少分数差距
    
    for model in models:
        mid = model['model_id']
        for task in ['chat', 'coding', 'reasoning', 'image']:
            raw = raw_scores[mid][task]
            if raw is None or raw <= 0:
                score = 0
            else:
                # 计算softmax
                scores_list = [s for _, s in task_scores[task]]
                exp_sum = sum(math.exp(s / T) for s in scores_list)
                softmax_val = math.exp(raw / T) / exp_sum
                # 归一化：最大softmax值映射到100
                max_softmax = max(math.exp(s / T) for s in scores_list) / exp_sum
                score = round((softmax_val / max_softmax) * 100, 1)
            model[f'value_score_{task}'] = score
        
        # value_score = chat 类型得分（默认）
        model['value_score'] = model['value_score_chat']
    
    # 保存
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 输出结果
    print(f"\n{'模型名称':<25} {'质量':>5} {'价格':>7} {'性价比':>7} {'免费':>5}")
    print("-" * 80)
    
    sorted_models = sorted(models, key=lambda m: m.get('value_score', 0) or 0, reverse=True)
    for m in sorted_models[:20]:
        name = m['name'][:23]
        quality = m.get('composite_score', 0)
        price = m.get('output_price_per_1m', 0)
        value = m.get('value_score', 0)
        is_free = "✓" if (price <= 0) else ""
        print(f"{name:<25} {quality:>5} ${price:>6.2f} {value:>7.1f} {is_free:>5}")
    
    print("\n" + "=" * 80)
    print(f"已更新 {len(models)} 个模型的性价比评分")
    print("=" * 80)


if __name__ == '__main__':
    update_models_json()
