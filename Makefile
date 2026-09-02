PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip
QUARTO ?= $(shell if [ -x tools/quarto/bin/quarto ]; then echo tools/quarto/bin/quarto; elif command -v quarto >/dev/null 2>&1; then command -v quarto; else echo quarto; fi)
TINYTEX_BIN := $(HOME)/Library/TinyTeX/bin/universal-darwin
export PATH := $(CURDIR)/tools/quarto/bin:$(TINYTEX_BIN):$(PATH)

.PHONY: setup validate test preview pdf epub all clean

setup:
	python3 -m venv .venv
	$(PIP) install -U pip
	$(PIP) install pyyaml pytest
	@if [ ! -x tools/quarto/bin/quarto ]; then \
	  echo "NOTE: Local Quarto not found at tools/quarto. Run scripts/bootstrap_quarto.sh or install Quarto."; \
	fi
	@if [ ! -x "$(TINYTEX_BIN)/xelatex" ]; then \
	  echo "NOTE: TinyTeX/xelatex not found. PDF may fail until \`quarto install tinytex\`."; \
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

all: validate test preview

clean:
	rm -rf preview .pytest_cache __pycache__
