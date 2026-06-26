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
2. Verify end-to-end with a real Telegram message such as `/start`.
3. After verification, decide one of these access modes:
   - add known member numeric Telegram IDs to the allowlist;
   - open the concierge bot to all users if the bot is intentionally public;
   - keep the bot reachable by all Telegram users but require membership verification before intake;
   - keep the bot public but require an intake/approval step in the conversation or backing CRM/Airtable.

Do not use Telegram handles as allowlist entries; use numeric Telegram user IDs.

### Channel-gated member access

For communities with many rotating members, avoid manually maintaining weekly `allowed_users` lists. A better pattern is:

1. Add the concierge bot to the community Telegram channel/group (for example `@mombud`) and make it an admin if Telegram requires that for `getChatMember` checks.
2. Remove or relax the Hermes gateway hard allowlist so member messages reach the concierge at all; otherwise the gateway rejects the user before the agent/helper can check membership.
3. On `/start` or phrases like “I want a buddy,” use Telegram sender metadata automatically (`id`, username, first/last name/display name) and check that specific user against the channel with Telegram Bot API `getChatMember`.
4. Do **not** ask pairing/intake questions until membership is verified.
5. If verified, continue intake. If not verified, tell the user to join the required channel and try `/start` again. If the membership check errors, give a temporary verification-failure message and ask them to retry later.

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
