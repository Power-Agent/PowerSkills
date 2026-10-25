# Pandapower Examples

> 10 worked examples organized from basic to advanced.
> Each example is self-contained and can be run independently.

---

## Network Inspection

### Example 1: Load and Inspect a Test Network

```python
import pandapower as pp
import pandapower.networks as pn

net = pn.case14()

# Network overview
print(f"Number of buses:      {len(net.bus)}")
print(f"Number of lines:      {len(net.line)}")
print(f"Number of generators: {len(net.gen)}")
print(f"Number of loads:      {len(net.load)}")

# View element data
print("\n=== Bus Data ===")
print(net.bus[['name', 'vn_kv']])

print("\n=== Load Data ===")
print(net.load[['bus', 'p_mw', 'q_mvar']])
```

### Example 2: Save and Reload a Network

```python
import pandapower as pp
import pandapower.networks as pn

net = pn.case14()

# Modify the network
pp.create_load(net, bus=5, p_mw=10, q_mvar=5, name="New Load")

# Save
pp.to_json(net, "modified_case14.json")
print("Saved to modified_case14.json")

# Reload and verify
loaded_net = pp.from_json("modified_case14.json")
print(f"Loaded: {len(loaded_net.bus)} buses, {len(loaded_net.load)} loads")
```

---

## Power Flow Analysis

### Example 3: Run Power Flow and Read Results

```python
import pandapower as pp
import pandapower.networks as pn

net = pn.case14()
pp.runpp(net)

print(f"Converged: {net.converged}")

print("\n=== Bus Voltages ===")
print(net.res_bus[['vm_pu', 'va_degree']])

print("\n=== Line Loading ===")
print(net.res_line[['loading_percent', 'p_from_mw', 'pl_mw']])
```

### Example 4: Identify Voltage Violations

```python
import pandapower as pp
import pandapower.networks as pn

net = pn.case_ieee30()
pp.runpp(net)

V_MIN, V_MAX = 0.95, 1.05

undervoltage = net.res_bus[net.res_bus.vm_pu < V_MIN]
overvoltage  = net.res_bus[net.res_bus.vm_pu > V_MAX]

print(f"=== Undervoltage Buses (V < {V_MIN} p.u.) ===")
if len(undervoltage) > 0:
    for idx in undervoltage.index:
        print(f"  Bus {idx} ({net.bus.at[idx, 'name']}): {undervoltage.at[idx, 'vm_pu']:.4f} p.u.")
else:
    print("  None")

print(f"\n=== Overvoltage Buses (V > {V_MAX} p.u.) ===")
if len(overvoltage) > 0:
    for idx in overvoltage.index:
        print(f"  Bus {idx} ({net.bus.at[idx, 'name']}): {overvoltage.at[idx, 'vm_pu']:.4f} p.u.")
else:
    print("  None")

print(f"\nVoltage range: {net.res_bus.vm_pu.min():.4f} -- {net.res_bus.vm_pu.max():.4f} p.u.")
```

### Example 5: Identify Overloaded Equipment

```python
import pandapower as pp
import pandapower.networks as pn

net = pn.case39()
pp.runpp(net)

LOADING_LIMIT = 80.0

overloaded_lines  = net.res_line[net.res_line.loading_percent > LOADING_LIMIT]
overloaded_trafos = net.res_trafo[net.res_trafo.loading_percent > LOADING_LIMIT]

print(f"=== Overloaded Lines (> {LOADING_LIMIT}%) ===")
for idx in overloaded_lines.index:
    from_bus = net.line.at[idx, 'from_bus']
    to_bus   = net.line.at[idx, 'to_bus']
    loading  = overloaded_lines.at[idx, 'loading_percent']
    print(f"  Line {idx} ({from_bus} -> {to_bus}): {loading:.1f}%")

print(f"\n=== Overloaded Transformers (> {LOADING_LIMIT}%) ===")
for idx in overloaded_trafos.index:
    hv_bus  = net.trafo.at[idx, 'hv_bus']
    lv_bus  = net.trafo.at[idx, 'lv_bus']
    loading = overloaded_trafos.at[idx, 'loading_percent']
    print(f"  Trafo {idx} ({hv_bus} -> {lv_bus}): {loading:.1f}%")
```

### Example 6: Calculate System Losses

```python
import pandapower as pp
import pandapower.networks as pn

net = pn.case_ieee30()
pp.runpp(net)

# Line losses
line_losses_mw   = net.res_line.pl_mw.sum()
line_losses_mvar = net.res_line.ql_mvar.sum()

# Transformer losses
trafo_losses_mw   = net.res_trafo.pl_mw.sum() if len(net.trafo) > 0 else 0
trafo_losses_mvar = net.res_trafo.ql_mvar.sum() if len(net.trafo) > 0 else 0

total_losses_mw    = line_losses_mw + trafo_losses_mw
total_generation   = net.res_gen.p_mw.sum() + net.res_ext_grid.p_mw.sum()
loss_percentage    = (total_losses_mw / total_generation) * 100

print("=== System Losses ===")
print(f"  Line losses:       {line_losses_mw:.2f} MW,  {line_losses_mvar:.2f} Mvar")
print(f"  Trafo losses:      {trafo_losses_mw:.2f} MW, {trafo_losses_mvar:.2f} Mvar")
print(f"  Total losses:      {total_losses_mw:.2f} MW")
print(f"  Loss percentage:   {loss_percentage:.2f}%")
print(f"  Total generation:  {total_generation:.2f} MW")
```

---

## Network Creation

### Example 7: Build a 3-Bus System from Scratch

```python
import pandapower as pp

net = pp.create_empty_network(name="Simple 3-Bus System", f_hz=60.0)

# Create buses
bus1 = pp.create_bus(net, vn_kv=110, name="Slack Bus")
bus2 = pp.create_bus(net, vn_kv=110, name="Gen Bus")
bus3 = pp.create_bus(net, vn_kv=110, name="Load Bus")

# Add grid connection (slack), generator, and load
pp.create_ext_grid(net, bus=bus1, vm_pu=1.02, va_degree=0, name="Grid")
pp.create_gen(net, bus=bus2, p_mw=40, vm_pu=1.01, name="Generator 1")
pp.create_load(net, bus=bus3, p_mw=50, q_mvar=20, name="Load 1")

# Connect buses with lines
pp.create_line_from_parameters(net, from_bus=bus1, to_bus=bus2, length_km=50,
                                r_ohm_per_km=0.1, x_ohm_per_km=0.4,
                                c_nf_per_km=10, max_i_ka=0.5, name="Line 1-2")
pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=30,
                                r_ohm_per_km=0.1, x_ohm_per_km=0.4,
                                c_nf_per_km=10, max_i_ka=0.5, name="Line 2-3")
pp.create_line_from_parameters(net, from_bus=bus1, to_bus=bus3, length_km=40,
                                r_ohm_per_km=0.1, x_ohm_per_km=0.4,
                                c_nf_per_km=10, max_i_ka=0.5, name="Line 1-3")

# Solve and display results
pp.runpp(net)
print(f"Converged: {net.converged}")
print("\nBus Voltages:")
print(net.res_bus[['vm_pu', 'va_degree']])
print("\nLine Results:")
print(net.res_line[['p_from_mw', 'loading_percent', 'pl_mw']])
```

---

## Contingency Analysis

### Example 8: N-1 Contingency Analysis

```python
import copy
import pandapower as pp
import pandapower.networks as pn

V_MIN, V_MAX = 0.95, 1.05
LOADING_LIMIT = 100.0


def analyze_line_outages(net, run_power_flow=pp.runpp):
    """Run one N-1 case per line and account for every outcome."""
    results = []

    for line_idx in net.line.index:
        test_net = copy.deepcopy(net)
        test_net.line.at[line_idx, "in_service"] = False

        try:
            run_power_flow(test_net)
        except Exception as exc:
            results.append({
                "contingency": f"Line {line_idx}",
                "status": "failed",
                "error": str(exc),
                "voltage_violations": [],
                "line_overloads": [],
                "trafo_overloads": [],
            })
            continue

        if not test_net.converged:
            results.append({
                "contingency": f"Line {line_idx}",
                "status": "diverged",
                "voltage_violations": [],
                "line_overloads": [],
                "trafo_overloads": [],
            })
            continue

        voltage_violations = test_net.res_bus[
            (test_net.res_bus.vm_pu < V_MIN) | (test_net.res_bus.vm_pu > V_MAX)
        ].index.tolist()
        line_overloads = (
            test_net.res_line[test_net.res_line.loading_percent > LOADING_LIMIT]
            .index.tolist()
            if not test_net.res_line.empty else []
        )
        trafo_overloads = (
            test_net.res_trafo[test_net.res_trafo.loading_percent > LOADING_LIMIT]
            .index.tolist()
            if not test_net.res_trafo.empty else []
        )

        results.append({
            "contingency": f"Line {line_idx}",
            "status": "converged",
            "voltage_violations": voltage_violations,
            "line_overloads": line_overloads,
            "trafo_overloads": trafo_overloads,
        })

    return results


net = pn.case14()
pp.runpp(net)

if not net.converged:
    raise RuntimeError("Base-case power flow did not converge; stop before N-1 analysis.")

results = analyze_line_outages(net)

tested = len(results)
converged = sum(r["status"] == "converged" for r in results)
failed = sum(r["status"] == "failed" for r in results)
diverged = sum(r["status"] == "diverged" for r in results)
critical = sum(
    1 for r in results
    if (
        r["status"] != "converged"
        or r["voltage_violations"]
        or r["line_overloads"]
        or r["trafo_overloads"]
    )
)

print("=== N-1 Contingency Results ===")
print(f"Total analyzed: {tested}")
print(f"Converged:      {converged}")
print(f"Failed:         {failed}")
print(f"Diverged:       {diverged}")
print(f"Critical:       {critical}")

for r in results:
    if (
        r["status"] != "converged"
        or r["voltage_violations"]
        or r["line_overloads"]
        or r["trafo_overloads"]
    ):
        print(f"\n{r['contingency']}: {r['status']}")
        if r.get("error"):
            print(f"  Error: {r['error']}")
        if r["voltage_violations"]:
            print(f"  Voltage violations: {r['voltage_violations']}")
        if r["line_overloads"]:
            print(f"  Overloaded lines:   {r['line_overloads']}")
        if r["trafo_overloads"]:
            print(f"  Overloaded trafos:  {r['trafo_overloads']}")
```

The important distinction is that **failed/diverged contingencies are not treated as secure cases**. A complete sweep should account for every requested outage and report execution status separately from electrical violations.

---

## Advanced Studies

### Example 9: Load Scaling Study

```python
import pandapower as pp
import pandapower.networks as pn

net = pn.case9()

scaling_factors = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
original_p = net.load.p_mw.copy()
original_q = net.load.q_mvar.copy()

print(f"{'Scale':<8} {'Converged':<12} {'Min V (pu)':<14} {'Max Load (%)':<16} {'Losses (MW)'}")
print("-" * 65)

for scale in scaling_factors:
    net.load.p_mw   = original_p * scale
    net.load.q_mvar = original_q * scale
    pp.runpp(net)

    if net.converged:
        print(f"{scale:<8.2f} {'Yes':<12} {net.res_bus.vm_pu.min():<14.4f} "
              f"{net.res_line.loading_percent.max():<16.1f} {net.res_line.pl_mw.sum():.2f}")
    else:
        print(f"{scale:<8.2f} {'No':<12} {'--':<14} {'--':<16} {'--'}")

# Restore original loads
net.load.p_mw   = original_p
net.load.q_mvar = original_q
```

### Example 10: Topology and Transformer Tap Adjustment

```python
import pandapower as pp
import pandapower.networks as pn
import pandapower.topology as top

net = pn.case_ieee30()

# --- Topology check ---
print("=== Topology ===")
print(f"Connected components: {len(top.connected_components(net))}")
print(f"Unsupplied buses:    {top.unsupplied_buses(net)}")

# --- Tap adjustment study ---
target_trafo = 0
target_bus   = net.trafo.at[target_trafo, 'lv_bus']
tap_min      = net.trafo.at[target_trafo, 'tap_min']
tap_max      = net.trafo.at[target_trafo, 'tap_max']

print(f"\n=== Transformer {target_trafo} Tap Study ===")
print(f"Tap range: {tap_min} to {tap_max}")
print(f"{'Tap':<8} {'Bus {0} Voltage (pu)'.format(target_bus)}")
print("-" * 30)

best = None
for tap in range(tap_min, tap_max + 1):
    net.trafo.at[target_trafo, 'tap_pos'] = tap
    pp.runpp(net)
    if net.converged:
        v = net.res_bus.at[target_bus, 'vm_pu']
        print(f"{tap:<8} {v:.4f}")
        if best is None or abs(v - 1.0) < abs(best[1] - 1.0):
            best = (tap, v)

if best:
    print(f"\nBest tap for V = 1.0 pu: tap {best[0]} (V = {best[1]:.4f} pu)")
```
