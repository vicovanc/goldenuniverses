# 19 Multilingual and Signal Codec

## Language layer

- user I/O in multiple languages (for operator workflows)
- canonical internal command representation in English technical schema
- translation memory for recurring lab phrases and protocol terms

## Signal encoding modes

- binary symbol mode
- pulse timing mode
- Morse code mode
- custom GU phase-symbol mode

## Encode/decode flow

1. natural language text -> normalized semantic packet
2. semantic packet -> selected signal codec
3. transmitted signal -> decoded symbols
4. decoded symbols -> translated language output

## Integrity rules

- store both source and translated content
- store codec parameters and decoding confidence
- mark ambiguity when decode confidence below threshold
