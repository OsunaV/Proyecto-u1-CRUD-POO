import tkinter as tk
from tkinter import ttk
import datos as dt
import acciones



root = tk.Tk()

# Configuracion
root.title("Agenda")
root.geometry("700x500")
root.config()


#LabelFrame principal: Formulario de registro

Labelframe_titulo = tk.LabelFrame(root, text="Nuevo Videojuego") #LabelFrame en el que se encuentra el formulario
Labelframe_titulo.pack()
#Labels dentro del LabelFrame
label_juego_titulo = tk.Label(Labelframe_titulo, text="Título:") 
label_juego_titulo.grid(row= 2,column=0)

label_juego_genero = tk.Label(Labelframe_titulo, text="Género:") 
label_juego_genero.grid(row=3, column=0)

label_juego_plataforma = tk.Label(Labelframe_titulo, text="Plataforma:") 
label_juego_plataforma.grid(row=4, column=0)

label_juego_estado = tk.Label(Labelframe_titulo, text="Estado:")
label_juego_estado.grid(row=5, column=0)

#seccion 2 de la pantalla 
entry_juego_titulo = tk.Entry(Labelframe_titulo)        #Entry en el que se encuentran los botones
entry_juego_titulo.grid(row=2, column=1)

entry_juego_genero = ttk.Combobox(Labelframe_titulo, values= dt.Generos(), state="readonly", )
entry_juego_genero.current(0)
entry_juego_genero.grid(row=3, column=1)

entry_juego_plataforma = ttk.Combobox(Labelframe_titulo, values= dt.Plataforma(), state="readonly")
entry_juego_plataforma.current(0)
entry_juego_plataforma.grid(row=4, column=1)


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


entry_juego_estado = ttk.Combobox(Labelframe_titulo, values= dt.Estado(), state="readonly")
entry_juego_estado.current(0)
entry_juego_estado.grid(row=5, column= 1)

#

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
