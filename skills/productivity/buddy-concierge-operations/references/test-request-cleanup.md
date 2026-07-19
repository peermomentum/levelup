# Buddy Concierge test request cleanup

Use when Success Circles confirms that pending `Buddy Pairing Requests` records are test/trial records and should be removed from active admin/email queues without deleting Airtable history.

## Goal

Mark test records as resolved/cancelled so they do not appear in admin-review queues and do not trigger the main Hermes email watcher.

## Safe status update

For each confirmed test record in Airtable `Buddy Pairing Requests`, PATCH these fields:

```text
Status = Cancelled
Admin Approval Status = Rejected
Admin Decision At = [current UTC timestamp]
Admin Decision By = @successcircles
Admin Approval Raw Message = Marked resolved/completed test record per Success Circles admin request; not an actual buddy request.
Member Email Status = Not Sent - Rejected
Admin Email Status = Not Needed
Last Bot Action = test_record_resolved_cancelled
```

Why this shape:

- `Status = Cancelled` removes it from active buddy request work.
- `Admin Approval Status = Rejected` removes it from pending admin-approval filters.
- `Member Email Status = Not Sent - Rejected` prevents the approved-request email sender from ever sending member emails.
- Keeping the record preserves trial/audit history instead of deleting data.

## Verification after cleanup

Check counts in `Buddy Pairing Requests`:

```text
OR({Status}='Pending Admin Review',{Admin Approval Status}='Pending') = 0 or expected active-only count
AND({Admin Approval Status}='Approved', {Member Email Status}='Needs Sending') = 0 or expected active email queue count
{Member Email Status}='Failed' = 0 or known failures only
```

If `Status` or select choices differ, inspect Airtable schema first and choose the closest non-active/non-email-sending values rather than creating ambiguous custom statuses.