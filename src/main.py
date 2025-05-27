import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from concurrent.futures import ThreadPoolExecutor
from typing import Set
# Importar funciones y datos de los otros módulos
from utils import extraer_palabras, stopwords
from pdf_processor import procesar_pdf

# --- GUI y lógica principal ---

def seleccionar_carpeta():
    """Abre un cuadro de diálogo para que el usuario seleccione una carpeta."""
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_entry.delete(0, tk.END)
        carpeta_entry.insert(0, carpeta)

def mostrar_cv_resaltado(texto: str, coincidencias: Set[str], nombre: str):
    """
    Crea una nueva ventana para mostrar el texto de un CV con las palabras clave resaltadas.
    """
    ventana_cv = tk.Toplevel()
    ventana_cv.title(f"CV Coincidente - {nombre}")
    ventana_cv.geometry("800x600")

    text_frame = ttk.Frame(ventana_cv)
    text_frame.pack(expand=True, fill="both", padx=10, pady=10)

    texto_widget = tk.Text(text_frame, wrap="word", width=100, height=40, font=("Helvetica", 10))
    texto_widget.pack(side="left", expand=True, fill="both")

    scrollbar = ttk.Scrollbar(text_frame, command=texto_widget.yview)
    scrollbar.pack(side="right", fill="y")
    texto_widget.config(yscrollcommand=scrollbar.set)

    texto_widget.insert("1.0", texto)
    texto_widget.config(state="disabled") # Hacer el texto de solo lectura

    # Resaltar las palabras
    for palabra in coincidencias:
        inicio = "1.0"
        while True:
            inicio = texto_widget.search(palabra, inicio, stopindex="end", nocase=True)
            if not inicio:
                break
            fin = f"{inicio}+{len(palabra)}c"
            texto_widget.tag_add("coincidencia", inicio, fin)
            inicio = fin

    texto_widget.tag_config("coincidencia", background="#FFFF00", foreground="black") # Amarillo vibrante

def on_cv_select(event, listbox, results):
    """
    Callback para cuando un CV es seleccionado de la lista de resultados.
    Abre la ventana para mostrar el CV resaltado.
    """
    seleccion = listbox.curselection()
    if seleccion:
        indice = seleccion[0]
        # Asegurarse de que el índice es válido para evitar errores si la lista cambia.
        if 0 <= indice < len(results):
            archivo, coincidencias, texto_pdf = results[indice]
            mostrar_cv_resaltado(texto_pdf, coincidencias, archivo)

def filtrar_cvs():
    """
    Función principal que se ejecuta al presionar el botón "Filtrar CVs".
    Procesa los CVs, los filtra y los mueve.
    """
    descripcion = descripcion_text.get("1.0", tk.END).strip()
    carpeta = carpeta_entry.get()

    try:
        umbral = float(umbral_slider.get()) / 100.0 # Obtener valor del slider y convertir a flotante
    except ValueError:
        messagebox.showerror("Error de umbral", "El umbral de coincidencia debe ser un número válido.")
        return

    if not descripcion or not carpeta:
        messagebox.showwarning("Faltan datos", "Escribe una descripción y selecciona una carpeta.")
        return

    palabras_desc = extraer_palabras(descripcion, stopwords)

    if len(palabras_desc) == 0:
        messagebox.showwarning("Descripción vacía", "La descripción no contiene palabras clave válidas después de filtrar stopwords.")
        return

    # Mostrar mensaje de procesamiento
    status_label.config(text="Procesando CVs, por favor espera...", foreground="blue")
    ventana.update_idletasks() # Actualizar la GUI inmediatamente para mostrar el mensaje

    carpeta_filtrados = os.path.join(carpeta, "Filtrados_CVs")
    os.makedirs(carpeta_filtrados, exist_ok=True)

    archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(".pdf")]

    if not archivos:
        messagebox.showinfo("Sin PDFs", "No se encontraron archivos PDF en la carpeta seleccionada.")
        status_label.config(text="Listo", foreground="black")
        return

    resultados_coincidentes = []

    # Usar ThreadPoolExecutor para procesamiento concurrente
    with ThreadPoolExecutor() as executor:
        tareas = [executor.submit(procesar_pdf, archivo, carpeta, palabras_desc, umbral) for archivo in archivos]
        for i, tarea in enumerate(tareas):
            resultado = tarea.result() # Esperar a que la tarea termine y obtener su resultado
            if resultado:
                resultados_coincidentes.append(resultado)

            # Actualizar progreso en la barra de estado
            status_label.config(text=f"Procesando: {i+1}/{len(archivos)} PDFs")
            ventana.update_idletasks() # Forzar la actualización de la GUI

    movidos = 0
    if resultados_coincidentes:
        # Abrir una ventana para listar los CVs coincidentes
        ventana_resultados = tk.Toplevel()
        ventana_resultados.title("CVs Coincidentes")
        ventana_resultados.geometry("500x400")
        ventana_resultados.transient(ventana) # Hace que la ventana de resultados dependa de la principal

        ttk.Label(ventana_resultados, text="Haz clic para ver el CV resaltado:", font=("Helvetica", 10, "bold")).pack(pady=5)

        lista_cvs_frame = ttk.Frame(ventana_resultados)
        lista_cvs_frame.pack(expand=True, fill="both", padx=10, pady=5)

        lista_cvs = tk.Listbox(lista_cvs_frame, width=80, height=15, font=("Helvetica", 10))
        lista_cvs.pack(side="left", expand=True, fill="both")

        scrollbar_resultados = ttk.Scrollbar(lista_cvs_frame, command=lista_cvs.yview)
        scrollbar_resultados.pack(side="right", fill="y")
        lista_cvs.config(yscrollcommand=scrollbar_resultados.set)

        for i, (archivo, coincidencias, texto_pdf) in enumerate(resultados_coincidentes):
            lista_cvs.insert(tk.END, f"{archivo} (Coincidencias: {len(coincidencias)})")

            # Mover el archivo
            origen = os.path.join(carpeta, archivo)
            destino_base = os.path.join(carpeta_filtrados, archivo)

            # Manejo de nombres de archivo duplicados
            destino = destino_base
            contador = 1
            while os.path.exists(destino):
                nombre, ext = os.path.splitext(archivo)
                destino = os.path.join(carpeta_filtrados, f"{nombre}_{contador}{ext}")
                contador += 1

            try:
                shutil.move(origen, destino)
                movidos += 1
            except Exception as e:
                print(f"Error moviendo {origen} a {destino}: {e}")
                messagebox.showerror("Error al mover archivo", f"No se pudo mover {archivo}: {e}")

        # Vincular el evento de selección al Listbox solo después de llenarlo
        lista_cvs.bind("<<ListboxSelect>>",
                        lambda event: on_cv_select(event, lista_cvs, resultados_coincidentes))

        ttk.Button(ventana_resultados, text="Cerrar", command=ventana_resultados.destroy).pack(pady=10)
    else:
        messagebox.showinfo("Filtrado completo", "No se encontraron CVs que cumplan con el umbral.")

    status_label.config(text=f"Filtrado completo: Se movieron {movidos} CV(s) a '{os.path.basename(carpeta_filtrados)}'.", foreground="green")

# --- Interfaz gráfica ---

if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Filtro de CVs por Descripción de Trabajo")
    ventana.geometry("700x600")
    ventana.resizable(True, True)

    # Estilo para los widgets ttk
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Helvetica", 10), padding=6)
    style.configure("TLabel", font=("Helvetica", 10))
    style.configure("TEntry", font=("Helvetica", 10))
    style.configure("TScale", background=ventana.cget('bg'))

    # Frame principal para organizar los elementos
    main_frame = ttk.Frame(ventana, padding="20 20 20 20")
    main_frame.pack(expand=True, fill="both")

    # --- Descripción del trabajo ---
    ttk.Label(main_frame, text="1. Descripción del trabajo (palabras clave):").pack(anchor="w", pady=(0, 5))
    descripcion_text = tk.Text(main_frame, height=10, width=70, font=("Helvetica", 10), bd=1, relief="solid")
    descripcion_text.pack(fill="x", pady=(0, 10))

    # --- Carpeta de CVs ---
    ttk.Label(main_frame, text="2. Carpeta con los CVs (.pdf):").pack(anchor="w", pady=(0, 5))
    carpeta_frame = ttk.Frame(main_frame)
    carpeta_frame.pack(fill="x", pady=(0, 10))

    carpeta_entry = ttk.Entry(carpeta_frame, width=60)
    carpeta_entry.pack(side=tk.LEFT, expand=True, fill="x")
    ttk.Button(carpeta_frame, text="Seleccionar Carpeta", command=seleccionar_carpeta).pack(side=tk.LEFT, padx=(5,0))

    # --- Umbral de coincidencia ---
    ttk.Label(main_frame, text="3. Umbral de coincidencia (% de palabras clave):").pack(anchor="w", pady=(0, 5))
    umbral_frame = ttk.Frame(main_frame)
    umbral_frame.pack(fill="x", pady=(0, 10))

    umbral_label = ttk.Label(umbral_frame, text="40%")
    umbral_label.pack(side=tk.LEFT, padx=(10,0)) # Esto coloca el porcentaje a la derecha del slider inicialmente

    umbral_slider = ttk.Scale(umbral_frame, from_=10, to=100, orient="horizontal", command=lambda s: umbral_label.config(text=f"{int(float(s))}%"))
    umbral_slider.set(40) # Valor inicial del 40%
    umbral_slider.pack(side=tk.LEFT, expand=True, fill="x") # Esto coloca el slider a la izquierda

    # --- Botón de Filtrar ---
    filtrar_button = ttk.Button(main_frame, text="Filtrar CVs", command=filtrar_cvs, style="TButton")
    filtrar_button.pack(pady=20)

    # --- Barra de estado ---
    status_label = ttk.Label(main_frame, text="Listo", font=("Helvetica", 10, "italic"))
    status_label.pack(pady=(0, 10))

    ventana.mainloop()