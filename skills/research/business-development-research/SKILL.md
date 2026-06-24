---
name: business-development-research
description: Research and rank people, events, communities, and partnership opportunities for business growth, podcast guest booking, founder-community building, and outreach campaigns.
---

# Business Development Research

Use this skill when the user asks to identify, rank, or prepare outreach targets such as:
- Events to attend for a mission, company, community, or brand.
- Podcast guests, interview targets, speakers, authors, influencers, founders, investors, or operators.
- Communities, ecosystems, conferences, meetups, partner channels, or referral sources.
- Shortlists where fit matters more than exhaustive search.

The deliverable should be practical: a prioritized list with why each target matters, how to approach them, and any caveats about verification.

## Workflow

1. **Clarify the mission from available context before searching.**
   - If the user provides a website, fetch/read it and extract positioning, audience, and keywords.
   - If no website is provided but the user names the mission, infer carefully and label assumptions.
   - For SuccessCircles.com, core positioning observed: entrepreneurial peer accountability, Momentum Braintrust / buddy huddles, founder/C-suite growth, escaping isolation, daily/weekly execution momentum, and making accountability practical/fun.

2. **Ground current/date-sensitive facts with tools.**
   - For “today” or event-calendar tasks, run a date/time check in the relevant timezone when possible.
   - Fetch the source page directly. If it is a JavaScript/Next.js app, inspect embedded payloads before giving up.
   - For people/guest research, verify current roles, publications, and platform presence with live web lookups when tools are available. Do not imply follower counts were verified unless they were.

3. **Extract candidates broadly, then rank by fit.**
   - Prefer quality over volume. The user usually wants actionable picks, not every possible result.
   - Use scoring dimensions such as:
     - Audience fit: founders, entrepreneurial owners, C-suite, operators, investors.
     - Authority: author, founder, CEO, official ecosystem leader, respected practitioner.
     - Platform: podcast experience, speaking history, book credibility, social following.
     - Strategic value: referral access, partnership potential, category credibility.
     - Timing/logistics for events: current time, location clustering, overlap, invite status.

4. **For event calendars, make a route or priority plan.**
   - Include time, location, hosts, URL, and why it fits the mission.
   - Separate “best picks” from “secondary/use-if” options.
   - If some events are already in progress or likely past, say so plainly and suggest using the attendee list/follow-up angle when useful.

5. **For podcast/interview guest lists, provide booking-ready context.**
   - Include the person’s name, why they are credible, key books/companies/roles, best episode topic, fit for the user’s show, and a concise outreach angle.
   - Group by tier or category: direct ecosystem authorities, adjacent thought leaders, entrepreneur-owner journey authors, etc.
   - Call out “dream guests” versus likely more bookable guests.

6. **Verify social/platform strength carefully when asked.**
   - For LinkedIn follower checks, verify identity before extracting counts; common-name matches are not enough.
   - Preserve LinkedIn’s public rounded format (e.g. `~29K`) unless an exact count is visible.
   - Separate “verified counts” from “not verified / same-name risk” so the user can act without confusing guesses for facts.
   - See `references/linkedin-public-profile-verification.md` for the verification standard and answer pattern.
   - For EOS / Rules for Success guest research, see `references/eos-podcast-guest-research.md` for candidate categories, previously verified public LinkedIn counts, and a table-output pattern.

7. **Be transparent about verification.**
   - If live verification failed or was not done, explicitly say what is unverified.
   - Avoid invented bios, follower counts, or event details. If exact data is unavailable, provide a curated provisional list and recommend validation.

## Practical output patterns

### Event shortlist

Use this structure:

```markdown
As of [time/date], I found [N] events today and filtered for [mission].

## Best picks

### 1. [Event]
- Time:
- Location:
- Hosts:
- Link:
- Why it fits:
- Best angle:

## Suggested route
1. ...
```

### Podcast guest shortlist

Use this structure:

```markdown
## Top targets

### 1. [Name]
- Why:
- Books / platform:
- Best topic:
- Fit:
- Outreach angle:

## Best first outreach targets
1. ...
```

## Technical note: extracting Next.js / React Server Component event calendars

Some event calendars render from embedded `self.__next_f.push([...])` script chunks rather than a simple `__NEXT_DATA__` JSON blob. When a direct HTML fetch contains event data but no `__NEXT_DATA__`:

1. Fetch the page with a browser-like User-Agent.
2. Extract `<script>self.__next_f.push(...)</script>` chunks.
3. `json.loads()` the push argument; concatenate string payload entries.
4. Search the joined payload for JSON-like event objects by fields such as `id`, `name`, `url`, `date`, `time`, `hosts`, `location`.
5. Dedupe by event ID and sort by time.
6. Fetch linked event pages (e.g., Partiful URLs) for `og:description` / meta descriptions to improve ranking.

See `references/tech-week-calendar-extraction.md` for a compact example pattern.

## Success Circles / Joseph Varghese Lens

When the opportunity is for SuccessCircles.com or Joseph Varghese, rank through this mission lens: entrepreneurial peer accountability, EOS/Momentum-OS-style operating rhythms, structured execution, clarity, accountability, operational flow, and making founder/team execution practical and fun.

Prioritize:
- Founder, owner, C-suite, operator, and investor rooms.
- EOS / business operating system / accountability / leadership-rhythm relevance.
- AI workflow, automation, Notion, process optimization, and scalable execution communities.
- Podcast guest fit for *Rules for Success*: accomplished operators, authors, speakers, and people with meaningful social reach.

Output should be concise, action-oriented, and Telegram-friendly unless the user requests tables. Call out access risk, RSVP status, commute timing, audience mismatch, and direct conversation angles for Joseph.

A snapshot of the former Success Circles-specific package is stored at `references/absorbed-successcircles-business-development-research/` for exact prior heuristics and Tech Week/Partiful notes.

## Pitfalls

- Do not answer date-sensitive event questions from memory. Check the current date/time and source page.
- Do not over-optimize for famous names only; the best business-development targets may be ecosystem leaders with access and relevance, not only celebrity authors.
- Do not flatten everything into one list when the user needs decisions. Rank and explain tradeoffs.
- Do not present unverified follower counts or current roles as facts.
