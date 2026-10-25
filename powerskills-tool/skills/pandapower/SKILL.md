---
name: pandapower
description: Progressive-disclosure workflow for pandapower power-system studies. Use whenever the user wants to load, build, or inspect a pandapower network, run AC power flow, check bus voltages or line and transformer loading, or screen N-1 contingencies — even when they just say "run a load flow", "check this case", "is anything overloaded", or name a case file like case39.json. Exposes a clean base-case solve before advanced outage studies. Reach for this instead of answering pandapower grid questions unaided.
---

# pandapower workflow

Start with the network model and a clean base-case solve. Use contingency analysis only after the steady-state case is credible.

## Default tool ladder
1. `load_network(file_path)` or `create_empty_network()`
2. `get_network_info()` to inspect buses, lines, transformers, generators, loads, and switches.
3. `run_power_flow(...)` to establish the base operating point.
4. `run_contingency_analysis(...)` only after the base case solves and the monitoring limits are clear.

### Example sequence
Using the `case39.json` network shipped with this skill:
```
load_network("case39.json")   -> 39 buses, 34 lines, 12 transformers, 10 generators
get_network_info()            -> confirms slack bus, switch states, and rating fields
run_power_flow()              -> converged; report min/max res_bus.vm_pu and worst loading_percent
run_contingency_analysis()    -> report every attempted outage as converged or failed, then inspect violations
```
Read the base-case numbers before running contingencies, then verify that the contingency sweep accounted for every requested outage. Use the escalation table below on whatever the solve actually reports.

## Working rules
- Do not run contingencies before checking the base-case voltages and loading.
- Treat a failed contingency power flow as an explicit study outcome; do not interpret a partial result set as an all-clear.
- After N-1, distinguish failed/diverged cases from converged cases with voltage or loading violations.
- Use pandapower for AC feasibility and fast screening, then escalate only when the question requires more.

## Escalation triggers
Map what the solve reports to the mitigation skill that handles it, and quote the numbers that tripped it (bus + vm_pu, element + loading %) rather than saying "violations exist".

| Observation | Escalate to |
|---|---|
| `res_bus.vm_pu` < 0.95 or > 1.05 | `voltage-violation-mitigation` |
| `res_line` / `res_trafo` `loading_percent` > 100 | `thermal-overload-mitigation` |
| `run_contingency_analysis` flags any N-1 violation or islanding | `contingency-mitigation` |
| The base-case `run_power_flow` or a contingency power flow fails or diverges | `convergence-failure-mitigation` |
| The study is DER (PV, storage) integration on a distribution network | `der-hosting-capacity-mitigation` |

## Local assets in this skill
- `case39.json` — a ready test network.
- `scripts/network_analysis.py` — structured base-case review.
- `scripts/contingency_analysis.py` — local N-1 screening with per-contingency status and summary reporting.

## Deliver
- The network loaded and whether the base case converged.
- The key voltage or loading findings.
- For contingency studies, how many outages were attempted, how many converged, how many failed/diverged, and how many converged cases had violations.
- Whether contingency or mitigation work is now justified.
