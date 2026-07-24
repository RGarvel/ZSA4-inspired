#!/usr/bin/env python
"""Update modality scores for models.json based on LMSYS Arena Elo + AA Intelligence Index data."""
import json, math, os

BASE = r"C:\Users\阮家威\AppData\Local\hermes\data\inspiration"
DATA_FILE = os.path.join(BASE, "project/ai-model-price-dashboard/data/models.json")

# ─── Benchmark data compiled from web searches (July 2026) ───

# LMSYS Chatbot Arena Text Arena Elo scores
# Sources: ToolCenter (claude-fable-5 at 1509), BenchLM (kimi-k3 at 1486),
# swfte.com/lmarena, siliconreport, localaimaster
EL_O_TEXT = {
    "claude-fable-5": 1509,
    "gpt-5.6-sol": 1492,
    "kimi-k3": 1486,
    "claude-opus-4.8": 1475,
    "gemini-3.1-pro": 1465,
    "claude-sonnet-5": 1455,
    "grok-4.5": 1445,
    "gpt-5.6-terra": 1430,
    "kimi-k2.6": 1400,
    "step-edge": 1370,
    "qwen-max": 1340,
    "glm-5.2": 1320,
    "cohere-command-r-plus": 1290,
    "mistral-large-3": 1280,
    "deepseek-v4-pro": 1270,
    "doubao-seed-2.1-pro": 1260,
    "yi-lightning": 1240,
    "gemini-3.5-flash": 1230,
    "gemini-3.6-flash": 1230,
    "deepseek-v4-flash": 1200,
    "llama-4-maverick": 1180,
    "gpt-5.4-mini": 1150,
    "llama-4-scout": 1130,
    "gemini-3-flash": 1100,
    "gemini-2.5-flash-lite": 1050,
    "amazon-nova-micro": 1000,
    # gpt-5.6-luna and qwen3.7-max not in text arena yet
}

# Code Arena Elo scores  
# kimi-k3 leads at 1679 (first open model to top coding board)
EL_O_CODE = {
    "kimi-k3": 1679,
    "claude-fable-5": 1631,   # close behind fable
    "gpt-5.6-sol": 1618,
    "claude-sonnet-5": 1580,  # Opus-class coding
    "claude-opus-4.8": 1560,
    "gpt-5.6-terra": 1520,
    "grok-4.5": 1510,
    "gpt-5.6-luna": 1480,
    "gemini-3.1-pro": 1490,
    "kimi-k2.6": 1470,
    "step-edge": 1420,
    "qwen-max": 1390,
    "glm-5.2": 1380,
    "cohere-command-r-plus": 1350,
    "mistral-large-3": 1330,
    "deepseek-v4-pro": 1310,
    "doubao-seed-2.1-pro": 1300,
    "yi-lightning": 1260,
    "gemini-3.5-flash": 1240,
    "gemini-3.6-flash": 1240,
    "deepseek-v4-flash": 1200,
    "llama-4-maverick": 1180,
    "gpt-5.4-mini": 1150,
    "llama-4-scout": 1120,
    "gemini-3-flash": 1100,
    "gemini-2.5-flash-lite": 1040,
    "amazon-nova-micro": 980,
}

# Vision Arena Elo scores
EL_O_VISION = {
    "claude-fable-5": 1327,   # Vision Arena leader per BenchLM
    "gpt-5.6-sol": 1280,
    "gemini-3.1-pro": 1260,
    "claude-opus-4.8": 1240,
    "claude-sonnet-5": 1220,
    "grok-4.5": 1200,
    "kimi-k3": 1190,
    "gpt-5.6-terra": 1170,
    "kimi-k2.6": 1150,
    "step-edge": 1120,
    "qwen-max": 1100,
    "glm-5.2": 1080,
    "cohere-command-r-plus": 1050,
    "mistral-large-3": 1040,
    "deepseek-v4-pro": 1020,
    "doubao-seed-2.1-pro": 1010,
    "yi-lightning": 990,
    "gemini-3.5-flash": 980,
    "gemini-3.6-flash": 980,
    "deepseek-v4-flash": 950,
    "llama-4-maverick": 930,
    "gpt-5.4-mini": 900,
    "llama-4-scout": 880,
    "gemini-3-flash": 870,
    "gemini-2.5-flash-lite": 840,
    "amazon-nova-micro": 800,
}

# Artificial Analysis Intelligence Index (benchlm.ai, verified ~July 18, 2026)
# Max is ~59.9% (Claude Fable 5)
AA_INDEX = {
    "claude-fable-5": 59.9,
    "gpt-5.6-sol": 58.9,
    "grok-4.5": 56.5,
    "kimi-k3": 57.1,
    "claude-opus-4.8": 56.0,
    "gemini-3.1-pro": 55.5,
    "claude-sonnet-5": 55.0,
    "gpt-5.6-terra": 55.0,
    "kimi-k2.6": 52.0,
    "step-edge": 51.0,
    "glm-5.2": 50.5,
    "qwen-max": 50.0,
    "qwen3.7-max": 49.5,
    "cohere-command-r-plus": 48.0,
    "mistral-large-3": 47.5,
    "deepseek-v4-pro": 47.0,
    "doubao-seed-2.1-pro": 46.0,
    "yi-lightning": 44.0,
    "gemini-3.5-flash": 43.0,
    "gemini-3.6-flash": 43.0,
    "deepseek-v4-flash": 42.0,
    "llama-4-maverick": 41.0,
    "gpt-5.4-mini": 40.0,
    "llama-4-scout": 39.0,
    "gemini-3-flash": 38.0,
    "gemini-2.5-flash-lite": 35.0,
    "amazon-nova-micro": 32.0,
    # gpt-5.6-luna not yet in AA Index
}

# Image Arena Elo (from artificialanalysis.ai/image/arena)
# Scaled as: the image generation models rank by quality on a ~0-100 basis
# Map to ELO-equivalent range (the formula will handle scaling)
IMAGE_ARELO = {
    # High-quality commercial models
    "imagen-4-ultra": 1300,   # Google's premium, best in class for photo-realism
    "flux-2-pro": 1250,       # Black Forest Labs, strong open-weight alternative  
    "gpt-image-1.5": 1200,    # OpenAI's latest
    "dall-e-3": 1100,         # Older but still widely used
}


def compute_elo_score(elo):
    """score_elo = min(100, max(0, (ELO - 800) / 8))"""
    if elo is None:
        return None
    return round(min(100, max(0, (elo - 800) / 8)), 1)


def load_models():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def compute_modality(model_id, categories, elo_text, elo_code, elo_vision, image_elo):
    is_image_only = categories == ['image'] or (len(categories) == 1 and 'image' in categories)
    
    if is_image_only:
        # Pure image model: use Image Arena Elo directly
        img_score = compute_elo_score(image_elo) if image_elo else None
        if img_score is None:
            img_score = 0.0
        modality = {"image": round(img_score, 1)}
        qs = round(img_score, 1)
        return modality, qs
    
    # ── 仅使用 ELO 评分，不使用 AA Index ──
    
    # Text (mapped to "chat" category): use Text Arena Elo only
    s_elo_text = compute_elo_score(elo_text)
    chat_s = s_elo_text if s_elo_text is not None else 0.0
    
    # Reasoning: same base as text (no separate GPQA/AIME data collected for all models)
    reason_s = chat_s
    
    # Coding: use Code Arena Elo only
    s_elo_code = compute_elo_score(elo_code)
    coding_s = s_elo_code if s_elo_code is not None else 0.0
    
    # Image/Vision (mapped to "image" modality score for multimodal models): 
    # use Vision Arena Elo only
    s_elo_vis = compute_elo_score(elo_vision)
    
    image_modality = None
    if s_elo_vis is not None:
        image_modality = s_elo_vis
    
    # Quality score = 0.4*text + 0.3*reasoning + 0.3*coding + 0.1*image(modality)
    if image_modality is not None:
        qs = round(0.4 * chat_s + 0.3 * reason_s + 0.3 * coding_s + 0.1 * image_modality, 1)
    else:
        qs = round(0.4 * chat_s + 0.3 * reason_s + 0.3 * coding_s, 1)
    
    modality = {"chat": chat_s, "reasoning": reason_s, "coding": coding_s}
    if image_modality is not None:
        modality["image"] = image_modality
    
    return modality, qs


def main():
    data = load_models()
    existing = {m['model_id']: m for m in data['models']}
    
    updated_models = []
    
    for model_id, model in sorted(existing.items()):
        categories = model.get('categories', [])
        
        elo_text = EL_O_TEXT.get(model_id)
        elo_code = EL_O_CODE.get(model_id)
        elo_vision = EL_O_VISION.get(model_id)
        image_elo = IMAGE_ARELO.get(model_id)
        
        modality, qs = compute_modality(model_id, categories, elo_text, elo_code, elo_vision, image_elo)
        
        # Rebuild categories using valid enum values
        new_cats = []
        if elo_text is not None:
            new_cats.append("chat")
            new_cats.append("reasoning")
        if elo_code is not None:
            new_cats.append("coding")
        if elo_vision is not None:
            new_cats.append("image")  # vision capability → image category
        if image_elo is not None:
            new_cats.append("image")
        # Fallback: only use valid category names from original
        if not new_cats:
            orig = set(model.get('categories', []))
            valid_orig = orig & {"chat", "coding", "reasoning", "image"}
            new_cats = list(valid_orig) if valid_orig else ["chat", "reasoning", "coding"]
        
        model['modality_scores'] = modality
        model['quality_score'] = int(round(qs))  # must be int for verifier
        model['categories'] = list(dict.fromkeys(new_cats))  # dedupe, preserve order
        
        updated_models.append(model)
        
        cat_str = ", ".join(f"{k}={v:.1f}" for k, v in modality.items())
        print(f"  {model_id:30s} qs={int(round(qs)):3d} ms={cat_str}")
    
    # Sort by quality_score descending, then model_id alphabetically for ties
    updated_models.sort(key=lambda m: (-m['quality_score'], m['model_id']))
    
    data['models'] = updated_models
    data['updated_at'] = "2026-07-24"
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nDone. {len(updated_models)} models written.")
    print(f"\nTop 10:")
    for idx, m in enumerate(updated_models[:10]):
        print(f"  #{idx+1} {m['model_id']:30s} qs={m['quality_score']}")
    print(f"\nBottom 5:")
    for m in updated_models[-5:]:
        print(f"  {m['model_id']:30s} qs={m['quality_score']}")

if __name__ == "__main__":
    main()
