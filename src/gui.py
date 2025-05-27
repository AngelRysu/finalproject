import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from pdfminer.high_level import extract_text
from concurrent.futures import ThreadPoolExecutor
from typing import Set, Optional, Tuple

# --- Stopwords en español e inglés ---
stopwords_es = {
    "el", "la", "los", "las", "de", "del", "a", "y", "o", "en", "con", "por", "para",
    "un", "una", "unos", "unas", "que", "se", "es", "su", "al"
}

stopwords_en = {
    "the", "and", "or", "in", "on", "for", "to", "a", "an", "of", "with", "is", "are",
    "was", "were", "be", "this", "that", "it", "as"
}

stopwords = stopwords_es | stopwords_en

# --- Funciones funcionales puras ---

def extraer_palabras(texto: str, stopwords: Set[str]) -> Set[str]:
    """Extrae palabras filtrando stopwords."""
    palabras = re.findall(r'\b\w+\b', texto.lower())
    return {p for p in palabras if p not in stopwords}

def calcular_coincidencias(palabras_desc: Set[str], palabras_cv: Set[str]) -> Set[str]:
    return palabras_desc & palabras_cv

def cumple_umbral(coincidencias: Set[str], total: int, umbral: float) -> bool:
    return len(coincidencias) >= total * umbral

# --- Procesamiento concurrente ---

def procesar_pdf(archivo: str, carpeta: str, palabras_desc: Set[str], total_keywords: int) -> Optional[Tuple[str, Set[str], str]]:
    ruta_pdf = os.path.join(carpeta, archivo)
    try:
        texto_pdf = extract_text(ruta_pdf)
        palabras_pdf = extraer_palabras(texto_pdf, stopwords)
        coincidencias = calcular_coincidencias(palabras_desc, palabras_pdf)
        if cumple_umbral(coincidencias, total_keywords, 0.3):
            return archivo, coincidencias, texto_pdf
    except Exception as e:
        print(f"Error leyendo {archivo}: {e}")
    return None

# --- GUI y lógica principal ---

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_entry.delete(0, tk.END)
        carpeta_entry.insert(0, carpeta)

# Eliminada la función mostrar_cv_resaltado para no mostrar coincidencias

def filtrar_cvs():
    descripcion = descripcion_text.get("1.0", tk.END).strip()
    carpeta = carpeta_entry.get()

    if not descripcion or not carpeta:
        messagebox.showwarning("Faltan datos", "Escribe una descripción y selecciona una carpeta.")
        return

    palabras_desc = extraer_palabras(descripcion, stopwords)
    total_keywords = len(palabras_desc)

    if total_keywords == 0:
        messagebox.showwarning("Descripción vacía", "La descripción no contiene palabras clave válidas.")
        return

    carpeta_filtrados = os.path.join(carpeta, "Filtrados")
    os.makedirs(carpeta_filtrados, exist_ok=True)

    archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(".pdf")]

    resultados = []
    with ThreadPoolExecutor() as executor:
        tareas = [executor.submit(procesar_pdf, archivo, carpeta, palabras_desc, total_keywords) for archivo in archivos]
        for tarea in tareas:
            resultado = tarea.result()
            if resultado:
                resultados.append(resultado)

    movidos = 0
    for archivo, _, _ in resultados:  # Ignoramos coincidencias y texto para no mostrarlos
        origen = os.path.join(carpeta, archivo)
        destino = os.path.join(carpeta_filtrados, archivo)

        contador = 1
        while os.path.exists(destino):
            nombre, ext = os.path.splitext(archivo)
            destino = os.path.join(carpeta_filtrados, f"{nombre}_{contador}{ext}")
            contador += 1

        shutil.move(origen, destino)
        movidos += 1

    messagebox.showinfo("Filtrado completo", f"Se movieron {movidos} CV(s) a la carpeta 'Filtrados'.")

# --- Interfaz gráfica ---

ventana = tk.Tk()
ventana.title("Filtro de CVs por descripción de trabajo")

tk.Label(ventana, text="Descripción del trabajo:").pack(anchor="w", padx=10, pady=(10, 0))
descripcion_text = tk.Text(ventana, height=10, width=60)
descripcion_text.pack(padx=10)

tk.Label(ventana, text="Carpeta con los CVs (.pdf):").pack(anchor="w", padx=10, pady=(10, 0))
carpeta_frame = tk.Frame(ventana)
carpeta_frame.pack(padx=10, pady=(0, 10))

carpeta_entry = tk.Entry(carpeta_frame, width=50)
carpeta_entry.pack(side=tk.LEFT)
tk.Button(carpeta_frame, text="Seleccionar carpeta", command=seleccionar_carpeta).pack(side=tk.LEFT, padx=5)

tk.Button(ventana, text="Filtrar CVs", command=filtrar_cvs, bg="#4CAF50", fg="white").pack(pady=10)

ventana.mainloop()
