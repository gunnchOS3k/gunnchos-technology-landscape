# Quarto Print Profiles

| File | Profile id | Trim intent | Result |
| --- | --- | --- | --- |
| `_quarto-print-6x9.yml` | `print-6x9` | 6×9 primary | Rendered — see `PRINT_PROFILE_RESULTS.*` |
| `_quarto-print-7x10.yml` | `print-7x10` | 7×10 large alt | Rendered |
| `_quarto-print-85x11.yml` | `print-85x11` | 8.5×11 handout alt | Rendered |

**Usage:**

```bash
make adult-print-profiles
# or
./scripts/render_print_profiles.sh
python scripts/write_print_profile_results.py
```

**Feasibility:** Profiles are geometry overlays. POD certification still requires KDP upload
preview and live cover calculator (`LIVE_COVER_CALCULATOR_REQUIRED`).

**Review PDF intact:** Root `_quarto.yml` and `make full31-pdf` paths unchanged
(`DIGITAL_ACCESS_PDF` ≠ `PRINT_INTERIOR_PDF`).
