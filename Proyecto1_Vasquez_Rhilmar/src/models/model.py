class DataModel:
    """Encapsula la lógica bitwise y el formateo de resultados."""

    OPERATIONS = {
        "AND (&)": {
            "symbol": "&",
            "inputs": ("Primer entero", "Segundo entero"),
            "description": (
                "Activa un bit solo si ambos operandos tienen 1 "
                "en esa posición."
            ),
        },
        "OR (|)": {
            "symbol": "|",
            "inputs": ("Primer entero", "Segundo entero"),
            "description": (
                "Activa un bit si al menos uno de los operandos "
                "tiene 1."
            ),
        },
        "XOR (^)": {
            "symbol": "^",
            "inputs": ("Primer entero", "Segundo entero"),
            "description": (
                "Activa un bit si los operandos son distintos "
                "en esa posición."
            ),
        },
        "NOT (~)": {
            "symbol": "~",
            "inputs": ("Entero",),
            "description": "Invierte todos los bits del operando.",
        },
        "Desplazamiento izquierda (<<)": {
            "symbol": "<<",
            "inputs": ("Entero", "Cantidad de bits"),
            "description": (
                "Mueve los bits a la izquierda y rellena con "
                "ceros a la derecha."
            ),
        },
        "Desplazamiento derecha (>>)": {
            "symbol": ">>",
            "inputs": ("Entero", "Cantidad de bits"),
            "description": (
                "Mueve los bits a la derecha. En enteros con signo "
                "conserva el bit de signo."
            ),
        },
    }

    BIT_WIDTHS = (8, 16, 32, 64)

    def get_operation_names(self):
        return list(self.OPERATIONS.keys())

    def get_operation_config(self, operation_name):
        return self.OPERATIONS[operation_name]

    def calculate(self, operation_name, values, bit_width):
        if bit_width not in self.BIT_WIDTHS:
            raise ValueError("El ancho de bits debe ser 8, 16, 32 o 64.")

        config = self.get_operation_config(operation_name)
        symbol = config["symbol"]
        normalized_values = tuple(int(value) for value in values)
        result = self._execute(symbol, normalized_values)

        return {
            "operation": operation_name,
            "symbol": symbol,
            "description": config["description"],
            "inputs": normalized_values,
            "bit_width": bit_width,
            "result": result,
            "formatted_inputs": [
                self._format_value(value, bit_width)
                for value in normalized_values
            ],
            "formatted_result": self._format_value(result, bit_width),
        }

    def _execute(self, symbol, values):
        if symbol == "&":
            return values[0] & values[1]
        if symbol == "|":
            return values[0] | values[1]
        if symbol == "^":
            return values[0] ^ values[1]
        if symbol == "~":
            return ~values[0]
        if symbol == "<<":
            shift = values[1]
            if shift < 0:
                raise ValueError("La cantidad de bits no puede ser negativa.")
            return values[0] << shift
        if symbol == ">>":
            shift = values[1]
            if shift < 0:
                raise ValueError("La cantidad de bits no puede ser negativa.")
            return values[0] >> shift
        raise ValueError("Operación no soportada.")

    def _format_value(self, value, bit_width):
        mask = (1 << bit_width) - 1
        two_complement = value & mask
        binary = format(two_complement, f"0{bit_width}b")
        grouped_binary = " ".join(
            binary[index:index + 4] for index in range(0, len(binary), 4)
        )
        return {
            "decimal": value,
            "binary": grouped_binary,
            "hex": format(two_complement, f"0{bit_width // 4}X"),
        }
