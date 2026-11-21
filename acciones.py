"""Controlador: responde a los botones y conecta la vista con el catálogo."""
from tkinter import messagebox


class ControladorCatalogo:
    """Lógica de agregar, editar y eliminar juegos."""

    def __init__(self, catalogo, formulario, tabla, botonera=None):
        self.catalogo = catalogo
        self.formulario = formulario
        self.tabla = tabla
        self.botonera = botonera
        # Posición del juego que se está editando. None cuando no se edita nada.
        self.indice_en_edicion = None

    @property
    def editando(self):
        return self.indice_en_edicion is not None

    def refrescar_tabla(self):
        self.tabla.mostrar(self.catalogo.listar())

    def agregar(self):
        """Lee el formulario, guarda, limpia y refresca la tabla."""
        juego = self.formulario.obtener_juego()
        if juego is None:
            return  # no guardar juegos sin título

        self.catalogo.agregar(juego)
        self.formulario.limpiar()
        self.refrescar_tabla()

    def eliminar(self):
        """Borra el juego que está seleccionado en la tabla."""
        if self.editando:
            messagebox.showwarning("Edición en curso", "Guarda los cambios del juego que estás editando antes de eliminar.")
            return

        indice = self.tabla.indice_seleccionado()
        if indice is None:
            messagebox.showwarning("Sin selección", "Selecciona un juego de la tabla para eliminarlo.")
            return

        titulo = self.catalogo.obtener(indice).titulo
        if not messagebox.askyesno("Confirmar", f"¿Eliminar \"{titulo}\" del catálogo?"):
            return

        self.catalogo.eliminar(indice)
        self.refrescar_tabla()

    def editar(self):
        """Funciona en dos pasos con el mismo botón:
        1er clic: carga en el formulario el juego seleccionado en la tabla.
        2do clic: guarda los datos modificados del formulario.
        """
        if self.editando:
            self._guardar_edicion()
        else:
            self._iniciar_edicion()

    def _iniciar_edicion(self):
        indice = self.tabla.indice_seleccionado()
        if indice is None:
            messagebox.showwarning("Sin selección", "Selecciona un juego de la tabla para editarlo.")
            return

        self.formulario.mostrar_juego(self.catalogo.obtener(indice))
        self.indice_en_edicion = indice
        if self.botonera:
            self.botonera.modo_edicion(True)

    def _guardar_edicion(self):
        juego = self.formulario.obtener_juego()
        if juego is None:
            messagebox.showwarning("Título vacío", "El título no puede quedar vacío.")
            return

        self.catalogo.editar(self.indice_en_edicion, juego)
        self.indice_en_edicion = None
        if self.botonera:
            self.botonera.modo_edicion(False)
        self.formulario.limpiar()
        self.refrescar_tabla()
