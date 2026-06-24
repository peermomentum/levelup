---
name: apple-platform-automation
description: "Use when automating Apple ecosystem apps and devices: Notes, Reminders, iMessage/SMS, Find My, and macOS GUI/computer-use workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [apple, macos, notes, reminders, imessage, findmy, automation]
    related_skills: []
---

# Apple Platform Automation

## Overview

This umbrella covers class-level workflows for operating Apple-first tools from Hermes: Notes, Reminders, Messages/iMessage, Find My devices and AirTags, and direct macOS GUI/computer-use automation. Prefer this skill over narrow app-specific siblings when the user asks for anything in the Apple ecosystem.

## When to Use

- Creating, searching, editing, or organizing Apple Notes.
- Adding, listing, completing, or triaging Apple Reminders.
- Sending or reading iMessage/SMS through the configured CLI bridge.
- Locating Apple devices/AirTags or checking Find My status.
- Driving macOS apps through accessibility/computer-use when no CLI bridge exists.

Do not use this on Linux unless the task is to write instructions for a macOS host; these workflows require macOS and local Apple credentials/tools.

## Shared Approach

1. Confirm the task must run on a macOS host with the relevant local tool installed and authenticated.
2. Prefer purpose-built CLIs before GUI automation:
   - Notes: `memo` CLI.
   - Reminders: `remindctl`.
   - Messages: `imsg` CLI.
   - Find My: FindMy.app / configured Find My bridge.
3. Use GUI/computer-use only when no CLI route exists or the user explicitly asks for app UI actions.
4. Verify side effects by reading the created note/reminder/message status or device list after the action.
5. For user-visible communications, show the exact outgoing text before sending if the recipient or content is ambiguous.

## App-Specific Sections

### Apple Notes

Use the Notes CLI for create/search/edit flows. Treat note titles and folders as user-facing state: list matches before editing if the search could hit multiple notes. Preserve formatting where possible and prefer append/update operations over replacing a note wholesale.

### Apple Reminders

Use reminders for dated tasks, checklists, and recurring obligations. Capture due date, list name, priority, and completion state. After adding or completing a reminder, list the target reminder/list to verify the state changed.

### iMessage / SMS

Use the configured Messages CLI only when the user clearly identifies recipient and message. If the user names a person but the contact lookup is ambiguous, ask for clarification. After sending, report the CLI status or message identifier; do not invent delivery/read receipts.

### Find My

Use Find My workflows for Apple device and AirTag location/status checks. Treat locations as sensitive personal data: provide only what the user asked for and avoid exposing it to unrelated channels.

### macOS Computer Use

Use accessibility/browser/computer-use automation for UI-only actions. Before acting, identify the active app/window and the expected end state. Prefer deterministic menu items, keyboard shortcuts, and AppleScript where possible; verify with a screenshot or CLI state after each high-impact action.

## Package Notes

The previous narrow Apple skills were absorbed into this umbrella. If session-specific command examples are needed, look under `references/absorbed-*` for the archived source package snapshots.

## Common Pitfalls

- Running Apple workflows on a non-macOS Hermes host and pretending they succeeded.
- Editing the wrong note/reminder because a search term matched multiple items.
- Sending a message without resolving recipient ambiguity.
- Reporting Find My data beyond the user's requested scope.
- Using GUI automation when a dedicated CLI provides a verifiable result.

## Verification Checklist

- [ ] Host/platform supports the requested Apple workflow.
- [ ] Required CLI/app is installed and authenticated.
- [ ] Ambiguous recipients, note titles, or reminder names were disambiguated.
- [ ] Side effects were verified by reading back state or capturing UI evidence.
