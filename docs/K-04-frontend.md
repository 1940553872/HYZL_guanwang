# K-04 前端开发工程师：页面实现与性能

> 组别：K-B 网站开发类 ｜ 版本 v0.1 ｜ 2026-10-08
> 输入变量：
> - **{设计稿/需求}**：K-01 设计规范与视觉稿、K-02 信息架构与交互说明、[01 内容呈现与布局](./01-content-and-layout.md)
> - **{技术栈约束}**：SEO 友好（服务端渲染 / 静态生成）；中国内地部署，不依赖境外 CDN 和字体服务；内容由 CMS 管理；容器化交付
> - **{性能目标}**：Core Web Vitals 移动端 P75：LCP ≤ 2.5 s、INP ≤ 200 ms、CLS ≤ 0.1

---

## 1. 技术选型表

| 类别 | 选型 | 版本（立项时锁定最新稳定小版本） | 选型理由 |
|---|---|---|---|
| 运行时 | Node.js | 24 LTS | 长期支持；与构建、SSR 运行一致 |
| 框架 | Next.js（App Router） | 16.x | SSG + ISR 兼顾 SEO 和内容实时性；React Server Components 降低客户端 JS；内置图片优化、路由、i18n 路由段 |
| UI 运行时 | React | 19.x | Next.js 配套 |
| 语言 | TypeScript | 5.x（strict） | 类型安全；CMS 内容模型生成类型 |
| 样式 | Tailwind CSS | 4.x | 设计 Token 映射为 CSS 变量（`@theme`），保证与 K-01 一致；按需生成、体积小 |
| 无障碍交互原语 | Radix UI Primitives | 最新稳定版 | 下拉、Tab、手风琴、弹窗自带键盘与 ARIA 支持，样式完全自定义（不引入成品 UI 库，以免风格冲突） |
| 状态管理 | 以服务端组件 + URL 查询参数为主；少量客户端状态用 React 内置 `useState` / Context | — | 官网无复杂全局状态，不引入 Redux / Zustand，减少包体 |
| 表单 | React Hook Form + Zod | 最新稳定版 | 性能好；Zod 校验规则与后端共享（monorepo 共享包） |
| 国际化 | next-intl | 最新稳定版 | 支持 App Router、`/en/` 路由前缀、服务端翻译 |
| 动效 | CSS 过渡 + IntersectionObserver；复杂场景按需引入 Motion | — | 默认零依赖；尊重 `prefers-reduced-motion` |
| 图片 | `next/image` + sharp | — | 自动输出 AVIF / WebP、响应式尺寸、懒加载 |
| 内容源 | Headless CMS（Strapi 5，见 K-05） | — | REST 拉取；发布时 Webhook 触发按需重新生成 |
| 包管理 | pnpm（workspace） | 10.x | monorepo：`apps/web`、`packages/ui`、`packages/schema` |
| 质量 | ESLint、Prettier、Stylelint、Husky + lint-staged | — | 提交前自动检查 |
| 测试 | Vitest + Testing Library（单元）；Playwright（E2E，见 K-06）；Lighthouse CI | — | 流水线门禁 |
| 监控 | web-vitals（RUM 上报到后端 `/api/v1/rum`）；Sentry（自托管）前端错误 | — | 真实用户性能数据 |
| 统计 | Umami（自托管） | — | 数据不出境、无 Cookie 弹窗负担；按需另接百度统计【待确认】 |

---

## 2. 页面 / 组件实现清单

### 2.1 目录结构

```
apps/web/
├─ app/[locale]/(site)/          # 页面路由（zh 默认无前缀，en 为 /en）
│   ├─ page.tsx                  # P-01
│   ├─ products/spatigo/...      # P-02、P-03
│   ├─ ...
├─ components/                   # 页面级区块（HeroSection、TrustBand…）
├─ lib/cms.ts                    # CMS 访问（带缓存标签）
├─ lib/api.ts                    # 业务接口（线索、下载、搜索）
packages/ui/                     # 基础组件（Button、Card、Tabs…），对应 K-01 §4
packages/schema/                 # Zod 校验与类型（前后端共享）
packages/tokens/                 # design-tokens.json → CSS 变量
```

### 2.2 页面实现表

渲染方式：**SSG** 构建时生成 · **ISR** 按需重新生成（CMS 发布触发）· **SSR** 每次请求渲染 · **CSR** 客户端

| 页面 | 渲染 | 主要组件 | 接口依赖（K-05） | 状态管理说明 |
|---|---|---|---|---|
| P-01 首页 | ISR | Header、AnnouncementBar、VideoHero、StatGroup、StandardCard、LogoWall、ProductCard、CaseTabs、ArchDiagram、IndustryTabs、ResourceCard、NewsCard、CTABand、Footer | CMS：`/home`（单例）、`/products`、`/cases?featured`、`/standards?featured`、`/news?limit=3` | 公告条关闭状态存 localStorage（7 天）；Tab 选中为组件内状态 |
| P-02 产品总览 | ISR | ArchDiagram、ProductCard | CMS `/products` | 架构图选中层为组件内状态 |
| P-03 产品详情 ×4 | ISR（`generateStaticParams`） | ProductHero、CapabilityGrid、FlowDiagram、StatGroup、Accordion（规格）、DownloadButton | CMS `/products/:slug`；规格书文件 URL | 规格展开状态写入 URL hash |
| P-04 技术架构 | ISR | ArchDiagram（交互）、TechCard | CMS `/pages/architecture` | 选中层写入 URL hash（可分享） |
| P-05 模型与部署 | ISR | RangeChart、ComparisonTable | CMS `/pages/deployment` | — |
| P-06 / P-07 解决方案 | ISR | IndustryHero、PainPoints、ArchImage、RelatedCases | CMS `/solutions`、`/solutions/:slug` | — |
| P-08 案例列表 | ISR + 客户端筛选 | FilterBar、CaseCard、Pagination、EmptyState、Skeleton | CMS `/cases`（全量 ≤ 200 条，构建时内嵌） | 筛选条件 ↔ URL 查询参数（`?industry=oil-gas&product=ops`） |
| P-09 案例详情 | ISR | CaseHero、Timeline、StatGroup、RelatedProducts | CMS `/cases/:slug` | — |
| P-10 标准与研究 | ISR | StatGroup、StandardCard、StandardTable（筛选） | CMS `/standards`、`/papers` | 筛选 ↔ URL 查询参数 |
| P-11 资源中心 | ISR | ResourceCard、FilterBar | CMS `/resources` | 同 P-08 |
| P-12 白皮书下载 | ISR + CSR 表单 | ResourceDetail、LeadForm | 业务 `POST /api/v1/downloads`、`GET /api/v1/downloads/:token` | 表单状态由 React Hook Form 管理；"30 天内已登记"标识存在 HttpOnly Cookie（服务端判定） |
| P-13 / P-14 新闻 | ISR | NewsCard、Pagination、ArticleBody（富文本渲染）、ShareBar | CMS `/news`、`/news/:slug` | 分页 ↔ URL |
| P-15 关于我们 | ISR | MissionBlock、Timeline、HonorGrid | CMS `/pages/about` | — |
| P-16 加入我们 | ISR | JobList、EmptyState | CMS `/jobs` | — |
| P-17 联系 / 预约 | SSG + CSR 表单 | LeadForm、ContactInfo、MapLink | 业务 `POST /api/v1/leads`、`GET /api/v1/captcha` | 来源页、产品预填从 URL 查询参数（`?product=ops&from=p03`）读取 |
| P-18 搜索 | SSR | SearchBox、ResultGroup、EmptyState | 业务 `GET /api/v1/search?q=` | 关键词 ↔ URL |
| P-19 404 / 500 | SSG | ErrorState | — | — |
| P-20 隐私 / 法律 | SSG | ArticleBody | CMS `/pages/privacy` | — |

### 2.3 ISR 更新机制
1. CMS 发布或更新内容 → Webhook 调用 `POST /api/revalidate`（携带签名）。
2. 前端按内容类型执行 `revalidateTag('cases')` 等，CDN 再按 `Cache-Control: s-maxage=60, stale-while-revalidate=600` 回源刷新。
3. 兜底：每个页面设 `revalidate = 3600`。

---

## 3. 性能指标与优化手段

### 3.1 达标值（移动端 P75，数据来源：RUM 上报 + Lighthouse CI）

| 指标 | 目标 | 实验室门禁（Lighthouse CI，模拟 4G 中端机） |
|---|---|---|
| LCP | ≤ 2.5 s | ≤ 2.5 s |
| INP | ≤ 200 ms | TBT ≤ 200 ms（INP 的实验室替代指标） |
| CLS | ≤ 0.1 | ≤ 0.05 |
| 首屏 JS（gzip） | ≤ 150 KB | 超出即失败 |
| Lighthouse 性能分 | — | ≥ 90 |
| Lighthouse 无障碍 / SEO / 最佳实践 | — | ≥ 95 / ≥ 95 / ≥ 95 |

### 3.2 优化手段对照表

| 指标 | 风险点 | 优化手段 |
|---|---|---|
| LCP | Hero 背景视频、超大中文字体 | LCP 元素定为 **H1 文字**或**海报图**：海报 `priority` 预加载（AVIF，≤ 120 KB）；视频在 `load` 之后再挂载，移动端和省流模式（`Save-Data`）不加载视频 |
| LCP | 中文字体体积（全量 5—10 MB） | 自托管 WOFF2；按 `unicode-range` 切片（常用 3,500 字 + 页面实际用字）；`font-display: swap`；Hero 标题字体子集单独预加载 |
| LCP | 首字节时间 | SSG / ISR + CDN 边缘缓存，HTML 命中率目标 ≥ 90%；开启 HTTP/2、Brotli |
| INP | 水合（hydration）开销 | 默认服务端组件，只有交互组件（Tabs、表单、下拉）做客户端组件；第三方脚本 `afterInteractive` / `lazyOnload` |
| INP | 长任务 | 架构图交互用 CSS 状态切换；计数动画用 `requestAnimationFrame`；避免同步布局抖动 |
| CLS | 图片、视频、Logo 墙 | 所有媒体声明宽高 / `aspect-ratio`；字体回退调整 `size-adjust`；公告条预留高度；Cookie 提示与悬浮按钮使用 `position: fixed` 浮层 |
| 体积 | 动效与图标库 | SVG Sprite 图标；不引入整包图标库；动效库按需动态导入 |
| 缓存 | 静态资源 | `/_next/static/*` 文件名带哈希，`Cache-Control: public, max-age=31536000, immutable` |

---

## 4. 兼容性矩阵

| 浏览器 / 终端 | 版本范围 | 最低支持 | 通过情况（提测时填写） |
|---|---|---|---|
| Chrome（Windows / macOS） | 最新 2 个大版本 | 完整体验 | |
| Edge（Windows） | 最新 2 个大版本 | 完整体验 | |
| Firefox（Windows / macOS） | 最新 2 个大版本 | 完整体验 | |
| Safari（macOS） | 16+ | 完整体验 | |
| iOS Safari | 16+ | 完整体验 | |
| Android Chrome | 最新 2 个大版本 | 完整体验 | |
| 微信内置浏览器 | iOS / Android 当前版本 | 完整体验（PDF 下载引导到系统浏览器） | |
| 360 极速 / QQ 浏览器 | 当前版本（Chromium 内核） | 完整体验 | |
| 其他旧版浏览器 | 不在支持范围 | 内容可读（渐进降级），不保证动效 | |

构建目标：`browserslist` = `chrome >= 109, edge >= 109, firefox >= 115, safari >= 16, ios_saf >= 16`。

---

## 5. SEO 与可访问性实现核查表

| 类别 | 核查项 | 实现方式 | 结果 |
|---|---|---|---|
| 语义化 | 每页唯一 `<h1>`，标题层级不跳级 | 组件约束 + ESLint 规则 | |
| 语义化 | `header / nav / main / section / article / footer` 地标 | 布局组件 | |
| Meta | `title`（≤ 30 汉字）、`description`（≤ 80 汉字）、`canonical` | Next.js `generateMetadata`，CMS 字段可覆盖 | |
| Meta | Open Graph、微信分享图 | `og:image` 1200×630；微信 JS-SDK 分享配置【P1】 | |
| 多语言 | `hreflang`（zh-CN / en / x-default）、`<html lang>` | next-intl + metadata `alternates` | |
| 结构化数据 | JSON-LD：Organization（首页）、Product / SoftwareApplication（P-03）、Article（P-14）、BreadcrumbList（所有二级以下页面） | 服务端注入 | |
| 收录 | `sitemap.xml`（中英分开）、`robots.txt`；百度站长平台主动推送 | 构建生成 + 发布 Webhook 推送 | |
| 可访问性 | 图片 `alt`（CMS 必填字段）；装饰图 `alt=""` | CMS 校验 | |
| 可访问性 | 键盘可达：导航、下拉、Tab、手风琴、弹窗、表单 | Radix 原语 + Playwright 键盘用例 | |
| 可访问性 | 焦点可见、"跳到主内容"链接 | 全局样式 | |
| 可访问性 | 表单 `label` 关联、错误 `aria-describedby`、`aria-live` 提示 | LeadForm 组件 | |
| 可访问性 | 视频可暂停；`prefers-reduced-motion` | VideoHero、动效工具函数 | |
| 可访问性 | 自动化检测 | axe-core（Playwright 集成），零严重违规 | |

---

## 6. 交付清单

### 6.1 构建产物
- Docker 镜像 `registry/<ns>/hyzl-web:<git-sha>`（Next.js `output: 'standalone'`，基础镜像 `node:24-alpine`，非 root 运行，镜像 ≤ 300 MB）。
- 静态资源同步上传对象存储 / CDN 源站（`/_next/static`）。
- 构建报告：包体分析（`@next/bundle-analyzer`）、Lighthouse CI 报告。

### 6.2 环境变量说明

| 变量 | 示例 | 说明 | 必填 |
|---|---|---|---|
| `NEXT_PUBLIC_SITE_URL` | `https://www.huayunzhilian.cn` | 站点根地址（canonical、sitemap） | 是 |
| `CMS_API_URL` | `http://cms:1337/api` | CMS 内网地址 | 是 |
| `CMS_API_TOKEN` | （密钥） | CMS 只读令牌，仅服务端使用 | 是 |
| `API_BASE_URL` | `http://api:3000` | 业务服务内网地址 | 是 |
| `REVALIDATE_SECRET` | （密钥） | ISR Webhook 签名密钥 | 是 |
| `NEXT_PUBLIC_UMAMI_WEBSITE_ID` | uuid | 统计站点 ID | 否 |
| `NEXT_PUBLIC_SENTRY_DSN` | url | 前端错误上报 | 否 |
| `NEXT_PUBLIC_ICP_NO` / `NEXT_PUBLIC_PSB_NO` | 陕 ICP 备 XXXX 号 | 页脚备案信息 | 是 |

> 密钥由 K-07 的密钥管理统一注入，禁止写入镜像或仓库。

### 6.3 部署说明（与 K-07 衔接）
1. 合并到 `main` → CI 依次执行 lint、单元测试、构建、Lighthouse CI、Playwright 冒烟。
2. 推送镜像 → 部署测试环境 → K-06 回归 → 打 tag → 生产灰度（K-07 §1）。
3. 健康检查端点：`GET /api/health`（返回版本号与 CMS 连通性）。
4. 回滚：重新部署上一个镜像 tag，并执行全量 `revalidate`。
