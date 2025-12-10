# Effect of Containment Efforts on Epidemic Processes: Nonlinear SIR-X

This repository contains code to simulate and visualize the **nonlinear SIR-X epidemic model** introduced in

> **“Effect of containment efforts on epidemic processes: emergent cooperative phenomena”**

The model extends the standard SIR framework by including:
- A new compartment $X$ modeling isolated infected population,
- Two nonlinear (cooperative) containment rates that depend on the current number of infected individuals.

The codes:
- Integrate the nonlinear SIR-X equations,
- Plot epidemic curves (e.g. active cases),
- Process real COVID-19 data (Johns Hopkins University dataset) for comparison with the model,
- Fits real data by estimating the best NL-SIRX parameters via MSE.

---

## 1. Model Overview

We consider four populations:
- $S(t)$: susceptible  
- $I(t)$: infected (active cases)  
- $R(t)$: removed (recovered/dead or otherwise no longer infectious)  
- $X(t)$: isolated (quarantined / contained) individuals

Parameters:
- $\beta/N$ (`rr`): effective infection rate
- $\gamma$ (`a`): removal rate  
- $\kappa$ (`k`): rate of specific (quarantine) social distancing acting on infectious individuals  
- $\kappa_0$ (`k0`): rate of general (confinement) social distancing acting on the mixing population (susceptible and infectious)
- $n, m$: exponents controlling **cooperative response** of containment to the number of infecteds

The nonlinear SIR-X ODEs used in the code are:

$$
\begin{aligned}
\frac{dS}{dt} &= - \frac{\beta S I}{N} - \kappa_0 I^m S, \\
\frac{dI}{dt} &= \frac{\beta S I}{N} - \gamma I - \kappa_0 I^m I - \kappa I^n I, \\
\frac{dR}{dt} &= \gamma I + \kappa_0 I^m S, \\
\frac{dX}{dt} &= \kappa_0 I^m I + \kappa I^n I.
\end{aligned}
$$

The total population
$S + I + R + X$
is conserved.

---

## 2. Repository Contents

- `nlsirx.py`  
  Contains the function `sirx_nonlinear_ode_solver(...)` that numerically integrates the nonlinear SIR-X equations using SciPy’s `solve_ivp`.

- `plot_nlsirx.py`  
  Loads a `.dat` file produced by the solver and plots the **active cases** $I(t)$ on a semilogarithmic scale.

- `process_jhu_data.py`  
  - Load the JHU global time-series for confirmed, deaths, and recovered cases,
  - Aggregate by country,
  - Compute **Active = Confirmed − Deaths − Recovered**,
  - Save the cleaned data,
  - Plot active cases for checking.

---

## 3. Requirements

- Python 3.x
- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [SciPy](https://scipy.org/)
