# proyecto-prediccion-casas

# 🏡 Predicción de Precios de Casas - Sistema Inteligente Inmobiliario

Aplicación Fullstack orientada a Machine Learning desarrollada para el **Diplomado de Python Fullstack**. El proyecto tiene como objetivo resolver la incertidumbre en la valoración de inmuebles mediante la automatización de la recolección de datos del mercado y el despliegue de un modelo predictivo accesible desde una interfaz web intuitiva.

La solución fue construida siguiendo buenas prácticas de ingeniería de software, arquitectura modular, desacoplamiento de servicios y reproducibilidad total del entorno de desarrollo.

---

# 📖 Nombre y Descripción

El proyecto **Predicción de Precios de Casas** aborda la problemática de la fijación de precios en el mercado inmobiliario ecuatoriano, donde la estimación del valor de una propiedad suele ser empírica o requerir peritajes costosos.

Mediante técnicas de *Web Scraping*, procesamiento de datos y *Machine Learning*, la aplicación extrae la oferta actual de publicaciones residenciales, entrena un modelo de regresión supervisado y expone sus predicciones mediante un servicio de API REST y una interfaz web interactiva.

**Resultado esperado:** Una plataforma funcional donde el usuario ingrese las características de una vivienda (ubicación, superficie, dormitorios, baños y antigüedad) y reciba en tiempo real una estimación precisa de su precio comercial en dólares (USD).

---

# 🌐 Enlace al Repositorio

**Repositorio oficial en GitHub:**

👉 https://github.com/Byron432004/proyecto-prediccion-casas

---

# 🏗 Arquitectura o Flujo

El proyecto implementa un flujo de datos modular e independiente, estructurado en 6 etapas secuenciales:

```text
Scraping → Datos → Entrenamiento → PKL → FastAPI → Streamlit

1. Scraping: Extracción de datos de publicaciones de inmuebles en portales web.
2. Datos: Preprocesamiento y limpieza de datos extraídos.
3. Entrenamiento: Modelado de machine learning para predecir precios de inmuebles.
4. PKL: Exportación de modelo entrenado y sus transformadores en formato archivo.
5. FastAPI: Servicio web RESTful para consumo de datos y predicciones.
6. Streamlit: Interfaz web interactiva para visualización y entrada de datos.
```

---

# 📋 Requerimientos

Para ejecutar el proyecto, se requieren los siguientes requisitos previos:

* **Python 3.10 o superior:** Compatible con 3.11.
* **Librerías y dependencias:** `fastapi`, `uvicorn`, `streamlit`, `scikit-learn`, `pandas`, `numpy`, `beautifulsoup4`, `playwright`, `requests`.

---

# 🚀 Instalación y Configuración

Sigue estos pasos para instalar y configurar el proyecto en tu entorno local:

### 1. Crear y activar el entorno virtual

**En Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**En macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el servidor API (FastAPI)

```bash
uvicorn api.main:app --reload
```

### 4. Ejecutar la interfaz web (Streamlit)

```bash
streamlit run app/streamlit_app.py
```

---

# ⚠️ Limitaciones y Supuestos

* **Cobertura geográfica:** El modelo ha sido entrenado y validado exclusivamente con publicaciones de Quito, Guayaquil y Manabí. Ingresar ciudades fuera de esta cobertura generará predicciones con menor confiabilidad o errores de validación.

* **Tipo de inmuebles:** Restringido a casas y departamentos residenciales estándar. No aplica para terrenos vacíos, locales comerciales, oficinas ni inmuebles de lujo atípicos.

* **Supuestos del mercado:** Asume condiciones de oferta y demanda estables a la fecha de captura del web scraping. No contempla variaciones macroeconómicas en tiempo real (inflación, tasa de interés hipotecaria) ni remates judiciales.

# ⚠️ Limitaciones y Supuestos

proyecto-prediccion-casas/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── casas_plusvalia.csv
│   └── processed/
│       └── casas_limpias.csv
│
├── scraping/
│   └── scraper_plusvalia.py
│
├── notebooks/
│   └── entrenamiento_modelo.ipynb
│
├── models/
│   └── modelo_precios.pkl
│
├── api/
│   └── main.py
│
└── app/
    └── streamlit_app.py

# 📊 Ejemplo de Uso

Para probar la aplicación, puedes ingresar los siguientes datos en la interfaz web:

* **Ubicación:** Quito
* **Área total:** 150 m²
* **Número de Habitaciones:** 3
* **Número de Baños:** 2
* **Antigüedad:** 5 años

Una vez ingresados los datos, el sistema calculará el precio estimado de la vivienda en tiempo real y mostrará el resultado en la interfaz web.

---

# 📝 Créditos

* **Autor:** Byron Nasimba  
* **GitHub:** https://github.com/Byron432004  
* **LinkedIn:** https://www.linkedin.com/in/byronraulnasimba3/
* **Email:** byronraul3@hotmail.com  
---

# 📄 Licencia

Este proyecto está bajo la licencia MIT. Para más información, consulta el archivo `LICENSE` en la raíz del repositorio.

# 🚀 Estado del Proyecto

**Versión estable:** v1.0.0

* Web Scraping integrado y automatizado
* Dataset procesado y estructurado en CSV
* Modelo Random Forest entrenado, evaluado y exportado a PKL
* API RESTful en FastAPI activa con endpoint /predict
* Interfaz web interactiva construida con Streamlit
* Interfaz gráfica en Streamlit conectada al backend API
* Documentación completa y actualizada
