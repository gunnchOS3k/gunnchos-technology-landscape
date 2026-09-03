# Concept Edition preproduction figures (Agent F)

Outputs for CE-1/3/4/5/6 figure plans. Gate note: **GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING**.

- `ce-0N/*.svg` — implemented educational SVGs
- `accessibility/*.yaml` — a11y sidecars
- `manifests/*.blocked.yaml` — blocked figures (e.g. measured without fixture)
- `ce_figure_registry.yaml` — registry + counts

Templates live in `figures/templates/`. Validate with:

```bash
.venv/bin/python scripts/validate_ce_figures.py
```

Does not modify CH02-REVIEW-R1 reader package figures.
