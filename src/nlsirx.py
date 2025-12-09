import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def sirx_nonlinear_ode_solver(t_max: float, rr: float, S0: float, I0: float, R0: float, X0: float, 
                              a: float, k: float, k0: float, n: float, m: float, h=1e-3) -> pd.DataFrame:
    """
    Solves the nonlinear SIRX system using SciPy's adaptive ODE solver.
    """

    # Define the system of ODEs
    def derivatives(t, Y):
        S, I, R, X = Y
        I = np.abs(I) # To avoid small numerical errors
        
        # Pre-calculate k0(I) and k(I)
        kI = k*I**n
        k0I = k0*I**m

        # SIRX Equations
        dSdt = -rr * S * I - k0I * S
        dIdt = rr * S * I - a * I - k0I * I - kI * I
        dRdt = a * I + k0I * S
        dXdt = k0I * I + kI * I
        
        return [dSdt, dIdt, dRdt, dXdt]

    # Setup Solver
    Y0 = [S0, I0, R0, X0]
    t_span = [0.0, t_max]
    t_eval = np.arange(0.0, t_max + h, h)
    
    # Solve (RK45 is the default adaptive Runge-Kutta method)
    solution = solve_ivp(derivatives, t_span, Y0, t_eval=t_eval, method='RK45')

    # Process Results
    if not solution.success:
        print(f"Warning: ODE solver failed. Status: {solution.message}")

    df = pd.DataFrame({
        't': solution.t,
        'S': solution.y[0],
        'I': solution.y[1],
        'R': solution.y[2],
        'X': solution.y[3],
        'Total': np.sum(solution.y, axis=0)
    })
        
    return df

# Parameters
TOTAL = 50.0e6      # total population
T_MAX = 140.0       # timeframe
A = 7.0e-2          # gamma
K = 0.1             # kappa
K0 = 0.140          # kappa0
N = 0.2             # n
M = 0.0             # m
bN = 0.35 / TOTAL   # beta/N

# Initial Conditions
I0 = 1.0
R0 = 0.0
S0 = TOTAL - I0
X0 = 0.0

print("Running SIRX simulation...")
data = sirx_nonlinear_ode_solver(
    t_max=T_MAX, rr=bN, S0=S0, I0=I0, R0=R0, 
    X0=X0, a=A, k=K, k0=K0, n=N, m=M
)

filename = f"sirx_solution_bt{bN},gmm{A},kpp{K},kpp0{K0},n{N},m{M}.dat"
print("Saving to file...")
with open(filename, 'w') as f:
    f.write(data.to_string(index=False, header=True, float_format='%.10e'))
