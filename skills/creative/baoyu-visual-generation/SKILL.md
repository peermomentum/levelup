---
name: baoyu-visual-generation
description: "Use when creating Baoyu-style visual knowledge artifacts: article illustrations, educational comics, and infographics with structured prompts and reproducible image outputs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [baoyu, image-generation, infographic, comic, article-illustration, visual-knowledge]
    related_skills: [creative-production-workflow]
---

# Baoyu visual generation

## Overview

This umbrella consolidates the Baoyu visual knowledge skills into one class-level workflow. All three modes share the same concerns: analyze source content, choose a visual structure and style, save reproducible prompts before image generation, use `image_generate`, download the returned URL to a stable output path, and preserve source facts exactly.

The full original packages are retained under `references/absorbed-baoyu-*/` for their detailed galleries, layouts, tones, presets, and prompt templates.

## When to use

Use this skill when the user asks for:

- article illustrations / 为文章配图
- educational or knowledge comics / 知识漫画 / 教育漫画
- infographics / 信息图 / visual summaries / high-density information graphics
- Baoyu-style visual prompt workflows with output directories and reproducibility records

## Mode routing

| User wants | Mode |
|---|---|
| Add images into an existing article at useful positions | Article illustrator |
| Multi-page story, biography, tutorial, or concept comic | Knowledge comic |
| One standalone visual summary or information graphic | Infographic |

## Shared rules

- Preserve source data faithfully. Do not alter statistics, quotes, names, or terminology.
- Strip API keys, tokens, credentials, and secrets before writing source-derived output files.
- Save analysis and prompt files before generating images.
- `image_generate` accepts text prompt + aspect enum only. It returns a URL/path; download or copy it into the output directory before finalizing.
- Use absolute output paths for downloads to avoid terminal CWD drift.
- Reference images are not passed to `image_generate`; analyze them with vision and embed textual style/palette/scene traits into prompts.
- Map aspect ratios to tool enums: landscape, portrait, square.

## Article illustrator mode

Best for inserting multiple images into a prose article.

Output normally lives in the article's `imgs/` directory, or under `illustrations/<topic>/` for pasted content. Workflow:

1. Detect and describe any reference images.
2. Analyze article content, purpose, core arguments, and positions where images add value.
3. Confirm type, density, style, palette, and language when not specified.
4. Write `outline.md` with one entry per illustration.
5. Write a prompt file for each image under `prompts/`.
6. Generate each image, download it to the output directory, and insert markdown image references into the article.

Use article-specific labels and data in prompts; avoid generic placeholder text.

## Knowledge comic mode

Best for multi-page educational storytelling.

Output normally lives under `comic/<topic-slug>/` with source, analysis, storyboard, character definitions, prompt files, generated PNGs, and optional reference-image provenance.

Workflow:

1. Analyze content and detect language.
2. Confirm art style, tone, layout, aspect, review gates, and reference-image usage.
3. Generate storyboard and character descriptions.
4. Optionally review outline/prompts if the user asked for gates.
5. Save prompt files for cover/page images before generation.
6. Generate a character sheet when useful for human review.
7. Generate pages, embedding text character descriptions into every page prompt.

Character consistency comes from text descriptions; the character-sheet PNG is a review artifact, not an input to the generation model.

## Infographic mode

Best for one dense visual summary.

Output normally lives under `infographic/<topic-slug>/` with source, analysis, structured content, prompt, and final image.

Workflow:

1. Analyze topic, data type, complexity, tone, audience, language, and user design instructions.
2. Transform source into `structured-content.md` with titles, sections, data points, labels, and learning objectives.
3. Recommend layout × style combinations, checking keyword shortcuts first.
4. Confirm combination, aspect, and language if needed.
5. Assemble `prompts/infographic.md` from layout/style/base templates and structured content.
6. Generate image, download/save it, and report files created.

Common layouts include timelines, comparisons, matrices, bento grids, dashboards, roadmaps, cycles, and dense modules.

## Pitfalls

- Generating images before writing prompt files destroys reproducibility.
- `curl -o relative/path.png` can silently write to the wrong directory; use absolute paths.
- Literalizing metaphors often produces bad educational images; visualize the underlying concept.
- Skipping Step 2 confirmations can pick the wrong visual language.
- Treating a reference image as model input is wrong; convert reference traits to text.

## Verification checklist

- [ ] Source analysis saved.
- [ ] Output directory is unambiguous and conflict-safe.
- [ ] Prompt files exist before `image_generate` calls.
- [ ] Generated URLs were downloaded/copied to stable files.
- [ ] Files are non-empty and paths in markdown point to the saved images.
- [ ] Final report includes mode, style/layout choices, output path, and generation count.
