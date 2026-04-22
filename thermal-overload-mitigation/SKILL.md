---
name: thermal-overload-mitigation
description: "Senior power-engineer playbook for thermal overloads on lines and transformers. Use when power-flow or contingency studies show branch loading above MVA ratings, N-1 violations, line rating exceedances, or congestion, and the agent needs an operationally credible sequence of generation redispatch, bus-splitting, phase-shifter adjustment, conductor upsizing, or load curtailment."
---

# Thermal overload mitigation

Start with the monitored element, the applicable rating, and the driving condition.

## Preferred action order
1. **Confirm** the overload is real: correct rating set, correct outage state, and solved base case or contingency.
2. **Redispatch** generation or transfer patterns to unload the corridor.
3. **Reconfigure** topology or switching where operations permit (bus-splitting, line switching).
4. **Adjust controls** — phase shifters, HVDC schedules, or transformer taps — only when sensitivity evidence supports them.
5. **Reinforce** if the issue is persistent: reconductoring, uprating, or new facilities.
6. After each action, re-solve and verify the overload is relieved. If not, proceed to the next step.

**Example:** Line A–B loaded at 105 % of normal rating after N-1 loss of Line C–D. PTDF shows Generator G3 has −0.18 sensitivity. Redispatching 40 MW from G3 to G5 reduces loading to 94 % — verified by re-solving all monitored contingencies.

## Working rules
- Separate normal-rating issues from emergency-rating issues.
- Fix the smallest set of elements that relieve the monitored overload cluster.
- Validate a candidate fix on all critical monitored contingencies, not just the worst case.
- Use PTDF or LODF style sensitivities when the software provides them.

## Deliver
- The overloaded elements and rating basis.
- The dispatch or topology changes that help most.
- The recommended corrective action and the residual risk.
