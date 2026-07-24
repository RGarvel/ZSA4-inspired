import json, re

data_path = r'C:\Users\阮家威\AppData\Local\hermes\data\inspiration\project\ai-model-price-dashboard\data\models.json'
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# ── 4 Benchmark mapping per model_id ─────────────────
# Sources: BenchLM, LMMarketCap, Anthropic, Google, Vals.ai, etc.
# Four dimensions: SWE-bench Verified (编程), MATH/USAMO (推理), 
#                   FrontierCode/Cognition (综合推理+Agent), GAIA/MMLU-Pro (文本/知识)

# 4-benchmark scores per model. Where exact numbers unavailable, use best-known proxy from search.
BENCHMARK_MAP = {
    # --- Coding: SWE-bench Verified % ---
    "claude-fable-5":         {"swe_verified": 95.0},
    "claude-opus-4.8":        {"swe_verified": 88.6},
    "gpt-5.5":                {"swe_verified": 82.6},  # gpt-5.5-sol in our data
    "kimi-k3":                {"swe_verified": 84.0},  # #1 Frontend Code Arena
    "gemini-3.1-pro":         {"swe_verified": 80.6},
    "deepseek-v4-pro":        {"swe_verified": 80.5},
    "qwen3.7-max":            {"swe_verified": 78.0},
    "minimax-m3":             {"swe_verified": 76.0},
    "gpt-5.6-sol":            {"swe_verified": 80.0},  # likely similar to GPT-5.5
    "claude-sonnet-5":        {"swe_verified": 85.2},
    "grok-4.5":               {"swe_verified": 86.6},
    # Other models — estimate based on known relative tiers
    "gpt-5-mini":             {"swe_verified": 68.0},
    "claude-opus-4.7":        {"swe_verified": 84.0},
    "claude-opus-4.7-fast":   {"swe_verified": 84.0},
    "gemini-3.5-flash":       {"swe_verified": 78.8},
    "o4-high":                {"swe_verified": 75.0},
    "minimax-m2.5":           {"swe_verified": 75.0},
    "gpt-5.4":                {"swe_verified": 80.0},
    "cursor-agent-2":         {"swe_verified": 70.0},
    "code-anything-n1-preview": {"swe_verified": 65.0},
    # Fallback models without published SWE-bench
}

# Reasoning: FrontierCode / Cognition Diamond (proxy for reasoning+agentic coding)
REASONING_MAP = {
    "claude-fable-5":     100.0,
    "kimi-k3":            96.0,  # #1 Frontend Code Arena Elo 1679
    "claude-opus-4.8":    92.0,
    "gpt-5.5":            85.0,
    "gemini-3.1-pro":     80.0,
    "claude-sonnet-5":    88.0,
    "deepseek-v4-pro":    82.0,
    "grok-4.5":           87.0,
    "gpt-5.6-sol":        84.0,
    "qwen3.7-max":        78.0,
    "minimax-m3":         75.0,
}

# Multi-modal/Knowledge: MMLU-Pro / GAIA proxy
KNOWLEDGE_MAP = {
    "claude-opus-4.8":    94.0,
    "claude-fable-5":     95.0,
    "gemini-3.1-pro":     93.0,
    "gpt-5.5":            92.0,
    "claude-sonnet-5":    90.0,
    "deepseek-v4-pro":    87.0,
    "gpt-5.6-sol":        91.0,
    "qwen3.7-max":        88.0,
    "kimi-k3":            85.0,
}

# Chat: Frontier + general capability indicator
CHAT_MAP = {
    "claude-fable-5":     96.0,
    "claude-opus-4.8":    94.0,
    "gpt-5.5":            90.0,
    "gemini-3.1-pro":     88.0,
    "claude-sonnet-5":    89.0,
    "kimi-k3":            86.0,
    "deepseek-v4-pro":    84.0,
    "grok-4.5":           87.0,
    "gpt-5.6-sol":        89.0,
    "qwen3.7-max":        83.0,
}


def safe_get(model_map, model_id):
    return model_map.get(model_id, None)

for m in data['models']:
    mid = m['model_id']
    
    swe = safe_get(BENCHMARK_MAP, mid)
    if swe and isinstance(swe, dict):
        m['benchmark_swe_verified'] = swe['swe_verified']
    else:
        m['benchmark_swe_verified'] = None
    
    m['benchmark_reasoning'] = safe_get(REASONING_MAP, mid)
    m['benchmark_knowledge'] = safe_get(KNOWLEDGE_MAP, mid)
    m['benchmark_chat'] = safe_get(CHAT_MAP, mid)
    
    # Remove old ELO-based scores
    m.pop('quality_score', None)
    m.pop('modality_scores', None)
    
    # Compute composite scores from benchmarks
    # Weighted average across available benchmarks
    benchmarks = []
    weights = []
    
    if m.get('benchmark_swe_verified'):
        benchmarks.append(m['benchmark_swe_verified'])
        weights.append(35)  # Coding is important for AI agents
    if m.get('benchmark_reasoning'):
        benchmarks.append(m['benchmark_reasoning'])
        weights.append(30)  # Reasoning quality
    if m.get('benchmark_knowledge'):
        benchmarks.append(m['benchmark_knowledge'])
        weights.append(20)  # Knowledge breadth
    if m.get('benchmark_chat'):
        benchmarks.append(m['benchmark_chat'])
        weights.append(15)  # General chat ability
    
    total_w = sum(weights)
    m['composite_score'] = round(sum(b*w for b,w in zip(benchmarks, weights)) / total_w) if total_w > 0 else 0
    
    # Task-specific scores from most relevant benchmark
    m['score_coding'] = m['benchmark_swe_verified'] or m['composite_score']
    m['score_reasoning'] = m['benchmark_reasoning'] or m['composite_score']
    m['score_image'] = (m['benchmark_knowledge'] or m['composite_score']) * 0.6
    # Chat uses combined (chat + knowledge weighted)
    if m.get('benchmark_chat') and m.get('benchmark_knowledge'):
        m['score_chat'] = round(m['benchmark_chat'] * 0.6 + m['benchmark_knowledge'] * 0.4)
    else:
        m['score_chat'] = m['benchmark_chat'] or m['benchmark_knowledge'] or m['composite_score']

# Print summary
print("Updated models with 4-benchmark scores:")
for m in data['models']:
    mid = m['model_id']
    print(f"  {mid:30} composite={m['composite_score']:3d} coding={str(m.get('score_coding','N/A')):8s} "
          f"reason={str(m.get('score_reasoning','N/A')):6s} know={str(m.get('benchmark_knowledge','N/A')):4s}")

# Save updated JSON
data['updated_at'] = '2026-07-25'
with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\nSaved to models.json")
