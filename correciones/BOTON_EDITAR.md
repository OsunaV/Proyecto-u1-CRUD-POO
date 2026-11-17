# Botón Editar

Fecha: 17 de noviembre de 2026
Archivos modificados: `main.py`, `acciones.py`, `datos.py`, `README.md`

Este documento continúa a `TREEVIEW_Y_ELIMINAR.md`. Describe el botón **Editar**, que permite
modificar un juego que ya está guardado en `juegos.json`.

---

## Cómo funciona

El mismo botón trabaja en dos pasos:

| Clic | Qué hace | Texto del botón después |
|------|----------|-------------------------|
| Primero | Carga en el formulario el juego seleccionado en la tabla | Guardar Cambios |
| Segundo | Guarda en `juegos.json` los datos del formulario y refresca la tabla | Editar |

Para saber en qué paso está, el programa guarda la posición del juego que se edita en la
variable `indice_en_edicion`. Si vale `None`, no se está editando nada.

---

## 1. `datos.py`: `editar_juego`

```python
def editar_juego(indice, titulo, genero, plataforma, estado):
    """Reemplaza los datos del juego que está en la posición `indice` y reescribe el archivo."""
    juegos = leer_archivo()
    if 0 <= indice < len(juegos):
        juegos[indice] = {
            "titulo": titulo,
            "genero": genero,
            "plataforma": plataforma,
            "estado": estado
        }
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(juegos, archivo, indent=4, ensure_ascii=False)
```

Sigue el mismo patrón que `guardar_datos` y `eliminar_juego`: leer la lista completa,
modificarla y reescribir el archivo. En lugar de `append` o `pop`, aquí se reemplaza el
diccionario que está en la posición `indice`.

---

## 2. `acciones.py`: `editar_seleccionado`

Al inicio del archivo se agregó la variable que recuerda qué juego se está editando:

```python
indice_en_edicion = None
```

La función completa:

```python
def editar_seleccionado(tabla, entry_titulo, combo_genero, combo_plataforma, combo_estado, boton_editar):
    global indice_en_edicion

    # ---- Paso 1: cargar el juego seleccionado en el formulario ----
    if indice_en_edicion is None:
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un juego de la tabla para editarlo.")
            return

        indice = tabla.index(seleccion[0])
        juego = dt.leer_archivo()[indice]

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

    dt.editar_juego(indice_en_edicion, titulo=titulo, genero=combo_genero.get(),
                    plataforma=combo_plataforma.get(), estado=combo_estado.get())

    indice_en_edicion = None
    boton_editar.config(text="Editar")
    limpiar_formulario(entry_titulo, combo_genero, combo_plataforma, combo_estado)
    cargar_tabla(tabla)
```

Puntos a notar:

- **`global indice_en_edicion`** es necesario porque la función cambia el valor de una
  variable definida fuera de ella. Sin `global`, Python crearía una variable local nueva y
  el valor se perdería al terminar la función.
- **Los datos se leen del JSON, no de la tabla.** El Treeview convierte los valores que
  parecen números; un juego titulado "2048" llegaría como el entero `2048`. Leyendo
  `dt.leer_archivo()[indice]` se conservan los datos exactos.
- **`combo.set(valor)`** funciona aunque el Combobox esté en modo `readonly`. Ese modo solo
  impide que el usuario escriba, no que el código cambie el valor.
- **`boton_editar.config(text=...)`** cambia el texto del botón para que el usuario sepa en
  qué paso está.

### Protección en `eliminar_seleccionado`

Se agregó una comprobación al inicio de la función de eliminar:

```python
if indice_en_edicion is not None:
    messagebox.showwarning("Edición en curso", "Guarda los cambios del juego que estás editando antes de eliminar.")
    return
```

Si se borrara una fila mientras se edita otra, las posiciones de la lista se recorrerían y
`indice_en_edicion` apuntaría al juego equivocado. Bloquear la eliminación evita ese problema.

---

## 3. `main.py`: el botón

```python
boton_editar = tk.Button(frame_botonera,
    text="Editar",
    bg="#1565C0",
    activebackground="#0D47A1",
    command=lambda: acciones.editar_seleccionado(tabla_juegos, entry_juego_titulo, entry_juego_genero,
                                                 entry_juego_plataforma, entry_juego_estado,
                                                 boton_editar),
    **estilo_boton)
boton_editar.pack(side="left", padx=8)
```

- Se colocó entre "Agregar Juego" y "Eliminar", en color azul.
- Se pasa el propio `boton_editar` a la función para que pueda cambiar su texto. Dentro de la
  `lambda` esto funciona porque la variable se busca hasta el momento del clic, cuando el
  botón ya existe.
- La ventana pasó de 700x500 a 750x500 para que quepan los tres botones.

---

## 4. `README.md`

Se agregó la sección **Editar un juego** con los pasos de uso, y en la tabla de estructura
se añadió "editar" a la descripción de `acciones.py`.

---

## Verificación

Se simuló la aplicación con dos juegos en `juegos.json` (Zelda, Doom):

| Acción | Resultado |
|--------|-----------|
| Editar sin seleccionar | Aviso "Selecciona un juego de la tabla para editarlo." |
| Seleccionar Doom y pulsar Editar | El formulario muestra Doom, Shooter (FPS/TPS), Pendiente; el botón dice "Guardar Cambios" |
| Pulsar Eliminar durante la edición | Aviso y no se borra nada |
| Borrar el título y pulsar Guardar Cambios | Aviso "El título no puede quedar vacío." |
| Cambiar a "Doom Eternal", estado Completado, y guardar | Tabla y archivo actualizados; el botón vuelve a "Editar" y el formulario se limpia |
