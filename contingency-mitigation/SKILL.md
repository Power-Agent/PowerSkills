---
name: contingency-mitigation
description: "Senior power-engineer playbook for contingency violations. Use when N-1 or N-2 security analysis reveals voltage or thermal problems, transmission constraints, branch overloads, or power-flow violations, and the agent needs to move from ranking contingencies to identifying preventive or corrective actions such as generator redispatch, capacitor bank switching, topology changes, load curtailment, or remedial action schemes."
---

# Contingency mitigation

Start with a solved base case and a ranked list of critical contingencies.

## Preferred action order
1. **Verify** the contingency definitions, monitored elements, and limits.
2. **Group** critical contingencies by common corridor, interface, or weak area.
3. **Apply preventive actions** first: generator redispatch, shunt/capacitor switching, tap changes, or topology changes that help multiple contingencies.
4. **Evaluate corrective actions** next: post-contingency switching, redispatch, or RAS schemes with explicit triggers.
5. **Re-run** the full monitored set after any candidate fix. If violations remain, return to step 3 with updated rankings.
6. Use load shedding only as a last-resort action and state that clearly.
7. For recurring problems, recommend reinforcement or a revised operating guide.

**Example:** N-1 loss of Line X–Y causes thermal overload on Line A–B (108 % rating) and voltage dip at Bus C (0.91 pu). Grouping reveals both violations share the same east-west corridor. Redispatching 60 MW from G1 to G4 clears the thermal violation; switching in the 50 Mvar capacitor bank at Bus C restores voltage to 0.97 pu. Re-running all monitored contingencies confirms no new violations.

## Working rules
- Do not trust contingency results from a bad base case.
- Prefer actions that improve a family of contingencies rather than a single outage.
- Re-run the full monitored set after any candidate fix.

## Deliver
- The critical contingencies and the shared weak pattern.
- The best preventive action.
- Any corrective action that is still required after prevention.
