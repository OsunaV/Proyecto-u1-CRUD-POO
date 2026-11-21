#Catalogo de videojuegos
"""Modelo de datos: la clase Videojuego y la clase Catalogo que lo guarda en juegos.json."""
import json


class Videojuego:
    """Representa un juego del catálogo."""

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
        "Otro",
    ]

    PLATAFORMAS = [
        "PC",
        "PlayStation 5",
        "PlayStation 4",
        "Xbox Series X/S",
        "Xbox One",
        "Nintendo Switch",
        "Móvil (Android / iOS)",
        "Multiplataforma",
        "Retro / Emulador",
        "Otra",
    ]

    ESTADOS = [
        "Pendiente",
        "Jugando",
        "En pausa",
        "Completado",
        "100% / Platino",
        "Abandonado",
        "Rejugando",
    ]

    def __init__(self, titulo, genero, plataforma, estado):
        self.titulo = titulo
        self.genero = genero
        self.plataforma = plataforma
        self.estado = estado

    def a_diccionario(self):
        """Convierte el juego en un diccionario para guardarlo en el JSON."""
        return {
            "titulo": self.titulo,
            "genero": self.genero,
            "plataforma": self.plataforma,
            "estado": self.estado,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Crea un Videojuego a partir de un diccionario leído del JSON."""
        return cls(datos["titulo"], datos["genero"], datos["plataforma"], datos["estado"])

    def como_fila(self):
        """Devuelve los valores en el orden de las columnas de la tabla."""
        return (self.titulo, self.genero, self.plataforma, self.estado)

    def __repr__(self):
        return f"Videojuego({self.titulo!r}, {self.genero!r}, {self.plataforma!r}, {self.estado!r})"


class Catalogo:
    """Lista de videojuegos que se conserva en un archivo JSON."""

    def __init__(self, archivo="juegos.json"):
        self.archivo = archivo
        self.juegos = self._leer_archivo()

    # ---------- Lectura y escritura del archivo ----------

    def _leer_archivo(self):
        """Devuelve la lista de juegos guardada. Si el archivo no existe, devuelve una lista vacía."""
        try:
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                return [Videojuego.desde_diccionario(d) for d in json.load(archivo)]
        except FileNotFoundError:
            return []

    def _guardar_archivo(self):
        with open(self.archivo, "w", encoding="utf-8") as archivo:
            json.dump([j.a_diccionario() for j in self.juegos], archivo, indent=4, ensure_ascii=False)

    # ---------- Operaciones CRUD ----------

    def listar(self):
        return list(self.juegos)

    def obtener(self, indice):
        return self.juegos[indice]

    def agregar(self, juego):
        """Agrega un juego al catálogo sin borrar los anteriores."""
        self.juegos.append(juego)
        self._guardar_archivo()

    def editar(self, indice, juego):
        """Reemplaza el juego que está en la posición `indice`."""
        if 0 <= indice < len(self.juegos):
            self.juegos[indice] = juego
            self._guardar_archivo()

    def eliminar(self, indice):
        """Elimina el juego que está en la posición `indice`."""
        if 0 <= indice < len(self.juegos):
            self.juegos.pop(indice)
            self._guardar_archivo()

    def __len__(self):
        return len(self.juegos)
