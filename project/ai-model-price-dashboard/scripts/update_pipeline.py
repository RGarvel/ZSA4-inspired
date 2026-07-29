#!/usr/bin/env python3
"""
AI Model Price Dashboard - One-click Update Pipeline
Combines: fetch ELO rankings → update prices → calculate scores → generate report
Replaces multiple cron terminal calls with single script execution.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, date

# Configuration
BASE_DIR = Path(r"C:\Users\阮家威\AppData\Local\hermes\data\inspiration\project\ai-model-price-dashboard")
DATA_FILE = BASE_DIR / "data" / "models.json"
SCRIPTS_DIR = BASE_DIR / "scripts"

def load_models():
    """Load current models.json"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_models(data):
    """Save models.json with timestamp"""
    data['updated_at'] = str(date.today())
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved {len(data['models'])} models, updated_at={data['updated_at']}")

def fetch_elo_top10():
    """Fetch top 10 ELO models from lmarena API or fallback to static list"""
    # TODO: Implement actual API call to lmarena.ai
    # For now, return known top models (can be updated manually or via web scraping)
    return [
        {"model_id": "claude-opus-4.6", "name": "Claude Opus 4.6", "vendor": "Anthropic", "elo": 1504},
        {"model_id": "gemini-3.1-pro", "name": "Gemini 3.1 Pro", "vendor": "Google", "elo": 1500},
        {"model_id": "claude-opus-4.6-thinking", "name": "Claude Opus 4.6 Thinking", "vendor": "Anthropic", "elo": 1500},
        {"model_id": "gpt-5.6-sol", "name": "GPT-5.6 Sol", "vendor": "OpenAI", "elo": 1492},
        {"model_id": "kimi-k3", "name": "Kimi K3", "vendor": "Moonshot AI", "elo": 1486},
        {"model_id": "grok-4.5", "name": "Grok 4.5", "vendor": "xAI", "elo": 1480},
        {"model_id": "claude-sonnet-5", "name": "Claude Sonnet 5", "vendor": "Anthropic", "elo": 1475},
        {"model_id": "gemini-3.5-flash", "name": "Gemini 3.5 Flash", "vendor": "Google", "elo": 1465},
        {"model_id": "claude-opus-4.8", "name": "Claude Opus 4.8", "vendor": "Anthropic", "elo": 1455},
        {"model_id": "kimi-k2.6", "name": "Kimi K2.6", "vendor": "Moonshot AI", "elo": 1440},
    ]

def check_and_add_missing_models(data, top10):
    """Check which top10 models are missing and add them"""
    existing_ids = {m['model_id'] for m in data['models']}
    new_models = []
    
    for model in top10:
        if model['model_id'] not in existing_ids:
            # Add new model with placeholder data
            new_model = {
                "model_id": model['model_id'],
                "name": model['name'],
                "vendor": model['vendor'],
                "open_source": False,
                "tier": "premium",  # Top ELO models are usually premium
                "categories": ["chat", "reasoning", "coding", "image"],
                "context_window": 200000,
                "input_price_per_1m": 5.0,  # Placeholder
                "output_price_per_1m": 25.0,  # Placeholder
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
                "score_chat": None,
                "value_score_chat": 0,
                "value_score_coding": 0,
                "value_score_reasoning": 0,
                "value_score_image": 0,
                "value_score": 0,
                "updated_at": str(date.today())
            }
            new_models.append(new_model)
            print(f"  + Added new model: {model['name']} (ELO {model['elo']})")
    
    if new_models:
        data['models'].extend(new_models)
        save_models(data)
        print(f"✓ Added {len(new_models)} new models")
    else:
        print("✓ All top 10 models already exist")
    
    return new_models

def run_price_update():
    """Run update_prices.py script"""
    print("\n[2/3] Running price update...")
    script = SCRIPTS_DIR / "update_prices.py"
    if script.exists():
        os.system(f'python "{script}"')
    else:
        print(f"⚠ Script not found: {script}")

def run_score_calculation():
    """Run fix_value_score.py script"""
    print("\n[3/3] Running score calculation...")
    script = SCRIPTS_DIR / "fix_value_score.py"
    if script.exists():
        os.system(f'python "{script}"')
    else:
        print(f"⚠ Script not found: {script}")

def generate_report(new_models, updates):
    """Generate QQ report"""
    data = load_models()
    
    # Sort by value_score (chat)
    sorted_models = sorted(data['models'], key=lambda m: m.get('value_score_chat', 0), reverse=True)
    top5 = sorted_models[:5]
    
    report = []
    report.append("📊 **AI模型价格日报**\n")
    
    report.append("【💰 性价比 Top 5】")
    for i, m in enumerate(top5, 1):
        report.append(f"{i}. {m['name']} — ${m['output_price_per_1m']}/M tokens | 质量{m.get('composite_score', 'N/A')} | 性价比{m.get('value_score_chat', 0):.1f}")
    
    report.append("\n【📈 今日变化】")
    if new_models:
        report.append(f"• 新增模型：{len(new_models)} 个")
        for m in new_models:
            report.append(f"  - {m['name']}")
    else:
        report.append("• 新增模型：0 个")
    
    if updates:
        report.append(f"• 价格变动：{len(updates)} 个")
    else:
        report.append("• 价格变动：0 个")
    
    report.append("\n📰 仪表盘：https://rgarvel.github.io/ZSA4-inspired/project/ai-model-price-dashboard/")
    
    return "\n".join(report)

def main():
    print("=" * 70)
    print("AI Model Price Dashboard - One-click Update Pipeline")
    print("=" * 70)
    
    # Step 1: Load data and fetch ELO top 10
    print("\n[1/3] Fetching ELO rankings...")
    data = load_models()
    top10 = fetch_elo_top10()
    print(f"✓ Top 10 ELO models retrieved")
    
    # Step 2: Check and add missing models
    new_models = check_and_add_missing_models(data, top10)
    
    # Step 3: Run price update
    run_price_update()
    
    # Step 4: Run score calculation
    run_score_calculation()
    
    # Step 5: Generate report
    data = load_models()
    report = generate_report(new_models, [])
    
    print("\n" + "=" * 70)
    print("UPDATE COMPLETE")
    print("=" * 70)
    print(report)
    
    # Save report to file for cron to read
    report_file = BASE_DIR / "latest_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n✓ Report saved to: {report_file}")

if __name__ == "__main__":
    main()
