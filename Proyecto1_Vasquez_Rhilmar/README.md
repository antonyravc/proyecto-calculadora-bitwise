# Proyecto1_Vasquez_Rhilmar

Aplicación visual desarrollada en Python con Tkinter para realizar
operaciones bitwise sobre números enteros. El proyecto permite trabajar
con operaciones binarias, unarias y desplazamientos, mostrando el
resultado tanto en formato decimal como en formato binario con
representación en complemento a dos.

## Descripción

`Proyecto1_Vasquez_Rhilmar` es una calculadora de operaciones a nivel de
bits construida con una arquitectura tipo MVC. La interfaz gráfica guía
al usuario para:

- Seleccionar una operación bitwise.
- Ingresar los valores requeridos según el tipo de operación.
- Elegir el ancho de representación binaria: `8`, `16`, `32` o `64`
  bits.
- Ver el resultado en decimal, hexadecimal y binario.
- Comprender el comportamiento de enteros negativos usando complemento a
  dos.

## Características

- Interfaz gráfica visual con Tkinter.
- Validación de entradas para aceptar solo enteros válidos.
- Implementación real de operadores bitwise de Python.
- Soporte para números negativos.
- Representación binaria agrupada para facilitar la lectura.
- Organización modular separando modelo, vista y controlador.

## Operaciones implementadas

- `AND (&)`: activa un bit solo si ambos operandos tienen `1`.
- `OR (|)`: activa un bit si al menos uno de los operandos tiene `1`.
- `XOR (^)`: activa un bit si los operandos difieren en esa posición.
- `NOT (~)`: invierte todos los bits del operando.
- `Desplazamiento izquierda (<<)`: mueve bits a la izquierda.
- `Desplazamiento derecha (>>)`: mueve bits a la derecha.

## Estructura del proyecto

```text
Proyecto1_Vasquez_Rhilmar/
|-- README.md
|-- requirements.txt
`-- src/
    |-- main.py
    |-- controllers/
    |   `-- controller.py
    |-- models/
    |   `-- model.py
    `-- views/
        `-- view.py
```

## Requisitos

- Python `3.10` o superior.
- Tkinter disponible en la instalación de Python.

Nota: `Tkinter` forma parte de la biblioteca estándar de Python en la
mayoría de instalaciones de Windows, por lo que no se instala mediante
`pip`.

## Instalación

1. Descargar o clonar el proyecto.
2. Ubicarse en la carpeta raíz del proyecto.
3. Verificar que Python esté instalado:

```powershell
python --version
```

4. Revisar el archivo `requirements.txt`.

En este proyecto no es necesario instalar paquetes externos con `pip`,
ya que todas las dependencias utilizadas pertenecen a la biblioteca
estándar.

## Configuración

No se requiere configuración adicional. Solo asegúrate de ejecutar el
programa desde la carpeta `src` o desde la raíz invocando el archivo
principal.

## Ejecución

Desde la raíz del proyecto:

```powershell
python .\src\main.py
```

## Uso

1. Abrir la aplicación.
2. Seleccionar la operación deseada.
3. Elegir el ancho de bits para la representación binaria.
4. Ingresar uno o dos valores enteros según corresponda.
5. Presionar el botón `Calcular`.
6. Revisar el resultado generado en decimal, hexadecimal y binario.

## Funcionamiento

La aplicación adapta automáticamente los campos de entrada según la
operación seleccionada:

- `AND`, `OR` y `XOR`: solicitan dos enteros.
- `NOT`: solicita un solo entero.
- `<<` y `>>`: solicitan un entero y la cantidad de bits a desplazar.

El procesamiento usa directamente operadores bitwise del lenguaje
Python. Para mostrar el resultado binario de forma clara, el sistema:

1. Aplica una máscara según el ancho seleccionado (`8`, `16`, `32` o
   `64` bits).
2. Obtiene la representación en complemento a dos.
3. Agrupa los bits de cuatro en cuatro para hacer más legible la salida.

Ejemplo conceptual con `8` bits:

- Decimal: `-6`
- Binario en complemento a dos: `1111 1010`

## Arquitectura

El proyecto sigue una organización modular:

- `src/models/model.py`: contiene la lógica de negocio y las operaciones
  bitwise.
- `src/views/view.py`: construye la interfaz gráfica y presenta los
  resultados.
- `src/controllers/controller.py`: coordina eventos, validaciones y
  comunicación entre vista y modelo.
- `src/main.py`: inicializa la aplicación.

## Validaciones implementadas

- Campos obligatorios.
- Verificación de enteros válidos.
- Restricción de desplazamientos negativos.
- Restricción de anchos de representación a `8`, `16`, `32` o `64`
  bits.

## Dependencias

Las dependencias reales del proyecto son:

- `tkinter`
- `ttk`

Ambas pertenecen a la biblioteca estándar de Python, por lo que no
requieren instalación separada mediante `pip`.

## Autor

- Rhilmar Antony Vasquez Castedo
