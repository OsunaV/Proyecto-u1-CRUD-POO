# Treeview del catálogo y botón Eliminar

Fecha: 16 de noviembre de 2026
Archivos modificados: `main.py`, `acciones.py`, `datos.py`

Este documento continúa a `CORRECCIONES.md`. Describe dos funcionalidades nuevas:

1. Una tabla (`ttk.Treeview`) que muestra todo lo guardado en `juegos.json`.
2. El botón "Eliminar", que borra de la tabla y del archivo el juego seleccionado.

---

## 1. Treeview que muestra el contenido de `juegos.json`

### `main.py`: la tabla

Se agregó un `LabelFrame` llamado "Catálogo" debajo de la botonera. Dentro va la tabla
y una barra de desplazamiento.

```python
Labelframe_tabla = tk.LabelFrame(root, text="Catálogo")
Labelframe_tabla.pack(fill="both", expand=True, padx=10, pady=10)

columnas = ("titulo", "genero", "plataforma", "estado")
tabla_juegos = ttk.Treeview(Labelframe_tabla, columns=columnas, show="headings", height=10)

tabla_juegos.heading("titulo", text="Título")
tabla_juegos.heading("genero", text="Género")
tabla_juegos.heading("plataforma", text="Plataforma")
tabla_juegos.heading("estado", text="Estado")

tabla_juegos.column("titulo", width=200)
tabla_juegos.column("genero", width=150)
tabla_juegos.column("plataforma", width=150)
tabla_juegos.column("estado", width=120)

scroll_tabla = ttk.Scrollbar(Labelframe_tabla, orient="vertical", command=tabla_juegos.yview)
tabla_juegos.configure(yscrollcommand=scroll_tabla.set)

tabla_juegos.pack(side="left", fill="both", expand=True)
scroll_tabla.pack(side="right", fill="y")

acciones.cargar_tabla(tabla_juegos)
```

Puntos a notar:

- `columns=columnas` define las columnas de datos. Cada nombre se usa después en
  `heading` (texto del encabezado) y `column` (ancho).
- `show="headings"` oculta la primera columna de árbol que el Treeview trae por defecto
  y que quedaría vacía.
- La `Scrollbar` se conecta en dos direcciones: ella mueve la tabla con `command=tabla.yview`
  y la tabla actualiza la barra con `yscrollcommand=scroll.set`.
- `acciones.cargar_tabla(tabla_juegos)` se llama antes de `mainloop` para que al abrir el
  programa ya aparezcan los juegos guardados.
- La ventana creció de 600x400 a 700x500 para que quepa la tabla.

### `acciones.py`: `cargar_tabla`

```python
def cargar_tabla(tabla):
    """Vacía el Treeview y lo vuelve a llenar con todo lo que hay en juegos.json."""
    for fila in tabla.get_children():
        tabla.delete(fila)

    for juego in dt.leer_archivo():
        tabla.insert("", tk.END, values=(
            juego["titulo"],
            juego["genero"],
            juego["plataforma"],
            juego["estado"],
        ))
```

Es la forma habitual de refrescar un Treeview: borrar todas las filas y volver a llenar
desde la fuente de datos. Así la tabla siempre coincide con el archivo y no hay que
llevar la cuenta de qué fila cambió.

- `tabla.get_children()` devuelve los ids de todas las filas.
- `tabla.insert("", tk.END, values=...)` inserta al final. El primer argumento `""` indica
  que la fila va en el nivel raíz, sin padre.

### `agregar_juego` refresca la tabla

La función recibió un parámetro opcional `tabla`. Después de guardar y limpiar el
formulario, llama a `cargar_tabla` para que el juego nuevo aparezca de inmediato.

```python
def agregar_juego(entry_titulo, combo_genero, combo_plataforma, combo_estado, tabla=None):
    ...
    limpiar_formulario(entry_titulo, combo_genero, combo_plataforma, combo_estado)
    if tabla is not None:
        cargar_tabla(tabla)
```

En `main.py` el botón "Agregar Juego" ahora pasa `tabla_juegos` como último argumento.

---

## 2. Botón "Eliminar"

### Problema que tenía

El botón existía pero su `command` llamaba a `limpiar_formulario`, así que solo limpiaba
el formulario y no borraba nada. Además la variable se llamaba `botom_eliminarseleccionado`
(con errata); se renombró a `boton_eliminar`.

### `datos.py`: `eliminar_juego`

```python
def eliminar_juego(indice):
    """Elimina el juego que está en la posición `indice` de la lista y reescribe el archivo."""
    juegos = leer_archivo()
    if 0 <= indice < len(juegos):
        juegos.pop(indice)
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(juegos, archivo, indent=4, ensure_ascii=False)
```

Sigue el mismo patrón que `guardar_datos`: leer la lista completa, modificarla y
reescribir el archivo. La comprobación `0 <= indice < len(juegos)` evita un
`IndexError` si el índice no es válido.

### `acciones.py`: `eliminar_seleccionado`

```python
from tkinter import messagebox

def eliminar_seleccionado(tabla):
    """Borra de juegos.json el juego que está seleccionado en la tabla."""
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Selecciona un juego de la tabla para eliminarlo.")
        return

    fila = seleccion[0]
    titulo = tabla.item(fila)["values"][0]

    if not messagebox.askyesno("Confirmar", f"¿Eliminar \"{titulo}\" del catálogo?"):
        return

    indice = tabla.index(fila)
    dt.eliminar_juego(indice)
    cargar_tabla(tabla)
```

Paso a paso:

1. `tabla.selection()` devuelve una tupla con los ids de las filas seleccionadas. Si está
   vacía, se muestra un aviso con `messagebox.showwarning` y se sale.
2. `tabla.item(fila)["values"]` da los valores de esa fila; el primero es el título, que
   se usa en el mensaje de confirmación.
3. `messagebox.askyesno` devuelve `True` si el usuario pulsa "Sí". Si pulsa "No", no se
   borra nada.
4. `tabla.index(fila)` devuelve la posición de la fila en la tabla. Como `cargar_tabla`
   inserta los juegos en el mismo orden en que están en el archivo, esa posición coincide
   con el índice en la lista del JSON. Por eso basta con pasarla a `dt.eliminar_juego`.
5. `cargar_tabla(tabla)` refresca la tabla para que la fila desaparezca.

### `main.py`: el botón

```python
boton_eliminar = tk.Button(frame_botonera,
    text="Eliminar",
    bg="#C62828",
    activebackground="#8E0000",
    command=lambda: acciones.eliminar_seleccionado(tabla_juegos),
    **estilo_boton)
boton_eliminar.pack(side="left", padx=8)
```

Igual que con "Agregar Juego", se usa `command=lambda:` para que la función se ejecute
al hacer clic y no al crear el botón.

---

## Verificación

Se simuló la aplicación con tres juegos en `juegos.json` (Zelda, Doom, Celeste):

| Acción | Resultado |
|--------|-----------|
| Abrir el programa | La tabla muestra las tres filas |
| Agregar un juego | Aparece como cuarta fila y el formulario se limpia |
| Clic en Eliminar sin seleccionar | Aviso "Selecciona un juego de la tabla para eliminarlo." y no se borra nada |
| Seleccionar Doom, Eliminar, responder "No" | Se mantienen las tres filas |
| Seleccionar Doom, Eliminar, responder "Sí" | Quedan Zelda y Celeste, tanto en la tabla como en `juegos.json` |

Los tres archivos compilan sin errores y VS Code no muestra avisos.
