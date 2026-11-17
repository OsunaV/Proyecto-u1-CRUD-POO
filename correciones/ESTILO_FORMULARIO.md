# Estilo del formulario principal

Fecha: 17 de noviembre de 2026
Archivo modificado: `main.py`

Este documento continúa a `BOTON_EDITAR.md`. Describe el nuevo estilo visual del
`LabelFrame` "Nuevo Videojuego" y de todos los elementos que contiene: etiquetas, campo de
texto y listas desplegables. No cambia el funcionamiento del programa.

---

## Resumen

| Elemento | Antes | Después |
|----------|-------|---------|
| Recuadro | Gris del sistema, centrado y del ancho de su contenido | Fondo blanco, borde gris suave, ocupa todo el ancho con márgenes |
| Título "Nuevo Videojuego" | Texto normal negro | Azul `#1565C0`, negrita, tamaño 12 |
| Etiquetas | Texto normal, centradas | Gris oscuro, negrita, alineadas a la izquierda |
| Campo Título | Blanco con borde hundido | Fondo gris claro, borde fino que se pone azul al escribir |
| Listas desplegables | Fuente y tamaño por defecto | Fuente Segoe UI 10, más relleno, mismo ancho que el campo de texto |
| Ventana | 750x500 | 750x600, para que la tabla no quede corta |

Se usó la fuente **Segoe UI** y el azul del botón **Editar** para que el formulario combine
con la botonera, que ya tenía ese estilo.

---

## 1. Constantes de color y fuente

Al inicio de la sección se definen todos los colores y fuentes una sola vez. Para cambiar un
tono en todo el formulario basta con modificar una línea.

```python
COLOR_FONDO_FORM = "#FFFFFF"     # fondo blanco del formulario
COLOR_TITULO_FORM = "#1565C0"    # azul del título "Nuevo Videojuego"
COLOR_TEXTO = "#37474F"          # gris oscuro para las etiquetas
COLOR_CAMPO = "#F5F7FA"          # fondo gris muy claro del campo de texto
COLOR_BORDE = "#B0BEC5"          # borde del campo sin foco
COLOR_BORDE_FOCO = "#1565C0"     # borde del campo cuando se está escribiendo

FUENTE_TITULO_FORM = ("Segoe UI", 12, "bold")
FUENTE_ETIQUETA = ("Segoe UI", 10, "bold")
FUENTE_CAMPO = ("Segoe UI", 10)
```

Los nombres van en mayúsculas porque en Python es la convención para valores que no se
modifican durante la ejecución.

---

## 2. El `LabelFrame`

```python
Labelframe_titulo = tk.LabelFrame(root,
    text="  Nuevo Videojuego  ",
    font=FUENTE_TITULO_FORM,
    fg=COLOR_TITULO_FORM,
    bg=COLOR_FONDO_FORM,
    relief="groove",
    bd=2,
    padx=25,
    pady=12)
Labelframe_titulo.pack(fill="x", padx=15, pady=(12, 6))

Labelframe_titulo.columnconfigure(1, weight=1)
```

- **`fg` y `font`** cambian el color y la fuente del título del recuadro.
- **Los espacios en `text`** separan el título de la línea del borde para que no se vea pegado.
- **`relief="groove"`** dibuja un borde gris en relieve. Primero se probó `relief="solid"`,
  pero el borde negro resultaba demasiado marcado.
- **`padx` y `pady` del `LabelFrame`** son el espacio interior entre el borde y los campos.
- **`fill="x"` en `pack`** hace que el recuadro ocupe todo el ancho de la ventana. Los
  `padx` y `pady` de `pack` son el margen exterior. `pady=(12, 6)` pone 12 píxeles arriba
  y 6 abajo.
- **`columnconfigure(1, weight=1)`** indica que la columna 1 de la cuadrícula, donde están
  los campos, absorbe el espacio sobrante. La columna 0, la de las etiquetas, conserva su
  ancho mínimo.

---

## 3. Etiquetas

Las cuatro etiquetas comparten el mismo estilo, así que se agrupó en un diccionario que se
desempaqueta con `**`, igual que `estilo_boton`:

```python
estilo_etiqueta = {
    "bg": COLOR_FONDO_FORM,
    "fg": COLOR_TEXTO,
    "font": FUENTE_ETIQUETA,
    "anchor": "w",
}

grid_etiqueta = {"column": 0, "sticky": "w", "padx": (0, 15), "pady": 6}
grid_campo = {"column": 1, "sticky": "ew", "pady": 6, "ipady": 3}

label_juego_titulo = tk.Label(Labelframe_titulo, text="Título:", **estilo_etiqueta)
label_juego_titulo.grid(row=0, **grid_etiqueta)
```

- **`bg=COLOR_FONDO_FORM`** es necesario porque cada `Label` tiene su propio fondo. Sin
  él, las etiquetas se verían como rectángulos grises sobre el recuadro blanco.
- **`sticky="w"`** pega la etiqueta al lado izquierdo (*west*) de su celda.
- **`sticky="ew"`** en los campos los estira de izquierda a derecha, por eso todos tienen el
  mismo ancho.
- **`ipady=3`** agrega relleno interior arriba y abajo, para que los campos sean más altos.
- **`grid_etiqueta` y `grid_campo`** agrupan las opciones de acomodo, de modo que en cada
  línea solo cambia el número de fila.

También se renumeraron las filas de 0 a 3. Antes empezaban en 2, sin filas 0 y 1.

---

## 4. Campo de texto del título

```python
entry_juego_titulo = tk.Entry(Labelframe_titulo,
    font=FUENTE_CAMPO,
    fg=COLOR_TEXTO,
    bg=COLOR_CAMPO,
    relief="flat",
    highlightthickness=1,
    highlightbackground=COLOR_BORDE,
    highlightcolor=COLOR_BORDE_FOCO,
    insertbackground=COLOR_TITULO_FORM)
```

- **`relief="flat"`** quita el borde hundido clásico de Windows.
- **`highlightthickness`** dibuja en su lugar un borde fino de 1 píxel.
- **`highlightbackground`** es el color del borde cuando el campo no tiene el foco, y
  **`highlightcolor`** cuando sí lo tiene. Así el borde se pone azul mientras el usuario
  escribe, lo que indica en qué campo está.
- **`insertbackground`** es el color del cursor de texto.

---

## 5. Listas desplegables (Combobox)

Los `Combobox` son widgets de `ttk`. A diferencia de los de `tk`, no aceptan colores
directamente: su apariencia se define con un estilo de `ttk.Style`.

```python
estilo_ttk = ttk.Style()
estilo_ttk.configure("Formulario.TCombobox", padding=4, foreground=COLOR_TEXTO)
root.option_add("*TCombobox*Listbox.font", FUENTE_CAMPO)

estilo_combo = {
    "state": "readonly",
    "style": "Formulario.TCombobox",
    "font": FUENTE_CAMPO,
}

entry_juego_genero = ttk.Combobox(Labelframe_titulo, values=dt.Generos(), **estilo_combo)
```

- **`"Formulario.TCombobox"`** es un estilo propio. El nombre debe terminar en
  `.TCombobox` para que `ttk` sepa que deriva del estilo base de los Combobox. Usar un
  estilo propio en lugar de modificar `"TCombobox"` evita afectar a otros Combobox que se
  agreguen después.
- **`padding=4`** agrega relleno interior al texto.
- **`option_add("*TCombobox*Listbox.font", ...)`** cambia la fuente de la lista que se
  despliega al abrir el Combobox. Esa lista es un widget aparte y no toma la fuente del
  Combobox.
- **El fondo blanco** de los Combobox es el del tema de Windows. El tema `vista`, que Tkinter
  usa por defecto en Windows, no permite cambiar ese color sin cambiar el tema de toda la
  aplicación. Eso también alteraría la tabla, así que se dejó el tema por defecto.

---

## 6. Otros cambios en `main.py`

- La ventana pasó de **750x500 a 750x600**. Con el formulario más alto, la tabla del catálogo
  se quedaba con poco espacio.
- La definición de `entry_juego_estado` se movió junto a los otros Combobox. Antes estaba
  después de `estilo_boton`, separada del resto del formulario.
- Los nombres de todas las variables se mantuvieron iguales, así que `acciones.py` no
  necesitó cambios.

---

## Verificación

- `main.py` compila sin errores.
- Se tomó una captura de la ventana para comprobar el estilo: todos los campos quedan
  alineados y con el mismo ancho, y el borde del campo Título se vuelve azul al escribir.
- Se repitieron las pruebas de funcionamiento con el nuevo formulario:

| Acción | Resultado |
|--------|-----------|
| Agregar "Celeste", género Indie | Aparece en la tabla |
| Editar el título a "Celeste B" | La tabla muestra el título nuevo |
| Eliminar el juego | La tabla queda vacía |
