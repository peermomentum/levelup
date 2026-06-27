# Buddy Concierge post-intake recommendation workflow

Use this when extending the Success Circles / Momentum Buddy member-facing Concierge bot after access gating is working.

## Design sequence preference

The user prefers one-point-at-a-time design decisions before implementation. For Buddy Concierge changes:
1. Discuss and confirm the design.
2. Update Airtable structure if needed.
3. Then update the Concierge bot instructions/plugin.
4. Test with `@successcircles` before Joseph or other members.

## Airtable storage

Do not create a new Airtable base. Use the existing Success Circles base and create a new table/tab beside `Team Roster`:

- `Buddy Pairing Requests`

Recommended v1 fields:

| Field | Type | Notes |
|---|---|---|
| `Request Name` | single line text | Primary field. |
| `Requesting Member` | linked record to `Team Roster` | Member making request. |
| `Telegram Username` | single line text | Backup identity. |
| `Cycle` | single line text | Example date range. |
| `Person In Mind` | single line text | Name typed by member. |
| `Requested Buddy` | linked record to `Team Roster` | Specific requested person if found. |
| `Goals / Focus Areas` | long text | Intake answer. |
| `Preferred Buddy Type` | single line text | Intake answer. |
| `Preferred Cadence` | single line text | Intake answer. |
| `Upcoming Context` | long text | Intake answer. |
| `Intake Summary` | long text | Bot summary. |
| `Recommended Buddies Shown` | linked records to `Team Roster`, multiple | History of options shown. |
| `Rejected Suggestions` | linked records to `Team Roster`, multiple | Only people explicitly rejected. |
| `Selected Buddy` | linked record to `Team Roster` | Person member chose/confirmed. |
| `Adjustment Notes` | long text | Feedback after “I don’t like these.” |
| `Status` | single select | Workflow state. |
| `Admin Notes` | long text | Internal notes. |
| `Admin Notified` | checkbox | Whether backup alert was sent. |
| `Created By` | single select | `Concierge` / `Admin`. |
| `Created At` | created time | Airtable automatic timestamp. |
| `Last Updated` | last modified time | Airtable automatic timestamp. |

Recommended `Status` options:
- `Intake Started`
- `Intake Complete`
- `Recommendations Shown`
- `Member Requested Other Options`
- `Pending Admin Review`
- `Pending Buddy Confirmation`
- `Confirmed`
- `Declined`
- `Cancelled`

## Access vs candidate eligibility

Keep these separate:

### Concierge access gate
Only allow users who pass all checks:
- Telegram `getChatMember` shows member/admin/creator in `@mombud`.
- Airtable `Membership = Current`.
- Airtable `Team Roster = Yes`.

`Reserve` members do **not** get Concierge access unless the user explicitly changes this policy.

### Candidate recommendation eligibility
A candidate can be considered if:
- `Membership = Current` or `Reserve`.
- `Team Roster = Yes`.
- Normally `Availability = Available`.
- `Availability = Reserve - Potentially Available` is only used as backup: odd pool, explicit strategic request, or no strong available candidate.
- Not the requester.
- Not already rejected in this request.
- Not already paired/unavailable this cycle.
- No Do-Not-Pair / Unpairs conflict.
- Not paired with requester in the last 60 days unless Re-Up/admin override.
- At least one overlapping 30-minute availability window.

10x compatibility:
- If requester `10x Player? = Yes`, candidate may be `Yes`, `No`, or blank.
- If requester `10x Player? = No` or blank, candidate must be `No` or blank; candidate cannot be `Yes`.

## Scoring rules from Joseph's protocol

After hard filters, score/rank by:

| Priority | Rule | Weight |
|---|---:|---:|
| 1 | Explicit user request / Re-Up / specific target | +1000 |
| 2 | 10x / strategic peer alignment | +500 |
| 3 | Sensitive personal context | +300 |
| 4 | Accountability style sync | +150 |
| 5 | Schedule breadth / tight-window priority | +100 |
| 6 | Thematic synergy / shared programs / industry fit | +50 |

Do not expose sensitive/internal notes to members. Use privacy-safe reasons only.

## Member response flows

All finalized choices become `Pending Admin Review`; the bot must not silently confirm pairings.

- Member selects a recommended name: re-check eligibility, save `Selected Buddy`, status `Pending Admin Review`, admin note “Member selected from recommended list.”
- Member asks for a specific person: search roster; if found, save `Requested Buddy`; status `Pending Admin Review`; offer to also show other options. If not found or not clearly eligible, offer to save as special admin-review request and/or show alternatives.
- Member says “I don’t like these”: mark previously shown names as `Rejected Suggestions`, ask what to adjust, save `Adjustment Notes`, status `Member Requested Other Options`.
- Member says “show me others”: do **not** mark previous options rejected; append new names to `Recommended Buddies Shown`, exclude already-shown from the next set, status `Recommendations Shown`.
- Member says “you choose”: pick highest-scoring candidate, explain briefly, ask for confirmation first. After confirmation, save `Selected Buddy`, status `Pending Admin Review`, admin note “Concierge selected highest-scoring candidate after member said you choose.”

## Admin backup notification

When a request reaches `Pending Admin Review`, send a private Telegram backup alert to `@successcircles` / Telegram ID `110031638`.

Template:

```text
New Buddy Pairing Request — Pending Admin Review

Member: [Member Name]
Telegram: @[username]
Request type: [Selected recommendation / Specific requested person / You choose / Special request]
Requested buddy: [Name if any]
Status: Pending Admin Review

Intake summary:
[summary]

Recommended options shown:
1. [Name]
2. [Name]
3. [Name]

Member notes:
[notes]

Airtable request:
[link to record]
```

Member-facing message should remain simple: saved for Success Circles admin review; not confirmed yet; Success Circles will confirm availability and next steps.
