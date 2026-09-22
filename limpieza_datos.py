import pandas as pd
import numpy as np
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_ENTRADA = BASE_DIR / "Connacionales_inscritos_en_el_Registro_Ciudadano_en_Línea_20260921.csv"
ARCHIVO_SALIDA = BASE_DIR / "Connacionales_limpios.csv"
ARCHIVO_REPORTE = BASE_DIR / "resultados" / "reporte_limpieza.txt"

print("============================================================")
print("INICIANDO PROCESO DE LIMPIEZA Y PREPROCESAMIENTO DE DATOS")
print("============================================================")

df = pd.read_csv(ARCHIVO_ENTRADA, low_memory=False)
total_inicial = len(df)
print(f"Registros cargados: {total_inicial:,}\n")

reporte_cambios = []

def registrar(msg):
    print(msg)
    reporte_cambios.append(msg)

registrar(f"Total registros iniciales: {total_inicial:,}")

# ------------------------------------------------------------
# 1. ELIMINACIÓN DE ESPACIOS EN BLANCO EXTRAS (TRIM)
# ------------------------------------------------------------
registrar("\n--- 1. Eliminación de espacios en blanco extras ---")
for col in df.select_dtypes(include=['object', 'string']).columns:
    df[col] = df[col].astype(str).str.strip()

registrar("Se eliminaron espacios al inicio y final en todas las variables de texto.")

# ------------------------------------------------------------
# 2. HOMOGENEIZACIÓN Y CORRECCIÓN DE CÓDIGOS ISO Y PAÍSES
# ------------------------------------------------------------
registrar("\n--- 2. Corrección de Inconsistencias en Países e ISO ---")
# Correcciones específicas de nombres de países
mapeo_paises = {
    "CHINA, REPÚBLICA POPULAR": "CHINA",
    "VIET NAM": "VIETNAM",
    "ANTILLAS HOLANDESAS": "PAISES BAJOS"  # ISO NLD corresponde a Países Bajos (Antillas Holandesas disueltas)
}
for origen, destino in mapeo_paises.items():
    cant = (df["País"] == origen).sum()
    if cant > 0:
        df.loc[df["País"] == origen, "País"] = destino
        registrar(f"  - Se unificó '{origen}' -> '{destino}' ({cant:,} registros).")

# ------------------------------------------------------------
# 4. TRATAMIENTO DE VALORES FALTANTES IMPLÍCITOS (PLACEHOLDERS)
# ------------------------------------------------------------
registrar("\n--- 3. Estandarización de Valores Faltantes Implícitos ---")
# Unificar leyendas heterogéneas a un valor estándar 'SIN INFORMACIÓN'
placeholders = ["(NO REGISTRA)", "NO INFORMA", "DESCONOCIDO", "NO INDICA", "SIN INFORMACIÓN", "NINGUNO", "NINGUNA", "SIN ETNIA REGISTRADA"]

# Estandarización por columna relevante
# Nivel Académico
mask_nivel = df["Nivel Académico"].isin(["(NO REGISTRA)", "SIN INFORMACIÓN", "NINGUNO"])
df.loc[mask_nivel, "Nivel Académico"] = "SIN INFORMACIÓN"
registrar(f"  - Nivel Académico 'SIN INFORMACIÓN' unificado: {mask_nivel.sum():,} registros.")

# Área Conocimiento
mask_area = df["Área Conocimiento"].isin(["(NO REGISTRA)", "NO INDICA", "NINGUNA", "PROGRAMAS Y CERTIFICACIONES GENÉRICAS"])
df.loc[mask_area, "Área Conocimiento"] = "SIN INFORMACIÓN"
registrar(f"  - Área Conocimiento 'SIN INFORMACIÓN' unificada: {mask_area.sum():,} registros.")

# Estado Civil
mask_eciv = df["Estado civil"] == "DESCONOCIDO"
df.loc[mask_eciv, "Estado civil"] = "SIN INFORMACIÓN"
registrar(f"  - Estado civil 'SIN INFORMACIÓN' unificado: {mask_eciv.sum():,} registros.")

# Sexo
mask_sexo = df["Sexo"] == "DESCONOCIDO"
df.loc[mask_sexo, "Sexo"] = "SIN INFORMACIÓN"
registrar(f"  - Sexo 'SIN INFORMACIÓN' unificado: {mask_sexo.sum():,} registros.")

# Pertenencia étnica
mask_etnia = df["Pertenencia étnica"].isin(["NINGUNA", "SIN ETNIA REGISTRADA", "OTRO"])
df.loc[mask_etnia, "Pertenencia étnica"] = "NINGUNA / NO REGISTRA"
registrar(f"  - Pertenencia étnica 'NINGUNA / NO REGISTRA' unificada: {mask_etnia.sum():,} registros.")

# Ciudad de Nacimiento
mask_nac = df["Ciudad de Nacimiento"] == "(NO REGISTRA)"
df.loc[mask_nac, "Ciudad de Nacimiento"] = "SIN INFORMACIÓN"
registrar(f"  - Ciudad de Nacimiento 'SIN INFORMACIÓN' unificada: {mask_nac.sum():,} registros.")

# ------------------------------------------------------------
# 5. TRATAMIENTO DE FECHAS ANÓMALAS (1900-01)
# ------------------------------------------------------------
registrar("\n--- 4. Corrección de Fechas Sentinelas (1900-01) ---")
cant_1900 = (df["Fecha de Registro"] == "1900-01").sum()
df.loc[df["Fecha de Registro"] == "1900-01", "Fecha de Registro"] = "SIN INFORMACIÓN"
registrar(f"  - Registros con fecha sentinela '1900-01' marcados como 'SIN INFORMACIÓN': {cant_1900:,} registros.")

# ------------------------------------------------------------
# 6. TRATAMIENTO DE VALORES NULOS EN LOCALIZACIÓN
# ------------------------------------------------------------
registrar("\n--- 5. Imputación de Localización Nula ---")
cant_loc_null = df["Localización"].isnull().sum() + (df["Localización"] == "nan").sum()
df.loc[df["Localización"].isnull() | (df["Localización"] == "nan"), "Localización"] = "SIN INFORMACIÓN"
registrar(f"  - Registros de Localización nulos imputados como 'SIN INFORMACIÓN': {cant_loc_null:,} registros.")

# ------------------------------------------------------------
# 7. GUARDAR DATASET LIMPIO Y REPORTE
# ------------------------------------------------------------
registrar("\n--- 6. Exportación del Dataset Limpio ---")
df.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8")
registrar(f"Dataset limpio guardado exitosamente en:\n  {ARCHIVO_SALIDA}")

# Guardar reporte en texto
(BASE_DIR / "resultados").mkdir(exist_ok=True)
with open(ARCHIVO_REPORTE, "w", encoding="utf-8") as f:
    f.write("\n".join(reporte_cambios))

registrar(f"Reporte de limpieza guardado en:\n  {ARCHIVO_REPORTE}")
print("\n============================================================")
print("PROCESO DE LIMPIEZA COMPLETADO EXITOSAMENTE")
print("============================================================")
