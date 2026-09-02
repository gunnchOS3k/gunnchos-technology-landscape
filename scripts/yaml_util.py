"""YAML helpers. Prefer PyYAML; fail clearly if missing."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "PyYAML is required. Run `make setup` to create .venv and install dependencies."
        ) from exc
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def dump_yaml(data: Any) -> str:
    import yaml  # type: ignore

    return yaml.safe_dump(data, sort_keys=False)
