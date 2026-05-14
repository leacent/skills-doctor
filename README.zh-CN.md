# skills-doctor

`skills-doctor` 是一个用于检查本地 AI Agent 技能的工具和可安装 skill。它可以帮助 AI Agent 检查本地技能目录、识别质量和安全问题，并生成符合最佳实践的 HTML 报告。它支持 Python 3.9+。

扫描器不会修改被检查的技能、应用补丁或上传本地内容。安装器只会把内置的 `skills-doctor` skill 及其审计参考资料复制到本地 Agent skills 目录。

## 检查内容

- 在常见本地根目录中发现技能，例如 `.codex/skills`、`.claude/skills`、`~/.codex/skills` 和 `~/.claude/skills`。
- 检查 `SKILL.md` 结构和 frontmatter 质量。
- 通过安装后的审计清单检查触发描述的精确性和过宽描述。
- 估算 Index、Load 和 Runtime 三层的 token 成本热点。
- 检查渐进式披露问题。
- 检查过长描述、大型资源和高运行时上下文风险。
- 检查危险命令模式和敏感值。
- 检查硬编码本地路径。
- 检查空资源目录。
- 通过 Agent 审阅扫描清单，检查技能之间潜在的触发冲突。

## 安装

使用 `pipx` 直接从 GitHub 安装 CLI，然后安装内置 skill：

```bash
pipx install "git+https://github.com/leacent/skills-doctor.git"
skills-doctor install-skill --target all
```

也可以使用 `uv`：

```bash
uv tool install "git+https://github.com/leacent/skills-doctor.git"
skills-doctor install-skill --target all
```

这会把 `skills-doctor` 安装到：

- `~/.claude/skills/skills-doctor/SKILL.md`
- `~/.codex/skills/skills-doctor/SKILL.md`
- `~/.cursor/skills/skills-doctor/SKILL.md`

如果只想安装到某一个 Agent：

```bash
skills-doctor install-skill --target claude
```

已有文件默认不会被覆盖，除非传入 `--force`。安装完成后，可以让 Agent 执行 `skills doctor`、`audit skills` 或 `scan skill directories`。

本地开发安装：

```bash
git clone https://github.com/leacent/skills-doctor.git
cd skills-doctor
python3 -m pip install -e .
```

## 快速开始

为默认本地根目录生成 HTML 报告：

```bash
skills-doctor report --output skills-doctor-report.html
```

扫描显式指定的技能根目录：

```bash
skills-doctor report ~/.codex/skills ~/.claude/skills --output report.html
```

为自动化流程输出 JSON：

```bash
skills-doctor scan ~/.codex/skills --format json
```

为终端查看输出 Markdown：

```bash
skills-doctor scan ~/.codex/skills --format markdown
```

## CLI

```bash
skills-doctor scan [paths...] --format json|markdown|html
skills-doctor report [paths...] --output skills-doctor-report.html
skills-doctor review [paths...] --format markdown|json|html
skills-doctor install-skill --target claude|codex|cursor|all
```

未提供路径时，`skills-doctor` 只会扫描已存在的常见根目录。它不会搜索整个主目录。

## 报告边界

HTML 报告包含确定性扫描证据、影响、优先级、置信度和建议的下一步操作。安装后的 skill 会包含基于提示词的审计参考资料，用于定性判断。后续操作，例如重写描述、拆分参考资料、移动文件、禁用技能或合并重复项，均由用户自行决定。

## Token 估算模型

`skills-doctor` 报告的 token 成本是估算值，不是计费用量。默认估算器使用粗略的 `chars / 4` 启发式规则，用于相对风险排序。

- `estimated_index_tokens`：技能名称和描述，表示始终可见的触发面。
- `estimated_load_tokens`：`SKILL.md`，表示技能被选中后加载的内容。
- `estimated_runtime_tokens`：参考资料、脚本和资源，表示可能按需加载的上下文成本。
- `estimated_total_tokens`：以上三项估算值之和。

HTML 报告会按 Index、Load 和 Runtime 三层对发现的问题分组，帮助用户了解上下文成本和触发风险来自哪里。

## 技能形式

可安装的技能包位于 [`skill/`](skill/)，并已随 Python 包一起内置，供 `install-skill` 使用。`SKILL.md` 保持简短工作流，`skill/references/` 保存基于提示词的审计清单、反模式和报告模板。它的触发条件有意保持狭窄：仅用于 `doctor`、`skills check`、`audit skills`、`scan skill directories` 和本地技能报告请求。不要将它用于创建、安装、查找或学习如何编写技能。

## 开发

运行测试：

```bash
python3 -m unittest
```

直接运行包：

```bash
python3 -m skills_doctor report tests/fixtures --output /tmp/skills-doctor-report.html
```

## 隐私

`skills-doctor` 是本地优先的工具。它只读取用户提供的目录或已知的本地技能根目录。报告会在展示前遮蔽常见 secret 模式。

## License

MIT
