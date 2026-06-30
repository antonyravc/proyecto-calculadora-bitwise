# Torres de Hanoi con Tkinter

Proyecto en Python que implementa el juego de las Torres de Hanoi con
interfaz grafica usando Tkinter. El programa permite que el usuario resuelva
el juego manualmente seleccionando una torre de origen y luego una torre de
destino.

## Objetivo

El objetivo del proyecto es representar las Torres de Hanoi usando pilas
explicitas como estructura de datos principal.

Cada torre es una pila:

- `apilar()` coloca un disco arriba.
- `desapilar()` retira el disco superior.
- `ver_tope()` consulta el disco superior.
- `esta_vacia()` indica si la torre no tiene discos.
- `tamaño()` devuelve la cantidad de discos.

La regla principal del juego se valida dentro de `apilar()`: no se puede poner
un disco grande sobre uno mas pequenio.

## Estructura del proyecto

```text
hanoi/
|-- main.py
|-- modelo.py
|-- vista.py
|-- controlador.py
|-- README.md
```

## Arquitectura MVC

El programa esta organizado con arquitectura MVC.

### Modelo: `modelo.py`

Contiene la clase `Pila` y la logica principal del juego.

Responsabilidades:

- Crear las tres torres A, B y C.
- Guardar los discos dentro de pilas.
- Validar que no se coloque un disco grande sobre uno pequenio.
- Mover discos entre torres.
- Devolver el estado actual de las torres.

### Vista: `vista.py`

Contiene la interfaz grafica hecha con Tkinter.

Responsabilidades:

- Dibujar las torres y los discos en el canvas.
- Mostrar el panel lateral.
- Mostrar el contador de movimientos.
- Mostrar la meta minima.
- Registrar los movimientos en la bitacora.
- Detectar clics del usuario sobre el canvas.

### Controlador: `controlador.py`

Conecta el modelo con la vista.

Responsabilidades:

- Recibir los clics que detecta la vista.
- Saber si el clic representa una torre de origen o destino.
- Pedir al modelo que mueva el disco.
- Actualizar la vista despues de cada movimiento.
- Contar movimientos.
- Verificar si el usuario completo el juego.

### Punto de entrada: `main.py`

Inicia la aplicacion.

Define la constante:

```python
NUM_DISCOS = 4
```

Ese valor indica con cuantos discos empieza el juego.

## Como ejecutar

Desde PowerShell, dentro de la carpeta del proyecto:

```powershell
& "$env:LOCALAPPDATA\Python\bin\python.exe" main.py
```

Tambien puede ejecutarse con:

```powershell
python main.py
```

si Python esta configurado correctamente en el sistema.

## Como se usa

1. Escriba la cantidad de discos.
2. Presione `Nuevo juego`.
3. Haga clic en una torre de origen.
4. Haga clic en una torre de destino.
5. Si el movimiento es valido, el disco se mueve.
6. Si el movimiento es invalido, se muestra un mensaje.
7. El juego termina cuando todos los discos llegan a la torre C.

## Elementos de la ventana

- **Canvas:** zona donde se dibujan las torres y discos.
- **Cantidad de discos:** campo para elegir el numero de discos.
- **Nuevo juego:** reinicia el juego con la cantidad indicada.
- **Movimientos:** muestra cuantos movimientos hizo el usuario.
- **Meta minima:** muestra la cantidad minima teorica de movimientos.
- **Mensaje de estado:** indica que accion debe realizar el usuario.
- **Bitacora:** registra cada movimiento realizado.

## Ruta del dato

El dato principal es el estado de las torres.

Ejemplo con 4 discos:

```python
{
    "A": [4, 3, 2, 1],
    "B": [],
    "C": []
}
```

El recorrido es:

```text
Modelo -> Controlador -> Vista
```

Cuando el usuario hace clic:

```text
Vista -> Controlador -> Modelo -> Controlador -> Vista
```

Es decir:

1. La vista detecta el clic.
2. El controlador recibe la torre seleccionada.
3. El controlador pide al modelo mover el disco.
4. El modelo valida y actualiza las pilas.
5. El controlador pide el nuevo estado.
6. La vista redibuja las torres y discos.

## Registro de movimientos

Cada movimiento valido se registra en la bitacora con este formato:

```text
001 | Mover: disco 1 | A -> C
```

El registro se agrega desde el controlador y se muestra en la vista usando el
widget `Text` de Tkinter.

## Calculo de la meta minima

La cantidad minima de movimientos se calcula con la formula:

```python
2 ** num_discos - 1
```

Ejemplo:

```text
4 discos = 2^4 - 1 = 15 movimientos
```

## Conceptos aplicados

- Programacion orientada a objetos.
- Estructura de datos pila.
- Arquitectura MVC.
- Interfaz grafica con Tkinter.
- Validacion de reglas del juego.
- Manejo de eventos con clics.
- Representacion visual con canvas.

## Resumen para exposicion

Este proyecto representa las Torres de Hanoi usando pilas. Cada torre es una
instancia de la clase `Pila`, y los movimientos se realizan con `desapilar()` y
`apilar()`. La vista no modifica directamente los datos, solo muestra el estado
que recibe. El controlador se encarga de conectar los clics del usuario con las
operaciones del modelo. Asi se separan correctamente las responsabilidades del
programa.
