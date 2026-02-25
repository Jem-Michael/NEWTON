import customtkinter as ctk # type: ignore
import math
from tkinter import messagebox

# -------------------------------
# CONFIGURE APPEARANCE
# -------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -------------------------------
# PREDEFINED FUNCTIONS
# -------------------------------
FUNCTIONS = {
    "Polynomial: x³ - x - 2": {
        "func": lambda x: x**3 - x - 2,
        "dfunc": lambda x: 3*x**2 - 1
    },
    "Trigonometric: cos(x) - x": {
        "func": lambda x: math.cos(x) - x,
        "dfunc": lambda x: -math.sin(x) - 1
    },
    "Exponential: e^x - 3x": {
        "func": lambda x: math.exp(x) - 3*x,
        "dfunc": lambda x: math.exp(x) - 3
    },
    "Logarithmic: ln(x) + x² - 3": {
        "func": lambda x: math.log(x) + x**2 - 3,
        "dfunc": lambda x: 1/x + 2*x
    }
}

running = False
current_iteration = 0
steps_data = []
root_value = None

# -------------------------------
# APP WINDOW
# -------------------------------
app = ctk.CTk()
app.title("Newton-Raphson Root Finder")
app.geometry("950x720")

# -------------------------------
# HEADER
# -------------------------------
header = ctk.CTkLabel(
    app,
    text="Newton–Raphson Numerical Solver",
    font=("Segoe UI", 24, "bold")
)
header.pack(pady=20)

# -------------------------------
# INPUT FRAME
# -------------------------------
input_frame = ctk.CTkFrame(app, corner_radius=15)
input_frame.pack(fill="x", padx=30, pady=10)

function_menu = ctk.CTkOptionMenu(input_frame, values=list(FUNCTIONS.keys()))
function_menu.grid(row=0, column=1, padx=10, pady=10)
function_menu.set(list(FUNCTIONS.keys())[0])

ctk.CTkLabel(input_frame, text="Select Function:").grid(row=0, column=0, sticky="w", padx=10)
ctk.CTkLabel(input_frame, text="Initial Guess (x₀):").grid(row=1, column=0, sticky="w", padx=10)
ctk.CTkLabel(input_frame, text="Tolerance:").grid(row=2, column=0, sticky="w", padx=10)
ctk.CTkLabel(input_frame, text="Max Iterations:").grid(row=3, column=0, sticky="w", padx=10)

initial_guess = ctk.CTkEntry(input_frame)
initial_guess.insert(0, "1")
initial_guess.grid(row=1, column=1, padx=10)

tolerance = ctk.CTkEntry(input_frame)
tolerance.insert(0, "0.0001")
tolerance.grid(row=2, column=1, padx=10)

max_iterations = ctk.CTkEntry(input_frame)
max_iterations.insert(0, "20")
max_iterations.grid(row=3, column=1, padx=10)

# -------------------------------
# STATUS FRAME
# -------------------------------
status_frame = ctk.CTkFrame(app, corner_radius=15)
status_frame.pack(fill="x", padx=30, pady=10)

processing_label = ctk.CTkLabel(status_frame, text="", text_color="orange")
processing_label.pack(pady=5)

iteration_label = ctk.CTkLabel(status_frame, text="Iteration: 0")
iteration_label.pack()

progress = ctk.CTkProgressBar(status_frame, width=600)
progress.set(0)
progress.pack(pady=10)

# -------------------------------
# SOLUTION TRAIL
# -------------------------------
solution_frame = ctk.CTkFrame(app, corner_radius=15)
solution_frame.pack(fill="both", expand=True, padx=30, pady=10)

solution_box = ctk.CTkTextbox(solution_frame, font=("Consolas", 11))
solution_box.pack(fill="both", expand=True, padx=10, pady=10)

# -------------------------------
# FINAL ANSWER
# -------------------------------
final_frame = ctk.CTkFrame(app, corner_radius=15)
final_frame.pack(fill="x", padx=30, pady=10)

ctk.CTkLabel(final_frame, text="Final Root:", font=("Segoe UI", 14)).pack(side="left", padx=10)
result_box = ctk.CTkEntry(final_frame, width=200)
result_box.pack(side="left")

# -------------------------------
# BUTTONS
# -------------------------------
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=15)

# -------------------------------
# FUNCTIONS
# -------------------------------
def clear_all():
    global running
    running = False
    solution_box.delete("1.0", "end")
    result_box.delete(0, "end")
    iteration_label.configure(text="Iteration: 0")
    processing_label.configure(text="")
    progress.set(0)

def stop_process():
    global running
    running = False
    processing_label.configure(text="Process Stopped")

def type_writer(text, index=0):
    if not running:
        return
    if index < len(text):
        solution_box.insert("end", text[index])
        solution_box.see("end")
        app.after(5, lambda: type_writer(text, index + 1))

def animate_processing(count=0):
    if running:
        dots = "." * (count % 4)
        processing_label.configure(text=f"Processing{dots}")
        app.after(400, lambda: animate_processing(count + 1))

def newton_step():
    global current_iteration, running, root_value

    if not running:
        return

    if current_iteration < len(steps_data):
        iteration_label.configure(text=f"Iteration: {current_iteration + 1}")
        progress.set((current_iteration + 1) / len(steps_data))
        type_writer(steps_data[current_iteration])
        current_iteration += 1
        app.after(500, newton_step)
    else:
        running = False
        processing_label.configure(text="Converged Successfully")
        result_box.insert(0, f"{root_value:.8f}")

def compute():
    global running, current_iteration, steps_data, root_value

    try:
        solution_box.delete("1.0", "end")
        result_box.delete(0, "end")

        selected = function_menu.get()
        data = FUNCTIONS[selected]

        x = float(initial_guess.get())
        tol = float(tolerance.get())
        max_iter = int(max_iterations.get())

        f = data["func"]
        df = data["dfunc"]

        steps_data = []
        current_iteration = 0
        running = True

        for i in range(max_iter):
            fx = f(x)
            dfx = df(x)

            if dfx == 0:
                raise ValueError("Derivative became zero.")

            x_new = x - fx / dfx

            step_text = (
                f"\nIteration {i+1}\n"
                f"x = {x:.6f}\n"
                f"f(x) = {fx:.6f}\n"
                f"f'(x) = {dfx:.6f}\n"
                f"x_new = {x_new:.6f}\n"
                f"|Δx| = {abs(x_new - x):.6f}\n"
                "-----------------------------------\n"
            )

            steps_data.append(step_text)

            if abs(x_new - x) < tol:
                root_value = x_new
                break

            x = x_new
        else:
            root_value = x

        animate_processing()
        newton_step()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        running = False

ctk.CTkButton(button_frame, text="Compute", command=compute, width=120).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="Clear", command=clear_all, width=120).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="Stop", command=stop_process, width=120).pack(side="left", padx=10)

# -------------------------------
# RUN APP
# -------------------------------
app.mainloop()