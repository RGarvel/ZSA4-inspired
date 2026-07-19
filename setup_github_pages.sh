#!/bin/bash
# GitHub Pages 仓库初始化脚本
# 用于将灵感日报部署到 GitHub Pages

# 配置
REPO_NAME="inspiration-daily"
BRANCH="main"

echo "🚀 初始化 GitHub Pages 仓库..."

# 检查是否已存在仓库
if [ -d "$REPO_NAME" ]; then
    echo "⚠️  仓库已存在，跳过创建"
else
    # 创建仓库目录
    mkdir -p "$REPO_NAME"
    cd "$REPO_NAME"
    
    # 初始化 Git
    git init
    git checkout -b "$BRANCH"
    
    # 复制文件
    cp "../index.html" "./index.html"
    mkdir -p "./data"
    cp "../sample_data.json" "./data/all_inspiration.json"
    
    # 创建 README
    cat > README.md << 'EOF'
# 灵感日报 | Inspiration Daily

每日 AI 技术与创业灵感推送

## 功能
- 按日期浏览历史推送
- 按类别筛选（AI 技术 / 创业动态 / 产品工具）
- 深色主题，响应式设计

## 数据来源
- arXiv 论文
- 机器之心、量子位等中文媒体
- TechCrunch、Hacker News 等英文媒体
- Product Hunt 新产品

## 自动部署
本页面由 Hermes Agent 自动更新
EOF

    # 提交
    git add .
    git commit -m "Initial commit: Inspiration Daily website"
    
    echo "✅ 仓库创建完成"
    echo "📁 位置: $(pwd)"
fi

echo ""
echo "下一步："
echo "1. 登录 GitHub: gh auth login"
echo "2. 创建远程仓库: gh repo create $REPO_NAME --public"
echo "3. 推送代码: git push -u origin main"
echo "4. 启用 GitHub Pages: gh repo edit $REPO_NAME --enable-pages"
echo ""
echo "完成后访问: https://<your-username>.github.io/$REPO_NAME/"
