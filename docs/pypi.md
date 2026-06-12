# PyPI 发布规范

## 目标

将 `freeskill` 发布为 Python package, 让用户可以通过:

```bash
python -m pip install freeskill
```

获得 `freeskill` CLI.

## 当前包结构

```text
pyproject.toml
skills/
  __init__.py
  <skill-name>/
    SKILL.md
src/
  freeskill/
    __init__.py
    cli.py
    validator.py
```

命令入口:

```text
freeskill = freeskill.cli:main
```

## 发布前检查

- 确认 `freeskill` 包名在 PyPI 可用.
- 确认 `README.md` 内容适合作为 PyPI project description.
- 确认版本号已更新.
- 确认 `freeskill validate` 通过.
- 确认 `freeskill install` 的 symlink 和 copy 模式通过.
- 确认 wheel 中包含 `freeskill_skills`.
- 确认没有把 `.DS_Store`, 临时文件或私有数据打进包.

## 本地验证

源码入口验证:

```bash
PYTHONPATH=src python -m freeskill.cli validate
PYTHONPATH=src python -m freeskill.cli install _template --target claude --target-dir /tmp/freeskill-test
```

editable install 验证:

```bash
python -m pip install -e .
freeskill validate
```

如果本地 pip, setuptools 或 wheel 版本过旧, 先更新构建工具:

```bash
python -m pip install --upgrade pip setuptools wheel
```

## 构建

安装构建工具:

```bash
python -m pip install --upgrade build twine
```

构建 sdist 和 wheel:

```bash
python -m build
```

检查包:

```bash
python -m twine check dist/*
```

## TestPyPI

建议先发布到 TestPyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

安装测试:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ freeskill
```

## PyPI

正式发布:

```bash
python -m twine upload dist/*
```

需要 PyPI account/token. Token 不应写入仓库.

## 发布边界

PyPI package 发布 CLI, validator, 以及当前仓库 `skills/` 下的 skill 内容.
安装后默认从内置 `freeskill_skills` 查找 skill, 因此可以在任意工作目录运行:

```bash
freeskill validate
freeskill install format-code-style --target codex
```

如果需要使用本地开发版 skill, 可以通过 `--skills-root` 或 `FREESKILL_SKILLS_ROOT` 覆盖内置 skills:

```bash
freeskill validate --skills-root /path/to/freeskill/skills
freeskill install paperpost --target claude --skills-root /path/to/freeskill/skills
```
