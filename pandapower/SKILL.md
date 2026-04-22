---
name: pandapower
description: Progressive-disclosure workflow for pandapower studies. Use when the user asks to load or build a pandapower network, inspect network data, run AC power flow, or perform contingency screening, and when the agent should expose base-case power flow before advanced outage studies.
---

# pandapower workflow

Start with the network model and a clean base-case solve. Use contingency analysis only after the steady-state case is credible.

## Default tool ladder
1. `load_network(file_path)` or `create_empty_network()` — load or create the network model.
2. `get_network_info()` — inspect buses, lines, transformers, generators, loads, and switches.
3. `run_power_flow(net)` — establish the base operating point. Check `net.res_bus.vm_pu` for voltage and `net.res_line.loading_percent` for thermal limits.
4. `run_contingency_analysis(...)` — only after the base case solves and the monitoring limits are clear.

## Working rules
- Do not run contingencies before checking the base-case voltages and loading.
- Use pandapower for AC feasibility and fast screening, then escalate only when the question requires more.
- Use [voltage-violation-mitigation](../voltage-violation-mitigation/SKILL.md), [thermal-overload-mitigation](../thermal-overload-mitigation/SKILL.md), or [contingency-mitigation](../contingency-mitigation/SKILL.md) after violations are identified.

## Local assets in this repo
- `pandapower/case39.json` for a ready test network.
- `pandapower/scripts/network_analysis.py` for structured base-case review.
- `pandapower/scripts/contingency_analysis.py` for local N-1 screening.

## Deliver
- The network loaded and whether the base case converged.
- The key voltage or loading findings.
- Whether contingency or mitigation work is now justified.
