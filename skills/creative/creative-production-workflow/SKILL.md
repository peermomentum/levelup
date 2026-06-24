---
name: creative-production-workflow
description: "Use when producing creative artifacts: text-art, polished HTML designs, exploratory UI sketches, prose humanization, song lyrics, and AI-music prompts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, design, writing, ascii-art, prototyping, songwriting, workflow]
    related_skills: [excalidraw, popular-web-designs, design-md, p5js]
---

# Creative production workflow

## Overview

This umbrella covers small-to-medium creative output workflows that previously lived as separate narrow skills: terminal text art, one-off HTML designs, disposable UI sketches, humanizing prose, and songwriting / AI music prompting.

Detailed source playbooks from the absorbed narrow skills are retained under `references/absorbed-*.md` for maintainers who need the full original recipes.

Use specialized visual-system skills such as `popular-web-designs`, `design-md`, `excalidraw`, `p5js`, `pixel-art`, or `manim-video` when the user asks directly for those mediums. Use this umbrella when the request is about the broader creative production class or when multiple creative modes overlap.

## When to use

Load this skill when the user asks to:

- make ASCII / terminal art, banners, cowsay, boxes, or text decorations
- create a polished one-off HTML artifact, landing page, prototype, visual board, or deck
- sketch 2-3 disposable UI directions before building
- humanize, de-AI, or voice-match prose
- write lyrics, parody, song structures, Suno-style prompts, or AI music generation prompts

## Routing map

| Request | Apply this section |
|---|---|
| Terminal banner, decorative text, image-to-ASCII | ASCII / text art |
| Polished HTML artifact, deck, landing page, prototype | High-fidelity design artifact |
| "Sketch this", "show variants", "compare layouts" | UI sketch variants |
| "Humanize", "make this sound less AI", voice matching | Humanize prose |
| Lyrics, parody, Suno prompt, music style prompt | Songwriting and AI music |

## ASCII / text art

Choose the fastest reliable tool for the requested format:

- Text banner: `pyfiglet` locally, or the asciified API if pyfiglet is unavailable.
- Message bubble: `cowsay` / `cowthink`.
- Decorative frame: `boxes`.
- Colored terminal text: `toilet`.
- Image-to-ASCII: `ascii-image-converter` or `jp2a`.
- Pre-made subject art: `https://ascii.co.uk/art/<subject>` and extract `<pre>` blocks.
- QR code: `curl -s "qrenco.de/<text>"`.
- Weather/moon terminal art: `wttr.in`.

Preview 2-3 options for subjective art and preserve signatures on pre-made ASCII pieces.

## High-fidelity design artifact

Default output is a complete local HTML file with embedded CSS/JS unless the user asked for code inside an existing repo.

Workflow:

1. Understand artifact, audience, constraints, fidelity, and source materials.
2. Inspect available brand docs, screenshots, repo theme files, tokens, or components before inventing visuals.
3. Define a small design system: color, type, spacing, radii, shadows, motion, interaction rules.
4. Build the artifact: landing page, prototype, deck, component lab, motion study, etc.
5. Verify the file exists and, when browser tools are available, open it and check visual layout / console errors.
6. Report path, contents, verification, and next iteration.

Avoid generic AI-design sludge: gratuitous gradients, fake metrics, placeholder testimonials, random icon grids, and filler copy.

## UI sketch variants

Use sketches when the goal is to compare directions, not ship code.

- Build 2-3 variants, never just one.
- Each variant takes a different stance: density, hierarchy, aesthetic, layout, or interaction model.
- Store under `sketches/NNN-stance-name/index.html` with a short README for design stance, choices, trade-offs, and best fit.
- Include enough interactivity to feel the direction: hover states, one click path, one state transition.
- Finish with a head-to-head table and an opinionated recommendation.

If one sketch wins and the user wants production code, rebuild it in the project stack rather than preserving the throwaway file as the implementation.

## Humanize prose

When asked to de-AI or voice-match text:

1. Read the source text and any voice sample.
2. Identify common AI tells: inflated significance, promotional tone, vague attributions, `-ing` filler phrases, rule-of-three lists, em dash overuse, bold-header bullets, chatbot artifacts, and generic positive conclusions.
3. Rewrite for natural rhythm, specific claims, active voice, and a real point of view.
4. Preserve meaning and constraints; do not invent facts.
5. Do a final pass asking: "What still makes this obviously AI-generated?" Then revise again.

For file edits, use targeted `patch` when possible and show the changed section or diff.

## Songwriting and AI music

For lyrics and music prompts:

- Start with the hook or emotional core.
- Pick or invent a structure: ABABCB, AABA, strophic, or custom.
- Balance rhyme, stress, and singability; read or sing lines aloud when possible.
- For parody, map the original syllables, stresses, rhyme scheme, held vowels, and structure before writing replacements.
- For Suno-style generation, write a style prompt with genre, mood, era, instrumentation, vocal persona, production, dynamics, BPM/key if useful, and exclusions.
- Use bracketed metatags in lyrics for structure, dynamics, vocal performance, and atmosphere.
- Spell unusual words phonetically when AI singers are likely to mispronounce them.

Generate multiple options; music prompting usually needs several takes.

## Common pitfalls

- Designing from vibes when source context is available.
- Calling a static screenshot a prototype; include at least one meaningful interaction.
- Making sketch variants that differ only by accent color.
- Humanizing by merely removing a few buzzwords; rhythm and point of view matter too.
- Using artist names or trademarks in AI-music style prompts when descriptive sound cues would work.
- Forgetting to verify that the creative artifact was actually written and opens cleanly.

## Verification checklist

- [ ] Correct route chosen from the routing map.
- [ ] Artifact files exist at stated paths.
- [ ] HTML/CSS/JS artifacts were opened or syntax-checked when tools allowed.
- [ ] Text rewrites preserve meaning and do not invent facts.
- [ ] Music prompts include structure, performance, and dynamics when relevant.
- [ ] Final response gives the artifact path or the finished creative output directly.
