import tkinter as tk
from tkinter import messagebox
import datos as dt

# Posición (en juegos.json) del juego que se está editando.
# Vale None cuando no se está editando nada.
indice_en_edicion = None


def limpiar_formulario(entry_titulo, combo_genero, combo_plataforma, combo_estado):
    # 1. Borra el texto desde el carácter 0 hasta el final
    entry_titulo.delete(0, tk.END)

    # 2. Regresa los Combobox a su primera opción por defecto
    combo_genero.current(0)
    combo_plataforma.current(0)
    combo_estado.current(0)

    # 3. Coloca el cursor de nuevo en el título para seguir escribiendo
    entry_titulo.focus()


def cargar_tabla(tabla):
    """Vacía el Treeview y lo vuelve a llenar con todo lo que hay en juegos.json."""
    # 1. Borrar las filas que ya estaban en la tabla
    for fila in tabla.get_children():
        tabla.delete(fila)

    # 2. Insertar una fila por cada juego del archivo
    for juego in dt.leer_archivo():
        tabla.insert("", tk.END, values=(
            juego["titulo"],
            juego["genero"],
            juego["plataforma"],
            juego["estado"],
        ))


def agregar_juego(entry_titulo, combo_genero, combo_plataforma, combo_estado, tabla=None):
    """Se ejecuta al hacer clic en el botón: lee el formulario, guarda, limpia y refresca la tabla."""
    titulo = entry_titulo.get().strip()
    if not titulo:
        return  # no guardar juegos sin título

    dt.guardar_datos(
        titulo=titulo,
        genero=combo_genero.get(),
        plataforma=combo_plataforma.get(),
        estado=combo_estado.get(),
    )
    limpiar_formulario(entry_titulo, combo_genero, combo_plataforma, combo_estado)
    if tabla is not None:
        cargar_tabla(tabla)


def eliminar_seleccionado(tabla):
    """Borra de juegos.json el juego que está seleccionado en la tabla."""
    # 1. Ver qué fila está seleccionada. selection() devuelve una tupla de ids.
    if indice_en_edicion is not None:
        messagebox.showwarning("Edición en curso", "Guarda los cambios del juego que estás editando antes de eliminar.")
        return

    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Selecciona un juego de la tabla para eliminarlo.")
        return

    fila = seleccion[0]
    titulo = tabla.item(fila)["values"][0]

    # 2. Pedir confirmación antes de borrar
    if not messagebox.askyesno("Confirmar", f"¿Eliminar \"{titulo}\" del catálogo?"):
        return

    # 3. La posición de la fila en la tabla es la misma que en la lista del JSON,
    #    porque cargar_tabla inserta los juegos en el mismo orden del archivo.
    indice = tabla.index(fila)
    dt.eliminar_juego(indice)

    # 4. Refrescar la tabla para que desaparezca la fila
    cargar_tabla(tabla)


def editar_seleccionado(tabla, entry_titulo, combo_genero, combo_plataforma, combo_estado, boton_editar):
    """Funciona en dos pasos con el mismo botón:
    1er clic: carga en el formulario el juego seleccionado en la tabla.
    2do clic: guarda en juegos.json los datos modificados del formulario.
    """
    global indice_en_edicion

    # ---- Paso 1: cargar el juego seleccionado en el formulario ----
    if indice_en_edicion is None:
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un juego de la tabla para editarlo.")
            return

        indice = tabla.index(seleccion[0])
        juego = dt.leer_archivo()[indice]  # se lee del JSON para conservar los datos exactos

        limpiar_formulario(entry_titulo, combo_genero, combo_plataforma, combo_estado)
        entry_titulo.insert(0, juego["titulo"])
        combo_genero.set(juego["genero"])
        combo_plataforma.set(juego["plataforma"])
        combo_estado.set(juego["estado"])

        indice_en_edicion = indice
        boton_editar.config(text="Guardar Cambios")
        return

    # ---- Paso 2: guardar los cambios ----
    titulo = entry_titulo.get().strip()
    if not titulo:
        messagebox.showwarning("Título vacío", "El título no puede quedar vacío.")
        return

    dt.editar_juego(
        indice_en_edicion,
        titulo=titulo,
        genero=combo_genero.get(),
        plataforma=combo_plataforma.get(),
        estado=combo_estado.get(),
    )

    indice_en_edicion = None
    boton_editar.config(text="Editar")
    limpiar_formulario(entry_titulo, combo_genero, combo_plataforma, combo_estado)
    cargar_tabla(tabla)
