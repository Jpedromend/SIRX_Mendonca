# Effect of Containment Efforts on Epidemic Processes: Nonlinear SIR-X

This repository contains code to simulate and visualize the **nonlinear SIR-X epidemic model** introduced in

> **“Effect of containment efforts on epidemic processes: emergent cooperative phenomena”**

The model extends the standard SIR framework by including:
- A **quarantined** compartment \(X\),
- **Containment terms** that can act on both susceptibles and infecteds,
- **Nonlinear (cooperative) containment rates** that depend on the current number of infected individuals.

The code lets you:
- Integrate the nonlinear SIR-X equations,
- Plot epidemic curves (e.g. active cases),
- Process real COVID-19 data (Johns Hopkins University dataset) for comparison with the model.

---

## 1. Model Overview

We consider four populations:
- \(S(t)\): susceptible  
- \(I(t)\): infected (active cases)  
- \(R(t)\): removed (recovered/dead or otherwise no longer infectious)  
- \(X(t)\): quarantined / contained individuals  

Parameters:
- \(\beta\) (`rr`): infection rate (often written as \(\beta/N\) in the code)  
- \(\gamma\) (`a`): recovery/removal rate  
- \(\kappa\) (`k`): nonlinear containment rate acting on infecteds  
- \(\kappa_0\) (`k0`): nonlinear containment rate acting on susceptibles and infecteds  
- \(n, m\): exponents controlling **cooperative response** of containment to the number of infecteds

The nonlinear SIR-X ODEs used in the code are:

\[
\begin{aligned}
\frac{dS}{dt} &= - \beta S I - \kappa_0 I^m S, \\
\frac{dI}{dt} &= \beta S I - \gamma I - \kappa_0 I^m I - \kappa I^n I, \\
\frac{dR}{dt} &= \gamma I + \kappa_0 I^m S, \\
\frac{dX}{dt} &= \kappa_0 I^m I + \kappa I^n I.
\end{aligned}
\]

The total population \(S + I + R + X\) is conserved (up to numerical errors).

---

## 2. Repository Contents

A typical layout for this project is:

- `sirx_nonlinear.py`  
  Contains the function `sirx_nonlinear_ode_solver(...)` that numerically integrates the nonlinear SIR-X equations using SciPy’s `solve_ivp`.

- `plot_sirx.py`  
  Loads a `.dat` file produced by the solver and plots the **active cases** \(I(t)\) on a semilogarithmic scale.

- `process_jhu_data.py`  
  Utilities to:
  - Load the JHU global time-series for confirmed, deaths, and recovered cases,
  - Aggregate by country,
  - Compute **Active = Confirmed − Deaths − Recovered**,
  - Save the cleaned data and produce a sanity-check plot.

- `data_*.csv`  
  Output of `process_jhu_data.py` with processed country-level data.

- `sirx_solution_*.dat`  
  Output of `sirx_nonlinear_ode_solver(...)` containing the simulated SIR-X trajectories.

Feel free to rename the scripts as you prefer; the README assumes the logical roles above.

---

## 3. Requirements

- Python 3.x
- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [SciPy](https://scipy.org/)
