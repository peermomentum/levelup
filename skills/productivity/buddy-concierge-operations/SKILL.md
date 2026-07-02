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
Bot checks @mombud with Telegram getChatMember
↓
Bot checks Airtable Team Roster by Telegram username/link
↓
Bot only allows if Airtable Membership = Current
↓
Bot only allows if Airtable Team Roster = Yes
```

Key Airtable source of truth:

- Base: `appDxJWXndV2Bfec3` — Success Circles / Momentum Buddy roster.
- Roster table: `tbl8EZW9OIJRMs1bf` — `Team Roster`.
- Relevant fields:
  - `Telegram Account`
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
4. Verify logs show:
   ```text
   Connected to Telegram
   Gateway running
   ```
5. Test with the user's own `@successcircles` account before inviting Joseph or members.

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
Membership = Current
Team Roster = Yes
Availability = Available
not self
not already unavailable / already buddied this cycle
```

See `references/buddy-concierge-gate-and-flow.md` for the concrete access-gate and wording details captured from the implementation session.

## Email notification and admin approval expansion

When expanding the buddy workflow to email notifications, preserve the security boundary: Concierge remains member-facing and pairing-only, while main Hermes owns Gmail access. Use Airtable status fields as the handoff between them.

Key design rules:

- Gmail account: `connect@successcircles.com`.
- Preferred Gmail integration: Google OAuth Gmail API scoped to Gmail, configured only in the main Hermes profile; do not store Gmail credentials/tokens in `/opt/data/profiles/buddy-concierge`.
- Concierge sends the Telegram admin-review message after the requester confirms their buddy choice.
- Main Hermes sends the admin email after requester confirmation.
- Member emails are sent only after admin approval.
- Admin approves/rejects by replying to Concierge with requester + requested buddy names:
  ```text
  approve request of [Requester Name] with [Requested Buddy Name]
  reject request of [Requester Name] with [Requested Buddy Name]
  ```
- Do not require admin to paste a profile link; retrieve requester `Profile Link`, member `Email Address`, and `Mobile #` from Airtable `Team Roster`.
- Do not CC `connect@successcircles.com` on member emails; Gmail Sent Mail is the record.

See `references/buddy-concierge-email-approval-workflow.md` for the Airtable fields, status transitions, admin Telegram wording, Gmail handoff, and final email templates.
