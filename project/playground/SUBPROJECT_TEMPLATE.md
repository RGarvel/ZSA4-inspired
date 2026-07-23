# Playground 子项目构建模板

本模板用于创建 playground 下的新子项目。一个 Playground 子项目 = 一个子目录，内含 `index.html` + 可选的 `data/` 目录，完全静态，通过 GitHub Pages 部署。

---

## 一、目录结构

```
project/
└── <子项目名称>/
    ├── index.html          # 主页面（单文件，内嵌 CSS + JS）
    └── data/               # 可选：结构化数据源
        └── <data>.json     # JSON 数据文件
```

**路径约定：** Playground 页面上的子项目 `url` 字段使用相对路径 `'../<子项目名称>/index.html'`。

---

## 二、前端风格规范

### 2.1 共享 CSS 变量系统

所有子项目必须使用同一套 CSS 变量——确保亮/暗模式自动适配。

```css
:root {
  --bg-primary: #0d1117;      /* 页面背景 */
  --bg-secondary: #161b22;    /* 导航栏、控制栏背景 */
  --bg-card: #1c2333;         /* 卡片背景 */
  --text-primary: #e6edf3;    /* 主要文字 */
  --text-secondary: #8b949e;  /* 次要文字 */
  --accent-blue: #58a6ff;     /* 强调蓝 */
  --accent-green: #3fb950;    /* 成功/推荐绿 */
  --accent-purple: #bc8cff;   /* 紫色 */
  --accent-orange: #d29922;   /* 警告/高亮橙 */
  --border-color: #30363d;    /* 边框 */
}

body.light-mode {
  --bg-primary: #f6f8fa;
  --bg-secondary: #ffffff;
  --bg-card: #ffffff;
  --text-primary: #1f2328;
  --text-secondary: #656d76;
  --accent-blue: #0969da;
  --accent-green: #1a7f37;
  --accent-purple: #8250df;
  --accent-orange: #9a6700;
  --border-color: #d0d7de;
}
```

> **核心规则：** `body.light-mode` 只是重定义上述变量值，所有元素用 `var(--xxx)` 引用，亮色模式支持自动生效。仅保留硬编码覆盖处理 Bootstrap 等第三方库注入的 hardcoded color。

### 2.2 基础 CSS 骨架

每个子项目的 `<style>` 头部应包含以下基础样式：

```css
body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  transition: background-color 0.3s, color 0.3s;
  font-size: 0.92rem;
  line-height: 1.6;
  padding-bottom: 2rem;
}

.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--bg-secondary) !important;
  border-bottom: 1px solid var(--border-color);
  padding: 0.7rem 0;
  transition: background-color 0.3s, border-color 0.3s;
}

/* 返回链接 */
.back-link {
  color: var(--text-primary); text-decoration: none;
  padding: 0.5rem 1rem; border-radius: 25px; font-size: 0.85rem; font-weight: 500;
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: linear-gradient(135deg, rgba(88, 166, 255, 0.1), rgba(188, 140, 255, 0.05));
  border: 1px solid var(--border-color); transition: all 0.3s ease;
}
.back-link:hover {
  color: var(--accent-blue); border-color: var(--accent-blue);
  background: linear-gradient(135deg, rgba(88, 166, 255, 0.2), rgba(188, 140, 255, 0.1));
  transform: translateX(-3px); box-shadow: 0 2px 8px rgba(88, 166, 255, 0.2);
}

/* 主题切换按钮 */
.theme-toggle-btn {
  background: none; border: 1px solid var(--border-color); color: var(--text-primary);
  border-radius: 8px; padding: 0.4rem 0.6rem; cursor: pointer;
  transition: all 0.2s; font-size: 1.1rem;
}
.theme-toggle-btn:hover {
  border-color: var(--accent-blue); background-color: rgba(88, 166, 255, 0.1);
}

/* main-content wrapper */
.main-container { max-width: 1200px; margin: 0 auto; padding: 0 1.5rem; }
.main-content { padding-top: 1.75rem; padding-bottom: 4rem; }
```

### 2.3 品牌悬停过渡 (Brand Switcher)

子项目需要与灵感日报双向导航时，使用品牌悬停 CSS 类：

```html
<a class="navbar-brand d-flex align-items-center gap-2 brand-switcher" href="<PlaygroundURL>" id="brandLink">
  <i class="bi bi-<icon-name> brand-icon-default" id="brandIcon"></i>
  <i class="bi bi-lightbulb-fill brand-icon-hover" id="brandIconHover"></i>
  <span class="brand-text-default" id="brandText"><PageTitle></span>
  <span class="brand-text-hover" id="brandTextHover">灵感日报</span>
</a>
```

配套 CSS：
```css
.brand-switcher { position: relative; display: inline-flex; align-items: center; gap: 0.5rem; cursor: pointer; }
.brand-icon-default, .brand-icon-hover { transition: opacity 0.3s ease, transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1); font-size: 1.1rem; }
.brand-icon-default { color: var(--accent-orange) !important; }
.brand-icon-hover { position: absolute; left: 0; color: var(--accent-orange); opacity: 0; transform: scale(0.8); }
.brand-text-default, .brand-text-hover { font-size: 1rem; font-weight: 600; white-space: nowrap; transition: opacity 0.25s ease; }
.brand-text-hover { position: absolute; left: 2rem; background: linear-gradient(135deg, var(--accent-orange), var(--accent-purple)); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; opacity: 0; }
.brand-switcher:hover .brand-icon-default { opacity: 0; transform: scale(0.8); }
.brand-switcher:hover .brand-icon-hover { opacity: 1; transform: scale(1.15) rotate(-8deg); }
.brand-switcher:hover .brand-text-default { opacity: 0; }
.brand-switcher:hover .brand-text-hover { opacity: 1; }
body.light-mode .brand-icon-hover { color: #d29922 !important; }
body.light-mode .navbar-brand span { color: var(--text-primary) !important; }
```

---

## 三、固定功能组件

### 3.1 Navbar 结构（标准模板）

```html
<nav class="navbar" id="mainNavbar">
  <div class="container">
    <!-- 品牌 -->
    <a class="navbar-brand d-flex align-items-center gap-2 brand-switcher" href="<PlaygroundURL>" id="brandLink">
      <i class="bi bi-<icon-name> brand-icon-default" id="brandIcon"></i>
      <i class="bi bi-lightbulb-fill brand-icon-hover" id="brandIconHover"></i>
      <span class="brand-text-default" id="brandText"><PageTitle></span>
      <span class="brand-text-hover" id="brandTextHover">灵感日报</span>
    </a>
    <!-- 右侧操作区 -->
    <div class="d-flex align-items-center gap-2 ms-auto">
      <a class="back-link" href="<PlaygroundURL>">
        <i class="bi bi-house-door"></i> 返回Playground
      </a>
      <button class="theme-toggle-btn" onclick="toggleTheme()" title="切换亮暗模式">
        <i class="bi bi-moon-fill" id="themeIcon"></i>
      </button>
    </div>
  </div>
</nav>
```

> **关键约束：**
> - 外层 `<div>` 只用 `class="container"`，**不要用** `justify-content-between`
> - 右侧区域用 `ms-auto` 靠右，间距 `gap-2`（不是 gap-3）

### 3.2 主题管理（标准代码块）

```javascript
// 每个子项目必须使用独立 prefix 避免 localStorage 冲突
let isDarkMode = localStorage.getItem('<prefix>_theme') !== 'light';

function applyTheme() {
  document.body.classList.toggle('light-mode', !isDarkMode);
  const icon = $('themeIcon');
  if (icon) icon.className = isDarkMode ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
  localStorage.setItem('<prefix>_theme', isDarkMode ? 'dark' : 'light');
}
function toggleTheme() { isDarkMode = !isDarkMode; applyTheme(); }
```

> `<prefix>` 为项目缩写，如 `ct_theme`（compliance）、`pd_theme`（price-dashboard）。**不可共用** `'theme'`。

### 3.3 滚动置顶

```javascript
// Scroll to top when clicking navbar blank area
document.getElementById('mainNavbar')?.addEventListener('click', function(e) {
  const target = e.target;
  if (target.tagName === 'A' || target.closest('a') || target.tagName === 'BUTTON' || target.closest('button')) return;
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
```

### 3.4 DOM 缓存模式

```javascript
const $ = id => document.getElementById(id);

// 启动时一次性缓存所有需要的 DOM 引用
function cacheDom() {
  // 按需添加: $el.lastUpdated = $('lastUpdated');
}
```

---

## 四、数据接口规范

### 4.1 数据加载流程

```javascript
const DATA_URL = './data/models.json';

async function loadData() {
  try {
    const response = await fetch(DATA_URL);
    if (!response.ok) throw new Error('Failed to load data');
    return await response.json();
  } catch (error) {
    console.error('Error loading data:', error);
    return [];
  }
}
```

### 4.2 渲染建议

```javascript
// 使用 parts.push().join('') 而非 html +=（O(n²) → O(n)）
const parts = [];
for (const item of data) {
  parts.push(`<div class="card">${item.name}</div>`);
}
container.innerHTML = parts.join('');
```

---

## 五、性能优化清单

| 优化项 | 做法 |
|--------|------|
| HTML 渲染 | `parts.push().join('')` 替代 `+=` 拼接 |
| DOM 查询 | 启动时缓存到 `$el`，热路径零查询 |
| 过滤器查找 | `arr.includes(x)` → `new Set(arr).has(x)` |
| Chart.js | 数据聚合合并为单次 for 循环 |
| Section 折叠 | 缓存 NodeList，避免重复 querySelectorAll |

---

## 六、注册到 Playground 导航

在 `playground/index.html` 的 `projects` 数组中添加条目：

```javascript
{
  name: '子项目名称',
  icon: '📊',
  description: '一句话描述...',
  tags: ['技术栈1', '技术栈2'],
  url: '../<子项目名称>/index.html',
  status: 'live',       // 或 'dev'
  statusText: '已上线'
}
```

---

## 七、快速启动 Checklist

创建新子项目时逐项确认：

- [ ] 目录结构：`project/<子名称>/index.html` + 可选 `data/`
- [ ] CSS 变量系统已引入（`:root` + `body.light-mode`）
- [ ] 基础样式：body/font-size/line-height、navbar、back-link、theme-toggle-btn、main-container
- [ ] Brand switcher hover 动画已实现（icon-orange + text-gradient）
- [ ] localStorage key 使用项目独立 prefix（如 `<prefix>_theme`）
- [ ] Navbar 用 `container` + `ms-auto` + `gap-2`，**不用** `justify-content-between`
- [ ] 主题管理 `applyTheme` / `toggleTheme` 已集成
- [ ] DOMContentLoaded ≤ 1 个监听器
- [ ] loadData → render 严格串行 + catch fallback
- [ ] 渲染使用 `parts.push().join('')`
- [ ] Playground `projects` 数组已添加入口

---

## 八、常见陷阱

1. **白屏死因——重复标识符声明：** 多次 patch 可能导致同一文件出现 `const $ = ...` + `function $(id) { ... }` 共存。提交前 grep 短函数名（$、cacheDom 等）确认唯一。

2. **fetch 路径问题：** GitHub Pages 子目录下 `./data/file.json` 是相对当前 URL 解析的。子项目用 `./data/...` 即可。

3. **Bootstrap 表格背景硬编码：** Bootstrap 给 `<td>` 设白色背景。需用 `.table > :not(caption) > * > * { background-color: var(--bg-card) !important; }` 覆盖。

---

## 参考实现

| 项目 | 行数 | 特点 |
|------|------|------|
| `playground/index.html` | ~423 | 项目导航页 |
| `ai-model-price-dashboard/index.html` | ~1084 | 数据仪表盘 + Chart.js |
| `ai-compliance-tool/index.html` | ~862 | 交互式 checklist + 本地 JSON 数据 |
| `index.html` (灵感日报主页) | ~1086 | 每日推送 + 筛选交互 |
