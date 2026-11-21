import tkinter as tk

from datos import Catalogo
from vista import Formulario, Botonera, TablaJuegos
from acciones import ControladorCatalogo


class AplicacionCatalogo(tk.Tk):
    """Ventana principal: arma el formulario, la botonera y la tabla."""

    def __init__(self, archivo="juegos.json"):
        super().__init__()
        self.title("Biblioteca de videojuegos")
        self.geometry("750x600")

        self.formulario = Formulario(self)
        self.formulario.pack(fill="x", padx=15, pady=(12, 6))

        self.tabla = TablaJuegos(self)
        self.controlador = ControladorCatalogo(Catalogo(archivo), self.formulario, self.tabla)

        self.botonera = Botonera(self,
            al_agregar=self.controlador.agregar,
            al_editar=self.controlador.editar,
            al_eliminar=self.controlador.eliminar)
        self.controlador.botonera = self.botonera

        # La botonera va entre el formulario y la tabla
        self.botonera.pack()
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # Cargar lo que ya existe en juegos.json al abrir el programa
        self.controlador.refrescar_tabla()


if __name__ == "__main__":
    AplicacionCatalogo().mainloop()
