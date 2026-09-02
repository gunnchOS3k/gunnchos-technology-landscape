# Gate 3 responses intake

This directory holds **real human** reader feedback for Gate 3.

## Rules

1. **Only real human feedback belongs here.**
2. **Do not generate synthetic responses** for publication evidence.
3. **Redact** unnecessary personal information before committing.
4. Preserve **raw** responses here; put summaries/themes under `../analysis/`.
5. Each file must set `review_id` to the active snapshot (e.g. `CH02-REVIEW-R1`).
6. Prefer `reviewer_code` / pseudonym; optional name only if the reviewer chooses it.
7. Never store passwords, tokens, private messages, device serials, or precise location.

## Filename pattern

`RESP-<reader_level>-<reviewer_code>.yaml`

Example: `RESP-explorer-R07.yaml`

Conform to `../reader_feedback_schema.yaml`.

## Synthetic fixtures

Synthetic examples used by unit tests live only under `tests/fixtures/`.
They must **never** be copied into this directory.
