# freeskill Plugin 分层规范

## 目的

`freeskill` 首先是个人 Agent Skills 源仓库. Plugin packaging 是后续的分发层, 用于打包一组相关能力.

不要把整个仓库做成一个大 plugin. 只有当场景需要 plugin 能力时, 才按主题生成 plugin.

## Skill 与 Plugin

Skill:

- 描述 agent 如何完成一类任务.
- 使用 `SKILL.md` 作为核心入口.
- 可以包含 `scripts/`, `references/`, `assets/`.
- 适合直接 symlink 或 copy 安装.

Plugin:

- 是可安装的分发包.
- 可以包含多个 skills.
- 可以添加 commands, hooks, MCP servers, apps, dependencies 和 marketplace metadata.
- 适合主题或工作流级分发.

## 推荐分层

```text
freeskill = Agent Skills source repo
plugin   = theme-based distribution package generated from freeskill content
```

推荐仓库形态:

```text
skills/
  paper-reading/
  paper-review/
  code-style/
  freeplot/
  freerec/

plugins/
  paper/
  coding/
  plotting/
  freerec/
```

## 不要做超级 Plugin

避免这种设计:

```text
freeskill-as-one-plugin/
  skills/
    paper-reading/
    paper-review/
    code-style/
    freeplot/
    freerec/
    recboard/
```

问题:

- 安装粒度太粗.
- 不同主题的依赖会混在一起.
- 更新一个 skill 会影响整个 plugin package.
- 工具 UI 可能暴露太多无关 skills.
- 分享某个主题会变困难.

## 何时保持 Standalone Skill

以下情况应保持为独立 skill:

- 只处理一种任务类型.
- 只需要 `SKILL.md` 和 supporting files.
- 不需要 hooks, commands, MCP, app 或 packaged dependencies.
- 需要快速个人迭代.

## 何时创建 Plugin

以下情况适合创建主题 plugin:

- 一个主题包含多个相关 skills.
- 需要 commands 或 slash command wrappers.
- 需要生命周期 hooks.
- 需要 MCP server.
- 需要 web app 或 packaged dependencies.
- 需要 marketplace-style installation.

## 主题 Plugin 示例

```text
plugins/paper/
  skills/
    reading/
      SKILL.md
    summary/
      SKILL.md
    review/
      SKILL.md
    rebuttal/
      SKILL.md
  commands/
  hooks/
```

## 第一阶段策略

第一阶段:

- 不实现 plugin packaging.
- 不创建 plugin manifests.
- 不创建 marketplace metadata.
- 普通 skill 默认不放 hooks.

等有真实的主题工作流后, 再添加 Claude Code 和 Codex plugin manifests.
