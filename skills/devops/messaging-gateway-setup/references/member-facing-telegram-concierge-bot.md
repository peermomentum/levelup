# Member-facing Telegram concierge bot pattern

Use this reference when a community wants members to connect to a Hermes-powered concierge via Telegram, especially on Hostinger/Docker.

## Recommended architecture

- Do **not** create a new Hostinger server/container for every member or every member-facing workflow.
- Use one dedicated Telegram bot for the member-facing concierge, created in BotFather (for example `@BuddyConciergeBot`).
- Run that bot under a dedicated Hermes profile (for example `buddy-concierge`) so its instructions, skills, gateway token, allowlist, and logs are separated from the owner's private/admin Hermes bot.
- Keep the private/admin bot separate from the public/member concierge bot.

## Access model

Start safely, then broaden access:

1. During first setup, allowlist only the owner/admin numeric Telegram ID.
2. Verify end-to-end with a real Telegram message such as `/start` or a natural-language trigger like “I want a buddy.”
3. Be explicit about the two meanings of “limited” for member-facing bots:
   - **Limited by membership:** only verified community members should reach the intake flow.
   - **Limited by purpose:** the bot should only handle the pairing workflow, not general Hermes/admin tasks.
4. After verification, decide one of these access modes:
   - add known member numeric Telegram IDs to the allowlist;
   - keep the bot reachable by all Telegram users but require channel/roster verification before intake;
   - keep the bot public but require an intake/approval step in the conversation or backing CRM/Airtable.

Do not use Telegram handles as allowlist entries; use numeric Telegram user IDs. For a broad member launch, do not rely on prompt wording alone for safety: restrict the profile/toolsets and install a real access gate before broadening the gateway allowlist.

### Channel-gated member access

For communities with many rotating members, avoid manually maintaining weekly `allowed_users` lists. A better pattern is:

1. Add the concierge bot to the community Telegram channel/group (for example `@mombud`) and make it an admin if Telegram requires that for `getChatMember` checks.
2. Keep the initial gateway allowlist narrow while building the gate (for example only the owner/admin numeric Telegram ID). Do **not** open the gateway to all Telegram users until a replacement access gate is installed and verified.
3. Implement a real pre-intake access check, not just prompt instructions. A robust Hermes pattern is a `pre_gateway_dispatch` plugin/hook or equivalent gateway-side guard that runs before the agent receives the message:
   - accept `**kwargs` in the hook signature because gateway versions may pass extra metadata such as `telemetry_schema_version`;
   - read the sender Telegram numeric user ID from `MessageEvent.source.user_id` and username/display name from the raw Telegram message when available;
   - call Telegram Bot API `getChatMember` for the required channel/group (`@mombud`);
   - treat `member`, `administrator`, and `creator` as passing Telegram statuses;
   - check Airtable/CRM roster membership for the same Telegram account before allowing pairing intake;
   - check the active-member/status field, not only record existence. For Success Circles Airtable, `Team Roster.Membership = Current` is the active member gate; `Past` and `Reserve` should be blocked unless policy changes. `Availability` is cycle availability, not membership status;
   - if both checks pass, rewrite the message with a compact verified-access header so the agent does not try to verify again;
   - if either check fails, send a short denial/next-step message and skip agent dispatch.
4. Only after the gate passes with the owner/admin test account should you relax `TELEGRAM_ALLOWED_USERS` / gateway allowlist so all members can reach the gate. The gate, not the LLM prompt alone, is what limits access.
5. Keep scope-limiting separate from access-limiting: disable or block broad tools (terminal, file writes, memory edits, cron, GitHub/admin tools) and instruct the profile to refuse unrelated requests so the member bot remains pairing-only.
5. On `/start` or phrases like “I want a buddy,” use Telegram sender metadata automatically (`id`, username, first/last name/display name). Do **not** ask pairing/intake questions until both membership and roster checks are verified.
6. If verified, continue intake. If not verified, tell the user the bot is only for verified Momentum Buddy members and how to contact Success Circles support. If the membership check errors, give a temporary verification-failure message and ask them to retry later.

Telegram bots generally cannot export a full channel member list. Design the gate as “check this sender when they message the bot,” not “sync all subscribers.”
## Member onboarding flow

For member-facing concierge bots, `/start` and natural-language requests like “I want a buddy” should both be treated as intake entrypoints. Put the welcome/access/intake instruction in the **active concierge profile**, not in the admin profile. In practice, update the active profile's `SOUL.md` and/or an installed class-level concierge skill under the active profile's `skills/` directory.

First resolve the active paths:

```bash
hermes --profile PROFILE config path
hermes --profile PROFILE config env-path
```

Do not assume `~/.hermes/profiles/PROFILE`; some Hostinger/container installs use `/opt/data/profiles/PROFILE`.

Example Buddy Concierge verified-member message:

```text
Welcome to the Buddy Concierge!

I verified your Momentum Buddy Reminders access.

I’ll use your Telegram profile to help match you with the Success Circles roster. If the name you use in the Success Circles roster is different from your Telegram name, please mention it in your reply.

To pair you with a buddy who would best serve you over the next two weeks, please answer these questions:

1. Do you have someone in mind to pair with? Please type their name, or type “no preference.”
2. What are your goals or focus areas right now?
3. What is your preferred buddy type? For example: accountability, business growth, health, spiritual, creative, technical, etc.
4. What is your preferred cadence? For example: daily, weekly, once a week, SMS daily, or something else.
5. Is there something you are going through during the next couple of weeks that we should know about? If yes, please share.
```

Do not ask the pairing questions until membership is verified. Then collect answers either one-at-a-time or in a single message, summarize, and ask for confirmation before writing to external records. Avoid old command templates like `Pair [your name] with a Success Circles buddy`, and do not recommend a specific buddy before intake is complete and confirmed.

## Hostinger/Docker operational notes

- If `hermes` is not found in the VPS terminal, the user may be outside the container. Have them enter the Docker/container terminal first, then retry `hermes --version`.
- `hermes --profile PROFILE gateway setup` is the setup wizard for the dedicated concierge profile.
- If service installation is unsupported, run the gateway in the foreground for testing, then use a profile-specific `nohup` log as a simple background fallback.
- Avoid duplicate gateway processes when moving from foreground to background; stop the foreground run cleanly first.
- Never use broad kill commands such as `pkill -f "hermes.*gateway"` on a VPS with multiple Hermes profiles/gateways; it can stop the admin assistant gateway. Use profile-specific commands only, such as `pkill -f "hermes --profile buddy-concierge gateway run"`.
- If `ps` shows one active target gateway, do not run `gateway run --replace`; watch the active profile logs and test a real Telegram message first.
- If a natural-language phrase reaches the bot but `/start` appears silent, the token/gateway path is likely alive; inspect command handling and active profile instructions before re-running Telegram setup.
