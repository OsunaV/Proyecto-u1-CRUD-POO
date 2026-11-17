#Catalogo de videojuegos
import json

def Generos():
    GENEROS = [
    "Acción",
    "Aventura",
    "RPG / Rol",
    "Shooter (FPS/TPS)",
    "Estrategia",
    "Simulación",
    "Deportes",
    "Carreras",
    "Plataformas",
    "Terror / Survival",
    "Puzles",
    "Lucha / Peleas",
    "MOBA",
    "Sandbox / Mundo Abierto",
    "Indie",
    "Otro"
    ]
    return GENEROS

def Plataforma():
    PLATAFORMA =[
    "PC",
    "PlayStation 5",
    "PlayStation 4",
    "Xbox Series X/S",
    "Xbox One",
    "Nintendo Switch",
    "Móvil (Android / iOS)",
    "Multiplataforma",
    "Retro / Emulador",
    "Otra"
    ]
    return PLATAFORMA

def Estado ():
    ESTADO = [
    "Pendiente",
    "Jugando",
    "En pausa",
    "Completado",
    "100% / Platino",
    "Abandonado",
    "Rejugando"
    ]
    return ESTADO

ARCHIVO = "juegos.json"


def leer_archivo():
    """Devuelve la lista de juegos guardada. Si el archivo no existe, devuelve una lista vacía."""
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []


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


def eliminar_juego(indice):
    """Elimina el juego que está en la posición `indice` de la lista y reescribe el archivo."""
    juegos = leer_archivo()
    if 0 <= indice < len(juegos):
        juegos.pop(indice)
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(juegos, archivo, indent=4, ensure_ascii=False)


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
