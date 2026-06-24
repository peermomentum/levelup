# Tech Week / Partiful Extraction Notes

Use these notes when researching Tech Week NYC-style calendars for Success Circles event recommendations.

## Tech Week calendar pages

Example URL shapes:

- `https://www.tech-week.com/calendar/nyc`
- `https://www.tech-week.com/calendar/nyc?day=2026-06-04`

The rendered HTML may contain a Next.js / React Server Components payload rather than a simple JSON script. Calendar event cards can often be extracted from `self.__next_f.push(...)` script chunks.

Reliable extraction pattern used in-session:

1. Fetch the HTML with a browser-like user agent.
2. Extract all `<script>self.__next_f.push(...)</script>` payloads.
3. `json.loads()` the push argument.
4. Concatenate string chunks from array element `[1]`.
5. Search for event objects containing fields like:
   - `id`
   - `name`
   - `url`
   - `isInviteOnly`
   - `typeLabel`
   - `date`
   - `time`
   - `hosts`
   - `location`
   - `citySlug`
6. Filter by the requested date.
7. Sort by `time`.

The calendar object may only expose event start time and broad type label. Fetch the Partiful detail page for end time, agenda, speaker names, exact address, RSVP status, and richer description.

## Partiful detail pages

Partiful pages commonly expose useful facts in public HTML / metadata:

- `og:description` often contains the full event description and agenda.
- Visible text often includes date/time such as `6:30pm – 8:30pm`.
- Schema.org JSON can contain `startDate`, `endDate`, `location`, `organizer`, and address.
- RSVP status or capacity can appear in text snippets, e.g. `RSVPs closed`, `0/301 spots left`, `1/157 spots left`.

## Success Circles decision filters

For Joseph, do not merely list every event. Filter aggressively by:

- Current local time and commute time
- User availability windows
- Founder/operator/investor density
- Alignment with accountability, operating systems, AI workflows, workflow optimization, and structured execution
- Access caveats: RSVP closed, full, invite-only, confirmation required
- Whether enough event time remains after commute

## Output pattern

Recommended response shape:

1. State current time/date used for filtering.
2. State number of events found.
3. List the best remaining / best-fit options first.
4. For each recommended event include:
   - Time and end time
   - Location
   - Hosts
   - Link
   - Why it aligns with Success Circles
   - Caveat
   - Recommendation: go / optional / skip
5. End with a direct route/schedule recommendation.

## Pitfalls

- Calendar cards can omit end times; fetch detail pages before saying an event is viable.
- A high-profile host does not automatically mean high Success Circles fit. Prioritize founder/operator networking value.
- If LinkedIn/social founder research is requested, do not guess. Mark unverified when blocked or ambiguous.
