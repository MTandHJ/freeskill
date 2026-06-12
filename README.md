# freeskill

`freeskill` 是个人 Agent Skills 仓库和轻量 CLI, 用于维护 `skills/` 下的 Agent Skills, 并将它们安装到 Claude Code 或 Codex 的 skill 目录.

## 当前能力

- 使用 Agent Skills 标准维护 skills.
- 校验 `SKILL.md` frontmatter.
- 通过 symlink 或 copy 安装 skill.
- 支持 Claude Code 和 Codex 的 user/project scope.
- `pip install .` 后内置 `skills/`, 可在任意工作目录安装 skill.

## 本地使用

```bash
python -m pip install -e .
freeskill validate
freeskill install _template --target claude
freeskill install --all --target codex
```

安装包会内置当前仓库的 `skills/`. 因此完成 `pip install .` 后, 可以在任意目录运行:

```bash
freeskill install format-code-style --target codex
freeskill install --all --target codex
```

不安装包时也可以直接运行:

```bash
PYTHONPATH=src python -m freeskill.cli validate
PYTHONPATH=src python -m freeskill.cli install _template --target codex
```

## 文档

- `docs/skill-spec.md`: Skill 编写规范.
- `docs/install.md`: Install 规范.
- `docs/plugin-spec.md`: Plugin 分层规范.
- `docs/pypi.md`: PyPI 发布规范.
