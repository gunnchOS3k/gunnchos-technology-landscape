# Child-Media Research Report

**Status:** `DRAFT_INTERNAL`  
**Registers:** `CHILD_MEDIA_SOURCE_REGISTER.yaml`, `CHILD_MEDIA_EVIDENCE_REGISTER.yaml`  
**Retrieved / compiled:** 2026-09-03  
**QA audited:** 2026-09-03 (Track 4 — evidence quality)  
**Child testing in this wave:** none  
**Register versions:** `0.1.1`

## Counts (post-QA)

| Metric | Count |
| --- | --- |
| Sources in source register | 21 (−3 unused vanity sources removed) |
| Evidence entries retained | 30 (0 removed) |
| Evidence confidence downgraded | 3 (CME-004, CME-017, CME-027) |
| Production rules retained | 9 |
| Production rules downgraded (wording) | 1 (RULE-STABLE-CAST) |
| Mandatory topics covered | 23 / 23 |
| Explicitly rejected unsupported claims | 9 (+3 from QA) |

### Evidence by topic (entries)

| Topic | Entries |
| --- | --- |
| infant_visual_attention | 2 |
| color_contrast | 2 |
| visual_clutter | 2 |
| shape_complexity | 1 |
| child_directed_speech | 1 |
| pitch_contour | 1 |
| speaking_rate | 1 |
| repetition | 1 |
| pause_response_cadence | 1 |
| repeated_exposure | 1 |
| songs_rhyme | 1 |
| memory_word_learning | 1 |
| stable_characters | 1 |
| parasocial_character_learning | 1 |
| participatory_prompts | 1 |
| caregiver_co_use | 2 |
| serve_and_return | 1 |
| pacing | 1 |
| fast_fantastical_media | 1 |
| attention_vs_learning | 1 |
| child_centered_digital_design | 2 |
| autoplay_infinite_engagement | 2 |
| privacy_and_agency | 2 |

### Confidence mix (post-QA)

| Confidence | Entries |
| --- | --- |
| high | 18 |
| medium | 11 |
| low | 2 |
| provisional | 0 |

## QA actions (honest)

**URL / citation repairs (kept sources):**
- Horst repetition DOI `10.3388` → `10.3389` (was 404).
- Crawley participatory DOI page `.745` → `.630` (was 404; wrong pages).
- Teller acuity DOI/year corrected (`tb14255`/1979 → acuity-card 1986; PubMed landing).
- UNICEF GC25 path 404 → UN Digital Library `record/3897072`.
- Lillard & AAP Young Minds landings switched to PMC/PubMed where publisher bot-walls obscure DOI targets.
- Clarified Harvard Center on the Developing Child is **not** U.S. CDC.

**Removed sources (vanity / unused — no evidence links):**
- `SRC-AAP-MEDIA-SCHOOL-AGE`
- `SRC-NAEYC-DAP`
- `SRC-ZERO-TO-THREE-MEDIA`

**Downgrades (kept, weaker weight):**
- `CME-004` high → medium (AAP silence ≠ color-vision experiment).
- `CME-017` medium → low (parasocial→learning is attention/willingness, not proven causal learning).
- `CME-027` medium → low (5Rights advocacy secondary to ICO/AAP).
- `RULE-STABLE-CAST` statement stripped of editorial “omniscient AI” clause not supported by cited literature.

**Strong evidence preserved:** infant contrast/clutter (CME-001/003/005), CDS/prosody (CME-008/009), video-deficit / attention≠learning (CME-002/024), caregiver co-use + WHO under-5 (CME-019/030), ICO AADC / COPPA / CRC GC25 privacy-agency stack (CME-025/026/028/029).

## Findings (compressed)

**Vision / layout.** Infants need high contrast and low clutter; attention ≠ learning. Color supports salience but must never be the sole encoding; no magic “brain-activating” brand color.

**Speech / audio.** Child-directed speech features (expressive contour, clarity, slower rate, social contingency) support attention and language learning opportunities. Pitch *variation* and affect matter; constant squeaky pitch and Hz-IQ claims are rejected. Audio remains optional for access.

**Structure.** Repetition with variation, wait-time after prompts, and re-reading improve retention/participation more than one-shot novelty or continuous narration.

**Characters.** A small, stable, emotionally legible original cast can support engagement and teach-back; familiarity does **not** guarantee learning; do not copy third-party IP.

**Caregivers.** Serve-and-return and joint media engagement make caregiver co-use first-class for 0–5; print-first for infants/toddlers (AAP/WHO aligned). Do not claim digital prompts “wire the brain.”

**Pacing / ethics.** Fast fantastical pacing can briefly tax EF in preschool lab settings; design for comprehension, not watch-time; no permanent-EF-harm slogans. Autoplay off, no infinite engagement loops, privacy/agency by default (ICO AADC / COPPA / CRC GC25).

## Limitations

- Many studies are lab, short-term, or WEIRD-sample; cultural CDS variation exists.
- Educational-TV participation studies are used for **methodology only** (no IP imitation).
- Regulatory codes are jurisdiction-specific; counsel required before live digital launch.
- Publisher pages may bot-wall automated fetchers; DOI redirects / PubMed / PMC landings used for resolvability checks.
- This wave collected **no** child/caregiver outcome data.

## Adopted rules vs rejected claims

See `adopted_production_rules` and `rejected_unsupported_claims` in the evidence register.

**Adopted:** high salience + low clutter; natural prosody; repetition with variation; participatory wait; caregiver co-use + print-first for youngest; moderate pacing; no compulsion patterns; stable original cast (engagement, not guaranteed learning); color not sole encoding.

**Rejected (includes QA additions):** exact-color brain activation; 432 Hz intelligence; high-pitch-makes-learning; secret-frequency IQ songs; infant screen-attention-equals-learning; infinite personalized autoplay as education; character familiarity alone guarantees learning; permanent EF damage from fast cartoons; digital serve-and-return “wires the brain.”

## Integrator refresh (2026-09-03)

- Evidence/source registers remain the authority for design adoption.
- `make kids-media-evidence-check` is wired into family CI.
- No child validation was fabricated; media findings inform prototype rules only.
- Source count decreased after QA on purpose (no vanity inflation).
