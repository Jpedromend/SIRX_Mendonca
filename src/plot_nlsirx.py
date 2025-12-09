import pandas as pd
import matplotlib.pyplot as plt

#### Parameters
TOTAL = 50.0e6
A = 7.0e-2
K = 0.1
K0 = 0.01
N = 0.2
M = 0.0
bN = 0.35 / TOTAL

# Read file
filename = f"sirx_solution_bt{bN},gmm{A},kpp{K},kpp0{K0},n{N},m{M}.dat"

print(f"Attempting to read: {filename}")
try:
    df = pd.read_csv(filename, delim_whitespace=True)

    # Plot
    plt.figure(figsize=(6, 4), dpi=100)
    
    plt.plot(df['t'], df['I'], color='k', linewidth=2)
    # plt.semilogy(df['t'], df['I'], color='k', linewidth=2)
    
    plt.title("SIRX Model Simulation", fontsize=14)
    plt.xlabel('Time (days)', fontsize=12)
    plt.ylabel('Active Cases', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6, which='both')
    plt.tight_layout()
    
    plt.show()

except FileNotFoundError:
    print("\nError: File not found.")
