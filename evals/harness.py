from __future__ import annotations

import argparse
import copy
import json
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evals.loader import list_case_paths, load_case
from evals.metrics import MetricValue, compute_aggregate, compute_case_metrics, evaluate_expectations
from evals.report import write_json_report, write_markdown_report
from evals.schema import EvalCase


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from app.config import settings
from app.prompts import RESEARCH_SYSTEM, REWRITE_SYSTEM, STRATEGIST_SYSTEM, WRITER_SYSTEM
from app.state import AppState
from integrations.llm_openai import OpenAIClient
from integrations.serp import SerpClient
from workflow.graph import content_marketing_graph


def _node_name_from_system(system_prompt: str) -> str:
    if system_prompt.startswith(RESEARCH_SYSTEM):
        return "research"
    if system_prompt.startswith(STRATEGIST_SYSTEM):
        return "strategist"
    if system_prompt.startswith(WRITER_SYSTEM):
        return "writer"
    if system_prompt.startswith(REWRITE_SYSTEM):
        return "rewrite"
    return "unknown"


def _first_fixture_url(case: EvalCase) -> str:
    if case.fixtures.serp_fixture:
        return case.fixtures.serp_fixture[0].url
    return "https://example.com/source-one"


def _default_stub_payload(case: EvalCase, node_name: str) -> dict[str, Any]:
    citation_url = _first_fixture_url(case)
    cta = "Book a short strategy call today."
    if node_name == "research":
        return {
            "key_findings": [
                "Teams with clear workflows publish more consistently.",
                "Repeatable review loops improve post quality.",
                "Citation-backed claims increase trust in B2B content.",
            ],
            "angles": ["Operational consistency for B2B marketing teams"],
            "stats_or_quotes": [],
            "citations": [
                {
                    "url": citation_url,
                    "supporting_claim": "Teams with a repeatable process ship better content.",
                }
            ],
        }
    if node_name == "strategist":
        topic = case.inputs.user_query or case.inputs.topic or "AI content marketing"
        return {
            "topic": topic,
            "audience": case.inputs.audience,
            "objective": "Educate and engage",
            "channel": case.inputs.platform,
            "angle": "Operational consistency for B2B marketing teams",
            "outline": [
                "Name the workflow problem teams face.",
                "Show what breaks without process.",
                "Describe a repeatable operating rhythm.",
                "Connect the process to measurable output quality.",
                "End with a clear next step.",
            ],
            "cta": cta,
        }
    if node_name in {"writer", "rewrite"}:
        return {
            "channel": case.inputs.platform,
            "headline": "Operational workflows improve B2B content consistency",
            "body": (
                "Most teams do not need more content ideas.\n\n"
                "They need a repeatable system for research, drafting, and revision.\n\n"
                f"{cta}"
            ),
            "cta": cta,
            "citations": [
                {
                    "url": citation_url,
                    "supporting_claim": "Operational workflows improve quality and consistency.",
                    "source_title": "Workflow benchmark study",
                }
            ],
        }
    return {}


def _build_revise_seed_state(case: EvalCase) -> AppState:
    citation_url = _first_fixture_url(case)
    cta = "Book a short strategy call today."
    topic = case.inputs.user_query or case.inputs.topic or "AI content marketing"
    sources = []
    for item in case.fixtures.serp_fixture[:3]:
        source = item.model_dump()
        source["retrieved_at"] = datetime.now(timezone.utc).isoformat()
        source["source_type"] = "serp"
        sources.append(source)
    return {
        "research": {
            "user_query": topic,
            "search_queries": [topic],
            "sources": sources,
            "key_findings": ["A baseline finding."],
            "angles": ["A practical angle."],
            "stats_or_quotes": [],
            "citations": [
                {
                    "url": citation_url,
                    "supporting_claim": "A baseline claim.",
                    "source_title": "Baseline source",
                }
            ],
        },
        "brief": {
            "topic": topic,
            "audience": case.inputs.audience,
            "objective": "Educate and engage",
            "channel": case.inputs.platform,
            "angle": "A practical angle.",
            "outline": [
                "Point one",
                "Point two",
                "Point three",
                "Point four",
                "Point five",
            ],
            "cta": cta,
        },
        "draft": {
            "channel": case.inputs.platform,
            "headline": "Original draft headline",
            "body": "Old paragraph without enough formatting.",
            "cta": cta,
            "citations": [],
        },
        "quality_report": {
            "status": "fail",
            "reasons": ["Draft is not skimmable enough for LinkedIn."],
            "fixes": ["Use at least three short paragraphs separated by blank lines."],
            "checks": {"skim_ok": False},
        },
    }


@contextmanager
def _patched_integrations(case: EvalCase):
    original_search = SerpClient.search
    original_complete_json = OpenAIClient.complete_json

    def fake_search(
        self,
        query: str,
        num_results: int = 10,
        timeout_s: int = 20,
        hl: str = "en",
        gl: str = "us",
    ) -> list[dict[str, str]]:
        del query, timeout_s, hl, gl
        return [item.model_dump() for item in case.fixtures.serp_fixture[:num_results]]

    def fake_complete_json(
        self,
        system: str,
        user: str,
        temperature: float = 0.0,
        max_retries: int = 1,
    ) -> dict[str, Any]:
        del user, temperature, max_retries
        node_name = _node_name_from_system(system)
        payload = case.fixtures.stubbed_node_outputs.get(node_name)
        if isinstance(payload, dict):
            return copy.deepcopy(payload)
        return _default_stub_payload(case, node_name)

    SerpClient.search = fake_search
    OpenAIClient.complete_json = fake_complete_json
    try:
        yield
    finally:
        SerpClient.search = original_search
        OpenAIClient.complete_json = original_complete_json


def _build_initial_state(case: EvalCase) -> AppState:
    initial_state: AppState = {
        "intent": case.inputs.intent,
        "topic": case.inputs.topic or case.inputs.user_query or "",
        "user_query": case.inputs.user_query or case.inputs.topic or "",
        "audience": case.inputs.audience,
        "platform": case.inputs.platform,
        "constraints": case.inputs.constraints,
    }
    if case.inputs.revision_request:
        initial_state["revision_request"] = case.inputs.revision_request
    if case.inputs.intent.lower() == "revise":
        initial_state.update(_build_revise_seed_state(case))
    return initial_state


def run_case(case: EvalCase, case_file: Path) -> dict[str, Any]:
    with _patched_integrations(case):
        final_state = content_marketing_graph.invoke(_build_initial_state(case))

    metrics = compute_case_metrics(final_state=final_state, max_iterations=case.expectations.max_iterations)
    expectation_failures = evaluate_expectations(metrics=metrics, expectations=case.expectations)
    if not bool(metrics["quality_pass"]):
        expectation_failures.append("quality report status was not pass")

    return {
        "case_id": case.case_id,
        "file": str(case_file),
        "passed": len(expectation_failures) == 0,
        "expectation_failures": expectation_failures,
        "metrics": metrics,
        "quality_status": final_state.get("quality_report", {}).get("status"),
        "rewrite_count": final_state.get("rewrite_count", 0),
    }


def run_suite(suite: str, outdir: Path, fail_on_threshold: bool = False) -> dict[str, Any]:
    case_paths, manifest = list_case_paths(suite)
    case_results: list[dict[str, Any]] = []
    metric_rows: list[dict[str, MetricValue]] = []

    for case_path in case_paths:
        case = load_case(case_path)
        result = run_case(case, case_path)
        case_results.append(result)
        metric_rows.append(result["metrics"])

    aggregate = compute_aggregate(metric_rows)
    run_payload = {
        "suite": suite,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "golden_set_version": manifest.golden_set_version if manifest else None,
        "aggregate": aggregate,
        "cases": case_results,
    }

    json_path = write_json_report(run_payload, outdir=outdir)
    md_path = write_markdown_report(run_payload, outdir=outdir)

    if fail_on_threshold and any(not case["passed"] for case in case_results):
        raise RuntimeError(
            "One or more eval cases failed expectations. "
            f"See {json_path} and {md_path} for details."
        )

    return run_payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic offline eval suites.")
    parser.add_argument("--suite", choices=["golden", "challenge"], required=True)
    parser.add_argument("--outdir", default="evals/results")
    parser.add_argument("--fail-on-threshold", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    outdir = Path(args.outdir).resolve()
    try:
        payload = run_suite(
            suite=args.suite,
            outdir=outdir,
            fail_on_threshold=args.fail_on_threshold,
        )
    except RuntimeError as exc:
        print(str(exc))
        return 1

    print(
        json.dumps(
            {
                "suite": payload["suite"],
                "golden_set_version": payload.get("golden_set_version"),
                "case_count": len(payload["cases"]),
                "output_dir": str(outdir),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
