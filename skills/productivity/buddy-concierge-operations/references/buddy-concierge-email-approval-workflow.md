# Buddy Concierge Email + Admin Approval Workflow

Captured from the Success Circles buddy-pairing expansion design.

## Boundary rule

Keep Gmail access out of the member-facing `@BuddyConciergeBot` / `buddy-concierge` profile. Concierge and main Hermes should communicate through Airtable status fields.

- Concierge: Telegram intake/admin approval conversation + Airtable pairing request updates.
- Main Hermes: Gmail OAuth token for `connect@successcircles.com` + Airtable email watcher.
- Airtable: source of truth and handoff between Concierge and main Hermes.

## Gmail setup choice

Use Google OAuth Gmail API scoped to Gmail for `connect@successcircles.com`, configured only in the main Hermes profile. Do not place Gmail credentials/tokens in `/opt/data/profiles/buddy-concierge`.

## Timing rules

1. Requester confirms buddy choice in Concierge.
2. Concierge records Airtable request and sets admin review/email status.
3. Concierge sends Telegram admin-review message to `@successcircles`.
4. Main Hermes sends admin email after requester confirmation.
5. Admin approves/rejects by replying to Concierge.
6. Main Hermes sends member emails only after admin approval.

## Admin Telegram command format

Require requester name + requested buddy name for protection:

```text
approve request of [Requester Name] with [Requested Buddy Name]
reject request of [Requester Name] with [Requested Buddy Name]
```

Do not require the admin to paste a profile link. The requester profile link comes from Airtable Team Roster.

Concierge should reject vague commands like `approve`, `reject`, or `approve Maria`, and respond with the exact required format. If multiple pending requests match, do not approve automatically; ask for an exact requester/requested-buddy pair.

## Airtable fields used

Roster table: `Team Roster`

- `Email Address` — member email.
- `Mobile #` — member mobile number.
- `Profile Link` — requester profile URL for requested-buddy email.

Recommended snapshot fields in `Buddy Pairing Requests`:

- `Requester Email Address`
- `Requester Mobile #`
- `Requester Profile Link`
- `Requested Buddy Email Address`
- `Requested Buddy Mobile #`
- `Admin Approval Raw Message`

Status fields recommended in `Buddy Pairing Requests`:

- `Admin Approval Status`: `Pending`, `Approved`, `Rejected`.
- `Admin Decision At`
- `Admin Decision By`
- `Admin Email Status`: `Needs Sending`, `Sent`, `Failed`.
- `Admin Email Sent At`
- `Admin Email Message ID`
- `Admin Email Error`
- `Member Email Status`: `Waiting for Admin Approval`, `Needs Sending`, `Sent`, `Failed`, `Not Sent - Rejected`.
- `Requester Email Sent At`
- `Requested Buddy Email Sent At`
- `Requester Email Message ID`
- `Requested Buddy Email Message ID`
- `Member Email Error`

## Concierge admin review Telegram message

```text
Buddy Pairing Request — Admin Review Needed

Requester:
[Requester Name]

Requested buddy:
[Requested Buddy Name]

Focus / goal:
[Requester focus area]

Preferred cadence:
[Cadence]

Upcoming context:
[Upcoming life context]

To approve, reply with:

approve request of [Requester Name] with [Requested Buddy Name]

To reject, reply with:

reject request of [Requester Name] with [Requested Buddy Name]
```

## On admin approval

When `@successcircles` sends a valid approval command:

1. Verify sender is `@successcircles`.
2. Parse requester and requested buddy names.
3. Find exactly one pending request matching both names.
4. Retrieve from `Team Roster`:
   - requester `Email Address`, `Mobile #`, `Profile Link`.
   - requested buddy `Email Address`, `Mobile #`.
5. Snapshot these values into `Buddy Pairing Requests` if fields exist.
6. Set:

```text
Admin Approval Status = Approved
Admin Decision At = current timestamp
Admin Decision By = @successcircles
Member Email Status = Needs Sending
```

7. Reply to admin:

```text
Approved.

Hermes will now email [Requester Name] and [Requested Buddy Name] about the buddy pairing request.
```

## On admin rejection

Set:

```text
Admin Approval Status = Rejected
Admin Decision At = current timestamp
Admin Decision By = @successcircles
Member Email Status = Not Sent - Rejected
```

Reply:

```text
Rejected.

No member emails will be sent for [Requester Name]’s buddy request with [Requested Buddy Name].
```

## Admin email template

Sent by main Hermes after requester confirmation, before approval.

```text
Subject: Buddy Pairing Approval Needed: [Requester Name] → [Requested Buddy Name]

Hi Success Circles Admin,

[Requester Name] has confirmed that they would like to request [Requested Buddy Name] as their buddy.

Pairing request details:

Requester:
[Requester Name]
[Requester Email]
[Requester Telegram]

Requested buddy:
[Requested Buddy Name]
[Requested Buddy Email]
[Requested Buddy Telegram]

Requester’s focus/goals:
[Focus / goals]

Preferred cadence:
[Cadence]

Upcoming life context:
[Upcoming life context]

This request is currently pending admin approval.

To approve or reject, reply to the Concierge bot on Telegram using one of these:

approve request of [Requester Name] with [Requested Buddy Name]

reject request of [Requester Name] with [Requested Buddy Name]

— Success Circles Buddy Concierge
```

## Requester email template

No CC. Sent only after admin approval.

```text
Subject: Your Momentum Braintrust Buddy pairing request has been sent

Hi [Requester Name],

We have sent an email to [Requested Buddy Name] regarding your request to be their momentum buddy this next cycle.

We invited [Requested Buddy Name] to review your profile. We recommend to hop on a 5-minute call to see if there is alignment.

[Requested Buddy Name] Mobile: [Requested Buddy Mobile #]

Warmly,

Buddy Concierge AI
Success Circles

Email: connect@successcircles.com
SMS: +1 (747) 224-7253
```

## Requested buddy email template

No CC. Sent only after admin approval.

```text
Subject: Momentum Braintrust Buddy Pairing Request from [Requester Name]

Hi [Requested Buddy Name],

[Requester Name] has requested to be your momentum buddy this next cycle. You may check their profile at:

[profile link]

Feel free to hop on a 5-minute call to see if there is alignment.

[Requester Name] Mobile: [Requester Name Mobile #]

Let us know if you agree either via email or SMS.

Warmly,

Buddy Concierge AI
Success Circles

Email: connect@successcircles.com
SMS: +1 (747) 224-7253
```

## Member email sending guard

Main Hermes should send no partial member emails. Require all of:

- `Admin Approval Status = Approved`
- `Member Email Status = Needs Sending`
- requester email exists
- requester mobile exists
- requester profile link exists
- requested buddy email exists
- requested buddy mobile exists

If anything is missing, do not send either member email; set `Member Email Status = Failed` and write the missing field(s) to `Member Email Error`.
