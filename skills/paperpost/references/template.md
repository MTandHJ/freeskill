# Template

Use this annotated skeleton for the post shape. Comments explain what to write and should not be copied into the final post.

File naming:

- Prefer the paper nickname, such as `RQ-VAE.md` or `TIGER.md`.
- Otherwise use a concise title phrase.
- Keep `.md`.
- Check whether the target file already exists before writing.

```markdown
---
date: "YYYY-MM-DD" # writing date
draft: false # keep false for publishable posts
title: "Paper Title" # full paper title
description: "一句话概括" # short Chinese phrase or sentence
author: MTandHJ # keep unchanged
tags:
  - Paper # fixed, always first
  - <topic1> # reuse topic tags from references/tags.md when possible
  - <topic2> # optional second topic tag
  - Empirical | Theoretical | Seminal # paper type; choose what truly applies
  - <venue> # actual venue, such as SIGIR, KDD, ICLR, arXiv; do not invent
  - <year> # actual publication/preprint year; do not invent
pinned: false # keep false unless the user asks otherwise
---

## 研究背景

<!-- 问题背景: 这篇论文要解决什么问题, 为什么重要, 和哪些已有方向或站内文章有关. -->

## 核心思想

<!-- 核心方法: 写机制、架构、数据流、关键公式或算法步骤. -->
<!-- 公式规则: display formula 前后必须有空行; 使用单独一行的 $$. -->
<!-- 公式中的比较符写成带空格的形式, 例如 i < j 和 x > 0, 避免被识别成 HTML tag. -->

## 关键洞察

<!-- 关键实验结果、消融、主要结论、局限、反直觉点, 或源码/复现中发现的重要细节. -->

## 继往开来

<!-- 个人判断: 这篇论文和前后工作、未来方向、复现经验或自己的研究问题有什么关系. -->

## 附录

<!-- 可选: 只在有补充推导、预备知识、实现细节或额外实验时保留; 否则删除整个章节. -->

## 参考文献

<ol class="reference">
  <li>
    Author(s)
    <u>Title.</u>
    <i>Venue</i>, Year.
    <a href="URL" style="color: #007acc; font-weight: bold; text-decoration: none;">[PDF]</a>
    <a href="URL" style="color: #007acc; font-weight: bold; text-decoration: none;">[Code]</a>
  </li>
</ol>
```

Reference rules:

- Do not invent author list, venue, year, PDF URL, or code URL.
- Omit the `[Code]` link when no code link is known.
- Use the paper URL or arXiv URL as `[PDF]` when it is the best known source.
- If venue or year is unknown, mark it as uncertain in the final response instead of fabricating it.
