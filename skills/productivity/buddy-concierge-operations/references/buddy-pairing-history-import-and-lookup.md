# Buddy Pairing History import + lookup notes

Use this reference when importing historical Momentum Buddy cycles from Excel workbooks and wiring Concierge to answer dated past-buddy questions.

## Airtable source of truth

Base: `appDxJWXndV2Bfec3`

Tables:

- `Team Roster` — `tbl8EZW9OIJRMs1bf`
- `Buddy Pairing Requests` — `tbl4VxUqYbtg0knlP`
- `Buddy Pairing History` — `tblgShzMSniKPOXba`

`Buddy Pairing History` fields used by Concierge/history import:

- `Pairing Name` — primary text field
- `Buddy Pairing Type` — single select: `Duo`, `Triad`
- `Member A` — linked Team Roster record
- `Member B` — linked Team Roster record
- `Member C` — linked Team Roster record; only populated for triads
- `Cycle Start Date` — date
- `Cycle End Date` — date
- `Cycle Label` — original Excel sheet/tab label or current Concierge cycle label
- `Status` — historical imports use `Completed`; future Concierge-approved requests use `Active` initially
- `Source` — `Historical Excel Import`, `Concierge Approved Request`, or `Manual Admin Entry`
- `Source Sheet / Tab`, `Source File`, `Imported At`, `Notes`, `Request Record`

## Historical Excel import rules

User uploaded annual Excel files (`2024.xlsx`, `2025.xlsx`, `2026.xlsx`) where each cycle is a sheet/tab. The tab name carries the cycle date range, e.g. `Jun 28 - Jul 11`, `Dec 28 - Jan 10`, `July 12 - 25`.

Import algorithm:

1. Read workbook sheet names and skip sheet `X` / `x`.
2. Parse cycle dates from sheet name using the file year.
   - Same-month example: `July 12 - 25` in `2026.xlsx` → `2026-07-12` to `2026-07-25`.
   - Cross-month example: `Jun 28 - Jul 11` in `2026.xlsx` → `2026-06-28` to `2026-07-11`.
   - Cross-year example: `Dec 28 - Jan 10` in `2026.xlsx` → `2025-12-28` to `2026-01-10`.
3. Detect the header row (`NAME`, `EMAILS`, `NOTES`) because 2024 can use shifted columns (`E/F/G`) while later files often use `D/E/F`.
4. Treat blank rows as separators between buddy groups.
5. Treat a row named exactly or effectively `PAUSED TEMPORARILY:` as a stop marker. **Do not import any names below it**; they are unpaired members for that cycle, not pairings.
6. Import 2-person groups as one `Duo` record with `Member A` and `Member B`; leave `Member C` blank.
7. Import 3-person groups as one `Triad` record with `Member A`, `Member B`, and `Member C` populated. Do **not** expand triads into three separate pair-combination rows.
8. Skip single/no-partner groups unless the user explicitly asks to preserve them elsewhere; they are not buddy-pairing history.
9. Match workbook names conservatively to Team Roster, preferring email match, then normalized full name, then unique first+last match. Do not create new roster members during import.
10. Set historical rows to:
    - `Status = Completed`
    - `Source = Historical Excel Import`

Observed 2024–2026 import results after applying these rules:

- 837 historical pairing records imported
- 828 Duo records
- 9 Triad records
- 2 single/no-partner rows skipped: Elaine Williams in `2026.xlsx` / `Feb 8 - 21`; Marc Levine in `2024.xlsx` / `Oct 20 - Nov 2`
- 0 unmatched roster names

After import, 3 blank manually-created `Buddy Pairing History` rows were deleted with explicit user approval.

## Concierge lookup behavior

The member-facing plugin tool `buddy_concierge_pairing` supports:

```text
action = lookup_pairing_history
requester_record_id = [verified Team Roster record]
buddy_name = optional specific partner name
limit = optional, default 10
```

Use this action for member questions like:

- “Who was my last buddy?”
- “When did I last buddy with [Name]?”
- “Show my past buddies with dates.”
- “Who was my buddy in [cycle/date]?”

Response fields:

- `most_recent` — newest matching Duo/Triad history row
- `history` — newest rows up to `limit`
- each row includes `cycle_start_date`, `cycle_end_date`, `cycle_label`, `buddy_pairing_type`, and `partners`
- each partner includes `display_name`, e.g. `David Vogel (available)`

For triads, list both other members from `partners`.

Do not expose raw Airtable record IDs, private roster notes, emails, phone numbers, membership statuses, or full roster data.

## Availability display + requestability

For member-facing past/favorite/history output:

```text
Availability = Available → display as available
Availability = Reserve - potentially available → display as available
Everything else → display as unavailable
```

Only members whose Airtable `Availability` is exactly `Available` or `Reserve - potentially available` may be recommended/suggested/requested as a buddy. A past/favorite/history buddy shown as `unavailable` must not have a request email queued; ask the member to choose an available option, see other recommendations, or type `no preference`.

## Future approved-request writeback

Main Hermes script:

```text
/opt/data/scripts/buddy-concierge-email-watcher.py
```

Cron job:

```text
Buddy Concierge member-confirmed request email sender
job_id = 53cbeeb71fa6
schedule = every 2 minutes
```

After the requester confirms a requestable buddy, the email watcher sends one email to the requested buddy with the requester CC'd and creates a `Buddy Pairing History` record with `Status = Requested` for the pending pairing:

- `Buddy Pairing Type = Duo`
- `Member A = requester`
- `Member B = requested buddy`
- `Member C = blank`
- `Status = Active`
- `Source = Concierge Approved Request`
- `Request Record = linked Buddy Pairing Requests record`

The current implementation parses `Cycle` labels of the form `YYYY-MM-DD to YYYY-MM-DD` when available; otherwise it stores a fallback `Cycle Label` based on the approved request ID.

## Verification checklist

After import or code changes, verify:

1. Plugin compiles:
   ```bash
   python3 -m py_compile /opt/data/profiles/buddy-concierge/plugins/buddy_concierge_gate/__init__.py
   ```
2. Email watcher compiles:
   ```bash
   python3 -m py_compile /opt/data/scripts/buddy-concierge-email-watcher.py
   ```
3. Email watcher dry-run is clean:
   ```bash
   python3 /opt/data/scripts/buddy-concierge-email-watcher.py --dry-run --verbose
   ```
4. Airtable queues are clean:
   - pending admin-review = 0 unless real requests exist
   - approved-needs-email = 0 unless newly approved requests are waiting
   - failed email = 0
5. `Buddy Pairing History` historical rows have no missing required values for Duo/Triad.
6. Live lookup smoke tests return realistic results for a member with known history, including at least one Triad member if possible.
7. Restart only the `buddy-concierge` gateway and confirm logs show `Connected to Telegram` and `Gateway running with 1 platform(s)`.
