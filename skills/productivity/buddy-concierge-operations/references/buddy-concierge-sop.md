# Buddy Concierge SOP

Copy-ready standard operating procedure for Success Circles Team covering the backend flow, exact phrases, Airtable status transitions, and emails.

## Health checks before documenting or announcing changes

Before saying the workflow is live, verify all of these with real output:

- Concierge gateway is running for only the `buddy-concierge` profile.
- Gateway log shows `Connected to Telegram` and `Gateway running with 1 platform(s)`.
- Concierge plugin compiles: `python3 -m py_compile /opt/data/profiles/buddy-concierge/plugins/buddy_concierge_gate/__init__.py`.
- Email watcher script compiles: `python3 -m py_compile /opt/data/scripts/buddy-concierge-email-watcher.py`.
- Gmail OAuth profile resolves to `connect@successcircles.com`.
- Cron job `Buddy Concierge approved-request email sender` exists, is enabled, and has `last_status = ok` after at least one run.
- Airtable `Buddy Pairing Requests` has the required admin/email fields.
- Airtable `Team Roster` has required `Name`, `Email Address`, `Mobile #`, `Profile Link`, `Membership`, `Team Roster`, `Availability`, `Past Buddies`, and `Draft Picks / Fav Buddies` fields.
- Queue counts are known: approved requests needing email, failed member email records, pending admin-review records.

## End-to-end workflow

1. Member messages `@BuddyConciergeBot`.
2. Concierge verifies access:
   - Telegram sender is in `@mombud`.
   - Sender matches Airtable `Team Roster`.
   - `Membership = Current`.
   - `Team Roster = Yes`.
3. Concierge collects intake answers.
4. Member confirms the summary.
5. Concierge creates/updates a `Buddy Pairing Requests` record.
6. Concierge recommends or accepts the requested buddy.
7. Concierge submits the request for admin review.
8. Admin approves or rejects by messaging Concierge with the exact phrase.
9. If approved, Concierge sets `Member Email Status = Needs Sending`.
10. Main Hermes email watcher sends both member emails from `connect@successcircles.com`.
11. Members do a quick 5-minute alignment call.
12. If both agree, they inform Success Circles.
13. Success Circles updates buddy status.

## Member start phrases

Members may use any plain-English opener, including:

```text
Hi
```

```text
/start
```

```text
I want a buddy
```

```text
I want to request a Momentum Buddy
```

## Concierge intake questions

After verification, Concierge should ask:

```text
Welcome to the Buddy Concierge!

I verified your Momentum Buddy Reminders access.

I’ll use your Telegram profile to help match you with the Success Circles roster. If the name you use in the Success Circles roster is different from your Telegram name, please mention it in your reply.

To pair you with a buddy who would best serve you over the next two weeks, please answer these questions:

1. Do you have someone in mind to pair with? Please type their name, or type “no preference.”
2. What are your goals or focus areas right now?
3. What kind of buddy would help you most for this request? You can use your usual roster preference or describe what you need right now.
4. What cadence do you prefer for this request? Daily, weekly, weekly + SMS daily, flexible/not sure, or use your roster preference?
5. Is there something you are going through during the next couple of weeks that we should know about? If yes, please share.
```

## Past/favorite buddy lookup phrases

Members can ask:

```text
Who were my past buddies?
```

```text
Show me my past buddies
```

```text
Who are my favorite buddies?
```

```text
Show me my draft picks
```

Concierge checks both `Past Buddies` and `Draft Picks / Fav Buddies`, then shows clear/possible name matches without exposing raw roster notes or private details.

## Intake confirmation phrase

Concierge summarizes the intake and asks for confirmation. Member may reply:

```text
Yes, that’s correct
```

or

```text
Please change [specific detail]
```

## Recommendation handling phrases

Concierge asks:

```text
Would you like me to submit one of these for admin review, show other options, or request a specific person?
```

Member may reply:

```text
Submit [Name] for admin review
```

```text
Show me others
```

```text
I don’t like these
```

```text
You choose
```

```text
I want to request [Specific Name]
```

## Submission to admin review

Concierge tells the member:

```text
I’ve submitted this for admin review. This is not finalized yet — Success Circles will review and confirm next steps.
```

Airtable fields set:

```text
Status = Pending Admin Review
Admin Approval Status = Pending
Admin Email Status = Needs Sending
Member Email Status = Waiting for Admin Approval
Last Bot Action = submitted_pending_admin_review
Admin Notified = True
```

## Admin notification

Concierge privately notifies Admin:

```text
Buddy Pairing Request — Admin Review Needed

Request record: [Airtable Record ID]

Requester:
[Requester Name]

Requested buddy:
[Requested Buddy Name]

Focus / goal:
[Requester Focus / Goal]

Preferred cadence:
[Cadence]

Upcoming context:
[Upcoming Context]

To approve, reply exactly:

approve request of [Requester Name] with [Requested Buddy Name]

To reject, reply exactly:

reject request of [Requester Name] with [Requested Buddy Name]
```

## Exact admin phrases

Approve:

```text
approve request of [Requester Name] with [Requested Buddy Name]
```

Reject:

```text
reject request of [Requester Name] with [Requested Buddy Name]
```

Avoid vague phrases like `approve`, `approve Maria`, `yes approve it`, or `disapprove David`. Concierge should respond to incomplete approval/rejection attempts with the exact required format.

## On admin approval

Concierge updates Airtable:

```text
Admin Approval Status = Approved
Admin Decision At = [current timestamp]
Admin Decision By = @successcircles
Admin Approval Raw Message = [Admin’s exact message]
Status = Admin Approved
Last Bot Action = admin_approved
Member Email Status = Needs Sending
```

Concierge replies:

```text
Approved.

Hermes will now email [Requester Name] and [Requested Buddy Name] about the buddy pairing request.
```

## On admin rejection

Concierge updates Airtable:

```text
Admin Approval Status = Rejected
Admin Decision At = [current timestamp]
Admin Decision By = @successcircles
Admin Approval Raw Message = [Admin’s exact message]
Status = Admin Rejected
Last Bot Action = admin_rejected
Member Email Status = Not Sent - Rejected
```

Concierge replies:

```text
Rejected.

No member emails will be sent for [Requester Name]’s buddy request with [Requested Buddy Name].
```

## Main Hermes email automation

Main Hermes runs `/opt/data/scripts/buddy-concierge-email-watcher.py` every 2 minutes via cron job `Buddy Concierge approved-request email sender`.

It looks for:

```text
Admin Approval Status = Approved
Member Email Status = Needs Sending
```

After successful sending, Airtable is updated:

```text
Member Email Status = Sent
Requester Email Sent At = [timestamp]
Requested Buddy Email Sent At = [timestamp]
Requester Email Message ID = [Gmail message ID]
Requested Buddy Email Message ID = [Gmail message ID]
Member Email Error = [blank]
Last Bot Action = member_emails_sent
```

If required fields are missing, Hermes sends no partial member emails and sets:

```text
Member Email Status = Failed
Member Email Error = [missing field details]
```

Required requester fields: `Name`, `Email Address`, `Mobile #`, `Profile Link`.
Required requested-buddy fields: `Name`, `Email Address`, `Mobile #`.

## Requester email template

Subject:

```text
Your Momentum Braintrust Buddy pairing request has been sent
```

Body:

```text
Hi [Requester Name],

We have sent an email to [Requested Buddy Name] regarding your request to be their Momentum Buddy this next cycle.

We invited [Requested Buddy Name] to review your profile. We recommend hopping on a quick 5-minute call to see if there is alignment.

[Requested Buddy Name] Mobile: [Requested Buddy Mobile #]

After your 5-minute call, please let the Success Circles Team know if you both agree so we can update your buddy status.

Warmly,

Buddy Concierge AI
Success Circles

Email: connect@successcircles.com
SMS: +1 (747) 224-7253
```

## Requested buddy email template

Subject:

```text
Momentum Braintrust Buddy Pairing Request from [Requester Name]
```

Body:

```text
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
```

## Member onboarding email template

Subject:

```text
How to Use the Buddy Concierge Bot
```

Body:

```text
Hi [First Name],

We now have a simple Buddy Concierge bot to help you request a Momentum Buddy without overthinking the process.

Here’s exactly what to do:

Step 1: Open Telegram

Go to Telegram and search for:

@BuddyConciergeBot

Or click here:

https://t.me/BuddyConciergeBot

Step 2: Send the bot a message

You can simply type:

Hi

The bot will check that you’re a current Success Circles member and part of the Momentum Buddy Telegram group.

Step 3: If the bot asks you to share your phone number, tap the button

Sometimes the bot may need to match your Telegram account to your Success Circles roster record.

If it asks, just tap the Telegram button that says something like:

Share my phone number

No need to type your phone number manually.

Step 4: Answer the Buddy Concierge questions

The bot will ask a few simple questions, such as:

- Do you already have someone in mind?
- What are your goals or focus areas right now?
- What kind of buddy would be most helpful?
- How often would you like to connect?
- Is there anything coming up in your life we should know about?

You can answer one question at a time, or you can answer in one message if that feels easier.

Step 5: Ask to see past buddies if you want

If you’re not sure who to pick, you can type something like:

Who were my past buddies?

or

Show me my past buddies

The bot can help you see past/favorite buddy options from the roster so you don’t have to remember everyone.

Step 6: Confirm your answers

Before anything is submitted, the bot will summarize what you shared.

Just review it and say:

Yes, that’s correct

or tell the bot what to change.

What happens next

If your requested buddy is available and the request is approved by the Success Circles Team, we’ll send an email to both of you with next steps.

We’ll ask the two of you to hop on a quick 5-minute call to see if there’s alignment.

If you both agree, please inform the Success Circles Team so we can update your buddy status.

That’s it.

The Concierge bot does not instantly confirm a buddy match. It helps collect your request and preferences so we can make the best possible pairing.

If anything feels confusing, just message the bot in plain English. Keep it simple — you don’t need the perfect wording.
```
