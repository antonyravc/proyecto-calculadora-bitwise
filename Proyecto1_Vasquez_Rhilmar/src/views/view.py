import tkinter as tk
from tkinter import ttk


class View:
    """Construye la interfaz y delega la lógica al controlador."""

    def __init__(self, master):
        self.master = master
        self.master.title("Proyecto 1: Calculadora Bitwise")
        self.master.resizable(False, False)
        self.master.configure(bg="#f4efe6")

        self.operation_var = tk.StringVar()
        self.bit_width_var = tk.StringVar(value="8")
        self.input_vars = [tk.StringVar(), tk.StringVar()]
        self.description_var = tk.StringVar()
        self.error_var = tk.StringVar()
        self.result_var = tk.StringVar(
            value="Selecciona una operación e ingresa valores."
        )
        self.binary_var = tk.StringVar(value="-")
        self.detail_vars = [tk.StringVar(value="-"), tk.StringVar(value="-")]

        self.on_calculate = None
        self.on_operation_change = None

        self._configure_styles()
        self._build_layout()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("App.TFrame", background="#f4efe6")
        style.configure(
            "Card.TLabelframe",
            background="#fffaf2",
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "Card.TLabelframe.Label",
            background="#fffaf2",
            foreground="#153243",
            font=("Segoe UI Semibold", 10),
        )
        style.configure(
            "App.TLabel",
            background="#f4efe6",
            foreground="#153243",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Hero.TLabel",
            background="#f4efe6",
            foreground="#8c3d1f",
            font=("Segoe UI Semibold", 16),
        )
        style.configure(
            "Body.TLabel",
            background="#f4efe6",
            foreground="#3c4a57",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Accent.TButton",
            background="#d96c3f",
            foreground="white",
            font=("Segoe UI Semibold", 10),
            padding=(10, 8),
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#c85c32")],
            foreground=[("disabled", "#f6e7df")],
        )

    def _build_layout(self):
        container = ttk.Frame(
            self.master,
            padding=18,
            style="App.TFrame",
        )
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(1, weight=1)
        container.columnconfigure(2, weight=1)

        ttk.Label(
            container,
            text="Proyecto 1: Calculadora Bitwise",
            style="Hero.TLabel",
        ).grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(
            container,
            text=(
                "Calculadora visual de operaciones bitwise para "
                "números enteros con salida decimal y binaria."
            ),
            style="Body.TLabel",
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(4, 14))

        ttk.Label(
            container,
            text="Operación:",
            style="App.TLabel",
        ).grid(row=2, column=0, sticky="w")
        self.operation_combo = ttk.Combobox(
            container,
            textvariable=self.operation_var,
            state="readonly",
            width=32,
        )
        self.operation_combo.grid(
            row=2,
            column=1,
            columnspan=2,
            sticky="ew",
            pady=(0, 8),
        )
        self.operation_combo.bind(
            "<<ComboboxSelected>>",
            self._handle_operation_change,
        )

        ttk.Label(
            container,
            text="Representación:",
            style="App.TLabel",
        ).grid(row=3, column=0, sticky="w")
        self.bit_width_combo = ttk.Combobox(
            container,
            textvariable=self.bit_width_var,
            state="readonly",
            values=("8", "16", "32", "64"),
            width=10,
        )
        self.bit_width_combo.grid(row=3, column=1, sticky="w", pady=(0, 8))

        self.input_labels = []
        self.input_entries = []
        for row_index in range(2):
            label = ttk.Label(
                container,
                text=f"Valor {row_index + 1}:",
                style="App.TLabel",
            )
            entry = ttk.Entry(
                container,
                textvariable=self.input_vars[row_index],
                width=24,
            )
            label.grid(row=4 + row_index, column=0, sticky="w")
            entry.grid(
                row=4 + row_index,
                column=1,
                columnspan=2,
                sticky="ew",
                pady=4,
            )
            self.input_labels.append(label)
            self.input_entries.append(entry)

        ttk.Button(
            container,
            text="Calcular",
            command=self._handle_calculate,
            style="Accent.TButton",
        ).grid(
            row=6,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(10, 10),
        )

        ttk.Label(
            container,
            textvariable=self.description_var,
            wraplength=420,
            justify="left",
            style="Body.TLabel",
        ).grid(row=7, column=0, columnspan=3, sticky="w")

        ttk.Label(
            container,
            textvariable=self.error_var,
            foreground="#b00020",
            wraplength=420,
            justify="left",
            style="Body.TLabel",
        ).grid(row=8, column=0, columnspan=3, sticky="w", pady=(8, 0))

        result_frame = ttk.LabelFrame(
            container,
            text="Resultado",
            padding=12,
            style="Card.TLabelframe",
        )
        result_frame.grid(
            row=9,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(12, 0),
        )

        ttk.Label(
            result_frame,
            textvariable=self.result_var,
            wraplength=400,
            justify="left",
        ).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            result_frame,
            text="Binario:",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Label(
            result_frame,
            textvariable=self.binary_var,
            wraplength=400,
            justify="left",
        ).grid(row=2, column=0, sticky="w")

        detail_frame = ttk.LabelFrame(
            container,
            text="Operandos",
            padding=12,
            style="Card.TLabelframe",
        )
        detail_frame.grid(
            row=10,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(12, 0),
        )

        ttk.Label(
            detail_frame,
            textvariable=self.detail_vars[0],
            wraplength=400,
            justify="left",
        ).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            detail_frame,
            textvariable=self.detail_vars[1],
            wraplength=400,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        footer_text = (
            "Los valores negativos se muestran en complemento a dos "
            "según el ancho seleccionado."
        )
        ttk.Label(
            container,
            text=footer_text,
            style="Body.TLabel",
        ).grid(row=11, column=0, columnspan=3, sticky="w", pady=(12, 0))

    def set_operations(self, operations):
        self.operation_combo["values"] = operations
        if operations:
            self.operation_var.set(operations[0])

    def set_operation_inputs(self, labels):
        for index, label in enumerate(self.input_labels):
            if index < len(labels):
                label.config(text=f"{labels[index]}:")
                self.input_entries[index].grid()
                label.grid()
            else:
                self.input_entries[index].grid_remove()
                label.grid_remove()
                self.input_vars[index].set("")

    def set_description(self, description):
        self.description_var.set(description)

    def clear_error(self):
        self.error_var.set("")

    def show_error(self, message):
        self.error_var.set(message)

    def get_selected_operation(self):
        return self.operation_var.get()

    def get_bit_width(self):
        return int(self.bit_width_var.get())

    def get_input_values(self, amount):
        return [
            self.input_vars[index].get().strip()
            for index in range(amount)
        ]

    def show_result(self, payload):
        result = payload["formatted_result"]
        result_text = (
            f"Resultado decimal: {result['decimal']} | "
            f"hexadecimal: 0x{result['hex']}"
        )
        self.result_var.set(
            result_text
        )
        binary_text = (
            f"{result['binary']}  "
            f"(complemento a dos de {payload['bit_width']} bits)"
        )
        self.binary_var.set(
            binary_text
        )

        formatted_inputs = payload["formatted_inputs"]
        if formatted_inputs:
            first_operand = formatted_inputs[0]
            self.detail_vars[0].set(
                "Operando 1: "
                f"{first_operand['decimal']} | "
                f"binario: {first_operand['binary']}"
            )
        else:
            self.detail_vars[0].set("-")

        if len(formatted_inputs) > 1:
            second_operand = formatted_inputs[1]
            self.detail_vars[1].set(
                "Operando 2: "
                f"{second_operand['decimal']} | "
                f"binario: {second_operand['binary']}"
            )
        else:
            self.detail_vars[1].set("-")

    def _handle_calculate(self):
        if self.on_calculate:
            self.on_calculate()

    def _handle_operation_change(self, _event):
        if self.on_operation_change:
            self.on_operation_change()
