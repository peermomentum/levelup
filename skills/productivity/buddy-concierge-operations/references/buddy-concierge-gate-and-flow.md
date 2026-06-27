# Buddy Concierge gate and flow notes

These details came from the implementation/troubleshooting session for the Success Circles Buddy Concierge bot.

## Active profile and files

- Hermes profile: `buddy-concierge`.
- Profile path: `/opt/data/profiles/buddy-concierge`.
- Main prompt: `/opt/data/profiles/buddy-concierge/SOUL.md`.
- Profile-local Concierge skill: `/opt/data/profiles/buddy-concierge/skills/productivity/buddy-concierge/SKILL.md`.
- Access gate plugin: `/opt/data/profiles/buddy-concierge/plugins/buddy_concierge_gate/`.

## Final access policy

A member should reach the pairing intake only when all of these are true:

1. Telegram `getChatMember` says the sender is a member/admin/creator of `@mombud`.
2. Sender's Telegram username/link matches `Team Roster`.`Telegram Account` in Airtable.
3. Airtable `Membership` is `Current`.
4. Airtable `Team Roster` is `Yes`.

Do not use Airtable `Availability` as the front-door access flag. `Availability` is for matching/cycle availability.

## Airtable fields observed

Base/table:

- Base ID: `appDxJWXndV2Bfec3`.
- Roster table ID: `tbl8EZW9OIJRMs1bf`.

Relevant select fields:

- `Membership`: `Current`, `Past`, `Reserve`.
- `Team Roster`: `Yes`, `No`.
- `Availability`: `Available`, `Unavailable - Already Buddied Up Next Cycle`, `Reserve - Potentially Available`, `Travelling / Away This Next Cycle`, `Unavailable`.

## Important bug/pitfall fixed

The first `pre_gateway_dispatch` hook implementation failed because Hermes passed an extra keyword argument such as `telemetry_schema_version`.

Fix pattern:

```python
def pre_gateway_dispatch(event, gateway=None, session_store=None, **kwargs):
    ...
```

Make gateway hook signatures future-proof with `**kwargs`.

## Member-facing wording pitfall

The user objected to wording that sounded like “update Telegram.” Avoid telling members to update Telegram or implying their Telegram app/account is the problem when the real gate is Airtable eligibility.

Use Airtable-specific wording:

```text
I verified the @mombud membership step, but your Success Circles roster record is not currently marked as active for Concierge access. Concierge access requires Airtable Membership = Current and Team Roster = Yes.
```

When no active match exists:

```text
I verified the @mombud membership step, but I could not find a matching active Success Circles roster record. This Concierge is currently available only to people whose Airtable roster record is marked Membership = Current and Team Roster = Yes.
```

## Verification examples from the session

- `@successcircles` / Telegram ID `110031638` passed: `Membership = Current`, `Team Roster = Yes`.
- `@jimmydoromal` / Telegram ID `5697040135` was blocked after the policy was tightened because the Airtable record had `Membership = Reserve`.

## Post-intake v1 design direction

The bot should collect and summarize intake first, then move into recommendations. It should not directly confirm pairings. Recommended statuses/actions should be pending/admin-confirmable until both members or an admin confirms.

Needed future Airtable structure likely includes a separate request/history table such as `Buddy Pairing Requests` or `Buddy Pairings` with fields for requester, intake summary, shown recommendations, rejected suggestions, selected buddy, status, cycle, and admin notes.
