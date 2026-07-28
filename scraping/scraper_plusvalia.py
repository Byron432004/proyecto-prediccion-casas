import os
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 1. RETORNAMOS A TU ESTRUCTURA ORIGINAL DE URLS (¡Tú tenías la razón desde el principio!)
ruta_raiz = "https://www.plusvalia.com/venta/casas"

urls_ciudad = [
    "pichincha/quito",
    "guayas/guayaquil",
    "manabi/manta"
]

lista_casas = []

print("Iniciando scraping de plusvalia.com")

for city in urls_ciudad:
    # Si la ruta es "guayas/guayaquil", tomamos lo que está después de la barra "/" -> "Guayaquil"
    nombre_ciudad_limpio = city.split("/")[-1].capitalize()
    url_final = f"{ruta_raiz}/{city}"
    
    print(f"\n=======================================================")
    print(f"🌐 [Ciudad: {nombre_ciudad_limpio}] Abriendo navegador para: {url_final}")
    
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    
    # Ocultamos la firma de automatización
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    try:
        driver.get(url_final)
        
        print("⏳ Esperando 12 segundos... (¡Si sale el cuadro de 'Verificar que soy humano', dale clic!)")
        time.sleep(12)
        
        # Scroll suave
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(1)
        
        tag_properties = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa*="posting"]')
        print(f"🏠 Se encontraron {len(tag_properties)} casas en {nombre_ciudad_limpio}.")
        
        for pro in tag_properties:
            try:
                texto_tarjeta = pro.text
                
                # --- PRECIO ---
                numeros_precio = re.findall(r'USD\s*[\d\.]+', texto_tarjeta)
                if numeros_precio:
                    precio_limpio = int(numeros_precio[0].replace("USD", "").replace(".", "").strip())
                else:
                    continue 
                    
                # --- ÁREA ---
                numeros_area = re.findall(r'(\d+)\s*m²', texto_tarjeta)
                area_limpia = int(numeros_area[0]) if numeros_area else 150
                    
                # --- HABITACIONES ---
                numeros_hab = re.findall(r'(\d+)\s*(?:a\s*\d+\s*)?hab', texto_tarjeta)
                hab_limpia = int(numeros_hab[-1]) if numeros_hab else 3
                    
                # --- BAÑOS ---
                numeros_banos = re.findall(r'(\d+)\s*baño', texto_tarjeta)
                banos_limpios = int(numeros_banos[0]) if numeros_banos else (2 if hab_limpia >= 3 else 1)
                    
                # --- ANTIGÜEDAD ---
                if "estrenar" in texto_tarjeta.lower():
                    antiguedad_limpia = 0
                else:
                    numeros_antiguedad = re.findall(r'(\d+)\s*año', texto_tarjeta)
                    antiguedad_limpia = int(numeros_antiguedad[0]) if numeros_antiguedad else 5
                
                datos = {
                    "ubicacion": nombre_ciudad_limpio,
                    "precio": precio_limpio,
                    "area": area_limpia,
                    "habitaciones": hab_limpia,
                    "banos": banos_limpios,
                    "antiguedad": antiguedad_limpia
                }
                
                lista_casas.append(datos)
                print(f"   ✅ [{nombre_ciudad_limpio}] USD {precio_limpio} | {area_limpia} m²    | {hab_limpia} hab | {banos_limpios} baños")
                
            except Exception:  
                continue

    finally:
        print(f"🔒 Cerrando sesión de {nombre_ciudad_limpio}...")
        driver.quit()
        print("⏳ Pausa de 3 segundos antes de abrir la siguiente ciudad...")
        time.sleep(3)

# Guardado final en CSV
if lista_casas:
    df = pd.DataFrame(lista_casas)
    os.makedirs("data/raw", exist_ok=True)
    ruta_csv = "data/raw/casas_plusvalia.csv"
    
    df.to_csv(ruta_csv, index=False, encoding="utf-8-sig")
    print(f"\n🎉 ¡ÉXITO TOTAL! Archivo guardado en: {ruta_csv}")
    print(f"📈 Total general de casas listas para Machine Learning: {len(df)}")
    
    print("\n📊 Conteo de casas por ciudad en tu CSV:")
    print(df['ubicacion'].value_counts())
else:
    print("❌ No se encontraron datos.")