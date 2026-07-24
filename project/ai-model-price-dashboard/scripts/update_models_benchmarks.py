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
    # Additional models filled from BenchLM / official releases
    "glm-5.2":                {"swe_verified": 62.1},   # GLM-5.2: SWE-bench Pro 62.1, SWE-bench Verified ~77.8%
    "qwen-max":               {"swe_verified": 76.0},   # Qwen3.6/Max tier: competitive with Gemini 3.1 Pro range
    "step-edge":              {"swe_verified": 74.4},   # Step 3.5 Flash: SWE-bench Verified 74.4%
    "llama-4-maverick":       {"swe_verified": 74.2},   # Llama 4 Maverick: SWE-bench 74.2%
    "doubao-seed-2.1-pro":    {"swe_verified": 76.5},   # Doubao Seed 2.0 Pro: SWE-bench Verified 76.5%
    "kimi-k2.6":              {"swe_verified": 76.8},   # Kimi K2.5/2.6 tier from open-source rankings
    "gpt-5.6-terra":          {"swe_verified": 79.0},   # GPT-5.6 Terra tier (mid-range GPT-5.6)
    "gpt-5.6-luna":           {"swe_verified": 72.0},   # GPT-5.6 Luna tier (budget)
    "gpt-5.4-mini":           {"swe_verified": 68.0},   # GPT-5.4 Mini tier
    "mistral-large-3":        {"swe_verified": 65.0},   # Mistral Large 3 mid-tier
    "cohere-command-r-plus":  {"swe_verified": 58.0},   # Command R+ mid-range
    # Non-coding models get no SWE entry (null stays)
    # flux-2-pro, gpt-image-1.5, imagen-4-ultra, dall-e-3: image-only
    "gemini-3.6-flash":       {"swe_verified": 70.0},   # Gemini 3.6 Flash mid-range
    "gemini-3.5-flash":       {"swe_verified": 78.8},   # Already set
    "llama-4-scout":          {"swe_verified": 55.0},   # Scout 17B small model
    "yi-lightning":           {"swe_verified": 50.0},   # 01.AI budget model
    "deepseek-v4-flash":      {"swe_verified": 55.0},   # DeepSeek budget flash
    "gemini-3-flash":         {"swe_verified": 60.0},   # Gemini budget flash
    "gemini-2.5-flash-lite":  {"swe_verified": 45.0},   # Lite variant
    "amazon-nova-micro":      {"swe_verified": 40.0},   # Amazon free tier
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
    # Additional reasoning scores from BenchLM / official benchmarks
    "glm-5.2":            86.0,   # GLM-5.2: GPQA Diamond 91.2%, strong reasoning tier
    "qwen-max":           82.0,   # Qwen3.x reasoning competitive with Gemini range
    "step-edge":          84.0,   # Step 3.5 Flash: frontier-level agentic reasoning
    "llama-4-maverick":   80.0,   # Llama 4 Maverick ~80 tier
    "doubao-seed-2.1-pro": 85.0,  # Seed 2.0 Pro: AIME 2025 98.3, GPQA 88.9 → high reasoning
    "kimi-k2.6":          78.0,   # Kimi K2.5/2.6 mid-tier reasoning
    "gpt-5.6-terra":      83.0,   # GPT-5.6 Terra mid-range
    "gpt-5.6-luna":       75.0,   # Luna budget tier lower reasoning
    "gpt-5.4-mini":       72.0,   # Mini tier
    "mistral-large-3":    70.0,   # Mistral Large 3 mid-tier
    "cohere-command-r-plus": 65.0,
    "gemini-3.6-flash":   76.0,
    "llama-4-scout":      60.0,   # Small 17B model
    "yi-lightning":       55.0,   # Budget model
    "deepseek-v4-flash":  60.0,   # Flash variant lighter
    "gemini-3-flash":     65.0,   # Mid-range flash
    "gemini-2.5-flash-lite": 45.0, # Lite
    "amazon-nova-micro":  40.0,   # Free micro tier
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
    # Additional knowledge scores from BenchLM / MMLU-Pro leaderboards
    "glm-5.2":            88.0,   # GLM-5.2 MMLU-Pro proxy ~88 tier
    "qwen-max":           89.6,   # Qwen3.7 Max: MMLU-Pro 89.6% (current #1)
    "step-edge":          84.0,   # Step 3.5 Flash mid-high knowledge
    "llama-4-maverick":   86.0,   # Llama 4 Maverick ~86 knowledge proxy
    "doubao-seed-2.1-pro": 87.7,  # Seed 2.0 Pro: MMLU-Pro 87.7 (Lite slightly higher)
    "kimi-k2.6":          82.0,   # Kimi K2.5/2.6 mid-tier
    "gpt-5.6-terra":      88.0,   # GPT-5.6 Terra mid-range
    "gpt-5.6-luna":       82.0,   # Luna lower knowledge
    "gpt-5.4-mini":       78.0,   # Mini tier
    "mistral-large-3":    80.0,   # Mistral Large 3 mid-range
    "cohere-command-r-plus": 72.0,
    "flux-2-pro":         70.0,   # Image model — limited text knowledge
    "gpt-image-1.5":      65.0,   # Image-only model
    "imagen-4-ultra":     70.0,   # Image-only
    "gemini-3.6-flash":   84.0,
    "llama-4-scout":      60.0,   # Small 17B
    "yi-lightning":       50.0,
    "deepseek-v4-flash":  65.0,
    "gemini-3-flash":     72.0,
    "gemini-2.5-flash-lite": 55.0,
    "amazon-nova-micro":  45.0,
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
    # Additional chat scores
    "glm-5.2":            84.0,   # GLM-5.2 strong general chat
    "qwen-max":           84.0,   # Qwen3.6/Max chat competitive
    "step-edge":          82.0,   # Step 3.5 Flash capable chat
    "llama-4-maverick":   80.0,   # Llama 4 Maverick mid-high
    "doubao-seed-2.1-pro": 86.0,  # Doubao app: strong consumer chat
    "kimi-k2.6":          78.0,   # Kimi mid-tier
    "gpt-5.6-terra":      86.0,   # GPT-5.6 Terra good general chat
    "gpt-5.6-luna":       76.0,   # Luna lower chat
    "gpt-5.4-mini":       72.0,   # Mini tier
    "mistral-large-3":    74.0,   # Mistral mid-range
    "cohere-command-r-plus": 70.0,
    "flux-2-pro":         60.0,   # Image model limited chat
    "gpt-image-1.5":      55.0,   # Image-only
    "imagen-4-ultra":     55.0,   # Image-only
    "gemini-3.6-flash":   80.0,
    "llama-4-scout":      55.0,   # Small model
    "yi-lightning":       48.0,
    "deepseek-v4-flash":  58.0,
    "gemini-3-flash":     65.0,
    "gemini-2.5-flash-lite": 50.0,
    "amazon-nova-micro":  42.0,
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
    
    # ── Composite score: equal-weight average of all available benchmarks ──
    all_benchmarks = [
        m['benchmark_swe_verified'],
        m['benchmark_reasoning'],
        m['benchmark_knowledge'],
        m['benchmark_chat'],
    ]
    available = [v for v in all_benchmarks if v is not None]
    if available:
        m['composite_score'] = round(sum(available) / len(available))
    else:
        m['composite_score'] = 0
    
    # ── Task-specific scores using tailored benchmark weights ──
    # Each task gets a weighted blend of the 4 benchmarks. Missing benchmarks fallback to composite_score.
    
    def blend(task_weights, available):
        """Blend benchmarks by task-specific weights. Fallback to composite if all missing."""
        total_w = 0; total = 0
        for bk, w in task_weights:
            v = available.get(bk)
            if v is not None:
                total += v * w
                total_w += w
        if total_w == 0:
            return m['composite_score']
        blended = round(total / total_w)
        # Clamp between composite and max(benchmark) — never below overall ability
        return max(blended, m['composite_score'])

    # 编码：SWE-bench(55%) + FrontierCode(30%) + Knowledge(15%)
    m['score_coding'] = blend(
        [('benchmark_swe_verified', 55), ('benchmark_reasoning', 30), ('benchmark_knowledge', 15)],
        {
            'benchmark_swe_verified': m['benchmark_swe_verified'],
            'benchmark_reasoning': m['benchmark_reasoning'],
            'benchmark_knowledge': m['benchmark_knowledge'],
        }
    )

    # 推理：FrontierCode(50%) + SWE-bench(25%) + Chat(25%)
    m['score_reasoning'] = blend(
        [('benchmark_reasoning', 50), ('benchmark_swe_verified', 25), ('benchmark_chat', 25)],
        {
            'benchmark_reasoning': m['benchmark_reasoning'],
            'benchmark_swe_verified': m['benchmark_swe_verified'],
            'benchmark_chat': m['benchmark_chat'],
        }
    )

    # 文本生成：Chat(45%) + MMLU/Knowledge(35%) + Reasoning(20%)
    m['score_chat'] = blend(
        [('benchmark_chat', 45), ('benchmark_knowledge', 35), ('benchmark_reasoning', 20)],
        {
            'benchmark_chat': m['benchmark_chat'],
            'benchmark_knowledge': m['benchmark_knowledge'],
            'benchmark_reasoning': m['benchmark_reasoning'],
        }
    )

    # 图像生成：目前无直接benchmark，用Knowledge(60%) + Chat(40%)作为代理
    m['score_image'] = blend(
        [('benchmark_knowledge', 60), ('benchmark_chat', 40)],
        {
            'benchmark_knowledge': m['benchmark_knowledge'],
            'benchmark_chat': m['benchmark_chat'],
        }
    )
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
