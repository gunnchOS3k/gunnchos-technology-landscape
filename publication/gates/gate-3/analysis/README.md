# Gate 3 feedback analysis

Analysis outputs (summaries, theme lists, revision ledgers) belong here.

## Rules

- Derive analysis only from real files in `../responses/`.
- Keep raw responses in `responses/`; keep derived notes here.
- If `responses/` has no response YAML files, analysis must report `NO_READER_EVIDENCE`.
- Do not invent placeholder statistics.

## Tooling

```bash
make analyze-reader-feedback
# or
.venv/bin/python scripts/analyze_reader_feedback.py
```
