# Buddy Concierge @mombud + Airtable membership gate

Use this reference when a member-facing Success Circles / Momentum Buddy Concierge Telegram bot must be reachable by many members but constrained to pairing-only work.

## Desired access model

The bot should be "limited" in two separate ways:

1. **Membership-limited** — allow only Telegram senders who are members/admins/creator of `@mombud` and also present in the Success Circles Airtable roster.
2. **Purpose-limited** — the member-facing bot should only handle pairing intake/status/preferences/confirmation and should not act like the admin Hermes assistant.

## Safe rollout sequence

1. Keep the bot private while testing, e.g. `TELEGRAM_ALLOWED_USERS=<owner_numeric_id>`.
2. Build the real gate before opening the gateway allowlist:
   - Telegram Bot API `getChatMember(chat_id='@mombud', user_id=<sender_id>)`.
   - Airtable lookup in base `appDxJWXndV2Bfec3`, table `tbl8EZW9OIJRMs1bf` (`Team Roster`), matching `Telegram Account` against `@username`, bare username, and `t.me/<username>` URLs.
3. Only after the gate is installed, relax the gateway allowlist so member messages can reach the gate, for example `TELEGRAM_ALLOWED_USERS=*` plus `GATEWAY_ALLOW_ALL_USERS=true` if required by the gateway auth layer.
4. Restart only the target profile gateway; avoid broad process-kill patterns.
5. Verify first with the owner account, then with a non-owner member, then with a non-member/non-roster account.

## Implementation pattern used successfully

A profile-local plugin under `/opt/data/profiles/buddy-concierge/plugins/buddy_concierge_gate/` can register:

- `pre_gateway_dispatch` — runs before normal auth/agent dispatch; checks Telegram membership + Airtable roster, sends a denial message and returns `{'action':'skip'}` on failure, or rewrites the inbound text with a `[Buddy Concierge verified access]` block on success.
- `pre_tool_call` — blocks admin/system tools such as terminal, file writes, cron, memory, skill management, GitHub/admin tool prefixes, etc., so the public bot remains pairing-focused.

Enable the plugin in the profile config:

```yaml
plugins:
  enabled:
  - buddy-concierge-gate
```

Configure the profile env:

```bash
BUDDY_CONCIERGE_REQUIRED_CHAT=@mombud
BUDDY_CONCIERGE_AIRTABLE_BASE_ID=appDxJWXndV2Bfec3
BUDDY_CONCIERGE_AIRTABLE_ROSTER_TABLE_ID=tbl8EZW9OIJRMs1bf
```

## Instruction update pattern

Update the concierge profile's `SOUL.md` and the installed `buddy-concierge` skill so the agent knows the gate has already run:

- If the incoming message contains `[Buddy Concierge verified access]`, access is verified; do **not** try to verify again or say verification is unavailable.
- Use the injected Telegram/Airtable roster metadata.
- If no verified-access block exists, do not provide pairing help.
- Refuse unrelated requests and requests to change anything outside the pairing process.

## Verification probes

- Direct Telegram API probe for owner/member:
  - `getChatMember('@mombud', user_id)` should return `member`, `administrator`, or `creator`.
- Airtable probe:
  - Query `Team Roster` with a formula matching `Telegram Account` to `@username`, bare username, or `t.me/<username>`.
- Plugin probe:
  - Import the plugin with the profile `.env` loaded and call `pre_gateway_dispatch()` with a fake Telegram DM event; expect `action == 'rewrite'` and a verified-access header for a known valid user.
- Runtime log checks:
  - Plugin count should increase after restart, e.g. `Plugin discovery complete: ... enabled`.
  - Gateway should show `Connected to Telegram` and `Gateway running`.

## Important pitfall

If the agent is merely instructed to "verify @mombud membership" but no real tool/plugin performs that check, it may fall back to "I’m having trouble verifying..." even for valid members. The durable fix is a pre-dispatch gate or equivalent code path, not only prompt text.
