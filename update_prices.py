#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update AI model prices and calculate value scores - July 29 2026"""

import json
import math
from datetime import datetime
from pathlib import Path

# Load existing models
models_file = Path('C:/Users/阮家威/AppData/Local/hermes/data/inspiration/project/ai-model-price-dashboard/data/models.json')
with open(models_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Price updates from July 2026 search results
price_updates = {
    # Claude Opus 5 - NEW (July 24, 2026, $5/$25 per ofox.ai)
    "claude-opus-5": {"input": 5.0, "output": 25.0},
    
    # Gemini updates (from contacto.com May 2026 pricing guide)
    "gemini-3.5-flash": {"input": 1.50, "output": 9.00},
    "gemini-3.1-pro": {"input": 2.0, "output": 18.0},
    
    # Gemini 2.5 Flash Lite per contacto.com
    "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40},
    
    # Qwen updates per benchlm.ai (July 2026)
    "qwen-3.5-plus": {"input": 0.40, "output": 2.40},
    "qwen-3.5-flash": {"input": 0.10, "output": 0.40},
}

def calc_value_score(model, task_type):
    """
    Calculate value score for a given task type.
    Higher score = better value (performance per dollar).
    """
    composite = model.get('composite_score', 50)
    input_price = model.get('input_price_per_1m', 0)
    output_price = model.get('output_price_per_1m', 0)
    
    # Skip if no prices or zero prices (free models)
    if input_price <= 0 or output_price <= 0:
        return 100.0
    
    # Average cost per 1M tokens
    avg_cost = (input_price + output_price) / 2
    
    # Task type weights
    task_weights = {
        'chat': {'composite': 1.0, 'cost': 1.2},
        'coding': {'composite': 1.3, 'cost': 1.0},
        'reasoning': {'composite': 1.5, 'cost': 0.9},
        'image': {'composite': 0.8, 'cost': 1.1},
    }
    
    w = task_weights.get(task_type, task_weights['chat'])
    
    # Value = composite^w.composite / cost^w.cost
    value_raw = (composite ** w['composite']) / (avg_cost ** w['cost'])
    
    # Normalize to 0-100 using log scale
    value_score = min(100, max(0, 20 * math.log10(value_raw + 1)))
    
    return round(value_score, 2)

# Track changes
changes = []
today = datetime.now().strftime('%Y-%m-%d')

for model in data['models']:
    model_id = model.get('model_id', '')
    
    # Update prices if we have new data
    if model_id in price_updates:
        updates = price_updates[model_id]
        old_input = model.get('input_price_per_1m')
        old_output = model.get('output_price_per_1m')
        
        if 'input' in updates and model.get('input_price_per_1m') != updates['input']:
            changes.append(f"{model['name']}: input ${old_input} -> ${updates['input']}")
            model['input_price_per_1m'] = updates['input']
        if 'output' in updates and model.get('output_price_per_1m') != updates['output']:
            changes.append(f"{model['name']}: output ${old_output} -> ${updates['output']}")
            model['output_price_per_1m'] = updates['output']
    
    # Recalculate value scores for all task types
    for task_type in ['chat', 'coding', 'reasoning', 'image']:
        model[f'value_score_{task_type}'] = calc_value_score(model, task_type)
    
    model['updated_at'] = today

# Save
with open(models_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Total models: {len(data['models'])}")
print(f"Changes: {len(changes)}")
for c in changes:
    print(f"  {c}")

# Print top 10 by value_score_chat
print("\n=== Top 10 by Chat Value Score ===")
scored = [m for m in data['models'] if m.get('composite_score', 0) > 0]
sorted_models = sorted(scored, key=lambda m: m.get('value_score_chat', 0), reverse=True)
for i, m in enumerate(sorted_models[:10], 1):
    print(f"{i}. {m['name']} | composite={m.get('composite_score')} | ${m.get('input_price_per_1m')}/${m.get('output_price_per_1m')} | value_chat={m.get('value_score_chat')}")
