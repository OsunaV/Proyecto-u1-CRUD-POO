# Catálogo de Videojuegos

Aplicación de escritorio hecha en Python con Tkinter para llevar un catálogo personal de
videojuegos. Permite registrar un juego con su título, género, plataforma y estado, verlo en
una tabla y eliminarlo. Los datos se guardan en un archivo JSON, así que el catálogo se
conserva entre ejecuciones.

---

## Requisitos

- **Python 3.10 o superior.** El proyecto se desarrolló con Python 3.13.
- **Tkinter**, que viene incluido con la instalación estándar de Python en Windows y macOS.
  En Linux puede ser necesario instalarlo aparte (ver más abajo).

No se necesita instalar ninguna librería adicional con `pip`.

### Comprobar que Python está instalado

Abra una terminal (en Windows: *Símbolo del sistema* o *PowerShell*) y escriba:

```
python --version
```

Debe mostrar algo como `Python 3.13.0`. Si aparece un error, descargue Python desde
<https://www.python.org/downloads/> y, durante la instalación en Windows, marque la casilla
**"Add Python to PATH"**.

### Comprobar que Tkinter está disponible

```
python -m tkinter
```

Si se abre una ventana pequeña de prueba, todo está listo. Si da error en Linux, instale
Tkinter con:

```
sudo apt install python3-tk
```

---

## Cómo ejecutar el programa

1. Descargue o clone el proyecto y abra una terminal **dentro de la carpeta del proyecto**
   (la que contiene `main.py`).

   Si lo descargó de GitHub:

   ```
   git clone https://github.com/OsunaV/Proyecto-u1-CRUD-con-diccionarios.git
   cd Proyecto-u1-CRUD-con-diccionarios
   ```

2. Ejecute el archivo principal:

   ```
   python main.py
   ```

   En algunos sistemas el comando es `python3 main.py` o `py main.py`.

3. Se abrirá la ventana de la aplicación.

> **Importante:** el programa debe ejecutarse desde la carpeta del proyecto, porque el
> archivo `juegos.json` se busca en la carpeta actual. Si se ejecuta desde otra ubicación,
> se creará un catálogo nuevo y vacío en esa otra carpeta.

También puede abrir la carpeta en **Visual Studio Code**, abrir `main.py` y pulsar el botón
de ejecutar (triángulo verde en la esquina superior derecha).

---

## Cómo usar la aplicación

La ventana tiene dos secciones:

**Nuevo Videojuego** (parte superior)

1. Escriba el título del juego en el campo *Título*.
2. Elija el *Género*, la *Plataforma* y el *Estado* en las listas desplegables.
3. Pulse **Agregar Juego**. El juego aparece en la tabla y el formulario se limpia.
   Si el título está vacío, no se guarda nada.

**Catálogo** (parte inferior)

- Muestra todos los juegos guardados en `juegos.json`.
- Para borrar uno, haga clic sobre su fila y pulse **Eliminar**. El programa pedirá
  confirmación antes de borrarlo.
- Si pulsa **Eliminar** sin seleccionar nada, aparecerá un aviso.

**Editar un juego**

1. Haga clic sobre la fila del juego en la tabla y pulse **Editar**.
2. Los datos del juego aparecen en el formulario y el botón cambia a **Guardar Cambios**.
3. Modifique lo que necesite y pulse **Guardar Cambios**. La tabla se actualiza y el
   botón vuelve a decir **Editar**.

Mientras se edita un juego, el botón **Eliminar** queda bloqueado hasta guardar los cambios.

Los cambios se guardan automáticamente en el archivo al agregar, editar o eliminar.

---

## Estructura del proyecto

| Archivo | Descripción |
|---------|-------------|
| `main.py` | Punto de entrada. Construye la ventana, el formulario, los botones y la tabla. |
| `acciones.py` | Funciones que responden a los botones: agregar, editar, eliminar, limpiar formulario y refrescar la tabla. |
| `datos.py` | Listas de géneros, plataformas y estados, y las funciones que leen y escriben `juegos.json`. |
| `juegos.json` | Archivo donde se guarda el catálogo. Se crea solo si no existe. |
| `correciones/` | Documentos en Markdown con el registro de errores corregidos y funcionalidades agregadas. |

---

## Problemas comunes

| Mensaje o síntoma | Causa y solución |
|-------------------|------------------|
| `python no se reconoce como un comando` | Python no está en el PATH. Reinstale marcando "Add Python to PATH" o use `py main.py`. |
| `ModuleNotFoundError: No module named 'tkinter'` | Falta Tkinter. En Linux: `sudo apt install python3-tk`. En Windows, reinstale Python con la opción *tcl/tk* marcada. |
| `ModuleNotFoundError: No module named 'datos'` | La terminal no está en la carpeta del proyecto. Entre a la carpeta con `cd` y vuelva a ejecutar. |
| La tabla aparece vacía | Es normal la primera vez. Agregue un juego y aparecerá. Si ya tenía juegos, revise que esté ejecutando desde la carpeta correcta. |
