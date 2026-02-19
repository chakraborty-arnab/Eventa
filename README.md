# Eventa

A local, event-driven personal AI that logs your life via Discord.

Send a text, voice message, or image — Eventa understands and logs it.

## What it logs

- **Food** — "had a protein bar"
- **Weight** — "76kg" or photo of a scale
- **Sleep** — "slept at 11pm, woke at 7am"
- **Workout** — "bench press 3x8 60kg", "ran 5km"

## Setup

Add to `.env`:
```
DISCORD_TOKEN=
OPENROUTER_API_KEY=
```

See `ingress/README.md` for Discord bot setup.

## Run

```bash
make eventa
```
