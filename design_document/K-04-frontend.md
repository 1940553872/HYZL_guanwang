# K-04 前端开发工程师：页面实现与性能

> 组别：K-B 网站开发类 ｜ 版本 v0.2 ｜ 2026-10-08
> 输入变量：
> - **{设计稿/需求}**：K-01 设计规范与视觉稿、K-02 信息架构与交互、[02](./02-content-and-layout.md)、[03](./03-content-and-asset-migration.md)
> - **{技术栈约束}**：①SEO 友好（服务端渲染 / 预渲染）；②中国内地部署，不依赖境外 CDN 与字体服务；③**与公司现有团队技能一致**：招聘要求 Web 前端"精通 Vue / React / Angular 之一"，公司产品采用"H5 + Vue"；④容器化交付
> - **{性能目标}**：移动端 P75：LCP ≤ 2.5 s、INP ≤ 200 ms、CLS ≤ 0.1
> v0.2 变更：框架由 Next.js 改为 **Nuxt（Vue 3）**，以便公司前端团队接手维护；接口改为对接自建 Spring Boot 内容服务（K-05）；页面清单按新编号更新。

---

## 1. 技术选型表

| 类别 | 选型 | 版本（立项时锁定最新稳定小版本） | 选型理由 |
|---|---|---|---|
| 运行时 | Node.js | 22 LTS 或 24 LTS | Nuxt SSR 运行环境 |
| 框架 | Nuxt | 4.x | Vue 3 生态的 SSR / 预渲染框架；混合渲染（`routeRules`）可按页面选择预渲染、SWR 缓存或 SSR；与公司"H5 + Vue"技术栈一致，降低维护成本 |
| UI 运行时 | Vue | 3.5.x | Nuxt 配套 |
| 语言 | TypeScript | 5.x（strict） | 类型安全；由 K-05 的 OpenAPI 生成接口类型 |
| 样式 | Tailwind CSS | 4.x | Token 映射为 CSS 变量（`@theme`），与 K-01 同源 |
| 无障碍交互原语 | Reka UI（原 Radix Vue） | 2.x | 下拉、Tab、手风琴、弹窗、灯箱自带键盘与 ARIA 支持；样式完全自定义 |
| 状态管理 | Nuxt `useState` + URL 查询参数 | — | 官网无复杂全局状态，不引入 Pinia |
| 表单 | VeeValidate + Zod | 4.x / 3.x | 校验规则由 OpenAPI 定义同步生成，前后端一致 |
| 国际化 | @nuxtjs/i18n | 最新稳定版 | `/en/` 前缀策略、hreflang 自动生成 |
| 图片 | @nuxt/image + IPX（sharp，自托管） | 最新稳定版 | AVIF / WebP / JPEG、响应式尺寸、懒加载；不依赖第三方图片服务 |
| SEO | @nuxtjs/sitemap、nuxt-schema-org | 最新稳定版 | sitemap、JSON-LD |
| 动效 | CSS 过渡 + IntersectionObserver；架构图用原生 SVG | — | 零依赖；尊重 `prefers-reduced-motion` |
| 包管理 | pnpm（workspace） | 10.x | monorepo：`apps/web`、`apps/admin`（后台前端，见 K-05）、`packages/ui`、`packages/tokens`、`packages/api-types` |
| 质量 | ESLint（@nuxt/eslint）、Prettier、Stylelint、Husky + lint-staged | — | 提交前检查 |
| 测试 | Vitest + @nuxt/test-utils（单元 / 组件）；Playwright（E2E，见 K-06）；Lighthouse CI | — | 流水线门禁 |
| 监控 | web-vitals → `/api/v1/rum`；Sentry（自托管）前端错误 | — | 真实用户性能 |
| 统计 | Umami（自托管）【可选再接百度统计】 | — | 数据不出境 |

> 备选：若团队更熟悉 React，可换 Next.js，页面、组件、性能方案不变（见 v0.1）。

---

## 2. 页面 / 组件实现清单

### 2.1 目录结构

```
apps/web/
├─ app/pages/                     # 文件路由（中文默认无前缀，英文 /en）
│   ├─ index.vue                  # P-01
│   ├─ products/index.vue         # P-20
│   ├─ products/spatigo/[[sub]].vue        # P-21 总览与 4 子页
│   ├─ products/agents/[slug].vue          # P-23
│   ├─ products/software/[slug].vue        # P-25
│   └─ …
├─ app/components/sections/       # 页面区块（HeroSection、PainCards、ArchDiagram…）
├─ app/composables/useContent.ts  # 内容接口（带缓存键）
├─ server/api/revalidate.post.ts  # 内容发布后清缓存
packages/ui/                      # 基础组件（K-01 §4）
packages/tokens/                  # design-tokens.json → CSS 变量
packages/api-types/               # 由 K-05 OpenAPI 生成的类型与 Zod schema
```

### 2.2 渲染策略

渲染：**预渲染**（构建时生成）· **SWR**（服务端缓存，过期后后台刷新，可按键清除）· **SSR**（每次请求）· **CSR**（客户端）

| 页面 | 渲染 | 主要组件 | 接口依赖（K-05 §2） | 状态管理说明 |
|---|---|---|---|---|
| P-01 首页 | SWR 3600s | TopBar、Header、AnnouncementBar、Hero、ArchMotion、StatGroup、LogoWall、CommitteeBadges、PainCards、ArchDiagram、CaseTabs、DeployCards、IndustryTabs、StandardCards、CertCarousel、NewsCards（条件渲染）、CTABand、Footer、FloatingCTA | `GET /content/pages/home`、`/content/customers?authorized=true`、`/content/products?featured=true`、`/content/cases?featured=true`、`/content/standards?featured=true`、`/content/certificates`、`/content/news?limit=3&within=365` | 公告关闭状态 localStorage（7 天）；新闻区：接口返回 < 3 条时不渲染 |
| P-20 平台总览 | SWR | ArchDiagram（交互）、TechCards、DeployCards | `/content/pages/platform`、`/content/products?type=platform,model` | 选中层写入 URL hash |
| P-21 SpatiGo™ 与 4 子页 | SWR | ProductHero、PainList、CapabilityGrid、FlowDiagram、StatGroup、RelatedCases、Accordion、DownloadButton | `/content/products/spatigo`、`/content/products/{slug}` | 规格展开写入 hash |
| P-22 iMLLM | SWR | 同上 | `/content/products/imllm` | — |
| P-23 智能体（列表 + 7 详情） | SWR | ProductCard、ProductDetail | `/content/products?type=agent`、`/content/products/{slug}` | — |
| P-24 引擎群 | SWR | AnchorNav、EngineSection×7 | `/content/products?type=engine` | 锚点吸顶 |
| P-25 工业软件（列表 + 约 17 详情） | SWR | 列表分"标准软件 / 先进软件"两组；ProductDetail + Lightbox（产品截图） | `/content/products?type=software` | — |
| P-26 安全与集成 | 预渲染 | DataTable（协议矩阵）、SecurityCards | `/content/pages/security-integration` | — |
| P-30 / P-31 解决方案 | SWR | IndustryHero、PainList、ProductBundle、RelatedCases | `/content/solutions`、`/content/solutions/{slug}` | — |
| P-40 案例列表 | SWR + 客户端筛选 | FilterBar、CaseCard、Pagination、EmptyState、Skeleton | `/content/cases`（≤ 200 条全量返回） | 筛选 ↔ URL 查询参数 |
| P-41 案例详情 | SWR | CaseHero、Timeline、StatGroup、RelatedProducts | `/content/cases/{slug}` | — |
| P-50 标准与研究 | SWR + 客户端筛选 | CommitteeBadges、StandardCards、DataTable×4、Lightbox | `/content/standards`、`/content/patents`、`/content/copyrights`、`/content/projects` | 表格筛选与编号搜索 ↔ URL |
| P-51 联合实验室 | 预渲染 | LabSection×3 | `/content/labs` | — |
| P-60 服务支持 | SWR | ServiceHotline、StepsDiagram、ResourceCards | `/content/pages/support`、`/content/resources` | — |
| P-61 资料下载 | SWR + CSR 表单 | ResourceDetail、LeadForm | `POST /api/v1/downloads`、`GET /api/v1/downloads/status` | 已登记状态由服务端 HttpOnly Cookie 判定 |
| P-70 公司介绍 | SWR | MissionBlock、Timeline、PhotoGrid、MediaBlock（自托管视频） | `/content/pages/about`、`/content/milestones` | — |
| P-71 资质荣誉 | SWR | CertCard（有效期状态）、AwardCard、Lightbox | `/content/certificates`、`/content/awards` | 证书状态由接口返回（有效 / 60 天内到期 / 已过期——过期不返回） |
| P-72 预约演示 | 预渲染 + CSR 表单 | LeadForm、TrustAside | `POST /api/v1/leads` | 产品、来源页从查询参数预填（`?product=spatigo-maintenance&from=p21`） |
| P-73 合作伙伴 | SWR | LogoWall（4 组） | `/content/partners` | — |
| P-74 联系我们 | 预渲染 | ContactCard、MapLink、QRCode | `/content/pages/contact` | — |
| P-75 加入我们 | SWR | JobAccordion、EmptyState | `/content/jobs` | — |
| P-80 / P-81 新闻 | SWR | NewsCard、Pagination、ArticleBody、ShareBar、"历史动态"标签 | `/content/news`、`/content/news/{slug}` | 分页 ↔ URL |
| P-90 搜索 | SSR | SearchBox、ResultGroup、EmptyState | `GET /api/v1/search?q=` | 关键词 ↔ URL |
| P-91 404 / 500 | 预渲染 | ErrorState | — | — |
| P-92 法律页 | 预渲染 | ArticleBody | `/content/pages/privacy` 等 | — |

### 2.3 缓存刷新机制
1. 内容后台发布 → K-05 调用前端 `POST /api/revalidate`（HMAC 签名），携带受影响的路由与缓存键。
2. Nitro 删除对应 SWR 缓存（缓存存储使用 Redis 驱动，多副本共享），并请求 CDN 刷新这些 URL。
3. 兜底：SWR 过期时间 3600 秒；预渲染页面随版本构建更新。

### 2.4 旧站兼容
- Nitro `routeRules` 配置旧 URL 301（03 §5）：`/index.html → /`、`/product.html → /products` 等。
- 首页强制极速内核：`<meta name="renderer" content="webkit">`、`<meta http-equiv="X-UA-Compatible" content="IE=edge">`。

---

## 3. 性能指标与优化手段

### 3.1 达标值（移动端 P75；数据源：RUM + Lighthouse CI）

| 指标 | 目标 | 实验室门禁（Lighthouse CI，模拟 4G 中端机，3 次取中位数） |
|---|---|---|
| LCP | ≤ 2.5 s | ≤ 2.5 s |
| INP | ≤ 200 ms | TBT ≤ 200 ms |
| CLS | ≤ 0.1 | ≤ 0.05 |
| 首屏 JS（gzip） | ≤ 150 KB | 超出即失败 |
| Lighthouse 性能 / 无障碍 / SEO / 最佳实践 | — | ≥ 90 / ≥ 95 / ≥ 95 / ≥ 95 |

### 3.2 优化手段对照表

| 指标 | 风险点 | 优化手段 |
|---|---|---|
| LCP | 首屏 H1 使用中文字体、Hero 媒体 | LCP 元素定为 H1 文字：H1 用字（约 20 字）单独子集化并预加载（< 20 KB）；Hero 动效为内联 SVG（< 30 KB），视频只在 `load` 后、非移动端、非省流模式挂载 |
| LCP | 中文字体全量体积 5—10 MB | 自托管 WOFF2，按 `unicode-range` 切片（常用 3,500 字 + 全站实际用字）；`font-display: swap`；回退字体 `size-adjust` 对齐，防跳动 |
| LCP | 首字节时间 | SWR + CDN 边缘缓存，HTML 命中率 ≥ 90%；HTTP/2、Brotli |
| INP | 水合开销 | 静态区块用 `<NuxtIsland>` / 惰性水合（`hydrate-on-visible`），只有 Tab、表单、下拉、灯箱、架构图在可见时水合；第三方脚本延迟加载 |
| INP | 数据表筛选（标准 30、软著 28 条等） | 数据量小，客户端筛选；输入防抖 150ms |
| CLS | 图片、证书缩略图、Logo 墙、公告条 | 所有媒体声明宽高 / `aspect-ratio`；公告条预留高度；悬浮咨询与 Cookie 提示用固定定位浮层 |
| 体积 | 图标、产品截图 | SVG Sprite；产品截图（约 1270×600）输出 AVIF ≤ 120 KB，灯箱再加载原图 |
| 缓存 | 静态资源 | `/_nuxt/*` 文件名带哈希：`Cache-Control: public, max-age=31536000, immutable` |

---

## 4. 兼容性矩阵

| 浏览器 / 终端 | 版本范围 | 支持级别 | 通过情况（提测时填写） |
|---|---|---|---|
| Chrome（Windows / macOS） | 最新 2 个大版本 | 完整 | |
| Edge（Windows） | 最新 2 个大版本 | 完整 | |
| Firefox | 最新 2 个大版本 | 完整 | |
| Safari（macOS） | 16+ | 完整 | |
| iOS Safari | 16+ | 完整 | |
| Android Chrome | 最新 2 个大版本 | 完整 | |
| 微信内置浏览器 | iOS / Android 当前版本 | 完整（下载引导到系统浏览器） | |
| 360 极速 / QQ 浏览器 | 当前版本（Chromium 内核，强制极速模式） | 完整 | |
| 其他旧浏览器 | 不支持 | 内容可读（渐进降级） | |

`browserslist`：`chrome >= 109, edge >= 109, firefox >= 115, safari >= 16, ios_saf >= 16`。

---

## 5. SEO 与可访问性实现核查表

| 类别 | 核查项 | 实现 | 结果 |
|---|---|---|---|
| URL | 每个产品、案例、标准页面独立 URL（纠正现网单 URL 问题）；slug 用英文 | 文件路由 + K-02 §2.1 | |
| 语义化 | 每页唯一 `<h1>`；`header / nav / main / section / article / footer` | 布局组件 + ESLint 规则 | |
| 文字不入图 | 所有文案为 HTML 文本 | 组件约束 + K-03 W-042 | |
| Meta | `title`（≤ 30 汉字，格式"页面名｜华云智联"）、`description`（≤ 80 汉字）、`canonical` | `useSeoMeta`，后台字段可覆盖 | |
| 分享 | Open Graph、微信分享图 | `og:image` 1200×630；微信 JS-SDK【P1】 | |
| 多语言 | `hreflang`（zh-CN / en / x-default）、`<html lang>` | @nuxtjs/i18n | |
| 结构化数据 | Organization（含 logo、联系电话）、SoftwareApplication（P-21 / P-23 / P-25）、Article（P-81）、BreadcrumbList | nuxt-schema-org | |
| 收录 | `sitemap.xml`（中英分开）、`robots.txt`；百度站长平台与必应站长主动推送 | 构建生成 + 发布时推送 | |
| 旧链接 | 旧 URL 301（03 §5） | `routeRules` | |
| 可访问性 | 图片 `alt` 为后台必填；装饰图 `alt=""` | 后台校验 | |
| 可访问性 | 键盘可达：导航、下拉、Tab、手风琴、灯箱、表单 | Reka UI + Playwright 键盘用例 | |
| 可访问性 | 焦点可见、"跳到主内容"、表单 `aria-describedby` 与 `aria-live` | 全局样式、LeadForm | |
| 可访问性 | 视频可暂停；`prefers-reduced-motion` | MediaBlock、动效工具函数 | |
| 自动化 | axe-core 零严重违规 | Playwright 集成 | |

---

## 6. 交付清单

### 6.1 构建产物
- Docker 镜像 `registry/<ns>/hyzl-web:<git-sha>`（Nuxt `node-server` 预设，基础镜像 `node:22-alpine`，非 root 运行，≤ 300 MB）。
- 静态资源上传对象存储作为 CDN 源站（`/_nuxt/*`）。
- 构建报告：包体分析（`nuxi analyze`）、Lighthouse CI 报告。

### 6.2 环境变量

| 变量 | 示例 | 说明 | 必填 |
|---|---|---|---|
| `NUXT_PUBLIC_SITE_URL` | `https://www.huayunzhilian.cn` | 站点根地址（canonical、sitemap） | 是 |
| `NUXT_API_BASE` | `http://hyzl-api:8080` | 内容与业务服务内网地址（仅服务端使用） | 是 |
| `NUXT_PUBLIC_API_BASE` | `/api` | 浏览器端接口前缀（经网关） | 是 |
| `NUXT_REVALIDATE_SECRET` | （密钥） | 缓存刷新签名密钥 | 是 |
| `NUXT_REDIS_URL` | `redis://…` | SWR 缓存存储 | 是 |
| `NUXT_PUBLIC_ICP_NO` | 陕ICP备2026024028号-1 | 页脚备案号 | 是 |
| `NUXT_PUBLIC_PSB_NO` | 【待办理】 | 公安联网备案号 | 是 |
| `NUXT_PUBLIC_HOTLINE` | 029-88810623 | 7×24 热线 | 是 |
| `NUXT_PUBLIC_UMAMI_ID` / `NUXT_PUBLIC_SENTRY_DSN` | — | 统计与错误上报 | 否 |

> 密钥由 K-07 统一注入，禁止写入镜像或仓库。

### 6.3 部署说明（与 K-07 衔接）
1. 合并到 `main` → CI：lint → 单元测试 → 构建 → Lighthouse CI → Playwright 冒烟。
2. 推送镜像 → 测试环境 → K-06 回归 → 打 tag → 生产灰度（K-07 §1）。
3. 健康检查：`GET /api/health`（返回版本号与内容服务连通性）。
4. 回滚：部署上一镜像 tag 并清空 SWR 缓存。
