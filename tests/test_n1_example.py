"""Regression tests for the documented pandapower N-1 example."""
from pathlib import Path

import pandapower as pp
import pandapower.networks as pn


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "powerskills-tool" / "skills" / "pandapower" / "references" / "EXAMPLES.md"
SECTION = "### Example 8: N-1 Contingency Analysis"


def _load_example_namespace():
    text = EXAMPLES.read_text(encoding="utf-8")
    section = text.split(SECTION, 1)[1]
    code = section.split("```python", 1)[1].split("```", 1)[0]
    namespace = {"__name__": "documented_n1_example"}
    exec(compile(code, str(EXAMPLES), "exec"), namespace)
    return namespace


def test_documented_n1_example_accounts_for_each_line_outage():
    namespace = _load_example_namespace()
    net = namespace["net"]
    results = namespace["results"]

    assert len(results) == len(net.line)
    assert all(r["status"] in {"converged", "failed", "diverged"} for r in results)
    assert all(
        {"voltage_violations", "line_overloads", "trafo_overloads"} <= r.keys()
        for r in results
    )
    assert sum(r["status"] == "converged" for r in results) > 0
    assert sum(r["status"] == "converged" for r in results) + sum(
        r["status"] == "failed" for r in results
    ) + sum(r["status"] == "diverged" for r in results) == len(net.line)


def test_n1_example_records_success_failure_and_divergence(monkeypatch):
    namespace = _load_example_namespace()
    net = namespace["net"]
    analyze_line_outages = namespace["analyze_line_outages"]
    original_runpp = pp.runpp
    line_ids = list(net.line.index)
    assert len(line_ids) >= 3
    fail_line, diverge_line = line_ids[:2]

    def controlled_runpp(test_net, **kwargs):
        outage_ids = test_net.line.index[~test_net.line["in_service"]]
        assert len(outage_ids) == 1
        outage_id = outage_ids[0]
        if outage_id == fail_line:
            raise RuntimeError("injected contingency failure")
        if outage_id == diverge_line:
            test_net.converged = False
            return None
        return original_runpp(test_net, **kwargs)

    results = analyze_line_outages(net, run_power_flow=controlled_runpp)
    by_id = {int(r["contingency"].split()[-1]): r for r in results}

    assert by_id[int(fail_line)]["status"] == "failed"
    assert "injected contingency failure" in by_id[int(fail_line)]["error"]
    assert by_id[int(diverge_line)]["status"] == "diverged"
    assert any(r["status"] == "converged" for r in results)
    assert len(results) == len(net.line)
