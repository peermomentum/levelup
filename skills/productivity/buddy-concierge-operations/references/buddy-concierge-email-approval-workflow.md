# Buddy Concierge Member-Confirmed Email Workflow

Captured from the Success Circles buddy-pairing flow after removing the active admin-review stage.

## Boundary rule

Keep Gmail access out of the member-facing `@BuddyConciergeBot` / `buddy-concierge` profile. Concierge and main Hermes communicate through Airtable status fields.

- Concierge: Telegram intake, recommendation, request confirmation, Airtable pairing request updates.
- Main Hermes: Gmail OAuth token for `connect@successcircles.com` + Airtable email watcher.
- Airtable: source of truth and handoff between Concierge and main Hermes.

## Timing rules

1. Requester completes intake and confirms the summary.
2. Concierge creates/updates the Airtable `Buddy Pairing Requests` record.
3. Concierge recommends available/requestable candidates or resolves a specific requested buddy.
4. Requester chooses a requestable buddy and confirms.
5. Concierge sets:

```text
Status = Member Confirmed - Email Queued
Member Email Status = Needs Sending
Last Bot Action = member_confirmed_email_queued
```

6. Main Hermes email watcher sends one email to the requested buddy and CCs the requester.
7. Main Hermes creates a `Buddy Pairing History` record with `Status = Requested` / pending.
8. Success Circles provides a weekly update of recent buddy pairings; use that update to mark Requested records `Active`, `Declined`, `Cancelled`, or `Completed`.

## Legacy admin commands

The old Telegram admin commands may remain available only for old pending records:

```text
approve request of [Requester Name] with [Requested Buddy Name]
reject request of [Requester Name] with [Requested Buddy Name]
```

Do not use these in the active member-facing flow.

## Airtable fields used

Roster table: `Team Roster`

- `Email Address` — member email.
- `Mobile #` — member mobile number.
- `Profile Link` — requester profile URL for requested-buddy email.

Request table: `Buddy Pairing Requests`

- `Status`: active send trigger value is `Member Confirmed - Email Queued`.
- `Member Email Status`: active send trigger value is `Needs Sending`.
- `Requesting Member Record` — linked requester roster record.
- `Requested Buddy Record` or `Selected Buddy` — linked requested buddy roster record.
- `Requested Buddy Email Sent At`
- `Requester Email Sent At` — same timestamp as the one email, because requester is CC'd.
- `Requested Buddy Email Message ID`
- `Requester Email Message ID` — same Gmail message ID as the one email, because requester is CC'd.
- `Member Email Error`
- `Last Bot Action`

## Member email sending guard

Main Hermes should send no partial emails. Require all of:

- `Status = Member Confirmed - Email Queued`
- `Member Email Status = Needs Sending`
- requester email exists
- requester mobile exists
- requester profile link exists
- requested buddy email exists
- requested buddy mobile exists

If anything is missing, do not send the email; set `Member Email Status = Failed` and write the missing field(s) to `Member Email Error`.

## Single request email template

Sent by Main Hermes from `connect@successcircles.com` after the requester confirms a requestable buddy.

```text
To: [Requested Buddy Email]
Cc: [Requester Email]
Subject: Momentum Braintrust Buddy Pairing Request from [Requester Name]

Hi [Requested Buddy Name],

[Requester Name] has requested to be your Momentum Buddy this next cycle. You may check their profile at:

[Requester Profile Link]

Feel free to hop on a quick 5-minute call to see if there is alignment.

[Requester Name] Mobile: [Requester Mobile #]

After your 5-minute call, please let the Success Circles Team know if you both agree so we can update your buddy status.

Warmly,

Buddy Concierge AI
Success Circles

Email: connect@successcircles.com
SMS: +1 (747) 224-7253

P.S. [Requested Buddy Name] Mobile: [Requested Buddy Mobile #]
```

## History writeback

After the email is sent, create or reuse a `Buddy Pairing History` Duo record:

```text
Pairing Name = [Requester] ↔ [Requested Buddy] — [Cycle]
Buddy Pairing Type = Duo
Member A = requester
Member B = requested buddy
Cycle Label = [Cycle]
Status = Requested
Source = Concierge Member-Confirmed Request
Request Record = [Buddy Pairing Requests record]
Notes = Created automatically after member-confirmed Concierge request email was sent. Weekly Success Circles update should later mark Active, Declined, Cancelled, or Completed.
```

If Airtable select choices do not already include `Requested` or `Concierge Member-Confirmed Request`, the watcher uses `typecast` to create those options.
