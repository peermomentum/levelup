# Buddy Concierge gated member access pattern

Use this reference when a member-facing Telegram concierge must be reachable by a community while remaining limited to an approved workflow.

## Access policy used for Success Circles Buddy Concierge

For `@BuddyConciergeBot`, the desired gate is:

```text
User messages Concierge
↓
Bot checks @mombud with Telegram getChatMember
↓
Bot checks Airtable Team Roster by Telegram Account username/link
↓
Bot only allows if Membership = Current
↓
Bot only allows if Team Roster = Yes
```

Relevant Airtable source:

- Base: `appDxJWXndV2Bfec3` — Success Circles / Momentum Buddy roster
- Table: `tbl8EZW9OIJRMs1bf` — `Team Roster`
- Telegram identity field: `Telegram Account`
- Active member field: `Membership`, allow only `Current`
- Roster inclusion field: `Team Roster`, allow only `Yes`

`Availability` is about the pairing cycle and should not be used as the primary access gate. Values like `Available`, `Unavailable`, and `Reserve - Potentially Available` are pairing availability states, not membership/access states.

## Implementation pattern

Use a profile-local plugin in the member-facing profile when instructions alone are insufficient. The plugin should run before the agent via `pre_gateway_dispatch`:

1. Extract Telegram sender metadata from `event.source` and `event.raw_message.from_user`.
2. Call Telegram Bot API `getChatMember` for `@mombud` and the sender's numeric Telegram ID.
3. Treat `member`, `administrator`, and `creator` as passing statuses.
4. Query Airtable `Team Roster` for the sender's Telegram username/link in `{Telegram Account}`.
5. Accept only records with `{Membership} = 'Current'` and `{Team Roster} = 'Yes'`.
6. If the checks pass, rewrite the message with a compact verified-access header so the agent does not try to re-verify.
7. If a check fails, send a short denial message directly and return `{"action": "skip"}` so the agent is not invoked.

## Plugin hook pitfall

`pre_gateway_dispatch` can receive extra gateway/internal keyword arguments such as `telemetry_schema_version`. Define the hook with `**kwargs` to avoid a runtime failure:

```python
def pre_gateway_dispatch(event, gateway=None, session_store=None, **kwargs):
    ...
```

If the hook raises before it can rewrite/skip, the message may fall through to old profile instructions and produce confusing fallback text such as “I’m having trouble verifying...” even though the verifier itself would have passed.

## Tool and scope limits

For member-facing concierge profiles, combine access gates with purpose limits:

- Keep the profile focused on one workflow: buddy pairing intake/status/preferences/confirmation.
- Use `pre_tool_call` to block admin/system tools such as terminal, file editing, memory editing, cron jobs, delegation, GitHub/admin toolsets, and broad system actions.
- Let the admin Hermes profile keep broad operational control; the member bot should not change server/profile state or unrelated Airtable fields.

## Operational sequence

1. Keep `TELEGRAM_ALLOWED_USERS` narrow while building the gate.
2. Install and enable the profile-local gate plugin.
3. Verify the owner/admin account passes the gate.
4. Only then relax gateway-level access (for example wildcard/open gateway reachability) so @mombud members can reach the plugin.
5. Restart only the target profile's gateway; avoid broad kill commands that can stop the admin assistant gateway.
6. Test with:
   - an admin/current roster account;
   - a @mombud member with `Membership = Past` or `Reserve`;
   - a record with `Team Roster = No` or blank;
   - a non-@mombud account if available.

## User-facing status style

For nontechnical gateway/bot troubleshooting, keep updates short and plain-language. Avoid long architecture dumps. Say what is true now, what broke, what changed, and the exact next test.
