import customtkinter as ctk
from tkinter import messagebox, filedialog
import math
from datetime import datetime

# Set appearance mode and color theme
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# Predefined functions and their derivatives for Newton-Raphson
PREDEFINED_FUNCTIONS = {
    "x^2 - 2": (lambda x: x**2 - 2, lambda x: 2*x),
    "cos(x) - x": (lambda x: math.cos(x) - x, lambda x: -math.sin(x) - 1),
    "x^3 - 3x + 1": (lambda x: x**3 - 3*x + 1, lambda x: 3*x**2 - 3),
    # Add more as needed
}

APP_VERSION = "v2.0 (CustomTkinter)"

class SolutionTrail:
    """Manage the step-by-step trail that appears in the UI and export files."""

    def __init__(self, text_widget: ctk.CTkTextbox):
        self.text_widget = text_widget
        self.step_counter = 0
        self.clear()

    def clear(self):
        self.step_counter = 0
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", "end")
        # write placeholder skeleton so UI always looks like a solved example
        self._write(
            "GIVEN:\n  f(x) = placeholder\n\n"
            "METHOD:\n  placeholder\n\n"
            "STEPS:\n  1. placeholder\n  2. placeholder\n  3. placeholder\n\n"
            "FINAL ANSWER:\n  placeholder\n\n"
            "VERIFICATION:\n  placeholder\n\n"
            "SUMMARY:\n  placeholder\n"
        )
        self.text_widget.configure(state="disabled")

    def add_heading(self, heading: str):
        self._write(f"\n{heading}:\n", is_heading=True)

    def add_step(self, content: str):
        self.step_counter += 1
        self._write(f"{self.step_counter}. {content}\n", is_step=True)

    def log(self, content: str):
        # Generic log without numbering
        self._write(f"{content}\n")

    def _write(self, msg: str, is_heading: bool = False, is_step: bool = False):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", msg)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")

    def export(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.text_widget.get("1.0", "end"))


APP_VERSION = "v2.0 (CustomTkinter)"

class NewtonRaphsonApp:
    def __init__(self, root: ctk.CTk):
        self.root = root
        root.title(f"🧮 Newton-Raphson Root Finder {APP_VERSION}")
        root.geometry("1400x750")
        root.minsize(1200, 700)

        self.create_widgets()

    def create_widgets(self):
        """Create all UI widgets using customtkinter."""
        
        # ============ MAIN CONTAINER ============
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # ============ HEADER ============
        header = ctk.CTkFrame(main_container, fg_color=("#2563eb", "#1e40af"), height=80)
        header.pack(fill="x", padx=0, pady=0)
        
        title_label = ctk.CTkLabel(
            header,
            text="🧮 Newton-Raphson Root Finder",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        title_label.pack(pady=20)
        
        # ============ CONTENT AREA ============
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configure grid layout: 2 columns (input panel and trail panel)
        content_frame.columnconfigure(0, weight=0)  # Input column
        content_frame.columnconfigure(1, weight=1)  # Trail column (expandable)
        content_frame.rowconfigure(0, weight=1)
        
        # ============ LEFT PANEL (INPUTS) ============
        left_panel = ctk.CTkFrame(content_frame, fg_color=("white", "#1e293b"))
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        # Input Card
        input_card = ctk.CTkFrame(left_panel, fg_color=("white", "#1e293b"), corner_radius=10)
        input_card.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Input Title
        input_title = ctk.CTkLabel(
            input_card,
            text="Solver Configuration",
            font=("Arial", 14, "bold"),
            text_color=("#1e293b", "#e2e8f0")
        )
        input_title.pack(pady=(15, 10), padx=15)
        
        # Method Selection
        method_label = ctk.CTkLabel(
            input_card,
            text="Method:",
            font=("Arial", 11, "bold"),
            text_color=("#1e293b", "#e2e8f0")
        )
        method_label.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.method_var = ctk.StringVar(value="Newton-Raphson")
        self.method_cb = ctk.CTkComboBox(
            input_card,
            values=["Newton-Raphson", "Secant"],
            variable=self.method_var,
            state="readonly",
            font=("Arial", 10),
            command=self._on_method_change
        )
        self.method_cb.pack(fill="x", padx=15, pady=5)
        
        # Function Selection
        func_label = ctk.CTkLabel(
            input_card,
            text="Function:",
            font=("Arial", 11, "bold"),
            text_color=("#1e293b", "#e2e8f0")
        )
        func_label.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.function_var = ctk.StringVar(value=list(PREDEFINED_FUNCTIONS.keys())[0])
        self.function_cb = ctk.CTkComboBox(
            input_card,
            values=list(PREDEFINED_FUNCTIONS.keys()),
            variable=self.function_var,
            state="readonly",
            font=("Arial", 10)
        )
        self.function_cb.pack(fill="x", padx=15, pady=5)
        
        # Initial Guess
        guess_label = ctk.CTkLabel(
            input_card,
            text="Initial Guess:",
            font=("Arial", 11, "bold"),
            text_color=("#1e293b", "#e2e8f0")
        )
        guess_label.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.guess_var = ctk.StringVar(value="1.5")
        self.guess_entry = ctk.CTkEntry(
            input_card,
            textvariable=self.guess_var,
            font=("Arial", 10),
            placeholder_text="e.g., 1.5"
        )
        self.guess_entry.pack(fill="x", padx=15, pady=5)
        
        # Second Guess (Secant method)
        self.guess2_label = ctk.CTkLabel(
            input_card,
            text="Second Guess:",
            font=("Arial", 11, "bold"),
            text_color=("#1e293b", "#e2e8f0")
        )
        
        self.guess2_var = ctk.StringVar(value="2.0")
        self.guess2_entry = ctk.CTkEntry(
            input_card,
            textvariable=self.guess2_var,
            font=("Arial", 10),
            placeholder_text="e.g., 2.0"
        )
        
        # Tolerance
        tol_label = ctk.CTkLabel(
            input_card,
            text="Tolerance:",
            font=("Arial", 11, "bold"),
            text_color=("#1e293b", "#e2e8f0")
        )
        tol_label.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.tol_var = ctk.StringVar(value="1e-6")
        self.tol_entry = ctk.CTkEntry(
            input_card,
            textvariable=self.tol_var,
            font=("Arial", 10),
            placeholder_text="e.g., 1e-6"
        )
        self.tol_entry.pack(fill="x", padx=15, pady=5)
        
        # Max Iterations
        maxiter_label = ctk.CTkLabel(
            input_card,
            text="Max Iterations:",
            font=("Arial", 11, "bold"),
            text_color=("#1e293b", "#e2e8f0")
        )
        maxiter_label.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.maxiter_var = ctk.StringVar(value="50")
        self.maxiter_entry = ctk.CTkEntry(
            input_card,
            textvariable=self.maxiter_var,
            font=("Arial", 10),
            placeholder_text="e.g., 50"
        )
        self.maxiter_entry.pack(fill="x", padx=15, pady=5)
        
        # ============ BUTTONS ============
        button_frame = ctk.CTkFrame(input_card, fg_color=("white", "#1e293b"))
        button_frame.pack(fill="x", padx=15, pady=15)
        
        compute_btn = ctk.CTkButton(
            button_frame,
            text="🔍 Compute",
            command=self.compute,
            font=("Arial", 11, "bold"),
            height=40,
            corner_radius=8
        )
        compute_btn.pack(side="left", fill="both", expand=True, padx=3)
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🧹 Clear",
            command=self.clear_all,
            font=("Arial", 11, "bold"),
            height=40,
            corner_radius=8,
            fg_color=("#888888", "#555555"),
            hover_color=("#666666", "#333333")
        )
        clear_btn.pack(side="left", fill="both", expand=True, padx=3)
        
        export_btn = ctk.CTkButton(
            button_frame,
            text="💾 Export",
            command=self.export_trail,
            font=("Arial", 11, "bold"),
            height=40,
            corner_radius=8,
            fg_color=("#16a34a", "#15803d"),
            hover_color=("#22c55e", "#16a34a")
        )
        export_btn.pack(side="left", fill="both", expand=True, padx=3)
        
        # ============ RESULT CARD ============
        result_card = ctk.CTkFrame(left_panel, fg_color=("#e0f2fe", "#0c4a6e"), corner_radius=10)
        result_card.pack(fill="x", padx=10, pady=(0, 10))
        
        result_label = ctk.CTkLabel(
            result_card,
            text="Final Root:",
            font=("Arial", 11, "bold"),
            text_color=("#0c4a6e", "#e0f2fe")
        )
        result_label.pack(pady=(10, 5), padx=15)
        
        self.final_var = ctk.StringVar(value="")
        self.final_label = ctk.CTkLabel(
            result_card,
            textvariable=self.final_var,
            font=("Arial", 16, "bold"),
            text_color=("#16a34a", "#22c55e")
        )
        self.final_label.pack(pady=(0, 15), padx=15)
        
        # ============ RIGHT PANEL (TRAIL) ============
        right_panel = ctk.CTkFrame(content_frame, fg_color=("white", "#1e293b"))
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        trail_title = ctk.CTkLabel(
            right_panel,
            text="Solution Trail",
            font=("Arial", 20, "bold"),
            text_color=("#1e293b", "#e2e8f0")
        )
        trail_title.pack(pady=(10, 5), padx=15)
        
        # Solution Trail Text Box
        self.trail_text = ctk.CTkTextbox(
            right_panel,
            font=("Courier New", 13),
            corner_radius=8
        )
        self.trail_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Initialize trail
        self.trail = SolutionTrail(self.trail_text)
        
        # ============ FOOTER ============
        footer = ctk.CTkFrame(self.root, fg_color=("#f0f4f8", "#0f172a"))
        footer.pack(fill="x", padx=0, pady=0)
        
        appearance_label = ctk.CTkLabel(
            footer,
            text="Theme:",
            font=("Arial", 10),
            text_color=("#1e293b", "#e2e8f0")
        )
        appearance_label.pack(side="left", padx=15, pady=10)
        
        appearance_menu = ctk.CTkOptionMenu(
            footer,
            values=["Light", "Dark"],
            command=self.change_appearance_mode,
            font=("Arial", 10)
        )
        appearance_menu.set("System")
        appearance_menu.pack(side="left", padx=5, pady=10)
        
        
        # Initially hide second guess
        self._on_method_change()

    def _on_method_change(self):
        """Show/hide second guess based on selected method."""
        if self.method_var.get() == "Secant":
            self.guess2_label.pack(anchor="w", padx=15, pady=(10, 0))
            self.guess2_entry.pack(fill="x", padx=15, pady=5)
        else:
            self.guess2_label.pack_forget()
            self.guess2_entry.pack_forget()

    def change_appearance_mode(self, mode: str):
        """Change the application appearance mode."""
        ctk.set_appearance_mode(mode.lower())

    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About",
            f"Newton-Raphson Root Finder {APP_VERSION}\n\n"
            "A numerical solver for finding roots using Newton-Raphson "
            "and Secant methods.\n\n"
            "Built with CustomTkinter for a modern UI experience."
        )

    def clear_all(self):
        """Clear all inputs and results."""
        self.guess_var.set("1.5")
        self.guess2_var.set("2.0")
        self.tol_var.set("1e-6")
        self.maxiter_var.set("50")
        # final root placeholder text
        self.final_var.set("placeholder")
        self.trail.clear()

    def validate_inputs(self):
        """Validate user inputs; return tuple(valid, errors_list, ...)"""
        errors = []
        method = self.method_var.get()
        if method not in ("Newton-Raphson", "Secant"):
            errors.append("Please select a valid method.")

        # function
        func = self.function_var.get()
        if func not in PREDEFINED_FUNCTIONS:
            errors.append("Please select a valid predefined function.")

        # initial guess
        try:
            x0 = float(self.guess_var.get())
        except ValueError:
            errors.append("Initial guess must be a number.")
            x0 = None

        x1 = None
        if method == "Secant":
            try:
                x1 = float(self.guess2_var.get())
            except ValueError:
                errors.append("Second guess must be a number for Secant method.")

        # tolerance
        try:
            tol = float(self.tol_var.get())
            if tol <= 0:
                errors.append("Tolerance must be positive.")
        except ValueError:
            errors.append("Tolerance must be a number.")
            tol = None

        # max iterations
        try:
            maxiter = int(self.maxiter_var.get())
            if maxiter <= 0:
                errors.append("Max iterations must be a positive integer.")
        except ValueError:
            errors.append("Max iterations must be an integer.")
            maxiter = None

        valid = len(errors) == 0
        return valid, errors, method, func, x0, x1, tol, maxiter

    def compute(self):
        """Display a skeleton of a solved run filled with placeholders."""
        # clear existing trail and set final value placeholder
        self.trail.clear()
        self.final_var.set("placeholder")
        # add full placeholder structure
        self.trail._write(
            "GIVEN:\n  f(x) = placeholder\n\n"
            "METHOD:\n  placeholder\n\n"
            "STEPS:\n  1. placeholder\n  2. placeholder\n  3. placeholder\n\n"
            "FINAL ANSWER:\n  placeholder\n\n"
            "VERIFICATION:\n  placeholder\n\n"
            "SUMMARY:\n  placeholder\n"
        )

    def export_trail(self):
        """Export the solution trail to a text file."""
        if not self.trail_text.get("1.0", "end-1c").strip():
            messagebox.showinfo("Export", "Nothing to export (trail is empty).")
            return
        filetypes = [("Text files", "*.txt"), ("All files", "*")]
        fname = filedialog.asksaveasfilename(
            title="Export solution trail",
            defaultextension=".txt",
            filetypes=filetypes,
        )
        if fname:
            try:
                self.trail.export(fname)
                messagebox.showinfo("Export", "Trail exported to %s" % fname)
            except Exception as e:
                messagebox.showerror("Export Error", str(e))


if __name__ == "__main__":
    root = ctk.CTk()
    app = NewtonRaphsonApp(root)
    root.mainloop()
