---
name: andes
description: "Sets up and runs ANDES power-flow cases, performs small-signal stability eigenvalue analysis, and executes time-domain transient simulations via PowerMCP. Use when the user asks to run load flow, eigenvalue analysis, transient stability, dynamic simulation, or voltage stability studies through ANDES, and when the agent should validate the base case before advancing to dynamic analysis."
---

# ANDES workflow

Expose ANDES tools in stages. Do not jump into dynamics until the base case is loaded, solved, and understood.

## Default tool ladder
1. `run_power_flow(file_path)` — load the case and solve the steady-state point.
2. `get_system_info()` — summarize buses, generators, dynamic states, and controls.
3. `run_eigenvalue_analysis(file_path)` — screen oscillatory modes and poor damping.
4. `run_time_domain_simulation(step_size, t_end)` — only after the disturbance and success criteria are explicit.

**Example sequence:**
```
run_power_flow("ieee14.xlsx")          → base case solved, 14 buses, 5 generators
get_system_info()                      → lists dynamic models, governor and exciter types
run_eigenvalue_analysis("ieee14.xlsx") → dominant mode 0.42 Hz, damping 3.1 % — flagged
run_time_domain_simulation(0.01, 10.0) → generator trip at t=1 s, monitor rotor angles
```

## Working rules
- Re-run the base power flow after any model or dispatch change before dynamic work.
- State the disturbance, clearing time, monitored channels, and pass or fail criteria before time-domain runs.
- Treat eigenvalue results as screening. Confirm critical cases in time domain.
- Hand off to [dynamic-stability-mitigation](../dynamic-stability-mitigation/SKILL.md) when damping, angle stability, or voltage recovery is unacceptable.

## Deliver
- The case used and whether the base case solved.
- The dynamic issue being checked.
- The main result and whether mitigation is now required.
