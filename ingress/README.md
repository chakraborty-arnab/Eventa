# Ingress — Discord Bot Setup

## 1. Create a Discord App
1. Go to https://discord.com/developers/applications → **New Application**
2. Name it (e.g. "Eventa") → **Create**

## 2. Create the Bot
1. **Bot** (left sidebar) → **Add Bot**
2. **Reset Token** → copy it → add to `.env`:
   ```
   DISCORD_TOKEN=your_token_here
   ```
3. Enable **Message Content Intent** (same page, scroll down)

## 3. Add Bot to Your Server
1. **OAuth2 → URL Generator** → check `bot` under Scopes
2. Under Bot Permissions check `Read Messages` + `Send Messages`
3. Open the generated URL → select your server → **Authorize**

## 4. Run
```bash
pip install -r requirements.txt
python ingress/discord_bot.py
```
