PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip
QUARTO ?= $(shell \
  if [ -n "$$QUARTO_BIN" ] && [ -x "$$QUARTO_BIN" ]; then echo "$$QUARTO_BIN"; \
  elif [ -x tools/quarto/bin/quarto ]; then echo tools/quarto/bin/quarto; \
  elif command -v quarto >/dev/null 2>&1; then command -v quarto; \
  else echo quarto; fi)

# Portable TeX discovery: env override, then common TinyTeX / TeX Live locations.
TEX_BIN_DIR ?= $(shell \
  if [ -n "$$TEXLIVE_BIN" ] && [ -d "$$TEXLIVE_BIN" ]; then echo "$$TEXLIVE_BIN"; \
  elif [ -d "$$HOME/Library/TinyTeX/bin/universal-darwin" ]; then echo "$$HOME/Library/TinyTeX/bin/universal-darwin"; \
  elif [ -d "$$HOME/Library/TinyTeX/bin/aarch64-darwin" ]; then echo "$$HOME/Library/TinyTeX/bin/aarch64-darwin"; \
  elif [ -d "$$HOME/Library/TinyTeX/bin/x86_64-darwin" ]; then echo "$$HOME/Library/TinyTeX/bin/x86_64-darwin"; \
  elif [ -d "$$HOME/.TinyTeX/bin/x86_64-linux" ]; then echo "$$HOME/.TinyTeX/bin/x86_64-linux"; \
  elif [ -d "$$HOME/bin" ] && [ -x "$$HOME/bin/xelatex" ]; then echo "$$HOME/bin"; \
  else echo ""; fi)

export PATH := $(CURDIR)/tools/quarto/bin:$(TEX_BIN_DIR):$(PATH)

# full31-draft-check default mode: infra (Batch 0). Override with FULL31_DRAFT_CHECK_MODE=strict
FULL31_DRAFT_CHECK_MODE ?= infra

.PHONY: setup validate test preview pdf epub book all ci clean reader-preview analyze-reader-feedback ce-preproduction-normalize ce-preproduction-check ce-labs-test ce-figures-check ce-sources-check full31-check full31-report full31-draft-check full31-assets-check full31-reference-check full31-inventory full31-html full31-pdf full31-epub full31-book continuation-check continuation-preview ce-source-integrity ce-visual-text-check full31-claim-sources-check full31-terminology-check full31-publication-qa full31-quality-audit full31-continuity-check full31-pre-review-check full31-epubcheck kids-media-evidence-check kids-concept-spiral-check kids-pilot-check kids-review-prototype-check kids-curriculum-generate kids-one-tap-review-generate distribution-requirements-check adult-release-package-check adult-artifact-package-check adult-print-profiles adult-artifact-packages print-profile-check kids-standards-generate kids-standards-check kids-standards-research-complete-check kids-pilot-mapped-check publication-family-check publication-secrets-scan kids-epubcheck

setup:
	python3 -m venv .venv
	$(PIP) install -U pip
	$(PIP) install pyyaml pytest pypdf
	@if [ ! -x tools/quarto/bin/quarto ] && ! command -v quarto >/dev/null 2>&1; then \
	  echo "NOTE: Quarto not found. Run scripts/bootstrap_quarto.sh or install Quarto."; \
	fi
	@if ! command -v xelatex >/dev/null 2>&1; then \
	  echo "NOTE: xelatex not found on PATH. PDF may fail until TinyTeX/TeX Live is installed."; \
	  echo "      Optional: export TEXLIVE_BIN=/path/to/tex/bin or QUARTO_BIN=/path/to/quarto"; \
	fi

validate:
	$(PYTHON) scripts/validate_book.py
	$(PYTHON) scripts/validate_claims.py
	$(PYTHON) scripts/validate_glossary.py
	$(PYTHON) scripts/validate_terminology.py
	$(PYTHON) scripts/validate_labs.py
	$(PYTHON) scripts/validate_figures.py
	$(PYTHON) scripts/validate_accessibility.py
	$(PYTHON) scripts/validate_links.py
	$(PYTHON) scripts/validate_waike.py
	$(PYTHON) scripts/validate_citations.py
	$(PYTHON) scripts/validate_gate3_review.py
	$(PYTHON) scripts/validate_ce_preproduction.py
	$(MAKE) continuation-check
	# Quality-convergence invariants (registry must exist after integrator land).
	@if [ -f publication/full31/quality/QUALITY_ISSUES.yaml ]; then \
	  $(PYTHON) scripts/build_quality_issues_registry.py --check; \
	fi

test:
	$(PYTHON) -m pytest -q

preview:
	@chmod +x scripts/render_formats.sh
	@./scripts/render_formats.sh html
	@$(MAKE) continuation-preview

pdf:
	@chmod +x scripts/render_formats.sh
	@./scripts/render_formats.sh pdf

epub:
	@chmod +x scripts/render_formats.sh
	@./scripts/render_formats.sh epub

book:
	@chmod +x scripts/render_formats.sh
	@./scripts/render_formats.sh book

# Full 31-chapter book artifacts (separate from CH02 reader package preview/ch02.*)
full31-html:
	@chmod +x scripts/render_full31.sh
	@./scripts/render_full31.sh html

full31-pdf:
	@chmod +x scripts/render_full31.sh
	@./scripts/render_full31.sh pdf

full31-epub:
	@chmod +x scripts/render_full31.sh
	@./scripts/render_full31.sh epub

full31-book:
	@chmod +x scripts/render_full31.sh
	@./scripts/render_full31.sh all

reader-preview:
	@chmod +x scripts/build_reader_preview.sh
	@./scripts/build_reader_preview.sh

analyze-reader-feedback:
	$(PYTHON) scripts/analyze_reader_feedback.py

ce-preproduction-normalize:
	$(PYTHON) scripts/normalize_ce_preproduction.py
	$(PYTHON) scripts/regenerate_ce_candidate_indexes.py

ce-preproduction-check:
	$(PYTHON) scripts/regenerate_ce_candidate_indexes.py --check
	$(PYTHON) scripts/validate_ce_sources.py --check
	$(PYTHON) scripts/validate_ce_preproduction.py

ce-source-integrity:
	$(PYTHON) scripts/validate_ce_sources.py
	$(PYTHON) scripts/regenerate_ce_candidate_indexes.py
	$(PYTHON) scripts/validate_ce_sources.py --check

ce-labs-test:
	$(PYTHON) scripts/validate_labs.py
	$(PYTHON) -m pytest -q tests/test_lab_sys_001.py tests/test_lab_pkt_001.py tests/test_lab_trust_001.py tests/test_lab_ce06_001.py labs/LAB-CMS-001/tests/test_lab_cms_001.py

ce-figures-check:
	$(PYTHON) scripts/validate_ce_figures.py
	$(PYTHON) scripts/validate_visual_text_integrity.py

ce-visual-text-check:
	$(PYTHON) scripts/validate_visual_text_integrity.py

ce-sources-check:
	$(PYTHON) scripts/validate_ce_sources.py --check

full31-claim-sources-check:
	$(PYTHON) scripts/check_full31_claim_sources.py --check

# Automated HTML/EPUB/PDF + manuscript a11y QA. Does not certify WCAG/EPUB/print.
# Coordinate with `make validate` (source validators); this target audits rendered full31 artifacts.
full31-publication-qa:
	$(PYTHON) scripts/publication_qa_full31.py --pdf-log /tmp/full31-pdf-render.log

# Official W3C EPUBCheck (pinned; cached under tools/cache/). Not an a11y certification.
full31-epubcheck:
	$(PYTHON) scripts/run_epubcheck.py

full31-report:
	$(PYTHON) scripts/merge_full31_registry.py
	$(PYTHON) scripts/aggregate_full31_waike.py

full31-check:
	$(PYTHON) scripts/merge_full31_registry.py --check
	$(PYTHON) scripts/aggregate_full31_waike.py --check
	$(PYTHON) scripts/validate_full31.py
	$(PYTHON) scripts/check_full31_claim_sources.py --check

full31-draft-check:
	$(PYTHON) scripts/validate_full31_draft.py --mode $(FULL31_DRAFT_CHECK_MODE)

full31-assets-check:
	$(PYTHON) scripts/validate_full31_assets.py --check
	$(PYTHON) scripts/validate_figure_truth_drift.py --check

full31-reference-check:
	$(PYTHON) scripts/validate_full31_assets.py --check
	$(PYTHON) scripts/validate_figure_truth_drift.py --check
	FULL31_DRAFT_CHECK_MODE=strict $(MAKE) full31-draft-check

full31-inventory:
	$(PYTHON) scripts/generate_full31_manuscript_inventory.py --write
	$(PYTHON) scripts/generate_full31_manuscript_inventory.py --check

full31-terminology-check:
	$(PYTHON) scripts/validate_terminology.py

# Rebuild/check central QUALITY_ISSUES.yaml from wave ledgers.
# Default is --check-only so CI does not dirty provenance hashes.
full31-quality-audit:
	$(PYTHON) scripts/full31_quality_audit.py --check-only

full31-quality-audit-write:
	$(PYTHON) scripts/full31_quality_audit.py

# Continuity / duplication audit aid (writes ledger + identity matrix).
full31-continuity-check:
	$(PYTHON) scripts/audit_full31_continuity.py

# Pre-human-review candidate gates (BLOCKER/MAJOR open=0 + package labels).
full31-pre-review-check:
	$(PYTHON) scripts/full31_pre_review_check.py

# Adult distribution research packages (not retailer upload; not PUBLICATION_READY).
distribution-requirements-check:
	$(PYTHON) scripts/check_distribution_requirements.py --check

adult-release-package-check:
	$(PYTHON) scripts/check_adult_release_packages.py

adult-artifact-package-check:
	$(PYTHON) scripts/check_adult_artifact_packages.py --negative-tests

print-profile-check:
	$(PYTHON) scripts/check_print_profiles.py

adult-print-profiles:
	@chmod +x scripts/render_print_profiles.sh
	@./scripts/render_print_profiles.sh
	$(PYTHON) scripts/write_print_profile_results.py
	$(PYTHON) scripts/check_print_profiles.py

adult-artifact-packages:
	$(PYTHON) scripts/build_adult_artifact_packages.py
	$(PYTHON) scripts/check_adult_artifact_packages.py --negative-tests

# Publication-family shared infrastructure + secrets scan (S1–S11).
publication-family-check:
	$(PYTHON) scripts/check_publication_family.py
	$(PYTHON) scripts/scan_publication_secrets.py

publication-secrets-scan:
	$(PYTHON) scripts/scan_publication_secrets.py

# Kids EPUBCheck only when kids EPUB artifacts exist (none in this wave → skip PASS).
kids-epubcheck:
	@set -e; \
	eps=$$(find kids -name '*.epub' 2>/dev/null | wc -l | tr -d ' '); \
	if [ "$$eps" = "0" ]; then \
	  echo "kids-epubcheck: SKIP (no kids EPUB artifacts)"; \
	else \
	  echo "kids-epubcheck: found $$eps EPUB(s) — run official EPUBCheck per artifact in CI when authored"; \
	  exit 1; \
	fi
continuation-preview:
	$(PYTHON) scripts/build_continuation_preview.py

continuation-check:
	$(MAKE) ce-figures-check
	$(MAKE) ce-sources-check
	$(MAKE) full31-check
	$(MAKE) full31-draft-check
	$(MAKE) full31-assets-check
	@echo "continuation-check: PASS"

# Kids Edition — concept spiral + ONE TAP pilot (developmental prototypes only).
kids-curriculum-generate:
	$(PYTHON) scripts/generate_kids_curriculum_pilot.py
	$(PYTHON) scripts/build_kids_one_tap_review_prototype.py

kids-one-tap-review-generate:
	$(PYTHON) scripts/build_kids_one_tap_review_prototype.py

kids-concept-spiral-check:
	$(PYTHON) scripts/validate_kids_concept_spiral.py

kids-pilot-check:
	$(PYTHON) scripts/validate_kids_pilot.py

kids-review-prototype-check:
	$(PYTHON) scripts/validate_kids_review_prototype.py
	$(PYTHON) scripts/validate_kids_pilot.py

# Authoritative full automated build (requires Quarto + TeX + SVG converter for PDF).
all: validate test preview pdf epub

# TeX-free subset: validation, tests, and HTML only.
# Hosted GitHub Actions provisions TeX/librsvg and additionally runs EPUB + PDF.
ci: validate test preview

# Kids Edition: child-media evidence/source registers + design artifact presence.
kids-media-evidence-check:
	$(PYTHON) scripts/validate_kids_media_evidence.py

clean:
	rm -rf preview _book .pytest_cache __pycache__

# Kids Global Standards Atlas (publication-family track)
kids-standards-generate:
	$(PYTHON) scripts/generate_kids_standards_atlas.py

kids-standards-check:
	$(PYTHON) scripts/validate_kids_standards.py --architecture --metrics
	$(PYTHON) -m pytest -q tests/test_kids_standards.py

kids-standards-research-complete-check:
	$(PYTHON) scripts/validate_kids_standards.py --research-complete --metrics

kids-pilot-mapped-check:
	$(PYTHON) scripts/validate_kids_standards.py --pilot-mapped
