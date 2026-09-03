# Agent EVIDENCE-A — Full31 standards/source closure

**Branch:** `agent/evidence-a-standards`  
**Accepted-main base:** `18ec58005529bd16d680ee7419e4dea13150e9c6` (PR #4 merge)  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**gate-3:** UNCHANGED (this agent does not modify `publication/gates/gate-3/`)

## Audit (accepted main)

| Metric | Count |
|---|---:|
| Starting `SOURCE_NEEDED` | 51 |
| Resolved this wave | 38 |
| Remaining `SOURCE_NEEDED` | 13 |
| `SOURCE_IDENTIFIED` after wave | 86 |

## Resolved claim IDs

`CLM-CH03-001`, `CLM-CH03-002`, `CLM-CH05-001`, `CLM-CH05-002`, `CLM-CH05-003`, `CLM-CH06-002`, `CLM-CH07-002`, `CLM-CH08-002`, `CLM-CH09-001`, `CLM-CH10-001`, `CLM-CH10-002`, `CLM-CH10-003`, `CLM-CH11-003`, `CLM-CH11-004`, `CLM-CH12-004`, `CLM-CH14-002`, `CLM-CH15-001`, `CLM-CH15-002`, `CLM-CH15-003`, `CLM-CH15-004`, `CLM-CH16-004`, `CLM-CH16-005`, `CLM-CH17-001`, `CLM-CH17-002`, `CLM-CH17-004`, `CLM-CH18-001`, `CLM-CH18-002`, `CLM-CH18-003`, `CLM-CH19-001`, `CLM-CH19-002`, `CLM-CH20-001`, `CLM-CH20-002`, `CLM-CH20-003`, `CLM-CH20-004`, `CLM-CH25-003`, `CLM-CH26-001`, `CLM-CH27-003`, `CLM-CH28-002`

Also repaired undated WCAG shortcut on `CLM-CH14-004` → dual keys `wcag22-20231005` + `wcag22-20241212`.

## New bib keys (additive, verified)

| Key | Class | Location |
|---|---|---|
| `uefi-secure-boot-2.10` | standards | `ce-05/references.local.bib` |
| `tcg-pc-client-pfp-1.06` | standards | `ce-05/references.local.bib` |
| `w3c-mediacapture-streams-20251009` | standards | `ce-01/references.local.bib` |
| `git-scm-docs` | official docs | `ce-01/references.local.bib` |
| `semver-2.0.0` | specification | `ce-01/references.local.bib` |
| `oci-runtime-spec` | official docs | `ce-04/references.local.bib` |
| `iso-23247-1-2021` | standards | `ce-06/references.local.bib` |
| `itu-facts-figures-2025` | official statistics | `ce-06/references.local.bib` |

Reused existing verified keys heavily (`patterson-hennessy`, `tanenbaum-bos`, RFCs, IEEE 802.11, 3GPP TS 23.501, ITU-T QoE, `otel-signals`, NIST SP 800-145 / 500-325, etc.).

## Remaining `SOURCE_NEEDED` + next steps

| Claim | Next step |
|---|---|
| `CLM-CH08-001` | Pin multimedia/graphics survey textbook edition OR platform display-timing official docs (no invented hitch thresholds). |
| `CLM-CH09-002` | Select specific IEC/UL battery-safety designation with catalogue verification; no DIY abuse labs. |
| `CLM-CH09-003` | Select non-marketing mechanical/industrial-design textbook or standards survey. |
| `CLM-CH11-006` | Pin vendor/OS capsule A/B update recovery docs (living) for interrupted-update failure modes. |
| `CLM-CH13-003` | Pin a database-systems textbook edition (distinct from OS Concepts) before ACID wording. |
| `CLM-CH13-004` | Distributed-systems / official sync conflict docs. |
| `CLM-CH13-005` | Privacy retention + storage GC primary docs (no recovery exploit steps). |
| `CLM-CH17-003` | 6G roadmap primary (3GPP study items) if cited; keep “not deployed consumer fact” boundary. |
| `CLM-CH19-003` | Orbit-class delay qualitative sources without inventing product latency numbers. |
| `CLM-CH19-004` | Operator capability-class docs distinguishing messaging-only vs broadband satellite modes. |
| `CLM-CH22-004` | Sensing/IMU/camera privacy primary standards selection. |
| `CLM-CH29-003` | Product-management BoK refs only if used beyond pedagogy; no invented PMI/ISBN. |
| `CLM-CH30-004` | Manual BLS OOH (or equivalent) retrieval — automated bots blocked; leave until human-verified table cite. |

## Checks

- `make ce-sources-check` (regenerate then `--check`)
- `make full31-check` (includes new `full31-claim-sources-check`)
- `publication/gates/gate-3/` tree SHA unchanged vs accepted main

## Intentionally not done

- No PR opened / no merge
- No Gate 3 PASS claim / no fabricated reader evidence
- No invented DOI/ISBN/edition/page/year
