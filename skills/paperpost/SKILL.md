---
name: paperpost
description: Use this skill when converting a research paper path or URL into a Hugo paper post under content/posts/paper, with Chinese research-note style, tag reuse, and safe overwrite checks.
---

# PaperPost

Use this skill to turn a research paper path or URL into a Hugo paper post.

## Workflow

1. Resolve the paper post directory by searching `content/posts/paper` from the current working directory; if there are zero or multiple matches, ask the user.
2. Run `scripts/resolve_input.py` on the paper path or URL, then run `scripts/parse_pdf.py` on the local PDF.
3. Read `references/template.md` and `references/tags.md`.
4. Draft the post, reuse existing tags when possible, and record any new tags.
5. Check the target filename; if it exists, ask whether to overwrite, rename, or stop before writing.
6. Report the output path, parser warnings, uncertain metadata, and any new tags.

## Ground Rules

- Do not fabricate paper claims, results, venue, year, PDF links, or code links.
- Do not silently overwrite an existing post.
- Omit the `[Code]` link when no code link is known.
- Keep `附录` only when extra derivation, background, or implementation detail is useful.
- If new tags are created, include `New tags: ...` in the final response.

## Writing Style

- Write in Chinese as a personal research note, not a generic paper summary.
- Use concise, plain, and direct language.
- Focus on the problem, mechanism, evidence, and personal judgment; do not aim for exhaustive coverage.

## References

- `references/template.md`: frontmatter, sections, file naming, reference format, and MPT example.
- `references/tags.md`: existing tags and tag selection rules.

## Scripts

```bash
python skills/paperpost/scripts/resolve_input.py PATH_OR_URL
python skills/paperpost/scripts/parse_pdf.py PAPER.pdf
```

Both scripts print JSON to stdout. Treat script warnings as uncertainty to resolve in the final post or final response.
