# Multilingual Architecture Notes

**Status:** `DRAFT_INTERNAL`  
**Hard rule:** Do **not** machine-translate final child-facing books and call them validated.

## Source language

```yaml
source_language: en
```

## Per-locale status fields (required before any “validated” claim)

```yaml
locale: # BCP-47, e.g. es-419, zh-Hans, ar
translation_status: NOT_STARTED | MT_DRAFT_UNVALIDATED | HUMAN_DRAFT | LINGUISTIC_REVIEWED | APPROVED
linguistic_review_status: NOT_STARTED | IN_PROGRESS | DONE
cultural_review_status: NOT_STARTED | IN_PROGRESS | DONE
technical_term_review_status: NOT_STARTED | IN_PROGRESS | DONE
read_aloud_review_status: NOT_STARTED | IN_PROGRESS | DONE | N_A
validator_claim_allowed: false  # flip true only when all required reviews DONE
```

Current wave: **no locale has `APPROVED` child-facing translation.** Any MT output is `MT_DRAFT_UNVALIDATED` only.

## Layout expansion

- Design figures/text boxes with **≥30%** expansion headroom for Romance/Germanic growth; more for some languages.  
- Prefer reflowable text for ELEM bands; fixed-layout young picture books need per-locale layout QA.  
- Avoid embedding English-only in illustration art when terms must translate.

## Priority (proposed, not committed)

Prioritize future languages using WAIKE / global-reach demand signals (owner to confirm). Placeholder priority list for planning only:

1. Spanish (es-419 / es-ES decision pending)  
2. Mandarin Chinese (script decision pending)  
3. Arabic (RTL layout path required)  
4. French  
5. Additional locales per reach data  

## Caregiver home language

Even before full book translation, caregiver guides should explicitly invite **home-language** naming and talk (see `CAREGIVER_GUIDE_SYSTEM.md`).
