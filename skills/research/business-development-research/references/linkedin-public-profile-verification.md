# LinkedIn public follower verification for guest/prospect lists

Use this reference when a user asks whether podcast guests, speakers, authors, or business-development prospects have a strong LinkedIn following.

## Verification standard

Only report a LinkedIn follower count as verified when all of these are true:

1. The profile identity matches the target person, not just the same name.
   - Check title/company/role/location/known book or organization when visible.
   - For common names, treat same-name matches as unverified unless role context clearly matches.
2. The count is visible on the public LinkedIn profile or another reliable public source quoting the profile.
3. The reported count is kept in LinkedIn's public rounded format when exact precision is unavailable (for example `29K`, `12K`, `6K`).

## Output labels

Use explicit confidence labels:

- **High:** Direct public profile page confirms the person's name/role and follower count.
- **Medium:** Profile URL is likely correct and identity is corroborated, but follower count is not visible or source is indirect.
- **Low / unknown:** Same-name risk, inaccessible page, or no follower count found.

Never fill unknown counts with estimates.

## Practical workflow

1. Build the prospect list from relevance first: category authority, books, speaking history, ecosystem role, and fit for the user's mission.
2. For each person, search or test likely LinkedIn profile slugs.
3. Confirm identity before parsing followers.
4. Extract only the public text pattern like `29K followers` / `500+ connections`.
5. Separate the final answer into:
   - Verified follower counts.
   - Not verified yet / same-name risk.
   - Recommended priorities if LinkedIn following matters.
6. Recommend prioritization by combined relevance + reputation + platform, not follower count alone.

## Common pitfalls

- Do not claim a count for an official ecosystem leader if the only profile found is a different person with the same name.
- Do not let a high follower count override poor topical fit.
- Do not imply a live verification happened if the count came from memory or prior knowledge.
- Public LinkedIn counts are often rounded; report them as approximate (e.g. `~29K`) unless an exact count is visible.

## Example answer pattern

```markdown
## Verified LinkedIn follower counts

- **Name**
  - **LinkedIn followers:** ~29K
  - **Profile:** https://www.linkedin.com/in/example
  - **Confidence:** High — public profile matched role/company and showed the count.
  - **Guest strength:** Strong because ...

## Not verified / same-name risk

- **Name**
  - **LinkedIn followers:** not verified
  - **Note:** Found same-name profiles, but none clearly matched [role/company].
```
