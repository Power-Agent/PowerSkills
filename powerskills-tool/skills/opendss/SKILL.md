---
name: opendss
description: Progressive-disclosure workflow for OpenDSS distribution-feeder studies. Use whenever the user wants to compile a DSS model, solve a distribution circuit, inspect feeder bus voltages or power, sweep load multipliers, or run daily / harmonic studies through PowerMCP — even when they just say "solve this feeder", "check the voltages", or "run a daily profile". Exposes a solved base feeder before advanced scenarios. Reach for this instead of answering OpenDSS feeder questions unaided.
---

# OpenDSS workflow

Start with a solved feeder. Do not jump to daily or harmonic studies until the base feeder compiles and the voltage profile is understood.

## Default tool ladder
1. `compile_opendss_file(dss_file)` to compile the DSS model.
2. `solve_snapshot()` to solve the compiled circuit and establish the base operating point.
3. `get_results_summary_records()` and `get_voltage_mag_ln_nodes_records()` to inspect the solve and node voltages.
4. `get_current_loading_percent_records()` and `get_losses_p_records()` to inspect equipment loading and active-power losses.
5. `get_loads_records()` and `edit_element(...)` to inspect or make a targeted model change before solving again.

## Working rules
- Fix compile or solve errors before any scenario analysis.
- For voltage issues, inspect node-voltage records first.
- Do not advertise daily-profile, load-multiplier, or harmonic workflows as available MCP operations unless the connected PowerMCP server exposes those tools.
- Keep feeder, meter, and load names explicit in the response.

## Escalation triggers
Quote the weak bus + voltage or the loaded element rather than saying "there is a problem".

| Observation | Escalate to |
|---|---|
| `get_voltage_mag_ln_nodes_records` shows pu outside the feeder band (e.g. < 0.95 or > 1.05) | `voltage-violation-mitigation` |
| A line, transformer, or regulator loaded above its rating | `thermal-overload-mitigation` |
| `solve_snapshot` fails or diverges after compilation | `convergence-failure-mitigation` |
| The study is DER (PV, storage) integration or hosting capacity on the feeder | `der-hosting-capacity-mitigation` |

## Deliver
- The compiled feeder and base-case status.
- The voltage or power quantities checked.
- Any scenario result and whether mitigation is needed.
