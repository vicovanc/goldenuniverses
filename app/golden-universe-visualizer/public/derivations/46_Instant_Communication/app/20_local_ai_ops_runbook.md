# 20 Local AI Ops Runbook

## Host prerequisites (macOS)

- Ollama installed and running locally
- local model pulled and validated
- host bridge running with approved device allowlist

## Startup sequence

1. start Docker services (`postgres` + backend stack)
2. verify DB and API health checks
3. verify local model runtime availability
4. load `dol.md` state and current protocol profile
5. start operator app and run a dry simulation cycle

## Failure handling

- if local model unavailable: degrade to manual-only mode
- if translation/codec fails: block transmission and request operator review
- if autonomy policy violation attempted: log critical anomaly and disable auto actions
