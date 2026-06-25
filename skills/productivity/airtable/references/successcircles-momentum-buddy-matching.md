# SuccessCircles / Momentum Buddy matching pattern

Use this reference when the Airtable base is the Success Circles / Momentum Buddy roster and the task is to find available suitable buddies or generate the two-week pairing cycle.

## Known source of truth

- Base: `appDxJWXndV2Bfec3` — `Success Circles🔑Momentum Buddy Roster`
- Roster table: `tbl8EZW9OIJRMs1bf` — `Team Roster`
- Program context: SuccessCircles and https://www.momentumbuddy.com
- Pairing cadence: every 2 weeks

Key roster fields observed in `Team Roster`:

- `Name`
- `Email Address`
- `Mobile #`
- `Program`
- `Telegram Account`
- `Occupation / Vocation`
- `LinkedIn Profile`
- `Time Zone`
- `Member Since`
- `What time(s) are you free for your Huddle Calls?`
- `Area(s) of life you want to have support & accountability?`
- `What are you looking for in a Momentum Buddy?`
- `Draft Picks / Fav Buddies`
- `Notes From Success Circles`

## Recommended Airtable additions

Add these fields to `Team Roster` if absent:

- `Buddy Status` — single select: `Available`, `Pending Confirmation`, `Confirmed`, `Paused`, `Not Participating`.
- `Has Buddy` — checkbox.
- `Current Buddy` — linked record to `Team Roster`.
- `Current Buddy Cycle` — text or linked record to a cycle table.
- `Available for Pairing` — formula:

```text
IF(
  OR(
    {Has Buddy},
    {Buddy Status} = "Confirmed",
    {Buddy Status} = "Pending Confirmation",
    {Buddy Status} = "Not Participating",
    {Buddy Status} = "Paused"
  ),
  "No",
  "Yes"
)
```

Create a view named `Available for Buddy Matching` filtered to `Available for Pairing = Yes`.

## Recommended pairing history table

Create a separate `Buddy Pairings` table to support cooldowns, continuation, and auditability:

- `Cycle` — e.g. `2026-07-01 to 2026-07-14`.
- `Member 1` — linked record to `Team Roster`.
- `Member 2` — linked record to `Team Roster`.
- `Status` — `Proposed`, `Pending Confirmation`, `Confirmed`, `Declined`, `Completed`, `Cancelled`.
- `Match Score` — number.
- `Match Reasons` — long text.
- `Risk / Concern Notes` — long text.
- `Member 1 Confirmed` — checkbox.
- `Member 2 Confirmed` — checkbox.
- `Both Confirmed` — formula:

```text
IF(AND({Member 1 Confirmed}, {Member 2 Confirmed}), "Yes", "No")
```

Optional: `Continued Pairing`, `Member 1 Wants Continue`, `Member 2 Wants Continue`, `Created By`.

## Matching workflow

1. Load base schema first and resolve table/field IDs when mutating.
2. Read the available roster view or filter members where `Available for Pairing = Yes` / `Buddy Status = Available`.
3. Exclude anyone already `Confirmed`, `Pending Confirmation`, `Paused`, or `Not Participating`.
4. Read `Buddy Pairings` history to avoid recent repeats unless both members explicitly requested continuation.
5. Score candidate pairs with reasons:
   - Time zone compatibility.
   - Huddle-call availability overlap.
   - Support/accountability area alignment.
   - Complementary strengths from `Occupation / Vocation` and free-text goals.
   - Stated preferences from `What are you looking for...` and `Draft Picks / Fav Buddies`.
   - Program compatibility.
   - Manual notes / exclusions.
6. Produce a ranked recommendation list for a single member, or a non-overlapping set of proposed pairs for the cycle.
7. Before holding a match, set both members to `Pending Confirmation` and create a `Buddy Pairings` record with `Status = Proposed` or `Pending Confirmation`.
8. Only mark `Confirmed` after both members confirm. Then set `Has Buddy = true`, `Current Buddy = [other member]`, and `Current Buddy Cycle = [cycle]` for both roster records.
9. If either declines, mark the pairing declined/cancelled and restore eligible members to `Available`.

## Member-facing access pattern

Prefer an Airtable Interface or simple form for members instead of exposing the full roster. Members should be able to update only their own pairing inputs:

- Availability this cycle.
- Preferred call times.
- Time zone.
- Areas where they want support/accountability.
- What they want in a buddy.
- Preferred/favorite buddies.
- Do-not-pair notes if needed.
- Continue with current buddy? yes/no.
- Confirm/decline proposed buddy.

Members should only see contact details for a confirmed buddy, not the whole roster.

## Safety rules

- Do not expose the full member roster or all contact details in member-facing responses.
- Do not delete Airtable records as part of matching.
- Do not confirm a pair until both members have confirmed.
- Do not pair someone marked `Paused`, `Not Participating`, `Confirmed`, or `Pending Confirmation`.
- Always include match reasons and any concerns when proposing pairs.
