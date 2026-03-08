from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json_report(payload: dict[str, Any], outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    json_path = outdir / "latest.json"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return json_path


def _format_metric(value: float) -> str:
    return f"{value:.3f}"


def write_markdown_report(payload: dict[str, Any], outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    md_path = outdir / "latest.md"

    suite = payload["suite"]
    golden_set_version = payload.get("golden_set_version")
    aggregate = payload["aggregate"]
    cases = payload["cases"]

    lines = [
        "# Eval Run Summary",
        "",
        f"- Suite: `{suite}`",
    ]
    if golden_set_version:
        lines.append(f"- Golden set version: `{golden_set_version}`")
    lines.extend(
        [
            f"- Cases: `{len(cases)}`",
            "",
            "## Aggregate Metrics",
            "",
            f"- quality_pass_rate: `{_format_metric(aggregate['quality_pass_rate'])}`",
            f"- rewrite_convergence_rate: `{_format_metric(aggregate['rewrite_convergence_rate'])}`",
            f"- avg_rewrite_count: `{_format_metric(aggregate['avg_rewrite_count'])}`",
            f"- headline_compliance_rate: `{_format_metric(aggregate['headline_compliance_rate'])}`",
            f"- cta_presence_rate: `{_format_metric(aggregate['cta_presence_rate'])}`",
            f"- skim_format_rate: `{_format_metric(aggregate['skim_format_rate'])}`",
            f"- citation_precision: `{_format_metric(aggregate['citation_precision'])}`",
            "",
            "## Case Results",
            "",
            "| Case | Status | Quality | Rewrites | Notes |",
            "|---|---|---:|---:|---|",
        ]
    )

    for case in cases:
        status = "PASS" if case["passed"] else "FAIL"
        quality = "1" if case["metrics"]["final_quality_pass"] else "0"
        rewrites = str(case["metrics"]["rewrite_count"])
        notes = "; ".join(case["expectation_failures"] or []) or "-"
        lines.append(f"| {case['case_id']} | {status} | {quality} | {rewrites} | {notes} |")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md_path
