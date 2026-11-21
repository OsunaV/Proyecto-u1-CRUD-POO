"""Vista: los widgets de la ventana (formulario, botonera y tabla)."""
import tkinter as tk
from tkinter import ttk

from datos import Videojuego


class Tema:
    """Paleta de colores y fuentes de la aplicación."""

    FONDO_FORM = "#FFFFFF"     # fondo blanco del formulario
    TITULO_FORM = "#1565C0"    # azul del título "Nuevo Videojuego"
    TEXTO = "#37474F"          # gris oscuro para las etiquetas
    CAMPO = "#F5F7FA"          # fondo gris muy claro del campo de texto
    BORDE = "#B0BEC5"          # borde del campo sin foco
    BORDE_FOCO = "#1565C0"     # borde del campo cuando se está escribiendo

    FUENTE_TITULO_FORM = ("Segoe UI", 12, "bold")
    FUENTE_ETIQUETA = ("Segoe UI", 10, "bold")
    FUENTE_CAMPO = ("Segoe UI", 10)
    FUENTE_BOTON = ("Segoe UI", 10, "bold")


class Formulario(tk.LabelFrame):
    """Formulario "Nuevo Videojuego" con el título y los tres Combobox."""

    def __init__(self, master):
        super().__init__(master,
            text="  Nuevo Videojuego  ",   # los espacios separan el título de la línea del borde
            font=Tema.FUENTE_TITULO_FORM,
            fg=Tema.TITULO_FORM,
            bg=Tema.FONDO_FORM,
            relief="groove",   # borde gris suave en relieve
            bd=2,
            padx=25,
            pady=12)

        # La columna 1 (los campos) se estira; la columna 0 (las etiquetas) no
        self.columnconfigure(1, weight=1)
        self._configurar_estilo_combobox()

        self.entry_titulo = self._crear_entry(fila=0, etiqueta="Título:")
        self.combo_genero = self._crear_combo(fila=1, etiqueta="Género:", valores=Videojuego.GENEROS)
        self.combo_plataforma = self._crear_combo(fila=2, etiqueta="Plataforma:", valores=Videojuego.PLATAFORMAS)
        self.combo_estado = self._crear_combo(fila=3, etiqueta="Estado:", valores=Videojuego.ESTADOS)

    # ---------- Construcción ----------

    def _configurar_estilo_combobox(self):
        # Los Combobox son widgets ttk, se configuran con ttk.Style
        estilo = ttk.Style()
        estilo.configure("Formulario.TCombobox", padding=4, foreground=Tema.TEXTO)
        # Fuente de la lista desplegable que aparece al abrir el Combobox
        self.option_add("*TCombobox*Listbox.font", Tema.FUENTE_CAMPO)

    def _crear_etiqueta(self, fila, texto):
        tk.Label(self, text=texto, bg=Tema.FONDO_FORM, fg=Tema.TEXTO,
                 font=Tema.FUENTE_ETIQUETA, anchor="w"
                 ).grid(row=fila, column=0, sticky="w", padx=(0, 15), pady=6)

    def _colocar_campo(self, widget, fila):
        widget.grid(row=fila, column=1, sticky="ew", pady=6, ipady=3)

    def _crear_entry(self, fila, etiqueta):
        self._crear_etiqueta(fila, etiqueta)
        entry = tk.Entry(self,
            font=Tema.FUENTE_CAMPO,
            fg=Tema.TEXTO,
            bg=Tema.CAMPO,
            relief="flat",
            highlightthickness=1,                  # grosor del borde
            highlightbackground=Tema.BORDE,        # color del borde sin foco
            highlightcolor=Tema.BORDE_FOCO,        # color del borde al escribir
            insertbackground=Tema.TITULO_FORM)     # color del cursor
        self._colocar_campo(entry, fila)
        return entry

    def _crear_combo(self, fila, etiqueta, valores):
        self._crear_etiqueta(fila, etiqueta)
        combo = ttk.Combobox(self, values=valores, state="readonly",
                             style="Formulario.TCombobox", font=Tema.FUENTE_CAMPO)
        combo.current(0)
        self._colocar_campo(combo, fila)
        return combo

    # ---------- Uso ----------

    def obtener_juego(self):
        """Devuelve un Videojuego con lo escrito en el formulario, o None si el título está vacío."""
        titulo = self.entry_titulo.get().strip()
        if not titulo:
            return None
        return Videojuego(titulo, self.combo_genero.get(),
                          self.combo_plataforma.get(), self.combo_estado.get())

    def mostrar_juego(self, juego):
        """Rellena el formulario con los datos de un juego."""
        self.limpiar()
        self.entry_titulo.insert(0, juego.titulo)
        self.combo_genero.set(juego.genero)
        self.combo_plataforma.set(juego.plataforma)
        self.combo_estado.set(juego.estado)

    def limpiar(self):
        # 1. Borra el texto desde el carácter 0 hasta el final
        self.entry_titulo.delete(0, tk.END)
        # 2. Regresa los Combobox a su primera opción por defecto
        for combo in (self.combo_genero, self.combo_plataforma, self.combo_estado):
            combo.current(0)
        # 3. Coloca el cursor de nuevo en el título para seguir escribiendo
        self.entry_titulo.focus()


class Botonera(tk.Frame):
    """Fila de botones: Agregar, Editar y Eliminar."""

    ESTILO_BOTON = {
        "fg": "#FFFFFF",
        "activeforeground": "#FFFFFF",
        "font": Tema.FUENTE_BOTON,
        "padx": 15,
        "pady": 6,
        "relief": "flat",
        "bd": 0,
        "cursor": "hand2",
        "width": 16,  # Mantiene todos los botones exactamente del mismo ancho
    }

    def __init__(self, master, al_agregar, al_editar, al_eliminar):
        super().__init__(master)
        self.boton_agregar = self._crear_boton("Agregar Juego", "#2E7D32", "#1B5E20", al_agregar)
        self.boton_editar = self._crear_boton("Editar", "#1565C0", "#0D47A1", al_editar)
        self.boton_eliminar = self._crear_boton("Eliminar", "#C62828", "#8E0000", al_eliminar)

    def _crear_boton(self, texto, color, color_activo, comando):
        boton = tk.Button(self, text=texto, bg=color, activebackground=color_activo,
                          command=comando, **self.ESTILO_BOTON)
        boton.pack(side="left", padx=8)
        return boton

    def modo_edicion(self, activo):
        """Cambia el texto del botón Editar según si se está editando un juego."""
        self.boton_editar.config(text="Guardar Cambios" if activo else "Editar")


class TablaJuegos(tk.LabelFrame):
    """Catálogo de juegos guardados mostrado en un Treeview con barra de desplazamiento."""

    COLUMNAS = {
        "titulo": ("Título", 200),
        "genero": ("Género", 150),
        "plataforma": ("Plataforma", 150),
        "estado": ("Estado", 120),
    }

    def __init__(self, master):
        super().__init__(master, text="Catálogo")

        self.tabla = ttk.Treeview(self, columns=tuple(self.COLUMNAS), show="headings", height=10)
        for columna, (encabezado, ancho) in self.COLUMNAS.items():
            self.tabla.heading(columna, text=encabezado)
            self.tabla.column(columna, width=ancho)

        # Barra de desplazamiento vertical
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def mostrar(self, juegos):
        """Vacía la tabla y la vuelve a llenar con la lista de juegos."""
        self.tabla.delete(*self.tabla.get_children())
        for juego in juegos:
            self.tabla.insert("", tk.END, values=juego.como_fila())

    def indice_seleccionado(self):
        """Posición de la fila seleccionada, o None si no hay selección.

        La posición en la tabla coincide con la del catálogo, porque `mostrar`
        inserta los juegos en el mismo orden.
        """
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        return self.tabla.index(seleccion[0])
