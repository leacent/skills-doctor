# skills-doctor

[English](README.md) | [简体中文](README.zh-CN.md)

`skills-doctor` 是一个用于审计本地 AI Agent skills 的 Agent Skill。它指导 AI Agent 以只读方式检查本地 skill 目录、触发质量、上下文成本、渐进式披露、安全风险和可维护性问题。

它刻意保持为纯 skill：没有 Python 包、没有后台服务，也不会自动修改文件。

## 安装

使用开放的 Agent Skills CLI 安装：

```bash
npx skills add leacent/skills-doctor -g
```

然后告诉你的 Agent：

```text
Use skills-doctor to audit my local agent skills.
```

`-g` 表示全局安装，让兼容的 Agent 可以在多个项目中使用这个 skill。

## 检查内容

- 在 Universal、项目级和主流 Agent 专属目录中发现 skills，包括 `.agents/skills`、`~/.agents/skills`、Claude Code、Codex、Cursor、OpenClaw、Cline、Gemini CLI、OpenCode、Warp、Augment、CodeBuddy 等已存在的已知 skill 目录。
- 检查 `SKILL.md` 结构和 frontmatter 质量。
- 检查过弱、过宽或潜在冲突的触发描述。
- 用粗略相对估算理解 Index / Load / Runtime 上下文成本。
- 检查渐进式披露问题，例如过早加载所有 references。
- 检查过长的 `SKILL.md`、大型 references 和运行时上下文风险。
- 检查危险命令模式和敏感示例值。
- 检查硬编码本地路径和可移植性问题。
- 检查空的或过期的资源目录。

## 仓库结构

```text
skills-doctor/
├── SKILL.md
├── references/
│   ├── anti-patterns.md
│   ├── report-template.md
│   └── review-checklist.md
├── README.md
├── README.zh-CN.md
└── LICENSE
```

## 审阅边界

`skills-doctor` 默认只读。它会要求 Agent 不编辑、删除、移动、安装、卸载、覆盖或 patch 被检查的用户 skills。它只应检查文件、总结风险并建议下一步修改。

如果用户要求 Agent 应用修复，那是单独任务，并且应先获得用户明确确认。

## 审阅模型

这个 skill 使用三层模型：

- `Index`：`name + description`，skill 被选择前可见的触发表面。
- `Load`：`SKILL.md`，skill 被选择后加载的正文。
- `Runtime`：`references/`、`scripts/`、`assets/` 和按需加载的命令输出。

Token 数量只是用于相对风险排序的粗略估算，不是计费用量。

## 默认 Skill 目录

当用户没有提供路径时，`skills-doctor` 会要求 Agent 只检查已经存在的已知目录：

- Universal：`.agents/skills`、`~/.agents/skills`。
- 项目级：`.codex/skills`、`.claude/skills`、`.cursor/skills`。
- 核心全局 Agent：`~/.codex/skills`、`~/.claude/skills`、`~/.cursor/skills`。
- 主流 Agent 专属目录：`~/.aider-desk/skills`、`~/.augment/skills`、`~/.bob/skills`、`~/.openclaw/skills`、`~/.codeartsdoer/skills`、`~/.codebuddy/skills`、`~/.codemaker/skills`。
- 其他已知目录存在时也可检查：`~/.amp/skills`、`~/.antigravity/skills`、`~/.cline/skills`、`~/.dexto/skills`、`~/.firebender/skills`、`~/.gemini/skills`、`~/.github-copilot/skills`、`~/.kimi/skills`、`~/.opencode/skills`、`~/.warp/skills`。

不要搜索整个 home 目录。

## 参考资料

- `references/review-checklist.md`：完整审计标准。
- `references/anti-patterns.md`：常见 skill 设计问题和更好的写法。
- `references/report-template.md`：最终回复使用的简洁报告格式。

## 隐私

`skills-doctor` 本地优先。它要求 Agent 只检查用户提供的路径或已知本地 skill 根目录，避免无边界扫描 home 目录，并在报告中遮蔽敏感值。

## License

MIT
