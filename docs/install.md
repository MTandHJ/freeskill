# freeskill Install 规范

## 目的

`freeskill install` 规划为轻量安装器, 用于把本仓库中的 Agent Skills 链接或复制到目标工具的 skill 目录.

它不是复杂格式转换器. 源 skill 应该已经符合 Agent Skills 结构.

## 规划命令

安装为 Python package 后, 标准命令是:

```bash
freeskill install <skill-name> --target <claude|codex> [--scope user|project] [--mode symlink|copy]
```

本地开发时可以使用:

```bash
python -m pip install -e .
freeskill validate
freeskill install <skill-name> --target <claude|codex>
```

不安装包时也可以运行:

```bash
PYTHONPATH=src python -m freeskill.cli validate
PYTHONPATH=src python -m freeskill.cli install <skill-name> --target <claude|codex>
```

默认行为:

```text
--scope user
--mode symlink
```

实现和测试阶段可以支持目标父目录覆盖:

```bash
freeskill install <skill-name> --target <claude|codex> --target-dir /tmp/freeskill-test
```

此时 skill 会安装到:

```text
/tmp/freeskill-test/<skill-name>/
```

## 安装流程

1. 定位 `skills/<skill-name>/`.
2. 检查 `SKILL.md` 是否存在.
3. 解析 `SKILL.md` frontmatter.
4. 检查必需字段: `name` 和 `description`.
5. 根据 `target` 和 `scope` 解析目标目录.
6. 创建目标父目录.
7. 使用 symlink 或 copy 安装.
8. 输出安装摘要和人工验证提示.

## 安装模式

### Symlink

Symlink 模式把源 skill 目录链接到目标工具目录.

优点:

- 源仓库更新能立即反映到目标目录.
- 适合个人 skill 仓库快速迭代.
- 不复制文件.

取舍:

- 某些工具或平台可能无法稳定跟随 symlink.
- Windows 支持需要单独验证.

### Copy

Copy 模式把完整 skill 目录复制到目标工具目录.

优点:

- 兼容性更保守.
- 目标目录自包含.

取舍:

- 源仓库更新不会自动同步.
- 修改后需要重新 install.

## 目标路径

目标路径必须允许配置, 因为工具版本和平台可能变化.

第一阶段建议默认:

```text
Claude Code user scope:
  ~/.claude/skills/<skill-name>/

Claude Code project scope:
  .claude/skills/<skill-name>/

Codex user scope:
  ~/.codex/skills/<skill-name>/

Codex project scope:
  .codex/skills/<skill-name>/
```

必要时支持兼容路径:

```text
Codex user compatibility path:
  ~/.agents/skills/<skill-name>/

Codex project compatibility path:
  .agents/skills/<skill-name>/
```

## 成功标准

安装成功表示:

- 源 skill 通过基础校验.
- 目标目录中存在该 skill 的链接或副本.
- 目标位置的 `SKILL.md` 可读取.

安装成功不表示:

- Claude Code 或 Codex 已经刷新 skill 列表.
- 当前对话已经能使用新 skill.
- Claude Code 和 Codex 共享同一种手动调用语法.

## 人工验证

安装后, 应在目标工具中询问具体 skill 内容.

更好的问法:

```text
Can you describe when the paper-reading skill should be used?
```

较弱的问法:

```text
Was paper-reading installed successfully?
```

前者能检查目标工具是否看到了真实 skill 指令. 后者可能诱发猜测.

## 失败处理

以下情况 installer 应失败或请求确认:

- 源 skill 不存在.
- `SKILL.md` 缺失.
- 必需 frontmatter 缺失.
- target 未知.
- scope 未知.
- 目标路径已存在且不是 freeskill 管理的链接或副本.
- symlink 创建失败.

如果 symlink 失败, installer 可以提示使用 `--mode copy`.

## PyPI 发布边界

`pyproject.toml` 定义了 Python package 和 console script. 后续发布到 PyPI 后, 用户可以通过:

```bash
python -m pip install freeskill
```

安装 CLI.

注意:

- PyPI package 首先发布 CLI 能力.
- skill 内容仍建议来自本仓库的 `skills/` 目录, 或通过 `--skills-root` 指向其他 skill 仓库.
- 真正上传 PyPI 需要维护者的 PyPI account/token.
- 发布前需要确认 `freeskill` 包名在 PyPI 上可用.
