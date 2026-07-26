import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrapear_plusvalia_didactico():
    print("🚀 Iniciando el Web Scraper de Plusvalía con Selenium...")

    # 1. Configuración de Selenium (Modo visual para que veas qué ocurre)
    options = Options()
    options.add_experimental_option("detach", True) # Evita que Chrome se cierre de golpe
    options.add_argument("--start-maximized")       # Abre la ventana maximizada
    
    # Iniciamos el navegador
    driver = webdriver.Chrome(options=options)
    
    # 2. Definimos la URL (Puedes cambiar a quito, guayaquil, manta, etc.)
    # Nota: Usamos la estructura de búsqueda de ventas que funciona en Plusvalía
    url_busqueda = "https://www.plusvalia.com/casas-en-venta-en-quito.html"
    
    print(f"🌐 Navegando hacia: {url_busqueda}")
    driver.get(url_busqueda)
    
    # Esperamos a que la página cargue los scripts de seguridad y anuncios
    print("⏳ Esperando 6 segundos para la carga de elementos dinámicos...")
    time.sleep(6)
    
    # Hacemos un scroll suave para obligar a la página a cargar todas las fotos y tarjetas
    driver.execute_script("window.scrollBy(0, 1500);")
    time.sleep(2)

    # 3. Buscamos todas las tarjetas de casas en la página actual
    # Buscamos cualquier contenedor que tenga un atributo data-qa que contenga la palabra "posting"
    tarjetas = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa*="posting"]')
    
    print(f"🏠 ¡Éxito! Se detectaron {len(tarjetas)} anuncios de casas en esta página.\n")
    
    # Lista vacía donde guardaremos un diccionario por cada casa encontrada
    datos_casas = []

    # 4. Iteramos sobre cada tarjeta para extraer los campos requeridos por tu guía
    for i, tarjeta in enumerate(tarjetas, 1):
        try:
            # --- PRECIO ---
            try:
                precio_el = tarjeta.find_element(By.CSS_SELECTOR, '[data-qa*="PRICE"], div[class*="Price"]')
                precio = precio_el.text.strip()
            except:
                precio = "No disponible"

            # --- UBICACIÓN ---
            try:
                ubicacion_el = tarjeta.find_element(By.CSS_SELECTOR, '[data-qa*="POSTING_CARD_LOCATION"], div[class*="Location"]')
                ubicacion = ubicacion_el.text.strip()
            except:
                ubicacion = "No disponible"

            # --- CARACTERÍSTICAS (Área, Habitaciones, Baños, Antigüedad) ---
            # Suelen estar juntas en una lista de etiquetas (ej: "200 m² | 3 hab. | 2 baños")
            try:
                # Buscamos todos los textos dentro de la sección de características
                features_els = tarjeta.find_elements(By.CSS_SELECTOR, '[data-qa*="POSTING_CARD_FEATURES"] span, [data-qa*="feature"] span')
                textos_features = [f.text.strip() for f in features_els if f.text.strip() != ""]
                
                # Clasificamos de forma inteligente usando palabras clave
                area = next((f for f in textos_features if "m²" in f.lower() or "totales" in f.lower()), "No disponible")
                habitaciones = next((f for f in textos_features if "hab" in f.lower() or "dorm" in f.lower()), "No disponible")
                banos = next((f for f in textos_features if "baño" in f.lower()), "No disponible")
                antiguedad = next((f for f in textos_features if "año" in f.lower() or "estrenar" in f.lower()), "No disponible")
            except:
                area, habitaciones, banos, antiguedad = "No disponible", "No disponible", "No disponible", "No disponible"

            # 5. Guardamos la información limpia en nuestra lista
            casa_info = {
                "ubicacion": ubicacion,
                "precio": precio,
                "area": area,
                "habitaciones": habitaciones,
                "banos": banos,
                "antiguedad": antiguedad
            }
            
            datos_casas.append(casa_info)
            print(f"   [{i}] Extraído: {precio} | {ubicacion} | {area} | {habitaciones}")

        except Exception as e:
            print(f"⚠️ Hubo un error menor leyendo la tarjeta {i}, saltando... ({e})")
            continue

    # Cerramos el navegador al terminar la extracción
    print("\n🔒 Cerrando navegador...")
    driver.quit()

    # 6. Guardamos todo en un archivo CSV en la carpeta data/raw/
    if datos_casas:
        print("📊 Convirtiendo datos a formato tabular (DataFrame)...")
        df = pd.DataFrame(datos_casas)
        
        # Nos aseguramos de que la carpeta data/raw exista usando rutas relativas (exigido por tu guía)
        os.makedirs("data/raw", exist_ok=True)
        ruta_csv = "data/raw/casas_plusvalia.csv"
        
        # Exportamos a CSV sin índice y con codificación UTF-8 para las tildes y caracteres especiales
        df.to_csv(ruta_csv, index=False, encoding="utf-8-sig")
        print(f"🎉 ¡MARAVILLOSO! Archivo generado con éxito en: {ruta_csv}")
        print(f"📈 Total de registros guardados: {len(df)}")
    else:
        print("❌ No se lograron extraer datos. Revisa si Plusvalía mostró un captcha o bloqueo.")

if __name__ == "__main__":
    scrapear_plusvalia_didactico()