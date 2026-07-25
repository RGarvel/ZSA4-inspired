#!/usr/bin/env python3
"""Update models.json with latest price data from web research."""
import json
from datetime import date

DATA_PATH = r"C:\Users\阮家威\AppData\Local\hermes\data\inspiration\project\ai-model-price-dashboard\data\models.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

models = {m["model_id"]: dict(m) for m in data["models"]}
updates = []
new_models_added = []

# ─── 1. OpenAI GPT-5.6 Sol: $5/$30 per 1M ───
if "gpt-5.6-sol" in models:
    old_i, old_o = models["gpt-5.6-sol"]["input_price_per_1m"], models["gpt-5.6-sol"]["output_price_per_1m"]
    models["gpt-5.6-sol"]["input_price_per_1m"] = 5.0
    if old_i != 5.0:
        updates.append((old_i, 30.0, 5.0, 30.0, "gpt-5.6-sol"))

# ─── 2. OpenAI GPT-5.6 Terra: $2.50/$15 per 1M ───
if "gpt-5.6-terra" in models:
    old_i, old_o = models["gpt-5.6-terra"]["input_price_per_1m"], models["gpt-5.6-terra"]["output_price_per_1m"]
    models["gpt-5.6-terra"]["input_price_per_1m"] = 2.5
    if old_i != 2.5:
        updates.append((old_i, old_o, 2.5, 15.0, "gpt-5.6-terra"))

# ─── 3. OpenAI GPT-5.6 Luna: $1/$6 per 1M ───
if "gpt-5.6-luna" in models:
    old_i, old_o = models["gpt-5.6-luna"]["input_price_per_1m"], models["gpt-5.6-luna"]["output_price_per_1m"]
    models["gpt-5.6-luna"]["input_price_per_1m"] = 1.0
    models["gpt-5.6-luna"]["output_price_per_1m"] = 6.0
    if old_i != 1.0 or old_o != 6.0:
        updates.append((old_i, old_o, 1.0, 6.0, "gpt-5.6-luna"))

# ─── 4. Claude Opus 5: $5/$25 (NEW, replaces Opus 4.8 at same price) ───
if "claude-opus-5" not in models:
    new = {
        "model_id": "claude-opus-5",
        "name": "Claude Opus 5",
        "vendor": "Anthropic",
        "open_source": False,
        "tier": "premium",
        "categories": ["chat", "reasoning", "coding", "image"],
        "context_window": 1000000,
        "input_price_per_1m": 5.0,
        "output_price_per_1m": 25.0,
        "image_generation_price": "/",
        "image_edit_price": "/",
        "benchmark_swe_verified": None,
        "benchmark_reasoning": None,
        "benchmark_knowledge": None,
        "benchmark_chat": None,
        "composite_score": None,
        "score_coding": None,
        "score_reasoning": None,
        "score_image": None,
        "score_chat": None
    }
    models["claude-opus-5"] = new
    new_models_added.append("claude-opus-5")

# ─── 5. Remove claude-opus-4.8 (superseded by opus-5) ───
if "claude-opus-4.8" in models:
    del models["claude-opus-4.8"]

# ─── 6. Grok 4.5: $2/$6 per 1M ───
if "grok-4.5" in models:
    old_i, old_o = models["grok-4.5"]["input_price_per_1m"], models["grok-4.5"]["output_price_per_1m"]
    models["grok-4.5"]["input_price_per_1m"] = 2.0
    models["grok-4.5"]["output_price_per_1m"] = 6.0
    if old_i != 2.0 or old_o != 6.0:
        updates.append((old_i, old_o, 2.0, 6.0, "grok-4.5"))

# ─── 7. Grok 4.3: $1.25/$2.50 (NEW) ───
if "grok-4.3" not in models:
    new = {
        "model_id": "grok-4.3",
        "name": "Grok 4.3",
        "vendor": "xAI",
        "open_source": False,
        "tier": "budget",
        "categories": ["chat", "reasoning", "coding"],
        "context_window": 131072,
        "input_price_per_1m": 1.25,
        "output_price_per_1m": 2.50,
        "image_generation_price": "/",
        "image_edit_price": "/",
        "benchmark_swe_verified": None,
        "benchmark_reasoning": None,
        "benchmark_knowledge": None,
        "benchmark_chat": None,
        "composite_score": None,
        "score_coding": None,
        "score_reasoning": None,
        "score_image": None,
        "score_chat": None
    }
    models["grok-4.3"] = new
    new_models_added.append("grok-4.3")

# ─── 8. Kimi K3: $3/$15 per 1M (OpenRouter listing) ───
if "kimi-k3" in models:
    old_i, old_o = models["kimi-k3"]["input_price_per_1m"], models["kimi-k3"]["output_price_per_1m"]
    models["kimi-k3"]["input_price_per_1m"] = 3.0
    models["kimi-k3"]["output_price_per_1m"] = 15.0
    if old_i != 3.0 or old_o != 15.0:
        updates.append((old_i, old_o, 3.0, 15.0, "kimi-k3"))

# ─── 9. Gemini 3.5 Flash: $1.50/$9 per 1M ───
if "gemini-3.5-flash" in models:
    old_i, old_o = models["gemini-3.5-flash"]["input_price_per_1m"], models["gemini-3.5-flash"]["output_price_per_1m"]
    models["gemini-3.5-flash"]["input_price_per_1m"] = 1.5
    models["gemini-3.5-flash"]["output_price_per_1m"] = 9.0
    if old_i != 1.5 or old_o != 9.0:
        updates.append((old_i, old_o, 1.5, 9.0, "gemini-3.5-flash"))

# ─── 10. Step 3.5 Flash: rename step-edge → step-3.5-flash, $0.10/$0.30 ───
if "step-edge" in models:
    old_entry = models.pop("step-edge")
    old_id = "step-edge"
    old_i, old_o = old_entry["input_price_per_1m"], old_entry["output_price_per_1m"]
    old_entry["model_id"] = "step-3.5-flash"
    old_entry["name"] = "Step 3.5 Flash"
    old_entry["input_price_per_1m"] = 0.10
    old_entry["output_price_per_1m"] = 0.30
    old_entry["context_window"] = 262144
    updates.append((old_i, old_o, 0.10, 0.30, old_id))
    models["step-3.5-flash"] = old_entry

# Rebuild list
data["models"] = list(models.values())
data["updated_at"] = str(date.today())

# Enforce 50-model cap: keep ones with benchmarks first, then alphabetically by model_id
with_bench = [m for m in data["models"] if any(m.get(k) is not None for k in ["benchmark_swe_verified", "benchmark_reasoning", "benchmark_knowledge", "benchmark_chat"])]
without_bench = sorted([m for m in data["models"] if all(m.get(k) is None for k in ["benchmark_swe_verified", "benchmark_reasoning", "benchmark_knowledge", "benchmark_chat"])], key=lambda x: x["model_id"])
keep = with_bench + without_bench[:max(0, 50 - len(with_bench))]
data["models"] = keep

# Write back
with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# ─── Report ───
print(f"Total models after update: {len(data['models'])}")
print(f"\n=== Price Updates ===")
for old_i, old_o, new_i, new_o, mid in updates:
    print(f"  {mid}: input ${old_i}→${new_i}, output ${old_o}→${new_o}")

print(f"\n=== New Models Added ===")
for nm in new_models_added:
    m = models[nm]
    print(f"  {nm}: {m['name']} (${m['input_price_per_1m']}/${m['output_price_per_1m']} per 1M)")

print("\nDone.")
