---
name: buddy-concierge-operations
description: Operate and improve the Success Circles Buddy Concierge bot across Hermes profile, Telegram access gates, Airtable roster checks, and pairing workflow design.
version: 1.0.0
author: Hermes Agent
license: private
tags: [success-circles, buddy-concierge, telegram, airtable, hermes-profile, pairing]
---

# Buddy Concierge Operations

Use this skill when configuring, troubleshooting, or improving the Success Circles / Momentum Buddy Concierge bot, especially `@BuddyConciergeBot`, the `buddy-concierge` Hermes profile, Telegram `@mombud` access control, Airtable roster eligibility, and post-intake pairing flow.

## Core paths and boundaries

- Active profile path on the VPS: `/opt/data/profiles/buddy-concierge`.
- Main behavior prompt: `/opt/data/profiles/buddy-concierge/SOUL.md`.
- Concierge behavior skill in that profile: `/opt/data/profiles/buddy-concierge/skills/productivity/buddy-concierge/SKILL.md`.
- Access gate plugin: `/opt/data/profiles/buddy-concierge/plugins/buddy_concierge_gate/`.
- Do not use broad process-kill commands. Restart only the `hermes --profile buddy-concierge gateway run` process.
- The member-facing Concierge bot must remain pairing-only; do not give it general Hermes/admin/server capabilities.

## Access gate rule

The intended access flow is:

```text
User messages Concierge
↓
Bot captures Telegram numeric user ID, display name, and public username if present
↓
Bot checks @mombud with Telegram getChatMember using the numeric Telegram user ID
↓
Bot checks Airtable Team Roster by stored Telegram User ID first, then public username / Telegram Account if present
↓
If no confident roster match exists, bot asks the member to tap Telegram's native “Share my phone number” contact button
↓
Bot accepts the contact only if Telegram contact.user_id equals the sender's Telegram user ID, then normalizes the phone number and matches it to Team Roster `Mobile #`
↓
If exactly one active roster record matches, bot stores the Telegram User ID and verification metadata on Team Roster for future access
↓
Bot only allows if Airtable Membership = Current
↓
Bot only allows if Airtable Team Roster = Yes
```

Display-name fallback is intentionally narrow because Telegram display names are user-editable: it requires a specific two-word-or-more display name that uniquely matches one active roster record by normalized full name or first+last name. Prefer the durable identity path: stored Telegram User ID, public `@username` when available, or explicit contact-share match against Team Roster `Mobile #`. Members should not be asked to create a public Telegram username just for Concierge access.

Key Airtable source of truth:

- Base: `appDxJWXndV2Bfec3` — Success Circles / Momentum Buddy roster.
- Roster table: `tbl8EZW9OIJRMs1bf` — `Team Roster`.
- Relevant fields:
  - `Telegram Account`
  - `Mobile #`
  - `Telegram User ID` (single line text; Concierge/Hermes may update only for identity verification)
  - `Telegram Verified At` (date/time; Concierge/Hermes may update only for identity verification)
  - `Telegram Verification Method` (single line text; Concierge/Hermes may update only for identity verification, e.g. `username`, `shared_mobile`, `admin_manual`)
  - `Telegram Display Name` (single line text; optional troubleshooting snapshot; Concierge/Hermes may update)
  - `Telegram Username` (single line text; optional snapshot; Concierge/Hermes may update)
  - `Membership` with active value `Current`.
  - `Team Roster` with allowed value `Yes`.
  - `Availability` for pairing-cycle eligibility, not front-door access.

## Critical wording pitfall

Do **not** tell users they need to “update Telegram” or imply the Telegram app/account needs changing when the real issue is Airtable eligibility.

Preferred blocked wording:

```text
Welcome to the Buddy Concierge!

I verified the @mombud membership step, but your Success Circles roster record is not currently marked as active for Concierge access. Concierge access requires Airtable Membership = Current and Team Roster = Yes.
```

If no active matching roster record is found:

```text
Welcome to the Buddy Concierge!

I verified the @mombud membership step, but I could not find a matching active Success Circles roster record. This Concierge is currently available only to people whose Airtable roster record is marked Membership = Current and Team Roster = Yes.
```

The bot may mention Telegram only for the `@mombud` membership check or for matching the Telegram username/link to Airtable; avoid phrasing that sounds like members must update Telegram.

## Gateway plugin implementation notes

- A `pre_gateway_dispatch` hook can gate messages before the agent sees them.
- Make hook signatures future-proof by accepting `**kwargs`; Hermes may pass fields such as `telemetry_schema_version`.
- On success, rewrite inbound messages with a `[Buddy Concierge verified access]` block containing compact metadata, so the model does not re-check membership.
- On denial, send a Telegram denial message directly and return `{"action": "skip", ...}`.
- Include defense-in-depth `pre_tool_call` blocking for member-facing sessions: block terminal/file/code/cron/memory/delegation/admin tools unless explicitly redesigning the bot.

## Kai naming and Telegram identity

The member-facing name of `@BuddyConciergeBot` is **Kai**. The bot should introduce itself as Kai in the verified welcome/intake flow and in access-gate denial/temporary-error messages. When the user says “Kai” or “Concierge bot,” treat that as referring to `@BuddyConciergeBot`.

Primary files to update for member-facing naming/copy:

- `/opt/data/profiles/buddy-concierge/SOUL.md` — main persona and verified welcome/intake wording.
- `/opt/data/profiles/buddy-concierge/skills/productivity/buddy-concierge/SKILL.md` — pairing behavior skill and welcome templates.
- `/opt/data/profiles/buddy-concierge/plugins/buddy_concierge_gate/__init__.py` — pre-agent access-gate denial/temporary-verification messages.

Recommended verified welcome opening:

```text
Hi, I’m Kai, your Success Circles Buddy Concierge.

I verified your Momentum Buddy Reminders access.
```

Recommended blocked/temporary opening:

```text
Hi, I’m Kai, the Success Circles Buddy Concierge.
```

Telegram handle guidance: prefer keeping the stable username `@BuddyConciergeBot` during rollout and branding the bot as Kai in the Telegram display name/messages. If changing via BotFather, low-risk changes are `/setname` to `Kai — Buddy Concierge` and `/setdescription`; avoid changing the `@...` username until links, SOPs, onboarding copy, and member instructions have been updated. Telegram bot usernames generally need to end in `bot`, so `@KaiBuddyConcierge` may be invalid; `@KaiBuddyConciergeBot` is the plausible later rename if truly needed.

## Restart and verification pattern

1. Syntax-check plugin edits:
   ```bash
   python3 -m py_compile /opt/data/profiles/buddy-concierge/plugins/buddy_concierge_gate/__init__.py
   ```
2. Stop only the profile-specific gateway process:
   ```bash
   ps aux | grep "hermes --profile buddy-concierge gateway run" | grep -v grep
   ```
   Then terminate the specific PID for that profile only.
3. Restart narrowly:
   ```bash
   cd /opt/hermes && /opt/hermes/.venv/bin/hermes --profile buddy-concierge gateway run
   ```
   If Hermes refuses an in-gateway restart with “Refusing to restart the gateway from inside the gateway process,” do not use broad `pkill`. Use an outside supervisor path such as a one-shot scheduler/cron script that targets only the exact buddy-concierge gateway command, or ask the user to run `/opt/hermes/.venv/bin/hermes --profile buddy-concierge gateway restart` from a separate shell.
4. Verify logs show:
   ```text
   Active profile: buddy-concierge
   Connected to Telegram
   Gateway running
   ```
5. Test with the user's own `@successcircles` account before inviting Joseph or members.

## Past/favorite buddies lookup

The member-facing `buddy_concierge_pairing` tool includes `action = lookup_past_favorite_buddies`. When a verified member asks for past buddies / favorite buddies / draft picks during the “someone in mind” intake question, the bot reads that member’s own Team Roster `Past Buddies` and `Draft Picks / Fav Buddies` long-text fields, matches them against Team Roster names, and returns `clear_matches` plus lower-confidence `possible_matches` for first-name/last-name-only text. The bot should show names as choices using `display_name` or `name (availability_label)`, e.g. `David Vogel (available)` or `Jorge Colon (unavailable)`. Airtable Availability values `Available` and `Reserve - potentially available` display as `available`; all other values display as `unavailable`. Ask the member to choose when partial matches exist, and never expose raw roster notes, contact details, membership status, or the full roster. A past/favorite buddy shown as unavailable must not be submitted/requested; ask the member to choose an available option, see other recommendations, or type `no preference`.

For bulk `Past Buddies` imports from CSV, follow `references/past-buddies-csv-import.md`: confirm overwrite/merge semantics, conservatively match CSV member names to Airtable `Name`, back up old values, PATCH in batches of 10, verify by readback, and report unmatched/ambiguous names without creating new roster members.

For dated past-buddy questions, use the normalized `Buddy Pairing History` table rather than stuffing dates into the `Past Buddies` text field. The live table is `tblgShzMSniKPOXba`. Concierge supports `buddy_concierge_pairing` action `lookup_pairing_history` for “Who was my last buddy?”, “When did I last buddy with [Name]?”, and “Show my past buddies with dates.” It returns `most_recent` and `history` records with cycle dates, Duo/Triad type, and partner `display_name` values. See `references/buddy-pairing-history.md` for the table design and `references/buddy-pairing-history-import-and-lookup.md` for the 2024-2026 Excel import rules, `PAUSED TEMPORARILY:` stop marker, Duo/Triad/Member C handling, availability display/requestability, and future Concierge-approved pairing writeback.

## Post-intake recommendation flow v1

When the authorized member completes intake, the bot should not immediately confirm a buddy pair. The safer v1 flow is:

1. Summarize the intake answers.
2. Ask the member to confirm the summary.
3. Check eligible candidates from Airtable.
4. Show 2–3 privacy-safe recommendations with brief fit reasons.
5. Handle member choices:
   - selected recommended name → re-check availability, mark preferred/pending, not confirmed;
   - specific requested name → search and eligibility-check that person first;
   - “I don’t like these” → ask what to adjust and save objections;
   - “show me others” → exclude already-shown candidates and present next options;
   - “you choose” → pick the top candidate and ask final confirmation.
6. Create or update a pairing request / pending confirmation record; only mark confirmed after both members or an admin confirms.

Candidate eligibility v1:

```text
Membership = Current or Reserve
Team Roster = Yes
Availability = Available OR Reserve - potentially available
not self
not already unavailable / already buddied this cycle
```

Only members whose Airtable Availability is exactly `Available` or `Reserve - potentially available` may be recommended/suggested/requested. Display `Reserve - potentially available` as member-facing `available`; all other Availability values display as `unavailable` and are not requestable.

See `references/buddy-concierge-gate-and-flow.md` for the concrete access-gate and wording details captured from the implementation session.

## Email notification and admin approval expansion

When expanding or describing the buddy workflow's email notifications, preserve the security boundary: Concierge remains member-facing and pairing-only, while main Hermes owns Gmail access. Use Airtable status fields as the handoff between them.

Before telling the user that member emails are live, distinguish the documented/intended design from actual implementation: inspect the Concierge plugin/admin actions, Airtable `Buddy Pairing Requests` email-status fields, main-profile scripts, and cron jobs/watchers. If only fields/templates exist but no watcher/sender is active, say the email workflow is documented/prepared but not fully automatic yet.

Key design rules:

- Gmail account: `connect@successcircles.com`.
- Preferred Gmail integration: Google OAuth Gmail API scoped to Gmail, configured only in the main Hermes profile; do not store Gmail credentials/tokens in `/opt/data/profiles/buddy-concierge`.
- Concierge sends the Telegram admin-review message after the requester confirms their buddy choice.
- Main Hermes sends the admin email after requester confirmation.
- Member emails are sent only after admin approval.
- When asked what emails are sent after approval, provide the two member templates from `references/buddy-concierge-email-approval-workflow.md`: requester notification (`Your Momentum Braintrust Buddy pairing request has been sent`) and requested-buddy request (`Momentum Braintrust Buddy Pairing Request from [Requester Name]`). Include the 5-minute alignment-call instruction and the requirement to let Success Circles know if both agree.
- Admin approves/rejects by replying to Concierge with requester + requested buddy names. This is the intended admin workflow and should not require manual Airtable editing:
  ```text
  approve request of [Requester Name] with [Requested Buddy Name]
  reject request of [Requester Name] with [Requested Buddy Name]
  ```
- The Concierge plugin handles these Telegram admin commands directly in `pre_gateway_dispatch`: it finds exactly one pending `Buddy Pairing Requests` record matching requester + requested buddy, then sets `Admin Approval Status`, `Admin Decision At`, `Admin Decision By`, `Admin Approval Raw Message`, `Status`, `Last Bot Action`, and `Member Email Status`.
- Approval sets `Member Email Status = Needs Sending`; rejection sets `Member Email Status = Not Sent - Rejected`.
- Main-profile script `/opt/data/scripts/buddy-concierge-email-watcher.py` polls approved requests and sends member emails from the Gmail OAuth account `/opt/data/google_token.json` (`connect@successcircles.com`). It is scheduled by cron job `Buddy Concierge approved-request email sender` (`job_id=53cbeeb71fa6`) every 2 minutes, no-agent/silent when there is no work.
- Concierge should not need broad Team Roster write access for approvals/rejections. Approval/rejection primarily updates `Buddy Pairing Requests`; Team Roster writes are limited to the Telegram verification fields only.
- Do not require admin to paste a profile link; the email watcher retrieves requester `Profile Link`, member `Email Address`, and `Mobile #` from Airtable `Team Roster` linked records.
- Do not CC `connect@successcircles.com` on member emails; Gmail Sent Mail is the record.
- When Success Circles confirms pending/admin-review records are only trial/test records, do not delete them. Mark them resolved/cancelled with non-email-sending statuses; see `references/test-request-cleanup.md`.

See `references/buddy-concierge-email-approval-workflow.md` for the Airtable fields, status transitions, admin Telegram wording, Gmail handoff, and final email templates. Use `references/buddy-concierge-sop.md` for a copy-ready Success Circles Team SOP with exact member/admin/bot phrases, backend steps, status transitions, verification checks, and email copy. Use `templates/member-onboarding-email.md` when drafting a concise member onboarding email for how to use `@BuddyConciergeBot` without overthinking.
