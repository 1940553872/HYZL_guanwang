# ADR-0001：技术栈与版本

- 状态：已采纳（2026-10-08）
- 关联：K-04 §1、K-05 §1

## 背景

v0.2 设计文档确定使用 Nuxt（Vue 3）+ Spring Boot + PostgreSQL，以便公司现有前端（Vue）和后端（Java Spring）团队接手维护。K-05 写的是"Spring Boot 3.x、MyBatis-Plus"。开发开始时（2026-10）：

- Spring Boot 4.1 已是当前稳定版。
- 3.x 系列已进入维护末期。
- Spring Boot 4 默认使用 Jackson 3。

## 决策

| 层 | 选型与版本 | 理由 |
|---|---|---|
| 前端框架 | Nuxt 4.6 / Vue 3.5 | 与 K-04 一致 |
| 样式 | Tailwind CSS 4.3（`@theme` 承载设计 Token） | Token 与 design-tokens.json 一一对应，组件内直接使用 |
| 无障碍组件 | reka-ui 2.11（Dialog、Tabs） | 免费、无样式、符合 WAI-ARIA，可完全套用品牌样式 |
| 表单校验 | zod 4 | 规则与后端 Bean Validation 保持一致，便于单元测试 |
| 后端框架 | **Spring Boot 4.1**（Java 21） | 在维护周期内的最新稳定版，避免上线即需升级大版本 |
| 数据访问 | Spring `JdbcClient` + Flyway | 表少（5 张）且 SQL 简单，不引入 MyBatis-Plus。团队如需，可平滑加入 |
| 数据库 | PostgreSQL 16（生产）/ H2 PostgreSQL 模式（本地） | 本地零安装即可演示；集成测试已在 PostgreSQL 16 上跑通 |
| 加密 | BouncyCastle 1.86（SM4-GCM）+ HMAC-SHA256 | K-05 §5 国密要求 |
| 接口文档 | springdoc-openapi 3 | 生成 Swagger UI，供前端与测试联调 |
| 测试 | JUnit 5 + MockMvc、Vitest 5、Playwright 1.56 | 覆盖 K-06 的单元、接口、端到端三层 |

## 影响

- 文档中的 "Spring Boot 3.x" 应理解为 "Spring Boot 4.x"。K-05 下次修订时同步。
- 选择 JdbcClient 意味着动态 SQL 手写。凡是可选参数为 NULL 的写法，都须同时兼容 H2 与 PostgreSQL（例如 `CAST(:p AS VARCHAR) IS NULL`）。这一点已由在 PostgreSQL 上运行的集成测试覆盖。
