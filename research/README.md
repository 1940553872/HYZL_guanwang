# HYZL 官网设计调研：AI 与工业软件头部企业

> 调研日期：2026-10-08
> 目的：为 HYZL 官网界面设计提供参考，覆盖国内外**人工智能**与**工业软件**头部企业官网的设计风格、设计元素、交互方式与呈现内容。

## 文档目录

| # | 文档 | 内容 | 对应任务 |
|---|---|---|---|
| 01 | [AI 头部企业官网设计风格与元素](./01-ai-companies-design.md) | 国外 12 家、国内 11 家 AI 企业逐家拆解；风格流派、色彩、字体、配图、组件、动效归纳；国内外对比 | 任务 1 |
| 02 | [工业软件头部企业官网设计风格与元素](./02-industrial-software-design.md) | 国外 10 家（另附 2 家自动化巨头作参照）、国内 12 家工业软件企业拆解；行业视觉母题；国内外对比 | 任务 1 |
| 03 | [官网交互与呈现内容汇总（索引 · 配图 · 设计 · 文案）](./03-interaction-and-content.md) | 导航与信息架构对比、首页区块编排、配图语言、组件与交互模式、文案（主张 / 句式 / CTA / 语气） | 任务 2 |
| 04 | [对 HYZL 官网的设计启示](./04-implications-for-hyzl.md) | 视觉方向提案、推荐信息架构、首页线框、配图 / 文案 / 交互规范、下一步 | 综合建议 |
| — | [data/companies.csv](./data/companies.csv) | 结构化对比表（43 条企业记录：风格、色彩、字体、首屏、导航、配图、文案、可信度），可直接用 Excel 打开 | 数据 |
| — | [sources.md](./sources.md) | 全部参考来源链接 | 出处 |

## 调研方法与可信度说明

| 标注 | 含义 |
|---|---|
| **【实测】** | 本次直接抓取官网 HTML 并解析所得（Anthropic、Microsoft AI） |
| **【公开】** | 来自官方品牌手册、官方新闻稿、设计机构案例或权威媒体报道（见 sources.md） |
| **【公开·第三方】** | 来自第三方对官网代码的逆向"设计系统"拆解，色值和字体为推测值，仅供参考 |
| **【观察】** | 基于 2025—2026 年对官网公开页面的观察归纳，本次未能实时复核 |
| **【待核验】** | 信息不足，需访问官网确认 |

**限制说明**：本次调研运行在云端环境中，其网络策略只允许访问少数域名，绝大多数企业官网（openai.com、baidu.com、siemens.com、zwsoft.cn 等）无法直接打开，因此**无法截图**，也无法逐一实测色值和导航。结论以公开资料检索和既有观察为主。官网改版频繁，正式设计前建议按下方核验清单截图确认。

## 核验清单

建议对以下官网首页各截取 **桌面端 1440px** 与 **移动端 390px** 两张全页截图，存入 `research/screenshots/<企业>/`，并核对导航、首屏文案、主色值：

**AI（国外）**：openai.com · anthropic.com · deepmind.google · microsoft.com/ai · nvidia.com · ai.meta.com · mistral.ai · x.ai · perplexity.ai · cohere.com · huggingface.co · runwayml.com
**AI（国内）**：cloud.baidu.com · aliyun.com · cloud.tencent.com · huaweicloud.com · volcengine.com · iflytek.com · sensetime.com · zhipuai.cn / bigmodel.cn / z.ai · kimi.com · deepseek.com · minimaxi.com
**工业软件（国外）**：sw.siemens.com · 3ds.com · autodesk.com · ptc.com · ansys.com · synopsys.com · cadence.com · hexagon.com / octave.com · aveva.com · bentley.com · se.com · rockwellautomation.com
**工业软件（国内）**：zwsoft.cn · empyrean.com.cn · glodon.com · supcon.com · baosight.com · yonyou.com · kingdee.com · gstarcad.com · caxa.com · rootcloud.com · cosmoplat.com

## 核心结论速览

1. **AI 头部**：国外在"去科技化"——暖色、衬线、手绘、自然隐喻、极简黑白，主动避开"科技蓝"；国内大厂官网本质是"云产品商城"，AI 创业公司（DeepSeek、Kimi、MiniMax）向极简和品牌手册化靠拢。
2. **工业软件头部**：核心是"可信度"。"数字孪生（虚实融合）"是最强视觉母题；国外巨头用世界观叙事、差异化品牌色和专属字体建立高级感，国内企业普遍是蓝色科技风加能力罗列，差异化不足。
3. **交互与内容**：AI 走"极简导航 + 独立产品站 + 发布卡片流"，工业软件走"Mega Menu + 行业索引 + 量化案例 + 资源中心"；两者正在"工业 AI / 智能体 / 世界模型"叙事上交汇。
4. **对 HYZL 的建议**：AI 头部的克制与温度做气质，工业软件的证据与场景做骨架；理性工业极简为主基调，深色数字孪生用于首屏和专题，选一个非蓝强调色建立辨识度。
