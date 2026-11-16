# Correcciones al catálogo de videojuegos

Fecha: 15 de noviembre de 2026
Archivos modificados: `main.py`, `acciones.py`, `datos.py`, `juegos.json`

---

## Resumen

Al ejecutar `main.py` el programa fallaba con un `TypeError` antes de mostrar la ventana.
Además había una importación circular entre `main.py` y `acciones.py`, y la función de guardado
borraba el catálogo en cada uso. Se corrigieron seis problemas en total.

| # | Archivo | Problema | Tipo |
|---|---------|----------|------|
| 1 | main.py | Coma faltante antes de `**estilo_boton` | Error en ejecución |
| 2 | main.py | `command=funcion()` ejecuta la función al crear el botón | Error de lógica |
| 3 | main.py / acciones.py | Importación circular | Error de diseño |
| 4 | datos.py | `guardar_datos` sobrescribía el archivo | Error de lógica |
| 5 | datos.py | `abrir_archivo` leía y escribía archivos distintos | Error de lógica |
| 6 | varios | Imports y variables sin usar | Avisos de Pylance |

---

## 1. `TypeError: unsupported operand type(s) for ** or pow(): 'NoneType' and 'dict'`

**Archivo:** `main.py`, líneas 71-73

**Causa:** faltaba una coma entre el argumento `command=...` y `**estilo_boton`.
Sin la coma, Python no interpreta `**` como "desempaquetar el diccionario", sino como el
operador de potencia. Como `guardar_datos` devuelve `None`, se intentaba calcular
`None ** estilo_boton`, lo cual no es válido.

Este error no lo detecta el compilador porque la sintaxis es correcta; solo aparece al ejecutar.

**Antes:**
```python
command=dt.guardar_datos(titulo=entry_juego_titulo.get(), genero=entry_juego_genero.get(),
                         plataforma=entry_juego_plataforma.get(), estado=entry_juego_estado.get())
**estilo_boton)
```

**Después:**
```python
command=lambda: acciones.agregar_juego(entry_juego_titulo, entry_juego_genero,
                                       entry_juego_plataforma, entry_juego_estado),
**estilo_boton)
```

---

## 2. El botón guardaba al arrancar el programa, no al hacer clic

**Archivo:** `main.py`, línea 71

**Causa:** `command=dt.guardar_datos(...)` lleva paréntesis, así que la función se llama
en el momento en que se construye el botón. Lo que recibe `command` es el valor devuelto
(`None`), por lo que el botón quedaba sin acción. Por eso `juegos.json` contenía un registro
con título vacío: se guardó al iniciar, antes de escribir nada.

**Solución:** usar `command=lambda: ...`. La `lambda` crea una función que se ejecuta
únicamente cuando el usuario hace clic, y permite pasar argumentos en ese momento.

**Regla general en Tkinter:**
- `command=funcion` (sin paréntesis) cuando no se necesitan argumentos.
- `command=lambda: funcion(argumentos)` cuando sí se necesitan.
- `command=funcion()` es un error: corre una sola vez al inicio.

---

## 3. Importación circular entre `main.py` y `acciones.py`

**Archivos:** `main.py` línea 4, `acciones.py` línea 3

**Causa:** `main` importaba `acciones` y `acciones` importaba `main`. Cuando se ejecuta
`main.py` como programa principal, Python lo registra con el nombre `__main__`. Al hacer
`import main` desde `acciones`, Python vuelve a ejecutar todo `main.py` como un módulo
distinto: se crearían dos ventanas y dos conjuntos de widgets.

En el traceback original se veía que el error ocurría dentro de esa segunda ejecución.

**Solución:** `acciones.py` ya no importa `main`. Sus funciones reciben los widgets como
parámetros, de modo que `acciones` no depende de `main`.

**`acciones.py` después:**
```python
import tkinter as tk
import datos as dt


def limpiar_formulario(entry_titulo, combo_genero, combo_plataforma, combo_estado):
    entry_titulo.delete(0, tk.END)
    combo_genero.current(0)
    combo_plataforma.current(0)
    combo_estado.current(0)
    entry_titulo.focus()


def agregar_juego(entry_titulo, combo_genero, combo_plataforma, combo_estado):
    """Se ejecuta al hacer clic en el botón: lee el formulario, guarda y limpia."""
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
```

Se agregó la función `agregar_juego`, que une los pasos de leer el formulario, guardar y
limpiar. También valida que el título no esté vacío.

---

## 4. `guardar_datos` borraba el catálogo en cada guardado

**Archivo:** `datos.py`, líneas 73-95

**Causa:** se abría el archivo con modo `"w"`, que vacía el archivo y escribe solo el juego
nuevo. Para acumular un catálogo hay que leer la lista existente, agregar el juego y volver a
escribir todo.

Además, el bloque `except FileNotFoundError` nunca se ejecutaba, porque el modo `"w"`
crea el archivo si no existe.

**Antes:**
```python
def guardar_datos(titulo, genero, plataforma, estado):
    datos = [{"titulo": titulo, "genero": genero, "plataforma": plataforma, "estado": estado}]
    try:
        with open("juegos.json", "w") as archivo:
            json.dump(datos, archivo)
    except FileNotFoundError:
        ...
```

**Después:**
```python
def guardar_datos(titulo, genero, plataforma, estado):
    """Agrega un juego al catálogo sin borrar los anteriores."""
    juegos = leer_archivo()
    juegos.append({
        "titulo": titulo,
        "genero": genero,
        "plataforma": plataforma,
        "estado": estado
    })
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(juegos, archivo, indent=4, ensure_ascii=False)
```

Se añadió `encoding="utf-8"` y `ensure_ascii=False` para que los acentos
(por ejemplo "Acción") se guarden legibles en el archivo en lugar de `Acci\u00f3n`.

---

## 5. `abrir_archivo` leía un archivo y escribía otro

**Archivo:** `datos.py`, líneas 52-70

**Causa:** intentaba leer `inventario.json` pero, si no existía, creaba `juegos.json`.
Además, cuando el archivo no existía la función no devolvía nada (`None`), lo que rompería
cualquier código que esperara una lista. La función `leer_archivo` existía pero solo tenía
`pass`.

**Solución:** se eliminó `abrir_archivo` y se implementó `leer_archivo`, que usa un solo
nombre de archivo definido en la constante `ARCHIVO` y siempre devuelve una lista.

```python
ARCHIVO = "juegos.json"


def leer_archivo():
    """Devuelve la lista de juegos guardada. Si el archivo no existe, devuelve una lista vacía."""
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []
```

---

## 6. Avisos de Pylance (no eran errores)

| Archivo | Aviso | Corrección |
|---------|-------|------------|
| main.py | `"acciones" is not accessed` | Ahora se usa en el `command` del botón |
| acciones.py | `"ttk" is not accessed` | Se eliminó el import |
| datos.py | `"archivo" is not accessed` | `leer_archivo` ya usa la variable |

Después de los cambios, el panel de problemas de VS Code quedó vacío.

---

## Otros cambios

- `juegos.json` se reinició a una lista vacía `[]`, porque el registro anterior con título
  vacío se había creado por el error del punto 2.

## Verificación

1. `python -m py_compile datos.py main.py acciones.py` compila sin errores.
2. `python main.py` abre la ventana sin excepciones.
3. Se simularon dos clics en "Agregar Juego" con títulos distintos: ambos quedaron en
   `juegos.json` y el formulario se limpió después de cada uno.
4. Un clic con el título vacío no guarda nada.
