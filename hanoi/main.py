"""Punto de entrada de la aplicación Torres de Hanói."""

import tkinter as interfaz

from controlador import ControladorHanoi


NUM_DISCOS = 4


def main():
    """Crea la ventana de Tkinter y llama al controlador"""
    raiz = interfaz.Tk()
    ControladorHanoi(raiz, NUM_DISCOS)
    raiz.mainloop()


if __name__ == "__main__":
    main()
