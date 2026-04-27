import tkinter as tk
from views.view import View
from controllers.controller import Controller
from models.model import DataModel as Model

def main():
    root = tk.Tk()
    root.title("Proyecto1_Vasquez_Rhilmar")

    model = Model()
    view = View(root)
    Controller(view, model)

    root.mainloop()

if __name__ == "__main__":
    main()
