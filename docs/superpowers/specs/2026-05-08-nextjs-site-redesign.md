# Next.js 静态站重构设计文档

**日期：** 2026-05-08  
**状态：** 待实现

---

## 背景

当前站点由 `site/build_site.py` 生成单个 `index.html`，所有日报内嵌其中。随着每日积累，文件将持续增大（当前 8 篇已达 80KB，一年后预计 3MB+），初始解析成本上升，且无法实现独立 URL、搜索、RSS 等功能。

## 目标

将站点迁移为 Next.js 静态站，实现：
- 每篇日报独立 URL（可分享、可深链）
- 全文搜索（Pagefind，支持中文）
- RSS Feed（`/feed.xml`，最近 20 篇）
- 保持现有设计风格，修复对比度问题

---

## 架构方案

**方案：在 `news-intel` 仓库内新增 Next.js 站点子目录**

```
news-intel/
  report/                    ← 数据源（不动）
  raw/                       ← 原始抓取（不动）
  scripts/fetch.py           ← 不动
  site/                      ← 替换现有 Python 站点，改为 Next.js 工程
    app/
      page.js                ← 首页，渲染最新日报
      [date]/
        page.js              ← 单篇日报页
      search/
        page.js              ← 搜索页（Pagefind UI）
      feed.xml/
        route.js             ← RSS Feed 路由
    lib/
      reports.js             ← 读取 ../report/*.md，解析 markdown
    components/
      Sidebar.js
      ReportBody.js
    public/
    next.config.js
    package.json
  .github/workflows/
    deploy.yml               ← 改为 npm run build
```

`report/` 目录完全不动，`site/lib/reports.js` 在构建时读取 `../report/*.md`。

---

## 路由设计

| URL | 内容 |
|-----|------|
| `https://cearl.cc/news-intel/` | 最新日报（同 `/2026-05-08`） |
| `https://cearl.cc/news-intel/2026-05-08` | 单篇日报 |
| `https://cearl.cc/news-intel/search` | 搜索页 |
| `https://cearl.cc/news-intel/feed.xml` | RSS Feed |

---

## Next.js 配置

```js
// next.config.js
module.exports = {
  basePath: '/news-intel',
  output: 'export',       // 纯静态导出，GitHub Pages 兼容
  trailingSlash: true,    // 兼容静态托管
}
```

`basePath` 统一管理，所有内部链接通过 Next.js `Link` 组件自动处理，RSS 和 Pagefind 中的绝对链接使用 `process.env.NEXT_PUBLIC_BASE_PATH`。

---

## 数据层

**`lib/reports.js`**

- 构建时 `fs.readdirSync('../report')` 读取所有 `.md` 文件
- 用 `gray-matter` 解析 frontmatter（兼容无 frontmatter 的现有文件）
- 用 `remark` + `remark-html` 将 markdown 转为 HTML
- 导出两个函数：
  - `getAllReports()` → 返回所有日报的 `{date, title, excerpt}` 列表（用于 Sidebar、RSS）
  - `getReport(date)` → 返回单篇日报的完整 HTML 内容

---

## 页面设计

### 首页 `/`

- 服务端读取最新日报，渲染与 `/[date]` 相同的内容
- 不跳转，直接展示

### 单篇日报 `/[date]`

- `generateStaticParams` 在构建时为每篇生成静态页
- 布局：左侧 Sidebar（日期列表）+ 右侧日报正文
- 当前日期在 Sidebar 中高亮
- 移动端：Sidebar 折叠为横向滚动日期条

### 搜索 `/search`

- 页面加载 Pagefind UI（CSS + JS）
- 搜索结果链接到对应 `/[date]` 页面
- Pagefind 在 `postbuild` 阶段对 `out/` 目录建立索引

### RSS `/feed.xml`

- Next.js Route Handler 在构建时生成静态 XML
- 包含最近 20 篇
- 每篇含：标题、链接、发布日期、正文前 200 字摘要

---

## 构建流程

```bash
cd site
npm run build
# postbuild: npx pagefind --site out --output-path out/pagefind
```

1. Next.js SSG 生成所有静态页到 `site/out/`
2. `postbuild` 运行 Pagefind，在 `out/pagefind/` 生成搜索索引
3. GitHub Actions 部署 `site/out/` 到 GitHub Pages

### GitHub Actions 改动

```yaml
- name: Install dependencies
  run: cd site && npm ci

- name: Build site
  run: cd site && npm run build

- name: Upload Pages artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: ./site/out
```

---

## 依赖

```json
{
  "dependencies": {
    "next": "^14",
    "react": "^18",
    "react-dom": "^18",
    "remark": "^15",
    "remark-html": "^16",
    "gray-matter": "^4"
  },
  "devDependencies": {
    "pagefind": "^1"
  },
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "postbuild": "npx pagefind --site out --output-path out/pagefind"
  }
}
```

不引入 TypeScript，减少配置复杂度，纯 JS。

---

## 设计风格

沿用刚完成的重设计风格：
- 背景色 `#0e1117`（深蓝黑）
- 主文本 `#f0f2f7`，副文本 `#b8c0d0`，muted `#7a8699`
- Accent 电蓝 `#4f8ef7`
- 字体：`Newsreader`（标题）+ 系统 sans-serif（正文）
- 全部满足 WCAG AA 对比度要求

CSS 直接写在 `app/globals.css`，复用现有设计 token，不引入 Tailwind。

---

## 不在本次范围内

- 邮件订阅（留到以后）
- 标签/分类系统
- 评论功能
- 暗色/亮色切换
