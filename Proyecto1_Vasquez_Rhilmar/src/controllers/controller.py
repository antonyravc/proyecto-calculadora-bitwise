class Controller:
    """Coordina validaciones, eventos de interfaz y cálculos del modelo."""

    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.view.on_calculate = self.handle_calculate
        self.view.on_operation_change = self.handle_operation_change

        operations = self.model.get_operation_names()
        self.view.set_operations(operations)
        self.handle_operation_change()

    def handle_operation_change(self):
        operation_name = self.view.get_selected_operation()
        config = self.model.get_operation_config(operation_name)
        self.view.set_operation_inputs(config["inputs"])
        self.view.set_description(config["description"])
        self.view.clear_error()

    def handle_calculate(self):
        operation_name = self.view.get_selected_operation()
        config = self.model.get_operation_config(operation_name)
        raw_values = self.view.get_input_values(len(config["inputs"]))

        try:
            values = [
                self._parse_integer(value, label)
                for value, label in zip(raw_values, config["inputs"])
            ]
            payload = self.model.calculate(
                operation_name,
                values,
                self.view.get_bit_width(),
            )
        except ValueError as error:
            self.view.show_error(str(error))
            return

        self.view.clear_error()
        self.view.show_result(payload)

    def _parse_integer(self, raw_value, field_name):
        if raw_value == "":
            raise ValueError(f"El campo '{field_name}' es obligatorio.")
        try:
            return int(raw_value)
        except ValueError as error:
            message = (
                f"El campo '{field_name}' debe contener "
                "un entero válido."
            )
            raise ValueError(message) from error
