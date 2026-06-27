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

## Recommended Concierge request-intake table

For member-facing Concierge intake, create a separate table in the same base named `Buddy Pairing Requests` (do not create a new base). This table captures a single member's request, shown recommendations, rejected suggestions, and admin-review state before any official pairing is confirmed.

Recommended fields:

- `Requesting Member` — primary/single line text, human-readable requester name.
- `Telegram Username` — single line text.
- `Cycle` — single line text, e.g. `2026-07-01 to 2026-07-14`.
- `Person In Mind` — long text.
- `Requested Buddy` — single line text for a typed name when an exact roster record is not yet resolved.
- `Requesting Member Record` — linked record to `Team Roster`.
- `Requested Buddy Record` — linked record to `Team Roster`.
- `Goals / Focus Areas` — long text.
- `Buddy Preference This Request` — long text; use this instead of overwriting the member's general roster preference.
- `Cadence This Request` — single select: `Daily`, `Weekly`, `Weekly + SMS daily`, `Flexible / Not sure`, `Use my roster preference`.
- `Upcoming Context` — long text.
- `Intake Summary` — long text.
- `Recommended Buddies Shown` — linked records to `Team Roster`, allow multiple.
- `Rejected Suggestions` — linked records to `Team Roster`, allow multiple.
- `Selected Buddy` — linked record to `Team Roster`.
- `Adjustment Notes` — long text.
- `Recommendation Reasoning` — long text.
- `Status` — single select: `Intake Started`, `Intake Complete`, `Recommendations Shown`, `Member Requested Other Options`, `Pending Admin Review`, `Pending Buddy Confirmation`, `Confirmed`, `Declined`, `Cancelled`.
- `Admin Notes` — long text.
- `Admin Notified` — checkbox.
- `Created By` — single select: `Concierge`, `Admin`, `Manual Import`.
- `Last Bot Action` — single line text, e.g. `intake_complete`, `shown_recommendations`, `submitted_pending_admin_review`.
- `Created At` — created time.
- `Last Updated` — last modified time.

Concierge request workflow:

1. Verify access first: Telegram sender is in `@mombud`, matches `Team Roster`, `Membership = Current`, and `Team Roster = Yes`.
2. Collect intake, summarize it, and ask the member to confirm before writing Airtable.
3. Create/update `Buddy Pairing Requests` with `Status = Intake Complete` and `Created By = Concierge`.
4. Recommend 2–3 eligible roster candidates with concise, non-private reasons. Do not expose the full roster or contact/private notes.
5. If the member chooses a recommendation or names a specific person, set the request to `Pending Admin Review`; do not auto-confirm a match.
6. If they ask for other options, show new recommendations without marking prior options rejected unless they clearly disliked them.
7. If they say they do not like the options, add shown candidates to `Rejected Suggestions`, store `Adjustment Notes`, then rerun recommendations.
8. If they say “you choose,” choose the highest-scoring option and ask for member confirmation before submitting for admin review.
9. Notify the admin when the request reaches `Pending Admin Review`.

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

## Concierge pairing request table pattern

For the Success Circles Concierge bot, keep member profile/default preference data in `Team Roster` and capture each cycle/request in a separate table in the same base, e.g. `Buddy Pairing Requests`. Do **not** create a new base for this workflow.

Recommended `Buddy Pairing Requests` fields:

- `Requesting Member` — primary single-line text, readable requester name.
- `Telegram Username` — single-line text.
- `Cycle` — single-line text, e.g. `2026-07-01 to 2026-07-14`.
- `Person In Mind` — long text for free-form requested person/name.
- `Requested Buddy` — single-line text backup/free-form name.
- `Requesting Member Record` — linked record to `Team Roster`.
- `Requested Buddy Record` — linked record to `Team Roster`.
- `Goals / Focus Areas` — long text.
- `Upcoming Context` — long text.
- `Intake Summary` — long text.
- `Buddy Preference This Request` — long text. Use this even when roster has general preference fields; roster = default preference, request table = current-cycle need.
- `Cadence This Request` — single select: `Daily`, `Weekly`, `Weekly + SMS daily`, `Flexible / Not sure`, `Use my roster preference`.
- `Recommended Buddies Shown` — linked records to `Team Roster`, allow multiple.
- `Rejected Suggestions` — linked records to `Team Roster`, allow multiple.
- `Selected Buddy` — linked record to `Team Roster`.
- `Adjustment Notes` — long text for “I don’t like these” / desired adjustment feedback.
- `Recommendation Reasoning` — long text explaining why candidates were suggested.

Manual setup workflow preferred by the user: guide one Airtable field batch at a time, then verify schema via the metadata API before giving the next batch or updating Concierge bot behavior. If a field already exists in `Team Roster`, distinguish default roster data from request-specific data instead of blindly duplicating the same field name.

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
