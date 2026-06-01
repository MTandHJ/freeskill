---
name: skill-name
description: Use this skill when the user needs this specific reusable workflow.
---

# Skill Title

## When To Use

使用这个 skill 当:

- 用户请求这个特定工作流.
- 任务需要复用固定说明, 参考材料或脚本.
- 输出需要遵循稳定的个人约定.

不要使用这个 skill 当:

- 请求与该工作流无关.
- 简单直接回答已经足够.
- 另一个更具体的 skill 更适合.

## Workflow

1. 明确用户目标和期望输出.
2. 读取相关文件或 supporting materials.
3. 按该工作流的步骤执行.
4. 只有在相关且适合当前任务时才使用 scripts.
5. 按预期格式产出结果.
6. 说明必要假设, 缺失输入或验证缺口.

## Inputs

- 用户请求.
- 相关文件或路径.
- `references/` 中的可选参考材料.
- `scripts/` 中的可选脚本.

## Outputs

- 符合用户请求格式的简洁结果.
- 工作流要求生成的文件或修改.
- 适用时提供简短验证说明.

## References

`references/` 用于长规则, 示例, checklist 或不适合直接放在 `SKILL.md` 的说明.

## Scripts

`scripts/` 用于工作流辅助脚本. 使用脚本前, 应说明脚本用途, 输入, 输出和失败模式.

## Constraints

- 让 skill 聚焦一个任务家族.
- 优先保持 Agent Skills 兼容结构.
- 除非已检查兼容性, 避免工具专属 frontmatter.
- 第一阶段 freeskill skill 不要求 `skill.json`.
