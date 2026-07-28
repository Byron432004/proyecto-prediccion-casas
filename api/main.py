import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# 1. Inicializar la aplicación FastAPI
app = FastAPI(
    title="API de Predicción de Precios de Inmuebles",
    description="Servicio backend para predecir precios de casas en Ecuador mediante Machine Learning.",
    version="1.0.0"
)

# 2. Localizar y cargar el modelo .pkl
# Manejador de ruta adaptable para ejecutar desde cualquier ubicación
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_modelo = os.path.join(directorio_actual, "..", "models", "modelo_precios.pkl")

if not os.path.exists(ruta_modelo):
    ruta_modelo = "models/modelo_precios.pkl"

try:
    modelo = joblib.load(ruta_modelo)
    print("✅ Modelo cargado exitosamente en la API.")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    modelo = None


# 3. Definir el esquema de datos de entrada con Pydantic
class CasaInput(BaseModel):
    ubicacion: str = Field(..., json_schema_extra={"example": "Quito"}, description="Ciudad: Quito, Guayaquil o Manta")
    area: float = Field(..., gt=0, json_schema_extra={"example": 150.0}, description="Área en metros cuadrados")
    habitaciones: int = Field(..., ge=1, json_schema_extra={"example": 3}, description="Número de habitaciones")
    banos: int = Field(..., ge=1, json_schema_extra={"example": 2}, description="Número de baños")
    antiguedad: int = Field(..., ge=0, json_schema_extra={"example": 5}, description="Antigüedad en años")


# 4. Rutas y Endpoints
@app.get("/")
def inicio():
    """Ruta raíz de bienvenida y estado del servicio."""
    return {
        "estado": "API Activa",
        "proyecto": "Predicción de Precios de Casas",
        "documentacion": "Visita /docs para probar los endpoints interactivos."
    }


@app.post("/predict")
def predecir_precio(datos: CasaInput):
    """Endpoint principal para recibir datos de la vivienda y retornar la predicción de precio."""
    if modelo is None:
        raise HTTPException(
            status_code=500, 
            detail="El modelo de Machine Learning no se encuentra disponible."
        )
    
    try:
        # Convertir los datos de entrada en un DataFrame de Pandas para el Pipeline
        df_entrada = pd.DataFrame([{
            "ubicacion": datos.ubicacion.capitalize(),
            "area": datos.area,
            "habitaciones": datos.habitaciones,
            "banos": datos.banos,
            "antiguedad": datos.antiguedad
        }])
        
        # Ejecutar la predicción
        prediccion = modelo.predict(df_entrada)[0]
        
        return {
            "exito": True,
            "precio_estimado_usd": round(float(prediccion), 2),
            "datos_recibidos": datos.model_dump()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error al procesar la predicción: {str(e)}"
        )