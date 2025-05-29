import matplotlib.pyplot as plt

def plot_sin_series(x_vals, approx_vals, true_vals, save_path="Task3/sin_plot.png"):
    """
    Plots the approximated and real sin functions.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, approx_vals, 'r--', label='Taylor Approximation')
    plt.plot(x_vals, true_vals, 'b-', label='math.sin(x)')

    plt.title("Sin Approximation by Taylor Series", fontsize=14)
    plt.xlabel("x (radians)", fontsize=12)
    plt.ylabel("sin(x)", fontsize=12)
    plt.legend()
    plt.grid(True)

    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    plt.savefig(save_path)
    print(f"Plot saved to: {save_path}")
    plt.show()
