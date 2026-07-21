# Buddy Pairing History table pattern

Use this when Success Circles wants Concierge to answer dated past-buddy questions such as:

- "Who was my last buddy?"
- "When did I last buddy with [Name]?"
- "Show me my past buddies with dates."
- "Who was my buddy during [cycle/date]?"

## Durable design decision

Do not store dated pairing history only in `Team Roster` → `Past Buddies` long text. Keep `Past Buddies` as a human-readable/cache field if useful, but use a normalized Airtable table as the source of truth.

Use the Airtable table in the existing Success Circles base:

```text
Buddy Pairing History
Table ID: tblgShzMSniKPOXba
```

Each row represents one buddy pair for one cycle.

## Recommended fields

| Field | Type | Purpose |
|---|---|---|
| `Pairing Name` | Single line text / primary | Example: `Maria Santos ↔ David Rush — 2026-06-26 to 2026-07-10` |
| `Member A` | Link to `Team Roster` | First member in pair |
| `Member B` | Link to `Team Roster` | Second member in pair |
| `Cycle Start Date` | Date | Start date parsed from Excel sheet/tab name |
| `Cycle End Date` | Date | End date parsed from Excel sheet/tab name |
| `Cycle Label` | Single line text | Original cycle label/tab name |
| `Status` | Single select | `Completed`, `Active`, `Cancelled`, `Test`, `Imported` |
| `Source` | Single select | `Historical Excel Import`, `Concierge Approved Request`, `Manual Admin Entry` |
| `Source Sheet / Tab` | Single line text | Original Excel tab name |
| `Source File` | Single line text | Uploaded workbook filename |
| `Imported At` | Date/time | Import timestamp |
| `Notes` | Long text | Admin/import notes |
| `Request Record` | Link to `Buddy Pairing Requests` | For future Concierge-approved pairings |

## Historical Excel import rule

The user clarified: when an Excel tab shows a cycle and two people were paired, treat that historical pairing as completed:

```text
Status = Completed
Source = Historical Excel Import
```

Use the Excel sheet/tab name as the source for the cycle date range. Parse it into:

```text
Cycle Start Date
Cycle End Date
Cycle Label
Source Sheet / Tab
```

If a member in the workbook is not confidently matched to `Team Roster`, skip or report the row rather than creating a bad link.

## Future Concierge-approved pairings

When Admin approves a new Concierge request, main Hermes should create a `Buddy Pairing History` row in addition to sending emails:

```text
Status = Active
Source = Concierge Approved Request
Request Record = [linked Buddy Pairing Requests record]
```

When the cycle is completed, Success Circles can mark the history row:

```text
Status = Completed
```

## Airtable permission pitfall

The current Airtable token may have schema read and record write permission but still fail to create tables via the meta API with:

```text
403 INVALID_PERMISSIONS_OR_MODEL_NOT_FOUND
```

If table creation fails, do not treat this as a blocker for the overall design. Give the user exact manual Airtable table-creation steps and then verify/import once the table exists.

## Bot answer behavior

Concierge should query `Buddy Pairing History` first for dated history. It may fall back to `Team Roster` → `Past Buddies` only when no structured history exists.

When showing past/favorite buddies as potential choices, include a member-facing availability label:

```text
[Name] (available)
[Name] (unavailable)
```

Treat Airtable `Availability = Available` and `Availability = Reserve - potentially available` as member-facing `available`. All other Availability values display as `unavailable`. Do not recommend, request, or submit unavailable people for admin review; ask the member to choose an available option, view other recommendations, or type `no preference`.

Member-facing answer examples:

```text
Your most recent recorded Momentum Buddy was [Buddy Name] for the cycle [Cycle Start Date] to [Cycle End Date].
```

```text
You were last recorded as buddies with [Buddy Name] from [Cycle Start Date] to [Cycle End Date].
```

```text
Here are your most recent recorded buddies:
1. [Name] — [Cycle Start Date] to [Cycle End Date]
2. [Name] — [Cycle Start Date] to [Cycle End Date]
```
