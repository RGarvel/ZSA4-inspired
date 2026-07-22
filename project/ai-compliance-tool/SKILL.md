---
name: ai-compliance-tool
description: AI合规检查清单工具 — 覆盖7大热门场景，用户自由勾选检查项，实时计算风险评分，饼图+时间线可视化，导出markdown报告
tags: [playground, compliance, ai-regulation]
created: 2026-07-22
---

# AI 合规检查清单工具 — 构建指南

## 项目结构
```
project/
└── ai-compliance-tool/
    ├── index.html          # 主页面（单文件，内嵌CSS+JS）
    └── data/
        ├── scenarios.json  # 所有场景+规则库
        └── regulations.json # 法规库（用于时间线）
```

## 数据文件设计

### scenarios.json
```json
{
  "scenarios": [
    {
      "id": "chatbot_eu",
      "name": "AI聊天机器人/客服",
      "icon": "💬",
      "jurisdiction": "欧盟AI法案",
      "regulation_id": "eu_ai_act",
      "risk_level": "高风险",
      "description": "面向消费者的AI对话系统，包括客服机器人、虚拟助手等",
      "checks": [
        {
          "id": "chatbot-1",
          "category": "透明度",
          "requirement": "必须明确告知用户正在与AI交互",
          "baseline_passed": false,
          "notes": "",
          "severity": "critical"
        },
        {
          "id": "chatbot-2",
          "category": "透明度",
          "requirement": "提供清晰的AI系统使用说明",
          "baseline_passed": false,
          "notes": "",
          "severity": "high"
        },
        {
          "id": "chatbot-3",
          "category": "数据安全",
          "requirement": "用户对话数据需符合GDPR要求",
          "baseline_passed": false,
          "notes": "",
          "severity": "critical"
        },
        {
          "id": "chatbot-4",
          "category": "内容安全",
          "requirement": "防止生成有害/违法内容",
          "baseline_passed": false,
          "notes": "",
          "severity": "high"
        },
        {
          "id": "chatbot-5",
          "category": "人工监督",
          "requirement": "高风险场景需有人工介入机制",
          "baseline_passed": false,
          "notes": "",
          "severity": "medium"
        },
        {
          "id": "chatbot-6",
          "category": "可解释性",
          "requirement": "用户有权要求AI决策的解释",
          "baseline_passed": false,
          "notes": "",
          "severity": "medium"
        },
        {
          "id": "chatbot-7",
          "category": "偏见检测",
          "requirement": "定期进行公平性测试，避免歧视性输出",
          "baseline_passed": false,
          "notes": "",
          "severity": "high"
        },
        {
          "id": "chatbot-8",
          "category": "日志记录",
          "requirement": "保留对话日志至少6个月用于审计",
          "baseline_passed": false,
          "notes": "",
          "severity": "low"
        }
      ],
      "recommendations": [
        "部署内容过滤中间件拦截敏感话题",
        "建立用户反馈机制收集AI错误案例",
        "定期更新训练数据避免知识过时",
        "设置明确的服务边界声明"
      ]
    }
  ]
}
```

### regulations.json
```json
{
  "regulations": [
    {
      "id": "eu_ai_act",
      "name": "欧盟AI法案",
      "enforcement_date": "2026-08-02",
      "regions": ["EU", "EEA"],
      "timeline": [
        {"date": "2024-03-13", "event": "欧洲议会投票通过"},
        {"date": "2024-04-13", "event": "欧盟理事会正式批准"},
        {"date": "2025-08-02", "event": "禁止性规定生效"},
        {"date": "2026-08-02", "event": "高风险系统全面执法"},
        {"date": "2027-08-02", "event": "全部条款生效"}
      ]
    }
  ]
}
```

## 核心功能模块

### 1. 场景选择器
- 左侧边栏列出所有场景（图标+名称+风险等级徽章）
- 点击切换，右侧显示详情
- 支持按风险等级/类别筛选

### 2. 检查清单编辑器（高自由度）
- 每个check项可独立勾选 passed/not passed
- 可添加自定义notes
- 支持批量操作：一键通过/全部不通过
- 拖拽重排检查项顺序
- 可折叠/展开不同category

### 3. 实时评分计算
- 按severity加权：critical=4, high=3, medium=2, low=1
- 总分 = Σ(passed ? weight : 0) / Σ(weight) * 100
- 风险等级判定：
  - ≥80%: 低风险（绿色）
  - 60-79%: 中风险（黄色）
  - 40-59%: 较高风险（橙色）
  - <40%: 高风险（红色）

### 4. 可视化
- **风险等级分布饼图** — Chart.js doughnut，显示各severity级别的通过/未通过比例
- **时间线趋势** — Chart.js line/bar，展示法规关键节点及合规进度

### 5. 导出功能
- 生成markdown格式合规报告
- 包含：场景信息、检查结果汇总、风险评分、建议
- 复制到剪贴板或下载为.md文件

### 6. 数据持久化
- localStorage 保存用户的勾选状态和notes
- 刷新页面后自动恢复

## UI 规范
- 复用 ZSA4-inspired 共享CSS变量系统
- Bootstrap 5.3.3 grid + components
- Bootstrap Icons
- Chart.js 4.x
- 响应式布局（sidebar + main content）
- 暗色/亮色模式切换

## 交互细节
- 勾选check项时实时更新评分和图表
- 评分变化时有动画过渡
- 筛选/搜索即时响应
- 导出报告前预览
- 操作有toast通知反馈

## 性能要求
- parts.push().join('') 渲染
- DOM缓存到$el
- Chart.js实例复用（销毁重建）
