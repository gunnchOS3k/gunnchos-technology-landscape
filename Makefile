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

.PHONY: setup validate test preview pdf epub book all ci clean reader-preview analyze-reader-feedback ce-preproduction-normalize ce-preproduction-check

setup:
	python3 -m venv .venv
	$(PIP) install -U pip
	$(PIP) install pyyaml pytest
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
	$(PYTHON) scripts/validate_labs.py
	$(PYTHON) scripts/validate_figures.py
	$(PYTHON) scripts/validate_accessibility.py
	$(PYTHON) scripts/validate_links.py
	$(PYTHON) scripts/validate_waike.py
	$(PYTHON) scripts/validate_citations.py
	$(PYTHON) scripts/validate_gate3_review.py
	$(PYTHON) scripts/validate_ce_preproduction.py

test:
	$(PYTHON) -m pytest -q

preview:
	@chmod +x scripts/render_formats.sh
	@./scripts/render_formats.sh html

pdf:
	@chmod +x scripts/render_formats.sh
	@./scripts/render_formats.sh pdf

epub:
	@chmod +x scripts/render_formats.sh
	@./scripts/render_formats.sh epub

book:
	@chmod +x scripts/render_formats.sh
	@./scripts/render_formats.sh book

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
	$(PYTHON) scripts/validate_ce_preproduction.py

# Authoritative full automated build (requires Quarto + TeX + SVG converter for PDF).
all: validate test preview pdf epub

# TeX-free subset: validation, tests, and HTML only.
# Hosted GitHub Actions provisions TeX/librsvg and additionally runs EPUB + PDF.
ci: validate test preview

clean:
	rm -rf preview _book .pytest_cache __pycache__
