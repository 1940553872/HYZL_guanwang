# 华云智联官网 V2.0：代码

依据 [design_document/](../design_document/README.md)（v0.2）和 [素材库/](../素材库/) 实现的公司官网，包括前端网站、内容与业务服务、内容生成工具、测试和本地一键启停脚本。

> **本地运行**：`./start.sh` → 打开 http://localhost:3000 → `./stop.sh`。
> **只看演示效果**：用静态演示包 `hyzl-website-demo.zip`（`./tools/build-demo.sh` 生成），解压后双击 `open-demo.bat`，无需 Java 与构建。
> **Windows**：双击 `start.bat` / `stop.bat`，或在 PowerShell 中运行 `.\start.bat` / `.\stop.bat`（不要运行 `./start.sh`）。
> 详细说明见 **[docs/本地部署说明.md](./docs/本地部署说明.md)**。

## 目录结构

```text
website/
├── apps/
│   ├── web/                 前端网站 hyzl-web（Nuxt 4 + Vue 3 + Tailwind CSS 4，SSR）—— K-04
│   │   ├── app/pages/       28 个页面文件（P-01 … P-92）
│   │   ├── app/components/  ui/ 基础组件 · layout/ 页头页脚 · sections/ 业务区块
│   │   ├── server/          接口代理、健康检查、sitemap.xml、robots.txt
│   │   ├── public/media/    由素材库生成的 WebP 图片（证书类带水印）
│   │   └── tests/           unit/（Vitest）· e2e/（Playwright）
│   └── api/                 内容与业务服务 hyzl-api（Spring Boot 4 + Java 21）—— K-05
│       ├── src/main/java/…  content 内容 · lead 留资 · search 搜索 · rum 性能上报 · admin 线索管理
│       ├── src/main/resources/db/migration/  Flyway 表结构
│       └── src/main/resources/seed/          内容种子（238 条，由 tools 生成）
├── tools/                   素材库 → seed JSON + WebP 图片 的内容生成脚本（Python）
├── docs/                    部署说明、架构、ADR、测试报告、内容待办
├── hyzl.sh / hyzl.ps1       一键启停脚本（start / stop / restart / status / logs）
└── start.sh / stop.sh / start.bat / stop.bat
```

## 页面清单（与 K-02 §2.1 编号一致）

| 编号 | 页面 | 路由 |
|---|---|---|
| P-01 | 首页 | `/` |
| P-20 | 平台总览（7+10+2+N） | `/products` |
| P-21 | 空间群弈™ SpatiGo™ 及 4 个子产品 | `/products/spatigo`、`/products/spatigo/{quality,maintenance,safety,embodied}` |
| P-22 | 工业增强大模型 iMLLM | `/products/imllm` |
| P-23 | 工业智能体应用（7 个） | `/products/agents`、`/products/agents/<slug>` |
| P-24 | 智能引擎群（7 个） | `/products/engines#<code>` |
| P-25 | 工业软件（17 款） | `/products/software`、`/products/software/<slug>` |
| P-26 | 安全与集成 | `/products/security-integration` |
| P-30 / P-31 | 解决方案总览 / 6 个行业方案 | `/solutions`、`/solutions/<slug>` |
| P-40 / P-41 | 客户案例列表 / 详情 | `/cases`、`/cases/<slug>` |
| P-50 / P-51 | 标准与研究 / 联合实验室 | `/research`、`/research/labs` |
| P-60 | 服务支持 | `/support` |
| P-70 / P-71 / P-73 / P-74 / P-75 | 公司介绍 / 资质荣誉 / 合作伙伴 / 联系我们 / 加入我们 | `/about/*` |
| P-72 | 预约现场演示 | `/demo` |
| P-80 / P-81 | 新闻列表 / 详情 | `/news`、`/news/<yyyy>/<slug>` |
| P-90 / P-91 / P-92 | 搜索 / 404·500 / 隐私政策 | `/search`、错误页、`/legal/privacy` |

旧站 `index.html`、`product.html`、`news.html`、`lab.html`、`service.html`、`about.html` 均 301 跳转到新地址。

## 开发流程与文档

| 阶段 | 产出 |
|---|---|
| 需求与设计 | [design_document/](../design_document/README.md)：IA、视觉 Token、组件、接口、测试与运维方案 |
| 架构与决策 | [docs/architecture.md](./docs/architecture.md) · [ADR-0001 技术栈](./docs/adr/0001-tech-stack.md) · [ADR-0002 内容模型](./docs/adr/0002-content-model.md) · [ADR-0003 本期范围](./docs/adr/0003-deferred-scope.md) |
| 内容迁移 | `tools/build_content.py`：解析素材库 → 勘误修正 → seed JSON + WebP；[docs/CONTENT_TODO.md](./docs/CONTENT_TODO.md) 列出上线前需业务确认的内容 |
| 实现 | `apps/web`、`apps/api` |
| 测试 | [docs/test-report.md](./docs/test-report.md)：后端 14 项、前端单元 12 项、端到端 70 项全部通过 |
| 部署 | [docs/本地部署说明.md](./docs/本地部署说明.md) |

## 常用命令

```bash
./hyzl.sh start [--rebuild] | stop | restart | status | logs [api|web]
cd apps/api && ./mvnw test                  # 后端测试
cd apps/web && npm test && npx playwright test   # 前端单元 + 端到端（需站点已启动）
python3 tools/build_content.py              # 素材库变更后重新生成内容
```
