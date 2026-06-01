# freeskill Skill 编写规范

## 目的

`freeskill` 使用 Agent Skills 作为源格式. freeskill skill 应该可以直接作为 Agent Skill 使用, 不依赖 freeskill 自定义 manifest 或目标工具专属改写.

本文档定义如何在本仓库中创建和维护 skill.

## 最小结构

每个 skill 必须是 `skills/` 下的一个目录, 且必须包含 `SKILL.md`.

```text
skills/<skill-name>/
  SKILL.md
```

推荐结构:

```text
skills/<skill-name>/
  SKILL.md
  scripts/
  references/
  assets/
```

可选结构:

```text
skills/<skill-name>/
  examples/
  tests/
```

## 目录职责

- `SKILL.md`: 必需. Agent Skills 主入口, 包含 YAML frontmatter 和工作流说明.
- `scripts/`: 可选. 存放 skill 可能要求 agent 执行的脚本.
- `references/`: 可选. 存放长规则, checklist, 示例和领域笔记.
- `assets/`: 可选. 存放静态文件, 模板, 图片或其他资源.
- `examples/`: 可选. 存放输入输出示例.
- `tests/`: 可选. 后续验证样例或脚本测试.

## SKILL.md Frontmatter

每个 `SKILL.md` 必须以 YAML frontmatter 开头, 至少包含 `name` 和 `description`.

```md
---
name: paper-reading
description: Use this skill when reading, summarizing, reviewing, or rebutting research papers.
---
```

字段要求:

- `name`: 稳定 skill ID. 应与目录名一致.
- `description`: 触发说明. 应说明何时使用该 skill, 不只是重复标题.

## SKILL.md 正文

推荐章节:

```md
# Skill Title

## When To Use

## Workflow

## Inputs

## Outputs

## References

## Scripts

## Constraints
```

主要流程应放在 `SKILL.md`. 较长的 checklist, 背景知识或复用规则应放进 `references/`, 并在 `SKILL.md` 中引用.

## Scripts

只有当脚本对工作流有明确价值时, 才放入 `scripts/`.

在 `SKILL.md` 中说明:

- 脚本做什么.
- agent 何时应该运行它.
- 需要哪些输入.
- 预期输出是什么.
- 有哪些重要失败场景.

## References

`references/` 用于存放有用但不适合直接放在主说明里的长材料.

示例:

- Review checklist.
- 写作风格指南.
- 领域规则.
- Rebuttal 模板.
- 项目约定.

## Assets

`assets/` 用于静态资源, 例如模板, 图片或示例文件.

## 不应做的事

- 第一阶段不要要求每个 skill 都有 `skill.json`.
- 不要在单独 manifest 中重复维护 `name` 和 `description`.
- 除非确认不兼容, 不要分别维护 Claude 版和 Codex 版 skill.
- 普通 skill 默认不要放生命周期 hooks.
- 除非已理解兼容性影响, 不要添加工具专属 frontmatter.

## 验证清单

一个合法的第一阶段 freeskill skill 应满足:

- 存在 `skills/<name>/SKILL.md`.
- 包含 YAML frontmatter.
- 包含 `name`.
- 包含 `description`.
- `description` 说明何时使用该 skill.
- supporting files 放在 Agent Skills 兼容目录中.
- 不要求 `skill.json`.
