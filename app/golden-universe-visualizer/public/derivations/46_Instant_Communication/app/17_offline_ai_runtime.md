# 17 Offline AI Runtime

## Requirements

- fully offline operation, no cloud dependencies
- local model provider compatibility via Ollama APIs
- support Kimi K2.5 class local models when packaged in Ollama-compatible runtime

## Runtime layers

1. model router (selects local model by task)
2. GU retrieval layer (loads equation/spec/protocol context)
3. autonomy policy engine (bounded actions only)
4. memory writer (stores decisions, outcomes, and learning notes)

## Safe autonomy policy

- AI can suggest and prefill actions
- AI cannot bypass blinding/integrity gates
- critical execution steps require operator acknowledgment
