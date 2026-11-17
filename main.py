import tkinter as tk
from tkinter import ttk
import datos as dt
import acciones



root = tk.Tk()

# Configuracion
root.title("Biblioteca de videojuegos")
root.geometry("750x600")
root.config()


#LabelFrame principal: Formulario de registro

# Paleta de colores del formulario (mismos tonos que los botones)
COLOR_FONDO_FORM = "#FFFFFF"     # fondo blanco del formulario
COLOR_TITULO_FORM = "#1565C0"    # azul del título "Nuevo Videojuego"
COLOR_TEXTO = "#37474F"          # gris oscuro para las etiquetas
COLOR_CAMPO = "#F5F7FA"          # fondo gris muy claro del campo de texto
COLOR_BORDE = "#B0BEC5"          # borde del campo sin foco
COLOR_BORDE_FOCO = "#1565C0"     # borde del campo cuando se está escribiendo

FUENTE_TITULO_FORM = ("Segoe UI", 12, "bold")
FUENTE_ETIQUETA = ("Segoe UI", 10, "bold")
FUENTE_CAMPO = ("Segoe UI", 10)

Labelframe_titulo = tk.LabelFrame(root,
    text="  Nuevo Videojuego  ",   # los espacios separan el título de la línea del borde
    font=FUENTE_TITULO_FORM,
    fg=COLOR_TITULO_FORM,
    bg=COLOR_FONDO_FORM,
    relief="groove",   # borde gris suave en relieve
    bd=2,
    padx=25,
    pady=12)
Labelframe_titulo.pack(fill="x", padx=15, pady=(12, 6))

# La columna 1 (los campos) se estira; la columna 0 (las etiquetas) no
Labelframe_titulo.columnconfigure(1, weight=1)

# Estilo común de las etiquetas
estilo_etiqueta = {
    "bg": COLOR_FONDO_FORM,
    "fg": COLOR_TEXTO,
    "font": FUENTE_ETIQUETA,
    "anchor": "w",
}

# Estilo común del acomodo en la cuadrícula
grid_etiqueta = {"column": 0, "sticky": "w", "padx": (0, 15), "pady": 6}
grid_campo = {"column": 1, "sticky": "ew", "pady": 6, "ipady": 3}

#Labels dentro del LabelFrame
label_juego_titulo = tk.Label(Labelframe_titulo, text="Título:", **estilo_etiqueta)
label_juego_titulo.grid(row=0, **grid_etiqueta)

label_juego_genero = tk.Label(Labelframe_titulo, text="Género:", **estilo_etiqueta)
label_juego_genero.grid(row=1, **grid_etiqueta)

label_juego_plataforma = tk.Label(Labelframe_titulo, text="Plataforma:", **estilo_etiqueta)
label_juego_plataforma.grid(row=2, **grid_etiqueta)

label_juego_estado = tk.Label(Labelframe_titulo, text="Estado:", **estilo_etiqueta)
label_juego_estado.grid(row=3, **grid_etiqueta)

#Campos del formulario
entry_juego_titulo = tk.Entry(Labelframe_titulo,
    font=FUENTE_CAMPO,
    fg=COLOR_TEXTO,
    bg=COLOR_CAMPO,
    relief="flat",
    highlightthickness=1,                  # grosor del borde
    highlightbackground=COLOR_BORDE,       # color del borde sin foco
    highlightcolor=COLOR_BORDE_FOCO,       # color del borde al escribir
    insertbackground=COLOR_TITULO_FORM)    # color del cursor
entry_juego_titulo.grid(row=0, **grid_campo)

# Estilo de los Combobox (son widgets ttk, se configuran con ttk.Style)
estilo_ttk = ttk.Style()
estilo_ttk.configure("Formulario.TCombobox", padding=4, foreground=COLOR_TEXTO)
# Fuente de la lista desplegable que aparece al abrir el Combobox
root.option_add("*TCombobox*Listbox.font", FUENTE_CAMPO)

estilo_combo = {
    "state": "readonly",
    "style": "Formulario.TCombobox",
    "font": FUENTE_CAMPO,
}

entry_juego_genero = ttk.Combobox(Labelframe_titulo, values=dt.Generos(), **estilo_combo)
entry_juego_genero.current(0)
entry_juego_genero.grid(row=1, **grid_campo)

entry_juego_plataforma = ttk.Combobox(Labelframe_titulo, values=dt.Plataforma(), **estilo_combo)
entry_juego_plataforma.current(0)
entry_juego_plataforma.grid(row=2, **grid_campo)

entry_juego_estado = ttk.Combobox(Labelframe_titulo, values=dt.Estado(), **estilo_combo)
entry_juego_estado.current(0)
entry_juego_estado.grid(row=3, **grid_campo)


estilo_boton = {
    "fg": "#FFFFFF",
    "activeforeground": "#FFFFFF",
    "font": ("Segoe UI", 10, "bold"),
    "padx": 15,
    "pady": 6,
    "relief": "flat",
    "bd": 0,
    "cursor": "hand2",
    "width": 16  # Mantiene ambos botones exactamente del mismo ancho
}


frame_botonera = tk.Frame()
frame_botonera.pack()

boton_agregar = tk.Button(frame_botonera,
    text="Agregar Juego",
    bg="#2E7D32",
    activebackground="#1B5E20",
    command=lambda: acciones.agregar_juego(entry_juego_titulo, entry_juego_genero,
                                           entry_juego_plataforma, entry_juego_estado,
                                           tabla_juegos),
    **estilo_boton)
boton_agregar.pack(side="left", padx=8)

boton_editar = tk.Button(frame_botonera,
    text="Editar",
    bg="#1565C0",
    activebackground="#0D47A1",
    command=lambda: acciones.editar_seleccionado(tabla_juegos, entry_juego_titulo, entry_juego_genero,
                                                 entry_juego_plataforma, entry_juego_estado,
                                                 boton_editar),
    **estilo_boton)
boton_editar.pack(side="left", padx=8)

boton_eliminar = tk.Button(frame_botonera,
    text="Eliminar",
    bg="#C62828",
    activebackground="#8E0000",
    command=lambda: acciones.eliminar_seleccionado(tabla_juegos),
    **estilo_boton)
boton_eliminar.pack(side="left", padx=8)


#LabelFrame de la tabla: Catálogo de juegos guardados

Labelframe_tabla = tk.LabelFrame(root, text="Catálogo")
Labelframe_tabla.pack(fill="both", expand=True, padx=10, pady=10)

columnas = ("titulo", "genero", "plataforma", "estado")
tabla_juegos = ttk.Treeview(Labelframe_tabla, columns=columnas, show="headings", height=10)

# Encabezados y ancho de cada columna
tabla_juegos.heading("titulo", text="Título")
tabla_juegos.heading("genero", text="Género")
tabla_juegos.heading("plataforma", text="Plataforma")
tabla_juegos.heading("estado", text="Estado")

tabla_juegos.column("titulo", width=200)
tabla_juegos.column("genero", width=150)
tabla_juegos.column("plataforma", width=150)
tabla_juegos.column("estado", width=120)

# Barra de desplazamiento vertical
scroll_tabla = ttk.Scrollbar(Labelframe_tabla, orient="vertical", command=tabla_juegos.yview)
tabla_juegos.configure(yscrollcommand=scroll_tabla.set)

tabla_juegos.pack(side="left", fill="both", expand=True)
scroll_tabla.pack(side="right", fill="y")

# Cargar lo que ya existe en juegos.json al abrir el programa
acciones.cargar_tabla(tabla_juegos)

root.mainloop()
