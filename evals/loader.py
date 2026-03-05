from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from evals.schema import EvalCase, GoldenManifest


EVALS_DIR = Path(__file__).resolve().parent
CASES_DIR = EVALS_DIR / "cases"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain an object: {path}")
    return data


def load_case(path: Path) -> EvalCase:
    return EvalCase.model_validate(_load_yaml(path))


def load_golden_manifest(path: Path | None = None) -> GoldenManifest:
    manifest_path = path or (CASES_DIR / "golden" / "manifest.yaml")
    return GoldenManifest.model_validate(_load_yaml(manifest_path))


def list_case_paths(suite: str) -> tuple[list[Path], GoldenManifest | None]:
    if suite == "golden":
        manifest = load_golden_manifest()
        golden_dir = CASES_DIR / "golden"
        return [golden_dir / case_name for case_name in manifest.cases], manifest

    if suite == "challenge":
        challenge_dir = CASES_DIR / "challenge"
        return sorted(challenge_dir.glob("*.yaml")), None

    raise ValueError(f"Unknown suite: {suite}")

