---
name: successcircles-business-development-research
description: "Research and prioritize business-development opportunities for Success Circles: events, networking rooms, podcast guests, EOS/operator communities, and social-proof validation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Success Circles, business development, events, podcast guests, EOS, networking, founder research]
---

# Success Circles Business Development Research

Use this skill when Joseph asks for:

- Events to attend for SuccessCircles.com growth
- Networking recommendations from calendars, Tech Week pages, Partiful, Meetup, Luma, Eventbrite, etc.
- Potential podcast guests for *Rules for Success*
- EOS / Entrepreneurial Operating System, founder, operator, AI workflow, business systems, accountability, or operational clarity prospects
- Social proof checks such as LinkedIn follower counts, author/platform credibility, founder background, or audience fit

## User mission lens

Joseph Varghese is building Success Circles around EOS/Momentum OS-style systems, workflow optimization, structured execution, clarity, accountability, and operational flow for entrepreneurs and teams.

When ranking opportunities, prioritize rooms/people with:

1. Entrepreneurial owners, founders, C-suite leaders, operators, and investors
2. EOS / business operating system / accountability / leadership rhythm relevance
3. AI workflow, automation, Notion, process optimization, and scalable execution relevance
4. High-quality referral potential for Success Circles
5. Podcast guest fit for *Rules for Success*: accomplished, well-revered, published authors, speakers, and people with meaningful social reach

## Output style for Joseph

- Be concise, clear, and action-oriented.
- Use structured bullets or simple Telegram-friendly row groups, not pipe tables unless explicitly requested.
- Give direct recommendations and rank the options.
- Call out tradeoffs plainly: access risk, RSVP closed, commute timing, audience mismatch, likely low-value room.
- Connect recommendations back to Success Circles growth, operational clarity, process design, founder accountability, or podcast guest value.
- If the user asks for a table, provide columns exactly as requested, but avoid overlong prose inside cells.

## Event research workflow

1. Confirm the actual date/time and timezone when timing matters.
2. Extract the complete event list for the requested day.
3. Filter by the user's availability and commute constraints.
4. Fetch event detail pages when possible for agenda, end time, speakers, host companies, location, and RSVP constraints.
5. Rank events by Success Circles fit, not by general popularity.
6. Provide:
   - Best picks
   - Why each aligns
   - Time/location/link
   - Access caveats
   - Suggested route/schedule
   - Conversation angle Joseph can use in the room

### Event fit scoring heuristics

High fit:
- Founder/operator/investor mixers
- B2B AI startup showcases
- Founder journey / acquisition / scaling talks
- Workforce, accountability, talent strategy, leadership, culture, or operating model sessions
- Rooms hosted by credible venture firms or startup platforms

Medium fit:
- AI infrastructure or technical builder events where operators/founders are likely present
- Broad closing parties with quality hosts but less structured programming

Lower fit:
- Deep hackathons unless Joseph is recruiting technical collaborators
- Highly technical panels with little founder/operator networking
- Events already ending before commute arrival

## Podcast guest prospecting workflow

1. Separate **core EOS** prospects from **adjacent entrepreneur-owner systems** prospects.
2. Prioritize guests by:
   - EOS relevance
   - Book/authorship/speaking credibility
   - LinkedIn/social reach
   - Fit with Success Circles themes: accountability, clarity, operating rhythm, founder freedom, people systems
   - Likelihood of being reachable/bookable
3. For social following, verify from public LinkedIn/profile pages where possible.
4. Never invent follower counts. If LinkedIn blocks access or same-name risk exists, mark as `Not verified`.
5. For same-name risk, only report counts when the profile identity matches the known role/company.
6. Include a short outreach angle or episode topic when useful.

## Known high-priority guest categories

Core EOS:
- Gino Wickman
- Mark C. Winters
- Mike Paton
- Mark O'Donnell
- Kelly Knight
- C.J. DuBe'
- René Boer
- Don Tinney

Adjacent entrepreneur-owner systems:
- Verne Harnish
- Mike Michalowicz
- John Warrillow
- Dan Sullivan
- Shannon Waller
- Rob Dube
- Bo Burlingham

## Verification and caveats

- LinkedIn often rounds follower counts publicly (e.g., `29K`) and may block unauthenticated access.
- Search results can surface wrong people with matching names; verify title/company before including a count.
- When exact follower counts cannot be verified, use `Not verified`, not a guessed estimate.
- For current events, always inspect the detail page when possible because calendar cards may omit end time, RSVP status, agenda, address, and speaker details.

## References

- `references/tech-week-partiful.md` — notes on extracting Tech Week calendar events and Partiful detail-page facts.
