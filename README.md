# HYZL_guanwang
设计公司官网界面

## 设计调研

- [research/](./research/README.md)：国内外人工智能与工业软件头部企业的官网设计调研
  - [01 AI 头部企业官网设计风格与元素](./research/01-ai-companies-design.md)
  - [02 工业软件头部企业官网设计风格与元素](./research/02-industrial-software-design.md)
  - [03 官网交互与呈现内容汇总（索引 · 配图 · 设计 · 文案）](./research/03-interaction-and-content.md)
  - [04 对 HYZL 官网的设计启示](./research/04-implications-for-hyzl.md)
  - [05 华云智联官网对标分析（用户提供）](./research/05-huayunzhilian-benchmark.md)
  - [结构化对比表 companies.csv](./research/data/companies.csv) ｜ [参考来源](./research/sources.md)

## 设计与开发前文档（华云智联官网 V2.0）

- [design_document/](./design_document/README.md)：项目基线、里程碑、待确认事项（v0.2）
  - [01 现网盘点与问题诊断](./design_document/01-current-site-audit.md) ｜ [02 内容呈现方式与整体布局风格](./design_document/02-content-and-layout.md) ｜ [03 内容与素材迁移方案](./design_document/03-content-and-asset-migration.md)
  - K-A 设计：[K-01 UI/视觉](./design_document/K-01-ui-visual-design.md) ｜ [K-02 UX/信息架构](./design_document/K-02-ux-ia-usability.md) ｜ [K-03 设计走查](./design_document/K-03-design-qa-acceptance.md)
  - K-B 开发：[K-04 前端](./design_document/K-04-frontend.md) ｜ [K-05 后端](./design_document/K-05-backend.md) ｜ [K-06 测试](./design_document/K-06-testing.md)
  - K-C 运维：[K-07 SRE](./design_document/K-07-sre.md)
  - [K 类驱动板（5W2H + SMART + SAO）](./design_document/K-drive-board.md) ｜ [设计 Token](./design_document/assets/design-tokens.json) ｜ [素材映射表](./design_document/assets/asset-mapping.csv)
  - [输入资料](./design_document/inputs/)：华云智联网站内容与元素整理（docx）、国内外 AI 与工业软件头部企业官网设计调研

## 官网代码（华云智联官网 V2.0）

- [website/](./website/README.md)：Nuxt 4 前端 + Spring Boot 4 内容服务，覆盖 K-02 全部 P0 页面
  - **本地运行**：`cd website && ./start.sh`，打开 http://localhost:3000，`./stop.sh` 停止；Windows 双击 `start.bat` / `stop.bat`，或在 PowerShell 中运行 `.\start.bat`
  - [本地部署说明](./website/docs/本地部署说明.md) ｜ [架构说明](./website/docs/architecture.md) ｜ [ADR](./website/docs/adr/) ｜ [测试报告](./website/docs/test-report.md) ｜ [内容待办](./website/docs/CONTENT_TODO.md)

## 素材库

- [素材库/](./素材库/)：现网原图 277 张、页面截图 58 张、官网补录文字、图片文字识别、素材索引
