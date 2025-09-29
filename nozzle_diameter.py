import tkinter as tk
from tkinter import messagebox
from math import sqrt, pi
import math

# ---- Secure safe_eval setup ----
safe_dict = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
safe_dict.update({'__builtins__': {}})

def safe_eval(expr):
    return eval(expr, safe_dict)

# ---- f(k) function ----
def f_k(k):
    return sqrt(k) / (((k + 1) / 2) ** ((k + 1) / (2*k - 2)))

# -------------------
# Calculate function
# -------------------
def calculate_d0(event=None):  # event=None allows Enter binding
    try:
        k = safe_eval(entries['k'].get())
        R_s = safe_eval(entries['R_s'].get())
        T_0 = safe_eval(entries['T_0'].get())
        T = safe_eval(entries['T'].get())
        c = safe_eval(entries['c'].get())
        delta_p = safe_eval(entries['Δp'].get())
        p_0 = safe_eval(entries['p_0'].get())
        fk = f_k(k)

        for param in S_parameters:
            s_val = entries[param].get()
            if s_val.strip():
                S = safe_eval(s_val)
                d0 = sqrt((4 / pi) * (1 / fk) * (S / sqrt(R_s)) * (sqrt(T_0) / T) * ((c * delta_p)) / p_0) * 10**3
                result_vars[param].set(f"d₀ = {d0:.6f} μm")
            else:
                result_vars[param].set("")
    except Exception:
        messagebox.showerror("Error", "Something went wrong. Please try again")

def clear_all():
    for e in entries.values():
        e.delete(0, tk.END)
    for var in result_vars.values():
        var.set("")

# -------------------
# GUI setup
# -------------------
root = tk.Tk()
root.title("Nozzle Diameter Calculator")

# Window size and centering
window_width = 420
window_height = 520
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_pos = int((screen_width - window_width) / 2)
y_pos = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
root.resizable(False, False)

# Container frame
main_frame = tk.Frame(root)
main_frame.pack(expand=True)

entries = {}

# Parameters (with subscripts for display)
fixed_parameters = {
    'k': 'k',
    'R_s': 'Rₛ',
    'T_0': 'T₀',
    'T': 'T',
    'c': 'C',
    'Δp': 'Δp (mbar)',
    'p_0': 'p₀ (bar)'
}
S_parameters = {'S1': 'S₁', 'S2': 'S₂', 'S3': 'S₃', 'S4': 'S₄'}

# Default values
default_values = {}

# Input fields for fixed parameters
for i, (param, label) in enumerate(fixed_parameters.items()):
    tk.Label(
        main_frame, text=f"{label}:", anchor="e", width=8,
        font=("Calibri", 14)
    ).grid(row=i, column=0, padx=10, pady=6)
    e = tk.Entry(main_frame, justify="center", width=12, font=("Calibri", 14))
    e.grid(row=i, column=1, padx=10, pady=6)
    if param in default_values:
        e.insert(0, default_values[param])
    entries[param] = e

# Input fields for multiple S values
offset = len(fixed_parameters)
for j, (param, label) in enumerate(S_parameters.items()):
    tk.Label(
        main_frame, text=f"{label}:", anchor="e", width=8,
        font=("Calibri", 14)
    ).grid(row=offset + j, column=0, padx=10, pady=6)
    e = tk.Entry(main_frame, justify="center", width=12, font=("Calibri", 14))
    e.grid(row=offset + j, column=1, padx=10, pady=6)
    entries[param] = e

# Result labels
result_vars = {}
for j, (param, label) in enumerate(S_parameters.items()):
    var = tk.StringVar()
    result_vars[param] = var
    tk.Label(
        main_frame, textvariable=var, justify="center",
        fg="blue", font=("Calibri", 14, "bold")
    ).grid(row=offset + j, column=2, padx=10, pady=6)

# Buttons row
button_frame = tk.Frame(main_frame)
button_frame.grid(row=offset + len(S_parameters), column=0, columnspan=3, pady=15)

tk.Button(button_frame, text="Calculate", width=12, command=calculate_d0, font=("Calibri", 13)).pack(side="left", padx=8)
tk.Button(button_frame, text="Clear", width=12, command=clear_all, font=("Calibri", 13)).pack(side="left", padx=8)

# Bind Enter key
root.bind("<Return>", calculate_d0)

# Start loop
root.mainloop()

