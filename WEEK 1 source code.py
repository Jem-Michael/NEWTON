import customtkinter as ctk # type: ignore

# -------------------------------
# APP CONFIG
# -------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Newton–Raphson Root Finder")
app.geometry("800x600")

# -------------------------------
# HEADER
# ------------------------------
header = ctk.CTkLabel(
    app,
    text="Newton–Raphson Numerical Solver",
    font=("Segoe UI", 20, "bold")
)
header.pack(pady=20)

# -------------------------------
# INPUT SECTION
# -------------------------------
input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=30, pady=10)

ctk.CTkLabel(input_frame, text="Function:").grid(row=0, column=0, padx=10, pady=10)
function_menu = ctk.CTkOptionMenu(
    input_frame,
    values=["x³ - x - 2", "cos(x) - x", "e^x - 3x"]
)
function_menu.grid(row=0, column=1)

ctk.CTkLabel(input_frame, text="Initial Guess (x₀):").grid(row=1, column=0, padx=10)
initial_guess = ctk.CTkEntry(input_frame)
initial_guess.grid(row=1, column=1)

ctk.CTkLabel(input_frame, text="Convergence Tolerance::").grid(row=2, column=0, padx=10)
tolerance = ctk.CTkEntry(input_frame)
tolerance.grid(row=2, column=1)

# -------------------------------
# SOLUTION TRAIL PANEL
# -------------------------------
trail_frame = ctk.CTkFrame(app)
trail_frame.pack(fill="both", expand=True, padx=30, pady=10)

ctk.CTkLabel(trail_frame, text="Solution Trail").pack()

solution_box = ctk.CTkTextbox(trail_frame, height=200)
solution_box.pack(fill="both", expand=True, padx=10, pady=10)

# -------------------------------
# FINAL ANSWER
# -------------------------------
final_frame = ctk.CTkFrame(app)
final_frame.pack(fill="x", padx=30, pady=10)

ctk.CTkLabel(final_frame, text="Final Answer:").pack(side="left", padx=10)
result_box = ctk.CTkEntry(final_frame, width=200)
result_box.pack(side="left")

# -------------------------------
# BUTTON FUNCTIONS
# -------------------------------
def compute():
    solution_box.delete("1.0", "end")
    solution_box.insert("end", "Iteration 1: Placeholder computation...\n")
    solution_box.insert("end", "Iteration 2: Placeholder computation...\n")
    result_box.delete(0, "end")
    result_box.insert(0, "Root ≈ ?")

def clear():
    solution_box.delete("1.0", "end")
    result_box.delete(0, "end")

# -------------------------------
# BUTTONS
# -------------------------------
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=15)

ctk.CTkButton(button_frame, text="Compute", command=compute).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="Clear", command=clear).pack(side="left", padx=10)

app.mainloop()
