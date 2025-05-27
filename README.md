<p align="center">
  <a href="https://github.com/AngelRysu/finalproject" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Filtro de CVs por Descripción de Trabajo</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/AngelRysu/finalproject)
[![GitHub Issues](https://img.shields.io/github/issues/AngelRysu/finalproject.svg)](https://github.com/AngelRysu/finalproject/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/AngelRysu/finalproject.svg)](https://github.com/AngelRysu/finalproject/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center">
  Una aplicación de escritorio para filtrar CVs en PDF basándose en una descripción de trabajo, utilizando concurrencia y principios de programación funcional.
    <br>
</p>

## 📝 Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Características Clave](#características-clave)
- [Cómo Empezar](#cómo-empezar)
  - [Requisitos](#requisitos)
  - [Clonar el Repositorio](#clonar-el-repositorio)
  - [Instalación](#instalación)
- [Ejecutar las Pruebas](#ejecutar-las-pruebas)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Construido Con](#construido-con)
- [Autores](#autores)
- [Agradecimientos](#agradecimientos)

## 🧐 Descripción del Proyecto <a name = "descripción-del-proyecto"></a>

Esta aplicación de escritorio, desarrollada en Python con `tkinter`, permite a los reclutadores y gerentes de contratación filtrar eficientemente archivos PDF de CVs. La herramienta compara el contenido de cada CV con una descripción de trabajo proporcionada por el usuario, identificando aquellos candidatos que cumplen con un umbral de coincidencia de palabras clave. Los CVs coincidentes se organizan automáticamente en una carpeta separada, y su contenido puede ser visualizado directamente en la aplicación, con las palabras clave relevantes resaltadas.

## ✨ Características Clave <a name = "características-clave"></a>

* **Programación Funcional**: Componentes centrales de la lógica (extracción de palabras, cálculo de coincidencias, y verificación de umbral) están implementados como funciones puras, lo que garantiza predictibilidad, facilita las pruebas y mejora la mantenibilidad del código.
* **Concurrencia**: Utiliza `ThreadPoolExecutor` para procesar múltiples archivos PDF de forma paralela. Esto mejora significativamente el rendimiento y la eficiencia, especialmente al manejar grandes volúmenes de CVs.
* **Interfaz Gráfica Intuitiva (GUI)**: Desarrollada con `tkinter` y estilizada con `ttk` para una experiencia de usuario moderna y agradable.
    * **Umbral Ajustable**: Permite al usuario definir el porcentaje de coincidencia de palabras clave requerido a través de un slider.
    * **Indicador de Progreso**: Proporciona retroalimentación en tiempo real sobre el estado del procesamiento de los CVs.
    * **Ventana de Resultados Consolidada**: Presenta los CVs coincidentes en una lista organizada, permitiendo al usuario abrir y revisar individualmente cada CV con las palabras clave resaltadas.
* **Gestión Automática de Archivos**: Los CVs que cumplen con el umbral se mueven automáticamente a una subcarpeta `Filtrados_CVs` para una mejor organización.

## 🚀 Cómo Empezar <a name = "cómo-empezar"></a>

Estas instrucciones te permitirán obtener una copia del proyecto y ejecutarlo en tu máquina local para fines de desarrollo y pruebas.

### Requisitos <a name = "requisitos"></a>

Asegúrate de tener instalado:

* **Python 3.6 o superior**
* Las dependencias listadas en `requirements.txt` (principalmente `pdfminer.six`).

### Clonar el Repositorio <a name = "clonar-el-repositorio"></a>

Para obtener una copia local del proyecto, clona el repositorio utilizando Git:

```bash
git clone [https://github.com/AngelRysu/finalproject.git](https://github.com/AngelRysu/finalproject.git)
cd finalproject
```
### Instalación <a name = "instalación"></a>

Sigue estos pasos para instalar las dependencias:

1.  **Navega al directorio raíz del proyecto** (donde se encuentran `src/` y `requirements.txt`).
    ```bash
    # Si ya estás en 'finalproject', no necesitas hacer nada.
    # De lo contrario: cd /ruta/a/finalproject
    ```

2.  **(Opcional pero recomendado) Crea un entorno virtual** para gestionar las dependencias del proyecto de forma aislada. Esto ayuda a evitar conflictos con otras instalaciones de Python:
    ```bash
    python3 -m venv env
    # En Windows: python -m venv env
    ```

3.  **Activa el entorno virtual**:
    * **macOS/Linux**:
        ```bash
        source env/bin/activate
        ```
    * **Windows (CMD)**:
        ```bash
        .\env\Scripts\activate
        ```
    * **Windows (PowerShell)**:
        ```powershell
        .\env\Scripts\Activate.ps1
        ```

4.  **Instala las dependencias** listadas en `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## 🔧 Ejecutar las Pruebas <a name = "ejecutar-las-pruebas"></a>

Para correr las pruebas unitarias, asegúrate de haber activado tu entorno virtual y de estar en el directorio raíz del proyecto (`finalproject`). Luego, ejecuta el siguiente comando:

```bash
python3 -m unittest discover tests
```
## 🎈 Uso <a name="uso"></a>

Una vez que hayas completado la instalación, puedes ejecutar la aplicación:

1.  Asegúrate de que el entorno virtual esté activado (ver paso 4 de "Instalación").
2.  Ejecuta la aplicación desde la terminal, navegando al directorio del proyecto y luego a `src/`:
    ```bash
    python3 src/main.py
    ```
    *(Si colocaste `main.py` directamente en la raíz del proyecto sin la carpeta `src`, el comando sería `python3 main.py`)*

3.  **Interfaz de Usuario:**
    * **1. Descripción del trabajo:** Ingresa el texto de la descripción del puesto para el que deseas filtrar los CVs. Sé lo más específico posible con las palabras clave.
    * **2. Carpeta con los CVs (.pdf):** Haz clic en el botón "Seleccionar Carpeta" para elegir el directorio que contiene todos los archivos PDF de los CVs que quieres procesar.
    * **3. Umbral de coincidencia (% de palabras clave):** Ajusta el slider para definir qué porcentaje de las palabras clave de tu descripción deben coincidir en un CV para que este sea considerado "aprobado".
    * **Filtrar CVs:** Haz clic en este botón para iniciar el proceso de filtrado.

4.  **Resultados:**
    * La aplicación mostrará el progreso en la barra de estado inferior.
    * Una vez finalizado, se abrirá una nueva ventana titulada "CVs Coincidentes" si se encontraron resultados.
    * Los CVs que cumplen con el umbral se moverán automáticamente a una subcarpeta llamada `Filtrados_CVs` dentro de la carpeta que seleccionaste originalmente.
    * En la ventana "CVs Coincidentes", haz clic en el nombre de cualquier CV de la lista para abrir una ventana individual que muestra el texto completo de ese CV, con las palabras clave coincidentes resaltadas en amarillo.

## 🏗️ Estructura del Proyecto <a name = "estructura-del-proyecto"></a>

El proyecto está organizado en varios módulos para una mejor separación de responsabilidades:

```bash
finalproject/
├── src/
│   ├── init.py       # Hace de 'src' un paquete Python.
│   ├── main.py           # Lógica principal de la GUI e interacción del usuario.
│   ├── pdf_processor.py  # Funciones para el procesamiento concurrente de PDFs.
│   └── utils.py          # Funciones auxiliares y puras (extracción de palabras, stopwords, etc.).
├── tests/
│   ├── test_utils.py     # Pruebas unitarias para las funciones de 'utils.py'.
│   └── test_pdf_processor.py # Pruebas unitarias para 'pdf_processor.py' (con mocking).
├── requirements.txt      # Lista de dependencias del proyecto.
└── README.md             # Este archivo.
```

## ⛏️ Construido Con <a name = "construido-con"></a>

* **Python**: Lenguaje de programación principal.
* **Tkinter**: Librería estándar de Python para la interfaz gráfica de usuario.
* **pdfminer.six**: Para la extracción de texto de archivos PDF.
* **`concurrent.futures.ThreadPoolExecutor`**: Para la implementación de concurrencia.
* **`unittest`**: Framework de pruebas unitarias de Python.

## ✍️ Autores <a name = "authors"></a>

* **Jesús Ángel Quezada Camacho** - [Tu perfil de GitHub](https://github.com/AngelRysu) - Desarrollador principal.

## 🎉 Agradecimientos <a name = "agradecimientos"></a>

* A la comunidad de Python y los desarrolladores de `pdfminer.six` por sus herramientas y recursos.
* [Añade cualquier otra persona o recurso que quieras agradecer]

---