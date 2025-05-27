import re
from typing import Set

# --- Stopwords en español e inglés ---
stopwords_es = {
    "el", "la", "los", "las", "de", "del", "a", "y", "o", "en", "con", "por", "para",
    "un", "una", "unos", "unas", "que", "se", "es", "su", "al"
}

stopwords_en = {
    "the", "and", "or", "in", "on", "for", "to", "a", "an", "of", "with", "is", "are",
    "was", "were", "be", "this", "that", "it", "as"
}

# Combinar todas las stopwords en un solo set
stopwords = stopwords_es | stopwords_en

# --- Funciones funcionales puras ---

def extraer_palabras(texto: str, stopwords: Set[str]) -> Set[str]:
    """
    Extrae palabras de un texto, las convierte a minúsculas, y filtra las stopwords.
    Es una función pura.
    """
    palabras = re.findall(r'\b\w+\b', texto.lower())
    return {p for p in palabras if p not in stopwords}

def calcular_coincidencias(palabras_desc: Set[str], palabras_cv: Set[str]) -> Set[str]:
    """
    Calcula la intersección (palabras coincidentes) entre dos conjuntos de palabras.
    Es una función pura.
    """
    return palabras_desc & palabras_cv

def cumple_umbral(coincidencias: Set[str], total: int, umbral: float) -> bool:
    """
    Verifica si el número de coincidencias cumple con un umbral porcentual dado.
    Es una función pura.
    """
    if total == 0: # Evitar división por cero si no hay keywords en la descripción
        return False
    return len(coincidencias) / total >= umbral