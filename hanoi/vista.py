"""Vista grafica Tkinter para Torres de Hanoi en modo manual."""

import time
import tkinter as interfaz
from tkinter import messagebox as mensajes


class VistaHanoi:
    """Construye y actualiza la interfaz grafica del juego."""

    def __init__(self, raiz):
        """Inicializa la ventana, los controles y el canvas principal."""
        self.raiz = raiz
        self.raiz.title("Torres Hanoi")
        self.raiz.minsize(980, 620)
        self.raiz.configure(bg="#18202a")

        self.estado_torres = {"A": [], "B": [], "C": []}
        self.discos_canvas = {}
        self.posiciones_torres = {}
        self.torre_seleccionada = None
        self.comando_seleccionar_torre = None
        self.total_discos = 0
        self.alto_disco = 24
        self.base_y = 380
        self.margen_superior = 54
        self.colores = [
            "#d1495b",
            "#edae49",
            "#00798c",
            "#30638e",
            "#6a4c93",
            "#2a9d8f",
            "#e76f51",
            "#8ab17d",
            "#577590",
            "#bc4749",
        ]

        self._crear_estructura()
        self.canvas.bind("<Configure>", self._al_redimensionar)
        self.canvas.bind("<Button-1>", self._al_hacer_clic_canvas)

    def _crear_estructura(self):
        """Crea el tablero, el panel lateral, botones y registro."""
        self.marco_principal = interfaz.Frame(self.raiz, bg="#18202a")
        self.marco_principal.pack(fill=interfaz.BOTH, expand=True)

        self.marco_tablero = interfaz.Frame(
            self.marco_principal,
            bg="#18202a",
            padx=14,
            pady=14,
        )
        self.marco_tablero.pack(
            side=interfaz.LEFT,
            fill=interfaz.BOTH,
            expand=True,
        )

        self.canvas = interfaz.Canvas(
            self.marco_tablero,
            bg="#edf6f2",
            height=520,
            highlightthickness=0,
        )
        self.canvas.pack(fill=interfaz.BOTH, expand=True)

        self.panel_lateral = interfaz.Frame(
            self.marco_principal,
            bg="#243447",
            width=300,
            padx=18,
            pady=18,
        )
        self.panel_lateral.pack(side=interfaz.RIGHT, fill=interfaz.Y)
        self.panel_lateral.pack_propagate(False)

        self.etiqueta_titulo = interfaz.Label(
            self.panel_lateral,
            text="Torres de Hanoi",
            bg="#243447",
            fg="#f8fafc",
            font=("Arial", 17, "bold"),
            anchor="w",
        )
        self.etiqueta_titulo.pack(fill=interfaz.X)

        self.etiqueta_subtitulo = interfaz.Label(
            self.panel_lateral,
            text="",
            bg="#243447",
            fg="#b8c7d9",
            font=("Arial", 10),
            anchor="w",
        )
        self.etiqueta_subtitulo.pack(fill=interfaz.X, pady=(0, 18))

        self._crear_control_discos()
        self._crear_botones()
        self._crear_indicadores()
        self._crear_estado()
        self._crear_registro()

    def _crear_control_discos(self):
        """Crea el campo para indicar la cantidad de discos."""
        self.etiqueta_discos = interfaz.Label(
            self.panel_lateral,
            text="Cantidad de discos",
            bg="#243447",
            fg="#f8fafc",
            anchor="w",
        )
        self.etiqueta_discos.pack(fill=interfaz.X)

        self.campo_num_discos = interfaz.Entry(
            self.panel_lateral,
            width=8,
            justify=interfaz.CENTER,
            font=("Arial", 13, "bold"),
        )
        self.campo_num_discos.pack(fill=interfaz.X, pady=(6, 14))

    def _crear_botones(self):
        """Crea los botones principales del juego manual."""
        self.boton_reiniciar = interfaz.Button(
            self.panel_lateral,
            text="Nuevo juego",
            command=None,
            bg="#35a7ff",
            fg="#07111f",
            activebackground="#79c7ff",
            relief=interfaz.FLAT,
            font=("Arial", 10, "bold"),
        )
        self.boton_reiniciar.pack(fill=interfaz.X, pady=(0, 18))

    def _crear_indicadores(self):
        """Crea los indicadores de movimientos y meta minima."""
        self.marco_indicadores = interfaz.Frame(
            self.panel_lateral,
            bg="#243447",
        )
        self.marco_indicadores.pack(fill=interfaz.X, pady=(0, 16))

        self.valor_movimientos = self._crear_indicador(
            "Movimientos",
            "0",
            0,
        )
        self.valor_meta = self._crear_indicador("Meta minima", "0", 1)

    def _crear_indicador(self, titulo, valor, columna):
        """Crea un indicador numerico dentro del panel lateral."""
        marco = interfaz.Frame(self.marco_indicadores, bg="#1b2a38")
        marco.grid(row=0, column=columna, padx=4, sticky="nsew")
        self.marco_indicadores.columnconfigure(columna, weight=1)

        etiqueta = interfaz.Label(
            marco,
            text=titulo,
            bg="#1b2a38",
            fg="#b8c7d9",
            font=("Arial", 8),
        )
        etiqueta.pack(fill=interfaz.X, pady=(8, 0))

        valor_etiqueta = interfaz.Label(
            marco,
            text=valor,
            bg="#1b2a38",
            fg="#ffffff",
            font=("Arial", 18, "bold"),
        )
        valor_etiqueta.pack(fill=interfaz.X, pady=(0, 8))
        return valor_etiqueta

    def _crear_estado(self):
        """Crea la etiqueta que comunica el estado actual del juego."""
        self.etiqueta_estado = interfaz.Label(
            self.panel_lateral,
            text="Seleccione una torre de origen.",
            bg="#15212d",
            fg="#f8fafc",
            justify=interfaz.LEFT,
            wraplength=250,
            padx=10,
            pady=10,
        )
        self.etiqueta_estado.pack(fill=interfaz.X, pady=(0, 14))

    def _crear_registro(self):
        """Crea el registro de movimientos con barra de desplazamiento."""
        self.etiqueta_registro = interfaz.Label(
            self.panel_lateral,
            text="Bitacora",
            bg="#243447",
            fg="#f8fafc",
            anchor="w",
        )
        self.etiqueta_registro.pack(fill=interfaz.X)

        self.marco_registro = interfaz.Frame(self.panel_lateral)
        self.marco_registro.pack(fill=interfaz.BOTH, expand=True, pady=(6, 0))

        self.registro_movimientos = interfaz.Text(
            self.marco_registro,
            height=10,
            wrap=interfaz.WORD,
            state=interfaz.DISABLED,
            bg="#101820",
            fg="#e6edf3",
            insertbackground="#e6edf3",
            relief=interfaz.FLAT,
            font=("Consolas", 9),
        )
        self.barra_registro = interfaz.Scrollbar(
            self.marco_registro,
            command=self.registro_movimientos.yview,
        )
        self.registro_movimientos.configure(
            yscrollcommand=self.barra_registro.set,
        )
        self.registro_movimientos.pack(
            side=interfaz.LEFT,
            fill=interfaz.BOTH,
            expand=True,
        )
        self.barra_registro.pack(side=interfaz.RIGHT, fill=interfaz.Y)

    def configurar_comandos(
        self,
        comando_reiniciar,
        comando_seleccionar_torre,
    ):
        """Conecta los controles de la vista con el controlador."""
        self.boton_reiniciar.configure(command=comando_reiniciar)
        self.comando_seleccionar_torre = comando_seleccionar_torre

    def establecer_num_discos(self, num_discos):
        """Muestra una cantidad de discos en el campo de entrada."""
        self.campo_num_discos.delete(0, interfaz.END)
        self.campo_num_discos.insert(0, str(num_discos))

    def obtener_num_discos(self):
        """Devuelve el texto ingresado como cantidad de discos."""
        return self.campo_num_discos.get().strip()

    def establecer_controles_activos(self, activos):
        """Activa o desactiva controles durante la animacion."""
        estado = interfaz.NORMAL if activos else interfaz.DISABLED
        self.boton_reiniciar.configure(state=estado)
        self.campo_num_discos.configure(state=estado)

    def dibujar_torres(self, estado_torres):
        """Dibuja las torres y discos segun el estado recibido."""
        self.estado_torres = {
            "A": list(estado_torres.get("A", [])),
            "B": list(estado_torres.get("B", [])),
            "C": list(estado_torres.get("C", [])),
        }
        self.total_discos = self._calcular_total_discos()
        self.canvas.delete("all")
        self.discos_canvas = {}

        ancho = max(self.canvas.winfo_width(), 640)
        alto = max(self.canvas.winfo_height(), 440)
        self.base_y = alto - 74
        self.margen_superior = 58
        espacio_vertical = max(180, self.base_y - self.margen_superior)
        self.alto_disco = max(
            16,
            min(30, espacio_vertical // max(self.total_discos + 2, 3)),
        )
        self.posiciones_torres = {
            "A": ancho * 0.20,
            "B": ancho * 0.50,
            "C": ancho * 0.80,
        }

        self._dibujar_fondo_tablero(ancho, alto)
        self._dibujar_base_y_postes(ancho)
        self._dibujar_discos()

    def resaltar_torre(self, torre):
        """Resalta visualmente la torre seleccionada por el usuario."""
        self.torre_seleccionada = torre
        self.dibujar_torres(self.estado_torres)

    def limpiar_seleccion_torre(self):
        """Quita cualquier resaltado de torre seleccionada."""
        self.torre_seleccionada = None
        self.dibujar_torres(self.estado_torres)

    def _calcular_total_discos(self):
        """Calcula la cantidad total de discos presentes en las torres."""
        total = 0
        for discos in self.estado_torres.values():
            total += len(discos)
        return total

    def _dibujar_fondo_tablero(self, ancho, alto):
        """Dibuja elementos de fondo del tablero."""
        self.canvas.create_rectangle(
            0,
            0,
            ancho,
            alto,
            fill="#edf6f2",
            outline="#edf6f2",
        )
        self.canvas.create_text(
            24,
            24,
            anchor="w",
            text="Mover: clic en origen y luego clic en destino",
            fill="#334155",
            font=("Arial", 11, "bold"),
        )

    def _dibujar_base_y_postes(self, ancho):
        """Dibuja la base horizontal y los tres postes verticales."""
        self.canvas.create_rectangle(
            44,
            self.base_y,
            ancho - 44,
            self.base_y + 16,
            fill="#263238",
            outline="#263238",
        )

        for nombre, posicion_x in self.posiciones_torres.items():
            self._dibujar_zona_torre(nombre, posicion_x)

    def _dibujar_zona_torre(self, nombre, posicion_x):
        """Dibuja la zona visual correspondiente a una torre."""
        seleccionada = nombre == self.torre_seleccionada
        color_poste = "#ef476f" if seleccionada else "#455a64"
        color_zona = "#cdece4" if seleccionada else "#dde9e5"

        self.canvas.create_rectangle(
            posicion_x - 112,
            self.margen_superior - 8,
            posicion_x + 112,
            self.base_y + 38,
            fill=color_zona,
            outline=color_zona,
        )
        self.canvas.create_rectangle(
            posicion_x - 5,
            self.margen_superior,
            posicion_x + 5,
            self.base_y,
            fill=color_poste,
            outline=color_poste,
        )
        self.canvas.create_oval(
            posicion_x - 18,
            self.base_y + 24,
            posicion_x + 18,
            self.base_y + 60,
            fill="#243447",
            outline="#243447",
        )
        self.canvas.create_text(
            posicion_x,
            self.base_y + 42,
            text=nombre,
            fill="#ffffff",
            font=("Arial", 12, "bold"),
        )

    def _dibujar_discos(self):
        """Dibuja cada disco de cada torre sobre el canvas."""
        for nombre_torre, discos in self.estado_torres.items():
            for nivel, disco in enumerate(discos):
                coordenadas = self.calcular_rectangulo_disco(
                    disco,
                    nombre_torre,
                    nivel,
                )
                color = self._obtener_color_disco(disco)
                rectangulo = self.canvas.create_rectangle(
                    *coordenadas,
                    fill=color,
                    outline="#1f2937",
                    width=1,
                )
                x_1, y_1, x_2, y_2 = coordenadas
                texto = self.canvas.create_text(
                    (x_1 + x_2) / 2,
                    (y_1 + y_2) / 2,
                    text=str(disco),
                    fill="#ffffff",
                    font=("Arial", 10, "bold"),
                )
                self.discos_canvas[disco] = (rectangulo, texto)

    def _obtener_color_disco(self, disco):
        """Devuelve un color estable para el disco indicado."""
        indice = (disco - 1) % len(self.colores)
        return self.colores[indice]

    def calcular_rectangulo_disco(self, disco, torre, nivel):
        """Calcula las coordenadas del rectangulo de un disco."""
        ancho_maximo = 210
        ancho_minimo = 64
        divisor = max(self.total_discos, 1)
        ancho = ancho_minimo + (ancho_maximo - ancho_minimo) * disco / divisor
        centro_x = self.posiciones_torres[torre]
        y_2 = self.base_y - (nivel * self.alto_disco)
        y_1 = y_2 - self.alto_disco + 4
        return centro_x - ancho / 2, y_1, centro_x + ancho / 2, y_2

    def animar_disco(
        self,
        disco,
        origen,
        destino,
        nivel_origen,
        nivel_destino,
    ):
        """Anima un disco desde una torre origen hasta una torre destino."""
        if disco not in self.discos_canvas:
            return

        rectangulo, texto = self.discos_canvas[disco]
        caja = self.canvas.bbox(rectangulo)
        if caja is None:
            return

        x_1, y_1, x_2, y_2 = caja
        x_actual = (x_1 + x_2) / 2
        y_actual = (y_1 + y_2) / 2
        objetivo = self.calcular_rectangulo_disco(
            disco,
            destino,
            nivel_destino,
        )
        x_objetivo = (objetivo[0] + objetivo[2]) / 2
        y_objetivo = (objetivo[1] + objetivo[3]) / 2
        y_elevado = self.margen_superior + self.alto_disco

        puntos = [
            (x_actual, y_actual),
            (x_actual, y_elevado),
            (x_objetivo, y_elevado),
            (x_objetivo, y_objetivo),
        ]
        pausa = 0.02
        pasos = 16

        for indice in range(len(puntos) - 1):
            self._animar_tramo(
                (rectangulo, texto),
                puntos[indice],
                puntos[indice + 1],
                pasos,
                pausa,
            )

        self._alinear_disco((rectangulo, texto), objetivo)

    def _animar_tramo(self, elementos, inicio, fin, pasos, pausa):
        """Mueve los elementos de un disco entre dos puntos."""
        x_inicio, y_inicio = inicio
        x_fin, y_fin = fin
        desplazamiento_x = (x_fin - x_inicio) / pasos
        desplazamiento_y = (y_fin - y_inicio) / pasos

        for _ in range(pasos):
            self.canvas.move(elementos[0], desplazamiento_x, desplazamiento_y)
            self.canvas.move(elementos[1], desplazamiento_x, desplazamiento_y)
            self.canvas.update_idletasks()
            self.raiz.update()
            time.sleep(pausa)

    def _alinear_disco(self, elementos, coordenadas_objetivo):
        """Ajusta el disco al rectangulo final para evitar deriva visual."""
        rectangulo, texto = elementos
        x_1, y_1, x_2, y_2 = coordenadas_objetivo
        self.canvas.coords(rectangulo, x_1, y_1, x_2, y_2)
        self.canvas.coords(texto, (x_1 + x_2) / 2, (y_1 + y_2) / 2)

    def agregar_movimiento(
        self,
        numero_evento,
        disco,
        origen,
        destino,
        tipo="Mover",
    ):
        """Agrega una linea al registro de movimientos."""
        linea = (
            f"{numero_evento:03d} | {tipo}: "
            f"disco {disco} | {origen} -> {destino}\n"
        )
        self.registro_movimientos.configure(state=interfaz.NORMAL)
        self.registro_movimientos.insert(interfaz.END, linea)
        self.registro_movimientos.see(interfaz.END)
        self.registro_movimientos.configure(state=interfaz.DISABLED)

    def limpiar_registro(self):
        """Elimina todas las lineas del registro de movimientos."""
        self.registro_movimientos.configure(state=interfaz.NORMAL)
        self.registro_movimientos.delete("1.0", interfaz.END)
        self.registro_movimientos.configure(state=interfaz.DISABLED)

    def actualizar_contador(self, cantidad, total):
        """Actualiza los contadores visibles del panel lateral."""
        self.valor_movimientos.configure(text=str(cantidad))
        self.valor_meta.configure(text=str(total))

    def actualizar_estado(self, mensaje):
        """Actualiza el mensaje de estado de la interfaz."""
        self.etiqueta_estado.configure(text=mensaje)

    def mostrar_error(self, titulo, mensaje):
        """Muestra un mensaje de error al usuario."""
        mensajes.showerror(titulo, mensaje)

    def mostrar_info(self, titulo, mensaje):
        """Muestra un mensaje informativo al usuario."""
        mensajes.showinfo(titulo, mensaje)

    def obtener_torre_desde_posicion(self, posicion_x):
        """Devuelve la torre mas cercana a una coordenada horizontal."""
        if not self.posiciones_torres:
            ancho = max(self.canvas.winfo_width(), 1)
            tercio = ancho / 3
            if posicion_x < tercio:
                return "A"
            if posicion_x < tercio * 2:
                return "B"
            return "C"

        return min(
            self.posiciones_torres,
            key=lambda torre: abs(self.posiciones_torres[torre] - posicion_x),
        )

    def _al_hacer_clic_canvas(self, evento):
        """Notifica al controlador la torre pulsada sobre el canvas."""
        if self.comando_seleccionar_torre is None:
            return

        torre = self.obtener_torre_desde_posicion(evento.x)
        self.comando_seleccionar_torre(torre)

    def _al_redimensionar(self, evento):
        """Redibuja la escena cuando cambia el tamaño del canvas."""
        if evento.width > 1 and evento.height > 1:
            self.dibujar_torres(self.estado_torres)
