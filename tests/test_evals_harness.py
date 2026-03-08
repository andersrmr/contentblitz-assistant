from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evals.harness import run_suite


def test_harness_runs_golden_suite_and_writes_reports(tmp_path):
    outdir = tmp_path / "eval_results"
    payload = run_suite(suite="golden", outdir=outdir, fail_on_threshold=True)

    assert payload["suite"] == "golden"
    assert payload["golden_set_version"] == "v1.2.0"
    assert len(payload["cases"]) >= 9
    assert all(case["passed"] for case in payload["cases"])

    json_path = outdir / "latest.json"
    md_path = outdir / "latest.md"
    assert json_path.exists()
    assert md_path.exists()

    parsed = json.loads(json_path.read_text(encoding="utf-8"))
    assert parsed["suite"] == "golden"
    assert parsed["golden_set_version"] == "v1.2.0"


def test_harness_runs_single_case_by_case_id(tmp_path):
    outdir = tmp_path / "eval_results_single"
    payload = run_suite(
        suite="golden",
        outdir=outdir,
        fail_on_threshold=True,
        case_id="case_007_tone_violation_rewrite",
    )

    assert payload["suite"] == "golden"
    assert len(payload["cases"]) == 1
    assert payload["cases"][0]["case_id"] == "case_007_tone_violation_rewrite"
    assert payload["cases"][0]["passed"] is True

    json_path = outdir / "latest.json"
    md_path = outdir / "latest.md"
    assert json_path.exists()
    assert md_path.exists()


def test_harness_single_case_invalid_case_id_raises(tmp_path):
    outdir = tmp_path / "eval_results_invalid"
    try:
        run_suite(
            suite="golden",
            outdir=outdir,
            case_id="case_does_not_exist",
        )
        assert False, "Expected RuntimeError for missing case_id."
    except RuntimeError as exc:
        assert "Eval case 'case_does_not_exist' not found in suite 'golden'." in str(exc)
