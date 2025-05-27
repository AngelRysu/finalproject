import os
from typing import Set, Optional, Tuple
from pdfminer.high_level import extract_text

# Importar funciones y datos de utils.py
from .utils import extraer_palabras, calcular_coincidencias, cumple_umbral, stopwords

def procesar_pdf(archivo: str, carpeta: str, palabras_desc: Set[str], umbral: float) -> Optional[Tuple[str, Set[str], str]]:
    """
    Procesa un archivo PDF, extrae su texto y calcula coincidencias con las palabras clave.
    Retorna los datos del CV si cumple el umbral, None en caso contrario o error.
    Diseñada para ser ejecutada concurrentemente.
    """
    ruta_pdf = os.path.join(carpeta, archivo)
    try:
        texto_pdf = extract_text(ruta_pdf)
        palabras_pdf = extraer_palabras(texto_pdf, stopwords)
        coincidencias = calcular_coincidencias(palabras_desc, palabras_pdf)

        total_keywords = len(palabras_desc) # Se calcula aquí, ya que palabras_desc es constante

        if cumple_umbral(coincidencias, total_keywords, umbral):
            return archivo, coincidencias, texto_pdf
    except Exception as e:
        # En una aplicación real, aquí usarías un sistema de logging en lugar de print
        print(f"Error leyendo {archivo}: {e}")
    return None