# skills-doctor 产品文档

## 1. 产品定位

`skills-doctor` 是一个辅助 AI 进行本地 skills 检查的 skill。

它本身以 skill 形态存在，被 Codex、Cursor、Claude Code 或其他兼容 Agent 触发后，辅助 AI 扫描和分析本地 skills，检查 skills 的安装位置、结构质量、触发边界、token 成本、冲突风险、安全风险和可维护性，最终按照最佳实践生成一份本地 HTML 检查报告。

目标支持的 AI 工具和模型生态包括：

- 海外 Agent 工具：Codex、Cursor、Claude Code 等。
- 国内模型 / Agent 工具：千问、GLM、DeepSeek、Kimi 等。
- 自定义本地 Agent、团队内部 AI 工具、插件化 agent runtime。

产品核心不是“再创建一个 skill”，也不是自动修复平台，而是为 AI 提供一套稳定、收敛、可复现的本地 skills 检查流程，并把检查结果沉淀为便于用户阅读和后续处理的 HTML 报告。

同时，`skills-doctor` 的触发范围必须保持收敛：它只应在用户明确表达“体检、检查、审计、诊断本地 skills 问题”时触发，不应因为普通提到 `skills`、创建 skill、安装 skill、查找 skill、学习 skill 写法等泛化关键词而触发。

## 2. 背景与痛点

随着大模型、AI IDE、Agent Runtime 和本地自动化工具的发展，用户本地会逐渐积累大量 skills、rules、prompts、plugins、MCP 配置和工具脚本。这些能力通常来源不同、格式不同、安装位置不同，长期维护成本会持续上升。

核心痛点包括：

- 安装位置分散：skills 可能散落在 `~/.codex/skills`、`~/.claude/skills`、项目级 `.codex/skills`、`.claude/skills`、Cursor 配置、插件缓存、团队共享目录等位置。
- 缺少统一索引：用户很难知道本地到底安装了哪些 skills、由谁触发、适用于什么场景、是否仍然有效。
- 多 skill 互相影响：多个设计类、代码审查类、规划类、文档类 skill 可能触发范围重叠，导致 Agent 注意力分散、行为冲突或输出风格不稳定。
- token 消耗不可控：过长的 `SKILL.md`、冗余 examples、内联大段参考资料、重复规则会增加上下文成本，降低 Agent 响应效率。
- skill 设计反模式：描述过宽、触发不精准、过度流程化、硬编码路径、隐藏网络调用、危险命令、敏感信息示例等都会影响安全性和可靠性。
- 跨工具迁移困难：Codex、Claude Code、Cursor 以及国内 Agent 工具对 skill 的发现、触发和上下文加载机制不同，缺少统一的兼容性评估。
- 检查结果难沉淀：即使 AI 在对话中发现问题，结果也容易散落在聊天上下文里，缺少一份结构化、可归档、可复查的本地报告。

## 3. 目标用户

主要用户：

- 高频使用 Codex、Claude Code、Cursor 等 AI 编程工具的开发者。
- 维护个人 AI 工作流和本地 skill 库的高级用户。
- 负责团队 AI 工具规范、prompt/skill 治理和安全审计的技术负责人。
- 构建内部 Agent 平台、插件市场或 AI 辅助研发体系的团队。

次要用户：

- 需要评估第三方 skill 包质量的用户。
- 需要将海外 AI 工具体系中的 skills 迁移到国内模型或工具链的团队。
- 希望减少 token 成本、提高 Agent 稳定性的个人或组织。

## 4. 产品目标

### 4.1 当前阶段目标

- 自动扫描本地常见 skill 安装位置。
- 识别 skills 的结构、元数据、触发描述、文件大小、引用资源、脚本和潜在风险。
- 借助 AI 对 skill 内容进行质量分析。
- 按最佳实践生成一份本地 HTML 检查报告。
- 在报告中给出问题证据、影响说明和后续处理建议，但不直接执行修复。

### 4.2 下一阶段目标

- 增强不同 Agent skill 目录和规则格式的识别能力。
- 增强 HTML 报告的可读性、可筛选性和可归档性。
- 增强问题分类、证据定位、风险分级和建议质量。
- 建立跨 Agent 的检查适配层，让同一套检查流程可被 Codex、Cursor、Claude Code、千问、GLM、DeepSeek、Kimi 等触发。

### 4.3 触发机制目标

`skills-doctor` 的触发机制应优先服务“检查和诊断”，而不是覆盖所有与 skills 相关的请求。

应触发的典型意图：

- `doctor`、`skills doctor`、`skill doctor`。
- `skills check`、`check my skills`、`检查我的 skills`。
- 审计、扫描、诊断、体检、评估本地 skills。
- 检查 `SKILL.md` 是否合理。
- 分析 skill 触发冲突、token 膨胀、反模式、安全风险。
- 对 Codex / Claude Code / Cursor 的 skill 目录做健康检查。
- 要求生成本地 skills 检查 HTML 报告。

不应触发的典型意图：

- 用户只是泛泛讨论 skills 概念。
- 用户想创建一个新 skill。
- 用户想安装、查找、推荐某个 skill。
- 用户想学习怎么写 skill。
- 用户要求改写普通 prompt、rules、AGENTS.md，但没有检查 skills 健康度的意图。
- 用户只是提到 `skills` 这个词，但目标不是检查、审计或诊断。

触发判断的核心原则：必须同时出现 `skills` 相关对象和 `doctor/check/audit/scan/diagnose/review/report` 这类检查报告意图；只有对象没有检查意图时，不触发 `skills-doctor`。

## 5. 核心使用场景

### 5.1 本地 skill 体检

用户希望知道本机到底有哪些 skills，以及它们是否健康。

典型流程：

1. 用户触发 `skills-doctor`。
2. 产品扫描常见 skill 根目录。
3. 输出 skill 清单、安装位置、大小、触发描述、资源结构和风险等级。
4. 生成整体健康评分、风险摘要和 HTML 检查报告。

### 5.2 冲突诊断

用户发现 AI 输出不稳定、多个 skill 同时触发、设计规则互相打架。

典型流程：

1. 产品读取多个 skill 的名称、description、触发条件和正文。
2. 分析触发范围是否重叠。
3. 标记可能冲突的 skill 组合。
4. 在 HTML 报告中给出边界收敛建议，例如改写 description、限定适用场景、合并重复规则或设置优先级。

### 5.3 token 成本治理

用户希望减少 skill 加载成本，让 Agent 更快、更准。

典型流程：

1. 产品统计 `SKILL.md` 字符数、粗略 token 数、reference/script/assets 规模。
2. 识别过长正文、重复内容、大段示例、应延迟加载的资料。
3. 建议将长内容移动到 `references/`，将确定性操作移动到 `scripts/`。
4. 在 HTML 报告中输出预计可减少的上下文规模。

### 5.4 skill 质量审计

用户希望评估某个第三方 skill 包是否值得安装或在团队中推广。

典型流程：

1. 产品扫描指定目录。
2. 按触发精准度、可移植性、上下文成本、安全性、可维护性评分。
3. 输出 HTML 检查报告，包含问题证据、风险等级和后续处理建议。
4. 给出“可直接使用 / 需要修改 / 不建议使用”的结论。

### 5.5 HTML 报告生成

用户希望将 AI 的检查结果沉淀为可阅读、可归档、可分享的本地文件。

典型流程：

1. 产品完成本地 skills 扫描和 AI 分析。
2. 产品按最佳实践组织报告结构。
3. 生成本地 HTML 文件。
4. 报告中展示总览、明细、证据、风险、建议和后续操作清单。
5. 用户根据报告自行决定是否修改、迁移、禁用或合并相关 skills。

## 6. 核心能力

### 6.1 Skill 发现与索引

- 扫描常见安装位置。
- 支持用户指定目录。
- 识别 Codex、Claude Code、Cursor、自定义目录结构。
- 生成本地 skill inventory。
- 记录 skill 名称、路径、描述、大小、依赖资源、脚本、元数据。

### 6.2 结构检查

- 是否存在 `SKILL.md`。
- frontmatter 是否完整。
- `name` 是否规范。
- `description` 是否足够具体。
- 是否存在空目录、未完成模板、无效 metadata。
- scripts、references、assets 是否组织合理。

### 6.3 触发质量分析

- description 是否能准确说明“什么时候使用”。
- 是否过宽、过泛、容易误触发。
- 是否与其他 skill 触发范围重叠。
- 是否把关键触发条件写在正文而不是 metadata。
- 是否存在“全局最佳实践类”泛化描述。

### 6.4 Token 成本分析

- 估算三层 token 成本，并明确这些值是风险排序估算，不是账单级精确值。
- `estimated_index_tokens`：name + description，对应常驻触发面。
- `estimated_load_tokens`：`SKILL.md`，对应 skill 被选中后的加载成本。
- `estimated_runtime_tokens`：references / scripts / assets，对应运行时按需加载的潜在成本。
- `estimated_total_tokens`：三层估算值合计。
- 标记过长正文。
- 标记过长 description。
- 标记过大的 resources 或单个大 reference/script/asset。
- 标记 runtime 成本过高风险。
- 识别重复规则和长示例。
- 判断内容是否应移动到 references。
- 判断确定性流程是否应移动到 scripts。

### 6.5 反模式检查

重点识别：

- 过宽触发。
- 过长正文。
- 大量教程式 padding。
- 与 Agent 默认行为重复。
- 隐藏危险操作。
- 硬编码绝对路径。
- 内含真实密钥、token、私有 endpoint。
- 无边界网络访问。
- 要求一次性读取全部 references。
- 多个同类 skill 缺少优先级或职责边界。
- 只适配单一工具，缺少跨 Agent 可移植性说明。

### 6.6 HTML 检查报告

报告应按最佳实践生成本地 HTML 文件，并包括：

- 总览评分。
- 扫描范围和 skill 数量。
- 高风险问题数量。
- Index / Load / Runtime 三层 token 估算成本。
- 按优先级排序的 findings。
- 每个问题的证据、影响、后续处理建议。
- 冲突 skill 组合。
- token 成本热点。
- 安全风险。
- 推荐的下一步操作清单。

HTML 报告应满足：

- 单文件可打开，尽量不依赖远程资源。
- 有清晰的摘要区、风险分布、目录导航和明细区。
- 按 Index / Load / Runtime 三层分区展示 findings。
- findings 按 P1 / P2 / P3 分级。
- 每个 finding 包含路径、证据、影响、建议和置信度。
- 对敏感信息只做脱敏展示。
- 适合用户保存、复查或转交给其他 AI / 人工继续处理。

### 6.7 后续操作建议

`skills-doctor` 可以在报告中建议用户后续如何处理问题，但不负责直接修改文件。

建议类型包括：

- 改写 description。
- 拆分长 `SKILL.md` 到 references。
- 删除未完成模板。
- 收敛触发边界。
- 合并重复 skills。
- 禁用或隔离冲突 skills。
- 迁移 skill 到更合理的目录。
- 生成跨 Agent 兼容版本。

这些动作属于用户后续操作范围，`skills-doctor` 的边界停留在检查、分析和报告生成。

## 7. 产品形态

### 7.1 Skill 形态

`skills-doctor` 首先应作为 skill 存在，可以被 Codex、Claude Code、Cursor 或兼容 Agent 触发，并辅助当前 AI 完成本地 skills 检查和 HTML 报告生成。

适合场景：

- 用户在 Agent 对话中直接说“检查我的 skills”。
- 用户在代码仓库中要求审计 `.codex/skills` 或 `.claude/skills`。
- 用户要求分析某个 skill 是否写得合理。

不适合场景：

- 用户只是问“怎么写一个 skill”。
- 用户只是要“找一个 skill”或“安装一个 skill”。
- 用户讨论 skill 产品形态、生态趋势或文档写法，但没有要求检查现有 skill 健康度。

作为 skill 形态时，`description` 应避免覆盖过宽的 `skills` 关键词，应围绕 `doctor`、`skills check`、`audit skills`、`scan skill directories`、`diagnose skill conflicts`、`token bloat in SKILL.md`、`generate skills report` 等检查报告类表达设计。

### 7.2 CLI 形态

CLI 负责确定性扫描和结构化输出。

建议命令形态：

```bash
skills-doctor scan ~/.codex/skills ~/.claude/skills --format markdown
skills-doctor scan ./my-skill-pack --format json
skills-doctor review ./my-skill-pack --ai
skills-doctor report ./my-skill-pack --format html
```

CLI 的核心价值是稳定、可复现、可集成 CI。

### 7.3 报告文件形态

HTML 报告是 `skills-doctor` 的主要交付物，应便于本地打开、归档和继续处理。

报告文件应支持：

- 单文件离线打开。
- 摘要区快速判断整体健康度。
- 明细区定位具体 skill 和证据。
- 风险分级和问题分类。
- 后续操作建议清单。
- 脱敏展示潜在敏感信息。
- 作为后续人工处理或再次交给 AI 分析的输入。

## 8. 跨 Agent 兼容策略

不同 Agent 对 skill 的定义、加载和触发机制不同，因此 `skills-doctor` 不应强绑定某一个平台。

建议采用四层架构：

- Core Scanner：负责目录扫描、文件解析、静态规则检查。
- Review Engine：负责 AI 分析、冲突判断、风险分级和后续建议。
- Report Renderer：负责把检查结果渲染为最佳实践 HTML 报告。
- Adapters：负责适配 Codex、Claude Code、Cursor、千问、GLM、DeepSeek、Kimi 等工具的 skill/rule/prompt 形态。

适配重点：

- Codex：识别 `SKILL.md`、frontmatter、references、scripts、project/global skills。
- Claude Code：识别 `.claude/skills`、项目级 skill、命令和上下文规则。
- Cursor：识别 rules、项目配置、可触发 prompt 规则。
- 国内模型工具：优先兼容“可被 Agent 调用的工具说明 + 本地文件扫描 + AI 分析 + HTML 报告生成”模式，不依赖特定私有 API。

## 9. MVP 范围

MVP 应聚焦“发现问题并输出高质量 HTML 报告”，不包含自动修复功能。

必须包含：

- 扫描指定目录。
- 扫描常见本地 skill 根目录。
- 识别 `SKILL.md` 和基础 metadata。
- 统计大小和粗略 token。
- 检查 description 质量。
- 标记长正文、弱触发、绝对路径、危险词、敏感信息风险。
- 输出本地 HTML 报告，并可保留 JSON 作为中间结构化数据。
- 给出优先级、证据、影响和后续处理建议。

暂不包含：

- 自动批量修改所有 skill。
- 自动生成或应用 patch。
- 复杂 GUI / App 操作。
- 跨设备同步。
- 团队权限系统。
- skill 市场。
- 深度依赖执行或真实运行 skill。

## 10. 成功指标

产品有效性的关键指标：

- 扫描覆盖率：能发现用户本地主要 skill 目录。
- 问题准确率：高优先级 finding 能被用户认可。
- 报告可用性：HTML 报告结构清晰，用户能据此继续处理问题。
- token 成本识别：能准确标出高 token 成本的 `SKILL.md` 和资源文件。
- 冲突识别：能准确标出触发范围重叠的 skill 组合。
- 安全风险识别：敏感信息、危险命令、隐藏网络调用能被发现并脱敏展示。
- 后续操作清晰度：每个问题都有明确的建议和处理方向。

## 11. 风险与约束

- 不同工具的 skill 标准不统一，需要通过 adapter 渐进兼容。
- AI 判断存在误报和漏报，静态扫描证据必须与 AI 结论分离。
- 修复不属于当前产品边界，报告中的建议不能被表述成已执行动作。
- 扫描本地目录涉及隐私和敏感信息，默认不应全盘扫描，只扫描明确目录或常见 skill 根目录。
- 不能把所有 prompt/rules 都强行抽象成 skill，否则产品边界会膨胀。
- 团队版涉及权限、审计、远程同步和供应链安全，应放到后续阶段。

## 12. 路线图

### Phase 1：检查报告

- 完成本地 scanner。
- 支持 JSON 中间结果和 HTML 报告输出。
- 建立反模式规则库。
- 支持基础 AI review。
- 输出证据充分、结构清晰的本地 HTML 检查报告。

### Phase 2：报告增强

- 支持风险分布图、token 成本排行、冲突矩阵。
- 支持 Index / Load / Runtime 三层 token 估算分区。
- 支持 description 过长、resource 过大、runtime 成本风险 finding。
- 支持报告目录导航、筛选和折叠明细。
- 支持报告脱敏策略。
- 支持历史报告对比。

### Phase 3：跨 Agent 生态

- 增加 Codex、Claude Code、Cursor adapter。
- 增加国内模型工具的通用适配方式。
- 支持不同 Agent 触发同一套本地检查流程。
- 支持生成统一结构的 HTML 报告。

## 13. 产品边界

`skills-doctor` 应专注于辅助 AI 检查本地 skills，并生成最佳实践 HTML 报告，不应扩展为自动修复工具、通用 AI IDE、通用 prompt 管理器或插件市场。

清晰边界：

- 做 skill 诊断，不做所有 AI 配置诊断。
- 做报告和建议，不生成或应用修复 patch。
- 做本地检查，不默认上传用户 skill 内容。
- 做跨工具兼容，不依赖单一平台私有能力。
- 做可验证 HTML 报告，不只输出主观评价。
- 后续修复、迁移、禁用、合并等动作交给用户自行决定和执行。

## 14. 一句话总结

`skills-doctor` 是一个辅助 AI 进行本地 skills 体检的 skill：它负责检查、分析并生成最佳实践 HTML 报告，修复动作交给用户后续自行处理。
