# US Airline Operations — Cómo ejecutar la aplicación (instrucciones en español)

Este repositorio contiene un dashboard interactivo construido con Streamlit. A continuación tienes pasos claros para ejecutar la aplicación en macOS (zsh).

Requisitos
- Python 3.8+ instalado
- Acceso a Internet (la app descarga tablas auxiliares: aeropuertos y lookup de aerolíneas)
- El fichero de datos `Airline_dataset.csv` colocado en la raíz del repositorio (mismo directorio que `app.py`).

Pasos rápidos
1. Abrir una terminal y situarse en la carpeta del proyecto:

```bash
cd /Users/milan/Documents/myUniDeb/LabDataVisualizations/Final_Project/GitHub_Files
```

2. (Recomendado) crear y activar un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Colocar el dataset:

- Asegúrate de que el archivo `Airline_dataset.csv` se encuentre en la carpeta del proyecto. Si no está, la app lanzará un FileNotFoundError indicando la ruta esperada.

5. Ejecutar la aplicación Streamlit:

```bash
streamlit run app.py
```

6. Abrir la URL que Streamlit muestre (por defecto http://localhost:8501) en tu navegador.

Notas y solución de problemas
- Si ves un error tipo FileNotFoundError: coloca el CSV en la raíz y revisa que se llame exactamente `Airline_dataset.csv`.
- La app usa Internet para descargar un lookup de aerolíneas y el dataset de aeropuertos. Si trabajas sin conexión, necesitarás proporcionar esos ficheros localmente y modificar `preprocess.py`.
- Si necesitas versiones concretas de librerías, prueba:

```bash
pip freeze > requirements.txt
```

Si quieres, puedo:
- Añadir instrucciones para descargar un dataset de ejemplo si el repositorio original lo tenía.
- Ejecutar una comprobación rápida en el entorno del workspace (si quieres que intente instalar/ejecutar aquí). 
