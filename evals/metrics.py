from __future__ import annotations

from statistics import mean
from typing import Any

from evals.schema import EvalCaseExpectations


def compute_case_metrics(final_state: dict[str, Any], max_iterations: int) -> dict[str, float | int | bool]:
    draft_data = final_state.get("draft")
    research_data = final_state.get("research")
    report_data = final_state.get("quality_report")
    rewrite_count = int(final_state.get("rewrite_count", 0) or 0)

    quality_pass = isinstance(report_data, dict) and report_data.get("status") == "pass"
    checks = report_data.get("checks", {}) if isinstance(report_data, dict) else {}
    headline_compliant = bool(
        isinstance(checks, dict) and checks.get("headline_len_ok") is True
    )
    cta_present = bool(isinstance(checks, dict) and checks.get("cta_present") is True)
    skim_format = bool(isinstance(checks, dict) and checks.get("skim_ok") is True)

    draft_citations = draft_data.get("citations", []) if isinstance(draft_data, dict) else []
    research_citations = research_data.get("citations", []) if isinstance(research_data, dict) else []
    draft_urls = {
        str(citation.get("url", ""))
        for citation in draft_citations
        if isinstance(citation, dict) and citation.get("url")
    }
    research_urls = {
        str(citation.get("url", ""))
        for citation in research_citations
        if isinstance(citation, dict) and citation.get("url")
    }
    if not draft_urls:
        citation_precision = 1.0
    elif not research_urls:
        citation_precision = 0.0
    else:
        citation_precision = len(draft_urls & research_urls) / len(draft_urls)

    citation_subset = draft_urls.issubset(research_urls) if draft_urls else True
    rewrite_converged = quality_pass and rewrite_count <= max_iterations

    return {
        "quality_pass": quality_pass,
        "rewrite_converged": rewrite_converged,
        "rewrite_count": rewrite_count,
        "route": str(final_state.get("route", "")),
        "headline_compliant": headline_compliant,
        "cta_present": cta_present,
        "skim_format": skim_format,
        "citation_precision": citation_precision,
        "citation_subset": citation_subset,
    }


def evaluate_expectations(
    metrics: dict[str, float | int | bool], expectations: EvalCaseExpectations
) -> list[str]:
    failures: list[str] = []

    rewrite_count = int(metrics["rewrite_count"])
    if rewrite_count > expectations.max_iterations:
        failures.append(
            f"rewrite_count {rewrite_count} exceeded max_iterations {expectations.max_iterations}"
        )
    if rewrite_count < expectations.min_rewrite_count:
        failures.append(
            f"rewrite_count {rewrite_count} was below min_rewrite_count {expectations.min_rewrite_count}"
        )
    if expectations.expected_route and str(metrics.get("route", "")) != expectations.expected_route:
        failures.append(
            f"route invariant failed: expected {expectations.expected_route}, got {metrics.get('route', '')}"
        )

    if expectations.require_citation_precision and not bool(metrics["citation_subset"]):
        failures.append("citation precision invariant failed (draft citation URLs must be subset of research URLs)")
    if expectations.require_headline_compliance and not bool(metrics["headline_compliant"]):
        failures.append("headline compliance invariant failed")
    if expectations.require_cta_presence and not bool(metrics["cta_present"]):
        failures.append("CTA presence invariant failed")
    if expectations.require_skim_format and not bool(metrics["skim_format"]):
        failures.append("skim format invariant failed")

    return failures


def compute_aggregate(case_metrics: list[dict[str, float | int | bool]]) -> dict[str, float]:
    if not case_metrics:
        return {
            "quality_pass_rate": 0.0,
            "rewrite_convergence_rate": 0.0,
            "avg_rewrite_count": 0.0,
            "headline_compliance_rate": 0.0,
            "cta_presence_rate": 0.0,
            "skim_format_rate": 0.0,
            "citation_precision": 0.0,
        }

    return {
        "quality_pass_rate": mean(1.0 if bool(item["quality_pass"]) else 0.0 for item in case_metrics),
        "rewrite_convergence_rate": mean(
            1.0 if bool(item["rewrite_converged"]) else 0.0 for item in case_metrics
        ),
        "avg_rewrite_count": mean(float(item["rewrite_count"]) for item in case_metrics),
        "headline_compliance_rate": mean(
            1.0 if bool(item["headline_compliant"]) else 0.0 for item in case_metrics
        ),
        "cta_presence_rate": mean(1.0 if bool(item["cta_present"]) else 0.0 for item in case_metrics),
        "skim_format_rate": mean(1.0 if bool(item["skim_format"]) else 0.0 for item in case_metrics),
        "citation_precision": mean(float(item["citation_precision"]) for item in case_metrics),
    }
