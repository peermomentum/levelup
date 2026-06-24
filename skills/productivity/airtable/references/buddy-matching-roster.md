# Buddy matching roster pattern

Use this reference when an Airtable roster is the source of truth for a buddy/accountability matching workflow.

## Secure connection over messaging

When helping through Telegram or another chat channel, do not ask the user to paste Airtable tokens into chat. Have them create a Personal Access Token at https://airtable.com/create/tokens with the minimum scopes:

- `data.records:read`
- `data.records:write`
- `schema.bases:read`

Then have them grant access only to the specific roster base and install it as:

```bash
mkdir -p ~/.hermes
nano ~/.hermes/.env
# add:
AIRTABLE_API_KEY=pat_your_actual_token_here
chmod 600 ~/.hermes/.env
```

Ask the user to paste only non-secret Airtable IDs from the roster URL:

```text
Base ID: app...
Roster Table ID: tbl...
Roster View ID: viw...
Roster table name:
Roster view name:
```

## Recommended roster fields

Add/confirm these fields in the member roster table:

- `Has Buddy` — checkbox.
- `Buddy Status` — single select: `Available`, `Pending Confirmation`, `Confirmed`, `Paused`, `Not Participating`.
- `Current Buddy` — linked record to the same roster/member table.
- `Current Buddy Cycle` — text or linked cycle record.
- `Available for Pairing` — formula:

```text
IF(
  OR(
    {Has Buddy},
    {Buddy Status} = "Confirmed",
    {Buddy Status} = "Pending Confirmation",
    {Buddy Status} = "Not Participating"
  ),
  "No",
  "Yes"
)
```

Create a view such as `Available for Buddy Matching` filtered to `Available for Pairing = Yes`. The agent usually does not need to modify the view definition; it updates the underlying fields and the view updates automatically.

## Pair confirmation workflow

1. Before proposing/holding a match, set both members to `Buddy Status = Pending Confirmation` so they are temporarily excluded from the available pool.
2. When both confirm, update both roster records:
   - `Has Buddy = true`
   - `Buddy Status = Confirmed`
   - `Current Buddy = [other member rec...]`
   - `Current Buddy Cycle = [cycle]`
3. If someone declines, mark the pairing record declined/cancelled and restore available members:
   - `Has Buddy = false`
   - `Buddy Status = Available`
   - clear `Current Buddy` if appropriate.

## Buddy history table

Use a separate `Buddy Pairings` table for continuation/cooldown rules and auditability. Suggested fields:

- `Cycle`
- `Member 1`
- `Member 2`
- `Status`: `Proposed`, `Pending Confirmation`, `Confirmed`, `Declined`, `Completed`, `Cancelled`
- `Continued Pairing` checkbox
- `Member 1 Wants Continue` checkbox
- `Member 2 Wants Continue` checkbox
- `Both Requested Continue` formula
- `Cycle Number`
- `Notes`

A matching engine should read this history before scoring so it can exclude unavailable members and enforce continuation/cooldown rules.