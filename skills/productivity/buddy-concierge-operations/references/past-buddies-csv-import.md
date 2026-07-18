# Past Buddies CSV import to Airtable Team Roster

Use when the user provides a spreadsheet of member names and historical buddies to populate the Success Circles / Momentum Buddy `Team Roster` `Past Buddies` field.

## Source of truth and write target

- Base: `appDxJWXndV2Bfec3`
- Table: `tbl8EZW9OIJRMs1bf` (`Team Roster`)
- Write field: `Past Buddies` (`multilineText`)
- CSV columns observed: `MEMBER NAME`, `PAST BUDDIES`

## Safe import workflow

1. Confirm the intended write mode: overwrite vs append/merge. For this workflow, overwrite means the CSV is the source of truth for matched rows.
2. Inspect Airtable schema before writing and verify `Past Buddies` exists and is writable.
3. Parse the CSV with Python `csv.DictReader`; preserve the `PAST BUDDIES` cell exactly as comma-separated text.
4. Fetch all Team Roster records with pagination, selecting at least `Name`, `Past Buddies`, `Membership`, and `Team Roster`.
5. Match CSV member names to Airtable names conservatively:
   - Normalize case, punctuation, whitespace, accents, and curly quotes.
   - Remove parenthetical Airtable suffixes such as `(10x Owner)` / `(10x)`.
   - Ignore honorifics such as `Dr.` for matching.
   - Allow first+last matching where middle names or suffixes differ.
   - Treat `Chris`/`Christopher` as a known first-name variant only when the last name also matches.
   - Do not update ambiguous matches; report them.
6. Write a before-overwrite backup with record IDs, Airtable names, CSV names, old values, and new values.
7. PATCH updates in Airtable batches of 10 records, respecting rate limits.
8. Verify by reading back a deterministic sample of updated records and comparing the exact `Past Buddies` value to the CSV value.
9. Report counts: CSV rows, Airtable records fetched, matched/updated rows, unchanged rows, unmatched ignored names, ambiguous ignored names, backup/report paths, and verification result.

## Concierge follow-up

After importing `Past Buddies`, verify the member-facing `lookup_past_favorite_buddies` path reads both `Past Buddies` and `Draft Picks / Fav Buddies`. It should return privacy-safe name matches only and must not expose raw roster notes or contact details.

## Pitfalls

- Do not create new roster members from a historical buddy CSV unless the user explicitly asks; unmatched CSV names can be ignored/reported.
- Do not match only by first name or last name for writes.
- Airtable record read endpoints may reject `fields[]` filtering on single-record URLs; read the record normally and compare the returned field values.
- Restart the Buddy Concierge gateway narrowly/profile-specifically only after code/prompt changes, not after pure Airtable data updates.