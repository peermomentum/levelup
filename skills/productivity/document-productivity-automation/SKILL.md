---
name: document-productivity-automation
description: "Umbrella workflow for document and workplace automation: PDFs/OCR, PowerPoint decks, Teams meeting pipeline, and Microsoft/Google workspace document operations."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [productivity, documents, pdf, ocr, powerpoint, teams, office, automation]
    related_skills: [google-workspace]
---

# Document productivity automation

Use this umbrella when the user asks for workplace document processing, presentation generation/editing, meeting-summary pipeline operations, OCR/PDF extraction or edits, and adjacent workspace automation.

## Routing map

| User need | Section |
|---|---|
| Extract text from scans/PDFs | OCR and document extraction |
| Edit PDF text/title/metadata | PDF editing |
| Create/read/edit `.pptx` decks | PowerPoint decks |
| Operate Teams meeting summaries/subscriptions | Teams meeting pipeline |
| Gmail/Calendar/Drive/Docs/Sheets | Workspace APIs |

## Shared workflow

1. Determine the document system and artifact format: PDF, scan/image, PowerPoint, meeting transcript, email/calendar/doc/sheet.
2. Locate the actual input files or IDs; do not guess paths or fabricate extracted text.
3. Use the narrowest safe tool: OCR/extraction for scans, nano-pdf for PDF text edits, python-pptx/deck tooling for slides, Graph/gws tools for cloud docs.
4. Verify by reading back the output file, checking page/slide counts, confirming changed text, or reporting a returned API/job ID.
5. Keep originals untouched unless the user explicitly requests in-place edits; write edited outputs with clear names.

## Sections

### OCR and document extraction
Use OCR/PDF extraction workflows for scans and mixed PDFs. Verify non-empty extracted text and flag low-confidence/garbled output.

### PDF editing
Use PDF edit tools for small typo/title/text edits. Preserve a backup or write a new output file, then verify the changed text or metadata.

### PowerPoint decks
Use deck tooling for slide creation, reading, edits, notes, and templates. Verify `.pptx` exists and inspect slide count/content before reporting success.

### Teams meeting pipeline
Use the Hermes/Graph pipeline controls to inspect status, summarize/replay meetings, and manage subscriptions. Report job IDs/status and avoid duplicate replays unless requested.

### Workspace APIs
For Google/Microsoft workspace operations, verify auth, target account, and object IDs. For sends/shares/deletes, confirm the target scope before side effects.

## Preserved source playbooks

Absorbed source skill packages live under `references/source-packages/<skill-name>/`; former `SKILL.md` files are renamed to `source-skill.md` to avoid nested skill registration while preserving templates/scripts.

## Verification checklist

- [ ] Input file/ID exists and was inspected.
- [ ] Output file/API result/job status was verified.
- [ ] Original files were preserved unless in-place editing was requested.
- [ ] Side effects such as sends/shares/subscription changes were scoped explicitly.
