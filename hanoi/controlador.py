"""Controlador que conecta el modelo manual de Hanoi con la vista."""

from modelo import calcular_minimo_movimientos
from modelo import crear_torres
from modelo import mover_disco
from modelo import obtener_estado_torres
from vista import VistaHanoi


class ControladorHanoi:
    """Coordina eventos de la interfaz y operaciones del modelo."""

    def __init__(self, raiz, num_discos_inicial):
        """Inicializa el controlador, la vista y el estado del juego."""
        self.raiz = raiz
        self.vista = VistaHanoi(raiz)
        self.num_discos = num_discos_inicial
        self.torre_a = None
        self.torre_b = None
        self.torre_c = None
        self.torres = {}
        self.movimientos_usuario = 0
        self.eventos_registro = 0
        self.total_minimo = 0
        self.torre_seleccionada = None
        self.animacion_activa = False
        self.juego_resuelto = False

        self.vista.configurar_comandos(
            self.reiniciar,
            self.seleccionar_torre,
        )
        self.vista.establecer_num_discos(self.num_discos)
        self.reiniciar()

    def seleccionar_torre(self, torre):
        """Gestiona la seleccion manual de torres desde el canvas."""
        if self.animacion_activa:
            return

        if self.juego_resuelto:
            self.vista.actualizar_estado(
                "Juego resuelto. Use Nuevo juego para empezar otra vez.",
            )
            return

        if self._entrada_cambio():
            if not self._reiniciar_desde_entrada():
                return

        if self.torre_seleccionada is None:
            self._seleccionar_origen(torre)
            return

        if self.torre_seleccionada == torre:
            self.torre_seleccionada = None
            self.vista.limpiar_seleccion_torre()
            self.vista.actualizar_estado("Seleccion cancelada.")
            return

        self._mover_manual(self.torre_seleccionada, torre)

    def reiniciar(self):
        """Restablece las torres, el registro y los contadores."""
        try:
            num_discos = self._leer_num_discos()
        except ValueError:
            num_discos = self.num_discos

        self.num_discos = num_discos
        self.torre_a, self.torre_b, self.torre_c = crear_torres(
            self.num_discos,
        )
        self.torres = {
            "A": self.torre_a,
            "B": self.torre_b,
            "C": self.torre_c,
        }
        self.movimientos_usuario = 0
        self.eventos_registro = 0
        self.total_minimo = calcular_minimo_movimientos(self.num_discos)
        self.torre_seleccionada = None
        self.animacion_activa = False
        self.juego_resuelto = False

        self.vista.establecer_controles_activos(True)
        self.vista.limpiar_registro()
        self.vista.limpiar_seleccion_torre()
        self.vista.actualizar_estado("Seleccione una torre de origen.")
        self.vista.actualizar_contador(0, self.total_minimo)
        self._dibujar_estado_actual()

    def _leer_num_discos(self):
        """Lee y valida el numero de discos indicado en la vista."""
        texto = self.vista.obtener_num_discos()
        try:
            num_discos = int(texto)
        except ValueError as error:
            raise ValueError("Ingrese un numero entero de discos.") from error

        if num_discos < 1:
            raise ValueError("Ingrese al menos un disco.")
        if num_discos > 10:
            raise ValueError(
                "Use 10 discos o menos para mantener la animacion legible.",
            )
        return num_discos

    def _entrada_cambio(self):
        """Indica si el campo de discos cambio respecto al juego actual."""
        try:
            return self._leer_num_discos() != self.num_discos
        except ValueError:
            return True

    def _reiniciar_desde_entrada(self):
        """Reinicia el juego manual usando el valor escrito por el usuario."""
        try:
            self.num_discos = self._leer_num_discos()
        except ValueError as error:
            self.vista.mostrar_error("Dato invalido", str(error))
            return False

        self.reiniciar()
        return True

    def _seleccionar_origen(self, torre):
        """Selecciona una torre origen si contiene al menos un disco."""
        if self.torres[torre].esta_vacia():
            self.vista.actualizar_estado(f"La torre {torre} esta vacia.")
            return

        self.torre_seleccionada = torre
        self.vista.resaltar_torre(torre)
        self.vista.actualizar_estado(
            f"Torre {torre} seleccionada como origen.",
        )

    def _mover_manual(self, origen, destino):
        """Aplica un movimiento manual validado por las pilas del modelo."""
        estado_antes = obtener_estado_torres(
            self.torre_a,
            self.torre_b,
            self.torre_c,
        )
        nivel_origen = len(estado_antes[origen]) - 1
        nivel_destino = len(estado_antes[destino])

        try:
            movimiento = mover_disco(self.torres[origen], self.torres[destino])
        except (IndexError, ValueError) as error:
            self.torre_seleccionada = None
            self.vista.limpiar_seleccion_torre()
            self.vista.actualizar_estado(str(error))
            return

        self.movimientos_usuario += 1
        self.torre_seleccionada = None
        self._animar_y_refrescar(
            movimiento,
            origen,
            destino,
            nivel_origen,
            nivel_destino,
        )
        self._registrar_evento(movimiento, "Mover")
        self.vista.actualizar_contador(
            self.movimientos_usuario,
            self.total_minimo,
        )
        self.vista.actualizar_estado("Movimiento aplicado.")
        self._verificar_victoria()

    def _animar_y_refrescar(
        self,
        movimiento,
        origen,
        destino,
        nivel_origen,
        nivel_destino,
    ):
        """Anima un movimiento ya validado y refresca el estado visible."""
        self.animacion_activa = True
        self.vista.establecer_controles_activos(False)
        self.vista.animar_disco(
            movimiento[0],
            origen,
            destino,
            nivel_origen,
            nivel_destino,
        )
        self._dibujar_estado_actual()
        self.animacion_activa = False
        self.vista.establecer_controles_activos(True)

    def _registrar_evento(self, movimiento, tipo):
        """Registra visualmente una accion ejecutada por el usuario."""
        self.eventos_registro += 1
        self.vista.agregar_movimiento(
            self.eventos_registro,
            movimiento[0],
            movimiento[1],
            movimiento[2],
            tipo,
        )

    def _dibujar_estado_actual(self):
        """Solicita a la vista dibujar el estado actual de las torres."""
        self.vista.dibujar_torres(
            obtener_estado_torres(self.torre_a, self.torre_b, self.torre_c),
        )

    def _verificar_victoria(self):
        """Comprueba si todos los discos llegaron a la torre C."""
        if self.torre_c.tamaño() != self.num_discos:
            return

        self.juego_resuelto = True
        mensaje = (
            "Juego resuelto en "
            f"{self.movimientos_usuario} movimientos. "
            f"Meta minima: {self.total_minimo}."
        )
        self.vista.actualizar_estado(mensaje)
        self.vista.mostrar_info("Torres de Hanoi", mensaje)
