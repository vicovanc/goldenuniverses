# Stage2 App Program

Bluesteel-grade operator and analysis application for GU instant communication research.

## Locked decisions

- Electron desktop app runs on macOS host.
- Backend services run in Docker.
- Postgres runs in Docker with local named volume persistence.
- USB/Serial device integration uses host bridge service.
- Local AI must run fully offline (Ollama-compatible, Kimi K2.5 class where available).
- App includes autonomous memory loop with GU-skill knowledge base and decision policies.
- App includes multilingual translation and signal codec layer (text <-> symbols <-> Morse).

## Program structure

- `01`-`04`: requirements, architecture, physics, device I/O
- `05`-`07`: database, benchmark gates, integrity
- `08`-`11`: UX, sensors, orchestration, APIs
- `12`-`16`: reliability, validation, roadmap, operations, final closure
- `17`-`20`: offline AI runtime, autonomy/memory, language and signal codecs
- `docker/`: compose and env
- `sql/`: schema and migrations
- `data_schemas/`: JSON contracts
