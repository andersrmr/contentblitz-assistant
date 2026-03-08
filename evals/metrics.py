from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Any

from evals.schema import EvalCaseExpectations

MetricValue = float | int | bool | str | list[str]

def compute_case_metrics(final_state: dict[str, Any], max_iterations: int) -> dict[str, MetricValue]:
    draft_data = final_state.get("draft")
    research_data = final_state.get("research")
    first_report_data = final_state.get("first_quality_report")
    final_report_data = final_state.get("quality_report")
    rewrite_count = int(final_state.get("rewrite_count", 0) or 0)

    first_quality_pass = (
        isinstance(first_report_data, dict) and first_report_data.get("status") == "pass"
    )
    final_quality_pass = (
        isinstance(final_report_data, dict) and final_report_data.get("status") == "pass"
    )
    rewrite_triggered = rewrite_count > 0
    rewrite_recovered = rewrite_triggered and (not first_quality_pass) and final_quality_pass
    first_failure_reasons = (
        list(first_report_data.get("reasons", []))
        if isinstance(first_report_data, dict)
        else []
    )
    checks = final_report_data.get("checks", {}) if isinstance(final_report_data, dict) else {}
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
    rewrite_converged = final_quality_pass and rewrite_count <= max_iterations

    return {
        "first_quality_pass": first_quality_pass,
        "final_quality_pass": final_quality_pass,
        "rewrite_triggered": rewrite_triggered,
        "rewrite_recovered": rewrite_recovered,
        "rewrite_converged": rewrite_converged,
        "rewrite_count": rewrite_count,
        "first_failure_reasons": first_failure_reasons,
        "route": str(final_state.get("route", "")),
        "headline_compliant": headline_compliant,
        "cta_present": cta_present,
        "skim_format": skim_format,
        "citation_precision": citation_precision,
        "citation_subset": citation_subset,
    }


def evaluate_expectations(metrics: dict[str, MetricValue], expectations: EvalCaseExpectations) -> list[str]:
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
    if expectations.require_quality_pass and not bool(metrics["final_quality_pass"]):
        failures.append("final quality report status was not pass")
    if not expectations.require_quality_pass and bool(metrics["final_quality_pass"]):
        failures.append("final quality report status unexpectedly passed")

    return failures


def compute_aggregate(case_metrics: list[dict[str, MetricValue]]) -> dict[str, Any]:
    if not case_metrics:
        return {
            "final_pass_rate": 0.0,
            "first_pass_pass_rate": 0.0,
            "rewrite_trigger_rate": 0.0,
            "rewrite_recovery_rate": 0.0,
            "avg_rewrite_count": 0.0,
            "first_pass_failure_reason_counts": {},
            "by_category": {},
        }

    rewritten_cases = [item for item in case_metrics if bool(item["rewrite_triggered"])]
    failure_reason_counts: Counter[str] = Counter()
    for item in case_metrics:
        failure_reason_counts.update(
            str(reason) for reason in item.get("first_failure_reasons", []) if isinstance(reason, str)
        )

    category_groups: dict[str, list[dict[str, MetricValue]]] = {}
    for item in case_metrics:
        category = str(item.get("category") or "uncategorized")
        category_groups.setdefault(category, []).append(item)

    by_category: dict[str, dict[str, float]] = {}
    for category, rows in category_groups.items():
        rewritten_rows = [row for row in rows if bool(row["rewrite_triggered"])]
        by_category[category] = {
            "final_pass_rate": mean(1.0 if bool(row["final_quality_pass"]) else 0.0 for row in rows),
            "first_pass_pass_rate": mean(1.0 if bool(row["first_quality_pass"]) else 0.0 for row in rows),
            "rewrite_trigger_rate": mean(1.0 if bool(row["rewrite_triggered"]) else 0.0 for row in rows),
            "rewrite_recovery_rate": (
                mean(1.0 if bool(row["rewrite_recovered"]) else 0.0 for row in rewritten_rows)
                if rewritten_rows
                else 0.0
            ),
        }

    return {
        "final_pass_rate": mean(
            1.0 if bool(item["final_quality_pass"]) else 0.0 for item in case_metrics
        ),
        "first_pass_pass_rate": mean(1.0 if bool(item["first_quality_pass"]) else 0.0 for item in case_metrics),
        "rewrite_trigger_rate": mean(1.0 if bool(item["rewrite_triggered"]) else 0.0 for item in case_metrics),
        "rewrite_recovery_rate": (
            mean(1.0 if bool(item["rewrite_recovered"]) else 0.0 for item in rewritten_cases)
            if rewritten_cases
            else 0.0
        ),
        "avg_rewrite_count": mean(float(item["rewrite_count"]) for item in case_metrics),
        "first_pass_failure_reason_counts": dict(failure_reason_counts),
        "by_category": by_category,
    }
