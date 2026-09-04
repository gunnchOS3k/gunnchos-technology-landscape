# Owner decisions needed

Only decisions that require the human owner — not automatable integrator work.

## Adult edition

1. **Imprint / publisher legal name** — set `publisher_legal_name` / `imprint` (currently `OWNER_DECISION_PENDING`).
2. **ISBN purchase** — buy format-level ISBNs for paperback / hardcover / (optional) ebook; placeholders must remain until purchased. Do not invent numbers.
3. **Retailer accounts** — create KDP / Apple / Google / Kobo / library-distributor accounts outside the repo. Never commit credentials, tax IDs, or payment secrets.
4. **Price approval** — confirm free-access strategy (Apple/Google/Kobo/direct free; Amazon minimum/price-match pathway; print at lowest sustainable price; **no KDP Select** under wide-access objective).
5. **Hardcover in v1?** — ship hardcover now or defer.
6. **BISAC / Thema subjects** — choose final subject codes (do not paste proprietary taxonomies wholesale into the repo).
7. **Direct hosting venue** — where free EPUB/PDF are hosted and how ARR free-access wording is presented.
8. **Cover art approval** — technical proof is not marketing art; approve art direction.
9. **Publication approval** — explicit go-live after Gate 3 reader evidence and human reviews.

## Kids edition

1. **Rights confirmation for Kids** — default is same ARR manuscript + MIT-scoped tooling; confirm or choose otherwise (no blanket CC by default).
2. **Child-development SME + caregiver + educator reviews** — schedule ethical human review; do not fabricate child validation.
3. **Illustration art direction** — prototype SVGs are not final art.
4. **Board-book / print vendor** — select vendor and proof path (KDP board-book feasibility remains an external gate).
5. **Translation / cultural review priorities** — which languages/regions first.
6. **Kids identifiers** — ISBN/ASIN assignment only after owner purchase / retailer setup.
7. **Kids publication approval** — explicit; never implied by prototype presence.

## Explicit non-decisions (already settled for this wave)

- Do **not** publish live, buy ISBNs via automation, enroll KDP Select, or mark `PUBLICATION_READY`.
- Gate 3 remains `READER_EVIDENCE_PENDING` — not an owner “skip”.
- Free price ≠ open license (ARR manuscript retained).
