---
name: pypsa
description: Progressive-disclosure workflow for PyPSA studies. Use when the user asks to load or build a PyPSA network, inspect components, run power flow, solve OPF, or perform investment optimization, and when the agent should expose network inspection and feasibility steps before large optimization studies.
---

# PyPSA workflow

Start by creating or loading a named network handle. Use network inspection before optimization, and use operational optimization before investment optimization.

## Default tool ladder
1. `load_network(file_path)` or `create_network(...)` — create the active network handle.
2. `get_network_info(network_name)` and `get_component_details(...)` — understand topology, assets, and time series.
3. `run_power_flow(network_name, linear=False)` — feasibility checks.
4. `optimize_network(network_name, ...)` — dispatch or operational studies.
5. `optimize_investment(network_name, ...)` — expansion questions.
6. `import_from_csv_folder(...)` or `export_to_csv_folder(...)` — once the network state is worth moving.

**Example sequence:**
```
load_network("case39.nc")                         → network "case39" active, 39 buses
get_network_info("case39")                        → 10 generators, 46 lines, 19 loads
run_power_flow("case39", linear=False)            → converged, max line loading 87 %
optimize_network("case39", solver_name="highs")   → dispatch cost $48,200/h
```

## Working rules
- Do not jump straight into expansion optimization when a dispatch study can answer the question.
- Use AC or DC power flow to sanity-check a network before relying on optimization outputs.
- Treat PyPSA as a planning and scheduling engine, not the final authority on detailed reactive mitigation.
- Hand off infeasibility, curtailment, and reserve issues to [operations-planning-mitigation](../operations-planning-mitigation/SKILL.md).

## Local assets in this repo
- [`PyPSA/case39.nc`](case39.nc) — ready test network.
- [`PyPSA/scripts/network_analysis.py`](scripts/network_analysis.py) — inspection.
- [`PyPSA/scripts/optimization_analysis.py`](scripts/optimization_analysis.py) — OPF result review.
- [`PyPSA/scripts/expansion_analysis.py`](scripts/expansion_analysis.py) — capacity expansion studies.
- [`PyPSA/scripts/contingency_analysis.py`](scripts/contingency_analysis.py) — local N-1 screening outside PowerMCP.

## Deliver
- The network handle and study type.
- The main feasibility or cost result.
- Whether the next step is mitigation, AC validation, or a larger optimization.
