import tkinter as tk
from tkinter import messagebox
import sympy as sp

# -------------------
# Solver function
# -------------------
def solve_system(knowns):
    s1, s2, dx, d12, l1, l2, h = sp.symbols("s1 s2 dx d12 l1 l2 h")

    eqs = [
        sp.Eq(dx/h, s1/(h - l1)),
        sp.Eq(dx/h, s2/(h - l2)),
        sp.Eq(d12, l1 - l2)
    ]

    subs = {eval(var): val for var, val in knowns.items()}
    sol_list = sp.solve([eq.subs(subs) for eq in eqs], [s1, s2, dx, d12, l1, l2, h], dict=True)

    if not sol_list:
        return None
    
    for sol in sol_list:
        sol_eval = {str(k): float(v.evalf()) for k, v in sol.items() if k != h}
        if all(val > 0 for val in sol_eval.values()):
            return sol_eval

    return None

# -------------------
# GUI Functions
# -------------------
def calculate(event=None):  # event=None allows Enter binding
    try:
        knowns = {}
        blanks = []
        for var in variables:
            val = entries[var].get().strip()
            if val:
                knowns[var] = float(val)
            else:
                blanks.append(var)

        result = solve_system(knowns)

        if not result:
            raise ValueError("Solver failed")

        shown = [f"{labels[var]} = {result[var]:.2f} mm" for var in blanks if var in result]
        if shown:
            output_text.set("\n".join(shown))
        else:
            raise ValueError("Nothing to show")
    except Exception:
        messagebox.showerror("Error", "Something went wrong. Please try again")

def clear_all():
    for e in entries.values():
        e.delete(0, tk.END)
    output_text.set("")

# -------------------
# Variables + Labels
# -------------------
variables = ["s1", "s2", "dx", "d12", "l1", "l2"]
labels = {
    "s1": "s₁",
    "s2": "s₂",
    "dx": "Δx",
    "d12": "d₁₂",
    "l1": "l₁",
    "l2": "l₂"
}

# -------------------
# Build GUI
# -------------------
root = tk.Tk()
root.title("Skimmers (in mm)")

# Window size and centering
window_width = 360
window_height = 420
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_pos = int((screen_width - window_width) / 2)
y_pos = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
root.resizable(False, False)

# Container frame
main_frame = tk.Frame(root)
main_frame.pack(expand=True)

# Input fields (Calibri for nicer subscripts)
entries = {}
for i, var in enumerate(variables):
    tk.Label(
        main_frame, text=f"{labels[var]}:", anchor="e", width=8,
        font=("Calibri", 14)
    ).grid(row=i, column=0, padx=10, pady=6)
    e = tk.Entry(main_frame, justify="center", width=12, font=("Calibri", 14))
    e.grid(row=i, column=1, padx=10, pady=6)
    entries[var] = e

# Buttons row
button_frame = tk.Frame(main_frame)
button_frame.grid(row=len(variables), column=0, columnspan=2, pady=15)

tk.Button(button_frame, text="Calculate", width=12, command=calculate, font=("Calibri", 13)).pack(side="left", padx=8)
tk.Button(button_frame, text="Clear", width=12, command=clear_all, font=("Calibri", 13)).pack(side="left", padx=8)

# Output label
output_text = tk.StringVar()
tk.Label(
    main_frame, textvariable=output_text, justify="center",
    fg="blue", font=("Calibri", 14, "bold")
).grid(row=len(variables)+1, column=0, columnspan=2, pady=10)

# Bind Enter key to calculate
root.bind("<Return>", calculate)

root.mainloop()

