# 11 API Contracts

## Core endpoints

- `POST /runs` create run
- `POST /runs/{runId}/preregister` freeze protocol
- `POST /runs/{runId}/start` start acquisition
- `POST /runs/{runId}/stop` stop and seal run
- `GET /runs/{runId}/metrics` live computed metrics
- `GET /runs/{runId}/benchmarks` gate evaluation status
- `POST /device/ingest` host bridge ingestion endpoint
- `GET /artifacts/{runId}` evidence ledger and hashes
- `POST /ai/query` offline model inference request
- `POST /ai/autonomy/step` run one autonomous decision cycle
- `GET /ai/memory/{runId}` retrieve autonomous memory trace
- `POST /codec/encode` encode text into signal mode (binary/morse/custom)
- `POST /codec/decode` decode signal stream into text
- `POST /translate` translate between human language and protocol language

## Event stream topics

- `run.state.changed`
- `telemetry.frame`
- `decode.trial`
- `benchmark.updated`
- `integrity.alert`
- `ai.recommendation`
- `ai.autonomy.step`
- `codec.decoded`

## API invariants

- no mutable overwrites for sealed run artifacts
- all writes include protocol version and operator identity
- AI actions require policy tag and confidence score
