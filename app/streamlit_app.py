import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Predicción de Precios de Casas",
    page_icon="🏡",
    layout="centered"
)

st.title("🏡 Predicción de Precios de Casas")

st.subheader("📋 Ingresa las características de la vivienda:")

col1, col2 = st.columns(2)

with col1:
    ubicacion = st.selectbox(
        "📍 Ciudad / Ubicación:",
        options=["Quito", "Guayaquil", "Manta"],
        help="Selecciona la ciudad donde se encuentra la propiedad."
    )
    
    area = st.number_input(
        "📐 Área total (m²):",
        min_value=20,
        max_value=10000,
        value=150,
        step=10,
        help="Superficie total de la casa en metros cuadrados."
    )
    
    antiguedad = st.number_input(
        "📅 Antigüedad (años):",
        min_value=0,
        max_value=100,
        value=5,
        step=1,
        help="Años de construcción de la propiedad (0 para estrenar)."
    )

with col2:
    habitaciones = st.number_input(
        "🛏️ Número de Habitaciones:",
        min_value=1,
        max_value=20,
        value=3,
        step=1
    )
    
    banos = st.number_input(
        "🚿 Número de Baños:",
        min_value=1,
        max_value=15,
        value=2,
        step=1
    )

st.markdown("---")


if st.button("🚀 Calcular Precio Estimado", use_container_width=True):
    datos_vivienda = {
        "ubicacion": ubicacion,
        "area": float(area),
        "habitaciones": int(habitaciones),
        "banos": int(banos),
        "antiguedad": int(antiguedad)
    }
    
    # URL local del servidor FastAPI
    url_api = "http://127.0.0.1:8000/predict"
    
    with st.spinner("Conectando con la API y calculando precio... ⚙️"):
        try:
            # Enviamos la solicitud POST a nuestra API
            respuesta = requests.post(url_api, json=datos_vivienda, timeout=5)
            
            # Verificamos si la API respondió correctamente (Código 200)
            if respuesta.status_code == 200:
                resultado = respuesta.json()
                precio_final = resultado["precio_estimado_usd"]
                
                # Formato visual elegante y comprensible solicitado en la guía
                st.success("¡Predicción calculada exitosamente!")
                st.metric(
                    label="💵 Precio Estimado de la Propiedad:",
                    value=f"USD {precio_final:,.2f}"
                )
                    
            else:
                st.error(f"⚠️ Error desde la API (Código {respuesta.status_code}): {respuesta.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ **No se pudo conectar con el servidor FastAPI.**")
            st.warning("👉 Asegúrate de tener la terminal de la API encendida corriendo el comando:\n`uvicorn api.main:app --reload`")
        except Exception as e:
            st.error(f"Ocurrió un error inesperado: {str(e)}")

st.markdown("<br><hr><center> <small>Byron Nasimba - Diplomado Python Full Stack</small> </center>", unsafe_allow_html=True)