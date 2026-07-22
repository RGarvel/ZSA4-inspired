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
  --text-secondary: #9da5b1;  /* 次要文字 */
  --accent-blue: #58a6ff;     /* 强调蓝 */
  --accent-green: #3fb950;    /* 成功/推荐绿 */
  --accent-purple: #bc8cff;   /* 紫色 */
  --accent-orange: #d29922;   /* 警告/高亮橙 */
  --accent-red: #ff5252;      /* 错误 */
  --border-color: #30363d;    /* 边框 */
}

body.light-mode {
  --bg-primary: #f6f8fa;
  --bg-secondary: #ffffff;
  --bg-card: #ffffff;
  --text-primary: #1f2328;
  --text-secondary: #656d76;    /* Playground: 比 dashboard 略暗 */
  --accent-blue: #0969da;
  --accent-green: #1a7f37;
  --accent-purple: #8250df;
  --accent-orange: #9a6700;
  --accent-red: #cf222e;
  --border-color: #d0d7de;
}
```

> **核心规则：** `body.light-mode` 只是重定义上述变量值，所有元素用 `var(--xxx)` 引用，亮色模式支持自动生效。仅保留硬编码覆盖处理 Bootstrap 等第三方库注入的 hardcoded color。

### 2.2 基础 CSS 骨架

每个子项目的 `<style>` 头部应包含以下基础样式：

```css
/* 页面与字体 */
body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  transition: background-color 0.3s, color 0.3s;
}

/* 导航栏 */
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--bg-secondary) !important;
  border-bottom: 1px solid var(--border-color);
  transition: background-color 0.3s, border-color 0.3s;
}

/* 返回链接（统一样式） */
.back-link {
  color: var(--text-primary);
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.85rem;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, rgba(88, 166, 255, 0.1), rgba(188, 140, 255, 0.05));
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}
.back-link:hover {
  color: var(--accent-blue);
  border-color: var(--accent-blue);
  background: linear-gradient(135deg, rgba(88, 166, 255, 0.2), rgba(188, 140, 255, 0.1));
  transform: translateX(-3px);
  box-shadow: 0 2px 8px rgba(88, 166, 255, 0.2);
}

/* 主题切换按钮 */
.theme-toggle-btn {
  background: none;
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  border-radius: 8px;
  padding: 0.4rem 0.6rem;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1.1rem;
}
.theme-toggle-btn:hover {
  border-color: var(--accent-blue);
  background-color: rgba(88, 166, 255, 0.1);
}
```

### 2.3 品牌悬停过渡（Dashboard 风格）

子项目需要与灵感日报双向导航时，使用品牌悬停 CSS 类：

```html
<!-- Brand switcher: hover transitions to 灵感日报 -->
<a class="navbar-brand d-flex align-items-center gap-2 brand-switcher" href="/ZSA4-inspired/index.html">
  <i class="bi bi-bar-chart-line-fill brand-icon-default" id="brandIcon"></i>
  <i class="bi bi-lightbulb-fill brand-icon-hover" id="brandIconHover"></i>
  <span class="brand-text-default" id="brandText">子项目名称</span>
  <span class="brand-text-hover" id="brandTextHover">灵感日报</span>
</a>
```

配套 CSS：
```css
.brand-switcher { position: relative; display: inline-flex; align-items: center; gap: 0.5rem; }
.brand-icon-default, .brand-icon-hover { transition: opacity 0.3s ease, transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1); font-size: 1.1rem; display: inline-flex; }
.brand-icon-default { color: var(--accent-blue) !important; }
.brand-icon-hover { position: absolute; left: 0; color: var(--accent-orange); opacity: 0; transform: scale(0.8); }
.brand-text-default, .brand-text-hover { font-size: 1rem; font-weight: 600; white-space: nowrap; transition: opacity 0.25s ease; display: inline-block; }
.brand-text-default { color: var(--text-primary); }
.brand-text-hover { position: absolute; left: 2rem; background: linear-gradient(135deg, var(--accent-orange), var(--accent-purple)); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; opacity: 0; }
.brand-switcher:hover .brand-icon-default { opacity: 0; transform: scale(0.8); }
.brand-switcher:hover .brand-icon-hover { opacity: 1; transform: scale(1.15) rotate(-8deg); }
.brand-switcher:hover .brand-text-default { opacity: 0; }
.brand-switcher:hover .brand-text-hover { opacity: 1; }
```

---

## 三、固定功能组件

### 3.1 Navbar 结构（标准模板）

```html
<nav class="navbar" id="mainNavbar">
  <div class="container">
    <!-- 品牌（带悬停过渡到灵感日报） -->
    <a class="navbar-brand d-flex align-items-center gap-2 brand-switcher" href="/ZSA4-inspired/index.html" id="brandLink">
      <i class="bi bi-bar-chart-line-fill brand-icon-default" id="brandIcon"></i>
      <i class="bi bi-lightbulb-fill brand-icon-hover" id="brandIconHover"></i>
      <span class="brand-text-default" id="brandText">子项目名称</span>
      <span class="brand-text-hover" id="brandTextHover">灵感日报</span>
    </a>
    
    <!-- 右侧操作区 -->
    <div class="d-flex align-items-center ms-auto gap-3">
      <small class="text-muted" id="lastUpdated">数据更新于: 加载中...</small>
      <a class="back-link" href="/ZSA4-inspired/project/playground/">
        <i class="bi bi-house-door"></i> 返回Playground
      </a>
      <button class="theme-toggle-btn" onclick="toggleTheme()" title="切换亮暗模式">
        <i class="bi bi-moon-fill" id="themeIcon"></i>
      </button>
    </div>
  </div>
</nav>
```

### 3.2 主题管理（标准代码块）

```javascript
// Theme management — MUST be included in every subproject
let isDarkMode = localStorage.getItem('theme') !== 'light';

function applyTheme() {
  document.body.classList.toggle('light-mode', !isDarkMode);
  const themeIcon = document.getElementById('themeIcon');
  if (themeIcon) themeIcon.className = isDarkMode ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
  localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
}

function toggleTheme() {
  isDarkMode = !isDarkMode;
  applyTheme();
}
```

### 3.3 滚动置顶

```javascript
// Scroll to top when clicking navbar blank area
document.getElementById('mainNavbar').addEventListener('click', function(e) {
  const target = e.target;
  const isLink = target.tagName === 'A' || target.closest('a');
  const isBtn = target.tagName === 'BUTTON' || target.closest('button');
  if (!isLink && !isBtn) {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
});
```

### 3.4 DOM 缓存模式

启动时一次性缓存所有需要的 DOM 引用，避免热路径重复查询：

```javascript
const $ = id => document.getElementById(id);

let $el = {};  // cached DOM refs

function cacheDom() {
  $el.lastUpdated = $('lastUpdated');
  // ... add any other needed IDs here
}
```

> **关键：所有 `$el.xxx.addEventListener()` 必须在 `cacheDom()` 之后注册，参见 memory 中的初始化时序规则。**

---

## 四、数据接口规范

### 4.1 数据加载流程

```javascript
const DATA_URL = './data/models.json';  // 相对路径，指向同目录下的 data/ 文件夹

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

### 4.2 数据结构约定

JSON 数据文件（如 `data/models.json`）结构由业务决定，但注意：

- **绝对日期 vs 相对日期：** 所有数据项的 `date` 字段应为今天的日期或具体 YYYY-MM-DD 格式
- **价格单位：** 如有价格字段，统一使用 USD per 1M tokens（文本）或 USD per image（图像）
- **枚举键名：** 保持小驼峰（camelCase），如 `open_source`, `quality_score`

### 4.3 数据处理建议

```javascript
// 标准化：类别映射等统一在加载时做一次
const NORMALIZE_MAP = { some_key: 'normalized_value' };
function normalizeKey(key) { return NORMALIZE_MAP[key] || key; }

// 加载后一次性规范化
allData.forEach(item => { item.category = normalizeKey(item.category); });

// 高性能渲染：使用 parts.push().join('') 而非 html +=
const parts = [];
for (const item of filteredData) {
  parts.push(`<div class="card">${item.name}</div>`);
}
container.innerHTML = parts.join('');
```

---

## 五、性能优化清单

| 优化项 | 做法 |
|--------|------|
| HTML 渲染 | 用 `parts.push().join('')` 替代 `html +=`（O(n²) → O(n)） |
| DOM 查询 | 启动时缓存到 `$el` 对象，热路径零 `getElementById` |
| 过滤器查找 | `arr.includes(x)` → `new Set(arr).has(x)`（O(n) → O(1)） |
| Chart.js 聚合 | 数据聚合合并为单次 `for` 循环，避免多次 `.map()` |
| Section 展开/折叠 | 缓存 NodeList，避免重复 `querySelectorAll` |

---

## 六、注册到 Playground 导航

在主 Playground 页面 `index.html` 的 `projects` 数组中添加条目：

```javascript
const projects = [
  {
    name: '子项目名称',
    icon: '📊',           // Emoji 图标
    description: '一句话描述...',
    tags: ['技术栈1', '技术栈2'],
    url: '../<子项目名称>/index.html',
    status: 'live',       // 或 'dev'
    statusText: '已上线'    // 或 '开发中'
  }
];
```

`status` 可选值：
- `live` → 绿色徽章 "已上线"
- `dev` → 橙色徽章 "开发中"

---

## 七、快速启动 Checklist

创建新子项目时逐项确认：

- [ ] 目录结构：`project/<子项目名称>/index.html` + 可选 `data/`
- [ ] CSS 变量系统已引入（复制 `:root` + `body.light-mode`）
- [ ] 基础样式：body、navbar、back-link、theme-toggle-btn
- [ ] Brand switcher 悬停过渡已实现
- [ ] 主题管理代码（`applyTheme` / `toggleTheme` / localStorage）
- [ ] Navbar ID 为 `mainNavbar`，滚动置顶功能存在
- [ ] 数据文件路径：`./data/<file>.json`（相对当前目录）
- [ ] DOM 缓存 `$el` 在 `DOMContentLoaded` 中正确初始化
- [ ] 事件监听器在 `cacheDom()` 之后注册
- [ ] 渲染使用 `parts.push().join('')`
- [ ] Playground `projects` 数组已添加入口

---

## 八、常见陷阱

1. **白屏死因——重复标识符声明：** 连续 patch 可能导致同一文件出现 `const $ = ...` + `function $(id) { ... }` 共存，浏览器 SyntaxError 杀死整个脚本。每次提交前 grep 短函数名 `$`、`cacheDom`。

2. **白屏死因——$el 访问在 cacheDom 之前：** 任何 `$(id)` 或 `$el.xxx` 的使用必须放在 `DOMContentLoaded` handler 内部，且确保 DOM 已就绪。

3. **fetch 路径问题：** GitHub Pages 子目录下 `./data/file.json` 是相对当前 URL 解析的。子项目用 `./data/...` 即可；如果目录层级不同需调整。

4. **Bootstrap 表格背景硬编码：** Bootstrap 直接给 `<td>` 设白色背景，你的 CSS 变量无法穿透。用 `.table > :not(caption) > * > * { background-color: var(--bg-card) !important; }` 覆盖。
