# Success Circles Buddy Concierge SOP — Current Live Flow

Use this SOP for the current no-admin-review Buddy Concierge flow.

## Summary

1. Member messages `@BuddyConciergeBot` / Kai.
2. Gateway verifies `@mombud` membership and Airtable Team Roster access.
3. Kai collects pairing intake.
4. Kai recommends available/requestable buddies or resolves a specific requested buddy.
5. Member confirms one requestable buddy.
6. Kai queues one request email by setting Airtable `Status = Member Confirmed - Email Queued` and `Member Email Status = Needs Sending`.
7. Main Hermes sends one email from `connect@successcircles.com` to the requested buddy and CCs the requester.
8. Main Hermes creates Buddy Pairing History as `Status = Requested` / pending.
9. Success Circles provides a weekly update of which requested pairs became Active, Declined, Cancelled, or Completed.

## Access requirements

- Telegram sender must be in `@mombud`.
- Airtable Team Roster record must have `Membership = Current` and `Team Roster = Yes`.
- If no safe Telegram username/display-name match exists, Kai asks the member to share their phone number via Telegram contact button and matches it to Team Roster `Mobile #`.

## Intake questions

Kai asks:

1. Do you have someone in mind to pair with? Type their name or `no preference`.
2. What are your goals or focus areas right now?
3. What kind of buddy would help you most for this request?
4. What cadence do you prefer for this request?
5. Is there something you are going through during the next couple weeks that we should know?

Kai summarizes the answers and asks the member to confirm before writing the request.

## Specific buddy safeguards

- Do not guess first-name-only, last-name-only, nickname, or partial names.
- Use `resolve_requested_buddy` first.
- If clarification is required, ask e.g. `Did you mean Ryan Brown?`
- Only queue emails with canonical full roster name and linked Airtable record ID.
- Do not queue unavailable people.

## Recommendation eligibility

A recommendation/request candidate must have:

```text
Membership = Current or Reserve
Team Roster = Yes
Availability = Available OR Reserve - potentially available
```

Display `Reserve - potentially available` as `available`. All other availability values are unavailable.

## Request email queue

After the member confirms a requestable selected/requested buddy, Kai calls:

```text
buddy_concierge_pairing action=submit_for_member_email
```

This sets:

```text
Status = Member Confirmed - Email Queued
Member Email Status = Needs Sending
Last Bot Action = member_confirmed_email_queued
```

Kai tells the member:

```text
I’ve queued the request email to [Requested Buddy Name] and you’ll be CC’d so you can coordinate a quick 5-minute alignment call. This is not an official pairing until you both agree and Success Circles updates the status.
```

## Single email sent by Main Hermes

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

## Email watcher trigger

The cron email watcher sends only records matching:

```text
Status = Member Confirmed - Email Queued
Member Email Status = Needs Sending
```

It requires requester email/mobile/profile link and requested buddy email/mobile. If anything is missing, it sets `Member Email Status = Failed` and writes `Member Email Error`.

## History writeback and weekly update

After the email sends, Main Hermes creates a Duo `Buddy Pairing History` record as:

```text
Status = Requested
Source = Concierge Member-Confirmed Request
```

Success Circles should send a weekly update like:

```text
Weekly Buddy Pairing Update

Confirmed pairings:
- Member A and Member B

Not moving forward:
- Member C and Member D

Still pending:
- Member E and Member F
```

Hermes will then update `Buddy Pairing History` statuses to `Active`, `Declined`, `Cancelled`, or leave as `Requested`.

## Legacy admin commands

Old admin commands may remain available for old pending records only:

```text
approve request of [Requester Name] with [Requested Buddy Name]
reject request of [Requester Name] with [Requested Buddy Name]
```

Do not use this for the current active flow.
