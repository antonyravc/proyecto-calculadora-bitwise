"""Modelo de Torres de Hanoi con juego manual y pilas explicitas."""


class Pila:
    """Representa una pila usada como torre del juego."""

    def __init__(self, nombre):
        """Inicializa una pila vacia con nombre."""
        self.nombre = nombre
        self._elementos = []

    def apilar(self, elemento):
        """Coloca un elemento sobre la pila validando la regla de Hanoi."""
        if not self.esta_vacia() and elemento > self.ver_tope():
            mensaje = (
                "Movimiento invalido: no se puede colocar el disco "
                f"{elemento} sobre el disco {self.ver_tope()}."
            )
            raise ValueError(mensaje)
        self._elementos.append(elemento)

    def desapilar(self):
        """Retira y devuelve el elemento ubicado en el tope de la pila."""
        if self.esta_vacia():
            raise IndexError(f"La pila {self.nombre} esta vacia.")
        return self._elementos.pop()

    def ver_tope(self):
        """Devuelve el elemento superior sin retirarlo de la pila."""
        if self.esta_vacia():
            return None
        return self._elementos[-1]

    def esta_vacia(self):
        """Indica si la pila no contiene elementos."""
        return len(self._elementos) == 0

    def tamaño(self):
        """Devuelve la cantidad de elementos almacenados en la pila."""
        return len(self._elementos)

    def obtener_contenido(self):
        """Devuelve una copia del contenido de la pila de base a tope."""
        return list(self._elementos)


_torres_actuales = None


def _registrar_torres(torre_a, torre_b, torre_c):
    """Guarda las torres usadas por el modelo para consultar su estado."""
    global _torres_actuales
    _torres_actuales = (torre_a, torre_b, torre_c)


def validar_numero_discos(num_discos):
    """Valida que la cantidad de discos sea un entero positivo."""
    if not isinstance(num_discos, int):
        raise TypeError("La cantidad de discos debe ser un numero entero.")
    if num_discos < 1:
        raise ValueError("La cantidad de discos debe ser mayor que cero.")


def calcular_minimo_movimientos(num_discos):
    """Calcula la cantidad minima teorica de movimientos del juego."""
    validar_numero_discos(num_discos)
    return (2 ** num_discos) - 1


def crear_torres(num_discos):
    """Crea las tres torres y apila los discos iniciales en la torre A."""
    validar_numero_discos(num_discos)
    torre_a = Pila("A")
    torre_b = Pila("B")
    torre_c = Pila("C")

    for disco in range(num_discos, 0, -1):
        torre_a.apilar(disco)

    _registrar_torres(torre_a, torre_b, torre_c)
    return torre_a, torre_b, torre_c


def mover_disco(origen, destino):
    """Mueve el disco superior desde una pila origen hacia una destino."""
    disco = origen.desapilar()
    try:
        destino.apilar(disco)
    except ValueError:
        origen.apilar(disco)
        raise
    return disco, origen.nombre, destino.nombre


def obtener_estado_torres(torre_a=None, torre_b=None, torre_c=None):
    """Devuelve el contenido actual de las tres pilas de base a tope."""
    if torre_a is None or torre_b is None or torre_c is None:
        if _torres_actuales is None:
            raise ValueError("No hay torres registradas en el modelo.")
        torre_a, torre_b, torre_c = _torres_actuales
    else:
        _registrar_torres(torre_a, torre_b, torre_c)

    return {
        torre_a.nombre: torre_a.obtener_contenido(),
        torre_b.nombre: torre_b.obtener_contenido(),
        torre_c.nombre: torre_c.obtener_contenido(),
    }
