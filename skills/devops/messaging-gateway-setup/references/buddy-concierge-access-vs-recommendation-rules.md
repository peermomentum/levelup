# Buddy Concierge access vs recommendation eligibility

Use for Success Circles / Momentum Buddy Concierge work where the member-facing Telegram bot and the pairing algorithm have different eligibility rules.

## Separate the two eligibility layers

1. **Concierge bot access** — who may talk to `@BuddyConciergeBot` and enter the intake flow.
2. **Recommendation candidate eligibility** — who may be recommended as someone else's buddy.

Do not merge these rules. The user explicitly wants access stricter than candidate eligibility.

## Current access gate policy

A Telegram sender may access the Concierge bot only when all are true:

- Telegram `getChatMember` verifies they are a `member`, `administrator`, or `creator` of `@mombud`.
- Airtable roster match is found by Telegram account/username.
- Airtable `Membership = Current`.
- Airtable `Team Roster = Yes`.

`Reserve` members should **not** get Concierge bot access unless the user explicitly changes this later.

## Candidate recommendation policy

A candidate may be considered for recommendations when:

- `Membership = Current` normally, or `Reserve` only when allowed by the pairing protocol.
- `Team Roster = Yes`.
- `Availability = Available` for the normal candidate pool.
- `Availability = Reserve - Potentially Available` only for odd-pool balancing, specific strategic requests, or no strong Available candidate.
- Candidate is not the requester.
- Candidate is not already paired/unavailable this cycle.
- Candidate is not already rejected in this request.
- No Do-Not-Pair/Unpairs conflict.
- No pairing with requester in last 60 days unless Re-Up/admin override.
- At least one overlapping 30-minute availability window.
- `10x Player?` compatibility is respected.

## 10x compatibility rule

- If requester has `10x Player? = Yes`, candidates may have `Yes`, `No`, or blank.
- If requester has `10x Player? = No` or blank, candidates may only have `No` or blank; candidates with `Yes` are excluded.

## Joseph's scoring protocol for Point 3

After hard filters, use this tiered order:

1. Explicit user request / Re-Up / specific target: `+1000`.
2. 10x / strategic peer alignment: `+500`.
3. Sensitive personal exception / current life-context fit: `+300`.
4. Accountability style sync: `+150`.
5. Schedule breadth / tight-window priority: `+100`.
6. Thematic synergy / shared programs / industry fit: `+50`.

Member-facing output should show short privacy-safe reasons only. Do not expose sensitive notes, blacklist reasons, or internal scoring details unless the user/admin asks.

## Workflow preference

The user wants design decisions discussed one point at a time and verified before implementation. Do not jump from design into code/plugin changes without approval.
