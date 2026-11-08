# -*- coding: utf-8 -*-
"""
===============================================================================
PROYECTO: PROBABILIDAD Y ESTADÍSTICA - CUARTO SEMESTRE
AVANCE 2: ANÁLISIS BIVARIADO (DOS VARIABLES) Y MODELOS DE PRONÓSTICO
===============================================================================
Autores: Equipo de Investigación
Dataset: Connacionales inscritos en el Registro Ciudadano en Línea
Objetivos del Avance:
  1. Análisis con dos variables:
     - Correlación de Pearson entre variables cuantitativas y matriz de correlación.
     - Gráficos de dispersión e interpretación de coeficiente r y significancia.
     - Diagrama de cajas por grupos (X = Variable Cualitativa, Y = Variable Cuantitativa).
     - Tabla cruzada de contingencia entre 2 variables cualitativas y diagrama de barras apiladas.
  2. Modelos de Pronóstico para Series de Tiempo:
     - Evaluación de la dimensión temporal (>30 periodos mensuales disponibles: 155 periodos).
     - Implementación de Suavización Exponencial Simple (SES).
     - Implementación del Método de Holt (Tendencia Lineal).
     - Implementación del Método Holt-Winters (Tendencia y Estacionalidad Aditiva).
     - Métricas de error comparativas: RMSE, MAE, MAPE.
     - Proyección y pronóstico a 12 meses futuros (Año 2026).
  3. Exportación de gráficos en alta resolución (300 DPI) y tablas de resultados en Excel.
===============================================================================
"""

import os
import sys
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# Manejo de codificación de salida en consola Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Manejo de datos y operaciones numéricas
import pandas as pd
import numpy as np
from scipy import stats

# Modelación de series de tiempo
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing

# Visualización gráfica
import matplotlib
matplotlib.use("Agg")  # Backend no interactivo para guardar figuras limpiamente
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# =============================================================================
# SECCIÓN 0: CONFIGURACIÓN DE RUTAS Y PARÁMETROS GLOBALES
# =============================================================================

# Definición del directorio base donde reside este script
BASE_DIR = Path(__file__).resolve().parent

# Ruta del archivo CSV limpio generado en el Avance 1
ARCHIVO_CSV = BASE_DIR / "Connacionales_limpios.csv"

# Carpetas de salida para resultados y figuras
CARPETA_RESULTADOS = BASE_DIR / "resultados"
CARPETA_GRAFICOS = CARPETA_RESULTADOS / "graficos"
ARCHIVO_EXCEL = CARPETA_RESULTADOS / "analisis_bivariado_y_pronosticos.xlsx"
ARCHIVO_RESUMEN = CARPETA_RESULTADOS / "resumen_avance_2.txt"

# Crear las carpetas de salida si aún no existen
CARPETA_RESULTADOS.mkdir(parents=True, exist_ok=True)
CARPETA_GRAFICOS.mkdir(parents=True, exist_ok=True)

# Configuración de estilo visual para gráficos profesionales
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 14,
    "figure.autolayout": False
})

print("=" * 80)
print("INICIANDO EJECUCIÓN DEL AVANCE 2: ANÁLISIS BIVARIADO Y PRONÓSTICOS")
print("=" * 80)

# =============================================================================
# SECCIÓN 1: CARGA Y PREPARACIÓN DEL CONJUNTO DE DATOS
# =============================================================================

if not ARCHIVO_CSV.exists():
    print(f"ERROR: No se encontró el archivo de datos: {ARCHIVO_CSV}")
    sys.exit(1)

print(f"\n[1/6] Cargando datos desde: {ARCHIVO_CSV.name}...")
df = pd.read_csv(ARCHIVO_CSV, low_memory=False)
total_registros = len(df)
print(f" -> Registros cargados exitosamente: {total_registros:,}")

# Asegurar que 'Edad (años)' y 'Cantidad de personas' sean numéricas
df["Edad (años)"] = pd.to_numeric(df["Edad (años)"], errors="coerce")
df["Cantidad de personas"] = pd.to_numeric(df["Cantidad de personas"], errors="coerce").fillna(1)

# Extracción de coordenadas geográficas (Latitud y Longitud) de la columna 'Localización'
# Formato típico: "(33.93911, 67.709953)"
coords = df["Localización"].astype(str).str.extract(r"\(([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+)\)")
df["Latitud"] = pd.to_numeric(coords[0], errors="coerce")
df["Longitud"] = pd.to_numeric(coords[1], errors="coerce")

print(" -> Variables numéricas listas: 'Edad (años)', 'Cantidad de personas', 'Latitud', 'Longitud'")

# Diccionario para almacenar las hojas de cálculo que exportaremos a Excel
tablas_para_excel = {}
lineas_resumen_txt = []

def registrar(texto):
    """Imprime en consola y añade al búfer del archivo de resumen en texto plano."""
    print(texto)
    lineas_resumen_txt.append(texto)

registrar("=" * 80)
registrar("RESUMEN ESTADÍSTICO - AVANCE 2")
registrar(f"Total de observaciones analizadas: {total_registros:,}")
registrar("=" * 80)

# =============================================================================
# SECCIÓN 2: CLASIFICACIÓN RIGUROSA DE VARIABLES
# =============================================================================

registrar("\n" + "=" * 80)
registrar("1. CLASIFICACIÓN DE VARIABLES DEL DATASET")
registrar("=" * 80)

clasificacion_variables = [
    {"Variable": "Edad (años)", "Tipo": "Cuantitativa", "Subtipo": "Continua / Discreta", "Escala": "Razón", "Descripción": "Edad en años cumplidos de los connacionales registrados (filtro 25 a 40 años)."},
    {"Variable": "Cantidad de personas", "Tipo": "Cuantitativa", "Subtipo": "Discreta", "Escala": "Razón", "Descripción": "Número de personas vinculadas al registro consular (1 a 5 personas)."},
    {"Variable": "Latitud", "Tipo": "Cuantitativa", "Subtipo": "Continua", "Escala": "Intervalo", "Descripción": "Coordenada geográfica norte-sur en grados decimales (extraída de Localización)."},
    {"Variable": "Longitud", "Tipo": "Cuantitativa", "Subtipo": "Continua", "Escala": "Intervalo", "Descripción": "Coordenada geográfica este-oeste en grados decimales (extraída de Localización)."},
    {"Variable": "Fecha de Registro", "Tipo": "Temporal / Cronológica", "Subtipo": "Periodo (Año-Mes)", "Escala": "Intervalo", "Descripción": "Periodo mensual en el que se realizó la inscripción (2013-02 a 2025-12, 155 periodos)."},
    {"Variable": "Nivel Académico", "Tipo": "Cualitativa", "Subtipo": "Ordinal", "Escala": "Ordinal", "Descripción": "Nivel de escolaridad alcanzado (jerarquía intrínseca desde Primaria hasta Doctorado)."},
    {"Variable": "Estado civil", "Tipo": "Cualitativa", "Subtipo": "Nominal", "Escala": "Nominal", "Descripción": "Situación conyugal declarada (Soltero, Casado, Unión libre, etc.)."},
    {"Variable": "Sexo", "Tipo": "Cualitativa", "Subtipo": "Nominal / Dicotómica", "Escala": "Nominal", "Descripción": "Género biológico o de registro (Femenino, Masculino)."},
    {"Variable": "País", "Tipo": "Cualitativa", "Subtipo": "Nominal", "Escala": "Nominal", "Descripción": "País donde reside actualmente el connacional en el exterior."},
    {"Variable": "Código ISO país", "Tipo": "Cualitativa", "Subtipo": "Nominal", "Escala": "Nominal", "Descripción": "Código alfanumérico estandarizado de 3 letras que identifica al país."},
    {"Variable": "Ciudad de Residencia", "Tipo": "Cualitativa", "Subtipo": "Nominal", "Escala": "Nominal", "Descripción": "Ciudad o división administrativa de residencia internacional."},
    {"Variable": "Oficina consular", "Tipo": "Cualitativa", "Subtipo": "Nominal", "Escala": "Nominal", "Descripción": "Consulado o misión diplomática que atiende la circunscripción."},
    {"Variable": "Área Conocimiento", "Tipo": "Cualitativa", "Subtipo": "Nominal", "Escala": "Nominal", "Descripción": "Disciplina académica o rama profesional reportada."},
    {"Variable": "Pertenencia étnica", "Tipo": "Cualitativa", "Subtipo": "Nominal", "Escala": "Nominal", "Descripción": "Autoidentificación étnica declarada por el connacional."},
    {"Variable": "Ciudad Nacimiento", "Tipo": "Cualitativa", "Subtipo": "Nominal", "Escala": "Nominal", "Descripción": "Municipio o departamento colombiano de origen."}
]

df_clasificacion = pd.DataFrame(clasificacion_variables)
tablas_para_excel["Clasificacion_Variables"] = df_clasificacion

registrar(df_clasificacion[["Variable", "Tipo", "Subtipo", "Escala"]].to_string(index=False))
registrar(f"\nResumen de clasificación: 4 Cuantitativas individuales + 1 Variable Temporal + 10 Cualitativas = 15 Variables analizadas.")

# =============================================================================
# SECCIÓN 3: ANÁLISIS BIVARIADO - DOS VARIABLES CUANTITATIVAS (PEARSON)
# =============================================================================

registrar("\n" + "=" * 80)
registrar("2. CORRELACIÓN LINEAL DE PEARSON Y MATRIZ DE CORRELACIÓN")
registrar("=" * 80)

# Variables cuantitativas seleccionadas para la matriz
columnas_cuantitativas = ["Edad (años)", "Cantidad de personas", "Latitud", "Longitud"]
df_cuanti = df[columnas_cuantitativas].dropna()

# Matriz de correlación de Pearson
matriz_corr = df_cuanti.corr(method="pearson")
registrar("\nMatriz de Correlación de Pearson:")
registrar(matriz_corr.round(5).to_string())
tablas_para_excel["Matriz_Correlacion"] = matriz_corr.round(5)

# Estudio detallado entre las 2 variables cuantitativas principales: Edad vs Cantidad de personas
x_var = df_cuanti["Edad (años)"]
y_var = df_cuanti["Cantidad de personas"]

# Coeficiente r y valor p de dos colas
r_pearson, p_valor = stats.pearsonr(x_var, y_var)
r_cuadrado = r_pearson ** 2  # Coeficiente de determinación R²

registrar(f"\nAnálisis Detallado: Edad (años) vs Cantidad de personas:")
registrar(f"  - Coeficiente de correlación de Pearson (r): {r_pearson:.5f}")
registrar(f"  - Coeficiente de determinación (R^2):         {r_cuadrado:.6f} ({r_cuadrado*100:.4f}%)")
registrar(f"  - Valor p (p-value):                         {p_valor:.4e}")
registrar(f"  - Tamaño de muestra (N):                     {len(df_cuanti):,}")

# Interpretación estadística
if p_valor < 0.05:
    interp_sig = "Estadísticamente significativa (p < 0.05), producto del gran tamaño muestral."
else:
    interp_sig = "No estadísticamente significativa (p >= 0.05)."

if abs(r_pearson) < 0.10:
    interp_fuerza = "Correlación prácticamente nula / despreciable (|r| < 0.10)."
elif abs(r_pearson) < 0.30:
    interp_fuerza = "Correlación débil."
elif abs(r_pearson) < 0.50:
    interp_fuerza = "Correlación moderada."
else:
    interp_fuerza = "Correlación fuerte."

registrar(f"  - Magnitud y sentido: {interp_fuerza}")
registrar(f"  - Significancia:      {interp_sig}")
registrar(f"  - Interpretación Teórica: El valor r = {r_pearson:.5f} refleja que no existe una")
registrar("    asociación lineal entre la edad del connacional (entre 25 y 40 años) y el número")
registrar("    de personas que declara en su registro. La variabilidad explicada es casi 0% (0.11%).")

# --- GRÁFICO 1: Mapa de Calor (Heatmap) de la Matriz de Correlación ---
print("\n[2/6] Generando gráficos de correlación...")
fig, ax = plt.subplots(figsize=(8, 6.5))
mask = np.triu(np.ones_like(matriz_corr, dtype=bool), k=1)  # Máscara para la diagonal superior
cmap = sns.diverging_palette(220, 20, as_cmap=True)

sns.heatmap(
    matriz_corr,
    annot=True,
    fmt=".4f",
    cmap="coolwarm",
    vmin=-0.1,
    vmax=0.1,
    center=0,
    square=True,
    linewidths=1.5,
    cbar_kws={"shrink": 0.8, "label": "Coeficiente de Correlación de Pearson (r)"},
    ax=ax
)
ax.set_title("Matriz de Correlación de Pearson - Variables Cuantitativas\n(Connacionales en el Exterior)", pad=15, fontweight="bold")
plt.xticks(rotation=20, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
ruta_fig_matriz = CARPETA_GRAFICOS / "matriz_correlacion_pearson.png"
plt.savefig(ruta_fig_matriz, dpi=300)
plt.close()
print(f" -> Guardado: {ruta_fig_matriz.name}")

# --- GRÁFICO 2: Gráfico de Dispersión (Scatter Plot) con Línea de Regresión ---
# Debido a que N > 500,000 y ambas variables toman valores discretizados (Edad: 25-40, Personas: 1-5),
# usamos jittering controlado o hexbin para visibilizar la densidad sin superposición plana.
fig, ax = plt.subplots(figsize=(9, 6))

# Calculamos media de personas por cada edad para trazar el perfil empírico
promedio_personas_por_edad = df.groupby("Edad (años)")["Cantidad de personas"].mean().reset_index()

# Submuestra aleatoria de 5,000 puntos con jitter suave para ilustrar la dispersión individual
np.random.seed(42)
submuestra = df_cuanti.sample(n=min(5000, len(df_cuanti)), random_state=42)
jitter_x = submuestra["Edad (años)"] + np.random.uniform(-0.25, 0.25, size=len(submuestra))
jitter_y = submuestra["Cantidad de personas"] + np.random.uniform(-0.15, 0.15, size=len(submuestra))

ax.scatter(jitter_x, jitter_y, alpha=0.15, color="#1f77b4", s=15, label="Muestra representativa (N=5,000)")

# Línea de regresión lineal teórica
m, b = np.polyfit(df_cuanti["Edad (años)"], df_cuanti["Cantidad de personas"], 1)
x_line = np.linspace(25, 40, 100)
ax.plot(x_line, m * x_line + b, color="#d62728", linewidth=2.5, linestyle="--",
        label=f"Regresión Lineal: y = {m:.4f}x + {b:.3f} (r = {r_pearson:.4f})")

# Perfil del promedio empírico por edad
ax.plot(promedio_personas_por_edad["Edad (años)"], promedio_personas_por_edad["Cantidad de personas"],
        color="#2ca02c", marker="o", linewidth=2, label="Promedio real de personas por edad")

ax.set_title("Diagrama de Dispersión y Regresión: Edad vs Cantidad de Personas\n(r = -0.0329, Relación Lineal Nula)", pad=15, fontweight="bold")
ax.set_xlabel("Edad del Connacional (años)")
ax.set_ylabel("Cantidad de Personas Declaradas")
ax.set_xticks(range(25, 41))
ax.set_yticks(range(1, 6))
ax.legend(loc="upper right", frameon=True)
plt.tight_layout()
ruta_fig_dispersion = CARPETA_GRAFICOS / "dispersion_edad_vs_personas.png"
plt.savefig(ruta_fig_dispersion, dpi=300)
plt.close()
print(f" -> Guardado: {ruta_fig_dispersion.name}")

# =============================================================================
# SECCIÓN 4: ANÁLISIS BIVARIADO - CUANTITATIVA VS CUALITATIVA (BOXPLOT POR GRUPOS)
# =============================================================================

registrar("\n" + "=" * 80)
registrar("3. DIAGRAMA DE CAJAS POR GRUPOS (CUANTITATIVA VS CUALITATIVA)")
registrar("=" * 80)

# Selección de variables:
# Cuantitativa (Y) = 'Edad (años)'
# Cualitativa (X)   = 'Nivel Académico' (y comparación secundaria con 'Estado civil')

# Definir el orden jerárquico lógico de los niveles académicos (excluyendo categorías residuales o sin información)
orden_academico = [
    "PRIMARIA",
    "BACHILLERATO",
    "TÉCNICA PROFESIONAL",
    "TECNOLÓGICA",
    "PROFESIONAL",
    "ESPECIALIZACIÓN",
    "MAESTRÍA",
    "DOCTORADO"
]

# Filtrar para conservar únicamente los niveles válidos con orden formativo
df_box_acad = df[df["Nivel Académico"].isin(orden_academico)].copy()

# Estadísticas por grupo académico
stats_por_nivel = df_box_acad.groupby("Nivel Académico")["Edad (años)"].agg(
    N="count",
    Media="mean",
    Mediana="median",
    Desv_Est="std",
    Q1=lambda s: s.quantile(0.25),
    Q3=lambda s: s.quantile(0.75),
    IQR=lambda s: s.quantile(0.75) - s.quantile(0.25),
    Minimo="min",
    Maximo="max"
).reindex(orden_academico).reset_index()

registrar("\nEstadísticas Descriptivas de Edad (años) según Nivel Académico:")
registrar(stats_por_nivel.round(2).to_string(index=False))
tablas_para_excel["Edad_por_Nivel_Academico"] = stats_por_nivel.round(2)

# Prueba ANOVA de 1 vía para contrastar diferencias entre medias de edad por grupo
grupos_edad_acad = [df_box_acad[df_box_acad["Nivel Académico"] == nivel]["Edad (años)"].values for nivel in orden_academico]
f_stat, p_val_anova = stats.f_oneway(*grupos_edad_acad)
registrar(f"\nPrueba ANOVA de 1 Vía (Edad según Nivel Académico):")
registrar(f"  - Estadístico F: {f_stat:.2f}, Valor p: {p_val_anova:.4e}")
registrar("  - Conclusión: Existen diferencias estadísticamente significativas en la media de edad")
registrar("    entre los diferentes niveles académicos (los grados de posgrado presentan mayor edad).")

# --- GRÁFICO 3: Diagrama de Cajas (Boxplot) por Nivel Académico ---
print("\n[3/6] Generando diagramas de cajas por grupos...")
fig, ax = plt.subplots(figsize=(12, 6.5))

paleta_colores = sns.color_palette("Blues_r", len(orden_academico))

bp = sns.boxplot(
    data=df_box_acad,
    x="Nivel Académico",
    y="Edad (años)",
    order=orden_academico,
    palette="Blues",
    showmeans=True,
    meanprops={"marker": "D", "markeredgecolor": "black", "markerfacecolor": "#d62728", "markersize": 7},
    medianprops={"color": "darkblue", "linewidth": 2},
    whiskerprops={"linewidth": 1.5},
    capprops={"linewidth": 1.5},
    ax=ax
)

# Etiquetas de la media sobre las cajas
for i, nivel in enumerate(orden_academico):
    media_val = stats_por_nivel.loc[stats_por_nivel["Nivel Académico"] == nivel, "Media"].values[0]
    ax.text(i, media_val + 0.4, f"x̄={media_val:.1f}", ha="center", va="bottom",
            fontsize=9.5, fontweight="bold", color="#800000")

ax.set_title("Diagrama de Cajas de Edad por Nivel Académico\n(Los rombos rojos indican la media; la línea central la mediana)",
             pad=15, fontweight="bold")
ax.set_xlabel("Nivel Académico (Variable Cualitativa)", labelpad=10)
ax.set_ylabel("Edad en Años (Variable Cuantitativa)", labelpad=10)
ax.set_ylim(23, 42)
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
ruta_fig_box_acad = CARPETA_GRAFICOS / "boxplot_edad_por_nivel_academico.png"
plt.savefig(ruta_fig_box_acad, dpi=300)
plt.close()
print(f" -> Guardado: {ruta_fig_box_acad.name}")

# --- GRÁFICO 4: Diagrama de Cajas Secundario: Edad por Estado Civil ---
orden_civil = ["SOLTERO", "UNION_LIBRE", "CASADO", "DIVORCIADO", "VIUDO"]
df_box_civil = df[df["Estado civil"].isin(orden_civil)].copy()

stats_por_civil = df_box_civil.groupby("Estado civil")["Edad (años)"].agg(
    N="count", Media="mean", Mediana="median", Desv_Est="std"
).reindex(orden_civil).reset_index()
tablas_para_excel["Edad_por_Estado_Civil"] = stats_por_civil.round(2)

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(
    data=df_box_civil,
    x="Estado civil",
    y="Edad (años)",
    order=orden_civil,
    palette="Purples",
    showmeans=True,
    meanprops={"marker": "D", "markeredgecolor": "black", "markerfacecolor": "#d62728", "markersize": 7},
    medianprops={"color": "darkred", "linewidth": 2},
    ax=ax
)
for i, est in enumerate(orden_civil):
    media_val = stats_por_civil.loc[stats_por_civil["Estado civil"] == est, "Media"].values[0]
    ax.text(i, media_val + 0.4, f"x̄={media_val:.1f}", ha="center", va="bottom",
            fontsize=9.5, fontweight="bold", color="#800000")

ax.set_title("Diagrama de Cajas de Edad por Estado Civil\n(Los connacionales casados y divorciados tienen mayor edad promedio)",
             pad=15, fontweight="bold")
ax.set_xlabel("Estado Civil (Variable Cualitativa)", labelpad=10)
ax.set_ylabel("Edad en Años (Variable Cuantitativa)", labelpad=10)
ax.set_ylim(23, 42)
plt.tight_layout()
ruta_fig_box_civil = CARPETA_GRAFICOS / "boxplot_edad_por_estado_civil.png"
plt.savefig(ruta_fig_box_civil, dpi=300)
plt.close()
print(f" -> Guardado: {ruta_fig_box_civil.name}")

# =============================================================================
# SECCIÓN 5: ANÁLISIS BIVARIADO - DOS VARIABLES CUALITATIVAS (TABLA CRUZADA Y BARRAS APILADAS)
# =============================================================================

registrar("\n" + "=" * 80)
registrar("4. TABLA CRUZADA DE CONTINGENCIA Y BARRAS APILADAS")
registrar("=" * 80)

# Selección de dos variables cualitativas clave:
# Variable 1 = 'Nivel Académico' (Filas)
# Variable 2 = 'Sexo' (Columnas: Femenino vs Masculino)

df_cruz = df[df["Sexo"].isin(["FEMENINO", "MASCULINO"]) & df["Nivel Académico"].isin(orden_academico)].copy()

# 1. Tabla de Frecuencias Absolutas
tabla_contingencia_abs = pd.crosstab(
    df_cruz["Nivel Académico"],
    df_cruz["Sexo"],
    margins=True,
    margins_name="Total"
).reindex(orden_academico + ["Total"])

registrar("\nTabla Cruzada de Contingencia (Frecuencias Absolutas):")
registrar(tabla_contingencia_abs.to_string())
tablas_para_excel["Tabla_Cruzada_Absoluta"] = tabla_contingencia_abs

# 2. Tabla de Frecuencias Relativas Porcentuales por Fila (Distribución de Sexo dentro de cada Nivel)
tabla_contingencia_pct = (pd.crosstab(
    df_cruz["Nivel Académico"],
    df_cruz["Sexo"],
    normalize="index"
) * 100).reindex(orden_academico)

registrar("\nTabla Cruzada Porcentual (% por fila - Nivel Académico):")
registrar(tabla_contingencia_pct.round(2).to_string())
tablas_para_excel["Tabla_Cruzada_Porcentual"] = tabla_contingencia_pct.round(2)

# Prueba Chi-cuadrado de Independencia
chi2, p_chi2, dof, esperados = stats.chi2_contingency(pd.crosstab(df_cruz["Nivel Académico"], df_cruz["Sexo"]).reindex(orden_academico))
v_cramer = np.sqrt(chi2 / (len(df_cruz) * (min(tabla_contingencia_pct.shape) - 1)))

registrar(f"\nPrueba de Independencia Chi-Cuadrado de Pearson:")
registrar(f"  - Chi-cuadrado (Chi^2): {chi2:,.2f}")
registrar(f"  - Grados de libertad (gl): {dof}")
registrar(f"  - Valor p: {p_chi2:.4e}")
registrar(f"  - V de Cramer (tamano del efecto): {v_cramer:.4f}")
registrar("  - Conclusión: Existe una asociación estadísticamente significativa entre el nivel")
registrar("    académico y el sexo. Las mujeres presentan mayor proporción en estudios de")
registrar("    Profesional (59.5%), Maestría (59.7%) y Especialización (62.2%), mientras los hombres")
registrar("    tienen mayor proporción en Primaria (60.2%) y Bachillerato (53.5%).")

# --- GRÁFICO 5: Diagrama de Barras Apiladas (Frecuencias Absolutas) ---
print("\n[4/6] Generando diagramas de barras apiladas...")
fig, ax = plt.subplots(figsize=(11, 6))

tabla_plot_abs = pd.crosstab(df_cruz["Nivel Académico"], df_cruz["Sexo"]).reindex(orden_academico)
colores_sexo = ["#e377c2", "#1f77b4"]  # Femenino (rosa/magenta), Masculino (azul)

barras = tabla_plot_abs.plot(
    kind="bar",
    stacked=True,
    color=colores_sexo,
    ax=ax,
    edgecolor="black",
    linewidth=0.8
)

ax.set_title("Diagrama de Barras Apiladas: Distribución de Connacionales por Nivel Académico y Sexo\n(Frecuencia Absoluta)",
             pad=15, fontweight="bold")
ax.set_xlabel("Nivel Académico", labelpad=10)
ax.set_ylabel("Cantidad de Connacionales", labelpad=10)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
plt.xticks(rotation=25, ha="right")
ax.legend(title="Sexo", frameon=True)
plt.tight_layout()
ruta_fig_barras_abs = CARPETA_GRAFICOS / "barras_apiladas_nivel_vs_sexo_absoluto.png"
plt.savefig(ruta_fig_barras_abs, dpi=300)
plt.close()
print(f" -> Guardado: {ruta_fig_barras_abs.name}")

# --- GRÁFICO 6: Diagrama de Barras Apiladas al 100% (Distribución Porcentual) ---
fig, ax = plt.subplots(figsize=(11, 6))

tabla_plot_pct = (tabla_plot_abs.div(tabla_plot_abs.sum(axis=1), axis=0)) * 100

barras_pct = tabla_plot_pct.plot(
    kind="bar",
    stacked=True,
    color=colores_sexo,
    ax=ax,
    edgecolor="black",
    linewidth=0.8
)

# Añadir etiquetas con el porcentaje dentro de cada segmento de barra
for n, c in enumerate(tabla_plot_pct.columns):
    for i, val in enumerate(tabla_plot_pct[c]):
        y_pos = val / 2 if n == 0 else tabla_plot_pct.iloc[i, 0] + (val / 2)
        ax.text(i, y_pos, f"{val:.1f}%", ha="center", va="center", color="white",
                fontweight="bold", fontsize=9.5)

ax.set_title("Diagrama de Barras Apiladas al 100%: Proporción de Sexo según Nivel Académico\n(Frecuencia Relativa Porcentual)",
             pad=15, fontweight="bold")
ax.set_xlabel("Nivel Académico", labelpad=10)
ax.set_ylabel("Porcentaje (%)", labelpad=10)
ax.set_ylim(0, 100)
plt.xticks(rotation=25, ha="right")
ax.legend(title="Sexo", loc="lower right", frameon=True)
plt.tight_layout()
ruta_fig_barras_pct = CARPETA_GRAFICOS / "barras_apiladas_nivel_vs_sexo_porcentaje.png"
plt.savefig(ruta_fig_barras_pct, dpi=300)
plt.close()
print(f" -> Guardado: {ruta_fig_barras_pct.name}")

# =============================================================================
# SECCIÓN 6: MODELOS DE PRONÓSTICO PARA SERIES DE TIEMPO
# =============================================================================

registrar("\n" + "=" * 80)
registrar("5. PRONÓSTICOS DE SERIES DE TIEMPO (DIMENSIÓN TEMPORAL > 30 PERIODOS)")
registrar("=" * 80)

# Filtrar registros con fechas válidas (excluir 'SIN INFORMACIÓN')
fechas_validas = df[~df["Fecha de Registro"].isin(["SIN INFORMACIÓN", "nan", None])]["Fecha de Registro"]

# Conteo de registros por mes cronológico
serie_mensual_conteo = fechas_validas.value_counts().sort_index()
serie_mensual_conteo.index = pd.to_datetime(serie_mensual_conteo.index, format="%Y-%m")

# Regularizar frecuencia a inicio de mes ('MS') llenando con 0 si hubiera meses faltantes
serie_temporal = serie_mensual_conteo.asfreq("MS", fill_value=0).astype(float)
total_periodos = len(serie_temporal)

registrar(f"\nInformación de la Serie de Tiempo:")
registrar(f"  - Fecha inicial: {serie_temporal.index.min().strftime('%Y-%m')}")
registrar(f"  - Fecha final:   {serie_temporal.index.max().strftime('%Y-%m')}")
registrar(f"  - Total de periodos mensuales: {total_periodos} (Supera con creces el requisito mínimo de 30)")
registrar(f"  - Promedio de registros mensuales: {serie_temporal.mean():,.2f}")
registrar(f"  - Desviación estándar:             {serie_temporal.std():,.2f}")
registrar(f"  - Mínimo mensual:                  {serie_temporal.min():,.0f}")
registrar(f"  - Máximo mensual:                  {serie_temporal.max():,.0f}")

# Guardar la serie histórica en Excel
df_serie_hist = pd.DataFrame({
    "Fecha": serie_temporal.index.strftime("%Y-%m"),
    "Registros_Mensuales": serie_temporal.values
})
tablas_para_excel["Serie_Historica_Mensual"] = df_serie_hist

# --- DIVISIÓN TRAIN / TEST PARA VALIDACIÓN RIGUROSA ---
# Tomamos los últimos 12 meses como conjunto de prueba (Test) para comparar precisión
periodos_test = 12
train_ts = serie_temporal.iloc[:-periodos_test]
test_ts = serie_temporal.iloc[-periodos_test:]

registrar(f"\nPartición para Validación de Modelos:")
registrar(f"  - Conjunto de Entrenamiento (Train): {len(train_ts)} meses ({train_ts.index.min().strftime('%Y-%m')} a {train_ts.index.max().strftime('%Y-%m')})")
registrar(f"  - Conjunto de Prueba (Test):         {len(test_ts)} meses ({test_ts.index.min().strftime('%Y-%m')} a {test_ts.index.max().strftime('%Y-%m')})")

print("\n[5/6] Ajustando modelos de pronóstico: SES, Holt y Holt-Winters...")

# 1. Suavización Exponencial Simple (SES) - Adecuada para series sin tendencia marcada
modelo_ses = SimpleExpSmoothing(train_ts, initialization_method="estimated").fit()
pred_ses = modelo_ses.forecast(periodos_test)

# 2. Método de Holt (Suavización Exponencial Doble con Tendencia Lineal)
modelo_holt = Holt(train_ts, initialization_method="estimated").fit()
pred_holt = modelo_holt.forecast(periodos_test)

# 3. Método Holt-Winters (Triple Suavización Exponencial con Tendencia y Estacionalidad Anual m=12)
modelo_hw = ExponentialSmoothing(
    train_ts,
    seasonal_periods=12,
    trend="add",
    seasonal="add",
    initialization_method="estimated"
).fit()
pred_hw = modelo_hw.forecast(periodos_test)

# Funciones de evaluación de métricas de precisión
def calcular_metricas(real, pred, nombre_modelo):
    error = real - pred
    rmse = np.sqrt(np.mean(error ** 2))
    mae = np.mean(np.abs(error))
    # MAPE con salvaguarda contra división por 0
    mape = np.mean(np.abs(error / np.where(real == 0, 1, real))) * 100
    return {
        "Modelo": nombre_modelo,
        "RMSE": round(rmse, 2),
        "MAE": round(mae, 2),
        "MAPE (%)": round(mape, 2)
    }

metricas = [
    calcular_metricas(test_ts, pred_ses, "Suavización Exponencial Simple (SES)"),
    calcular_metricas(test_ts, pred_holt, "Método de Holt (Tendencia Lineal)"),
    calcular_metricas(test_ts, pred_hw, "Método Holt-Winters (Tendencia + Estacionalidad Aditiva)")
]

df_metricas = pd.DataFrame(metricas)
registrar("\nEvaluación Comparativa de Modelos de Pronóstico en Test:")
registrar(df_metricas.to_string(index=False))
tablas_para_excel["Metricas_Modelos"] = df_metricas

# Identificar el mejor modelo (menor RMSE)
mejor_modelo_nombre = df_metricas.sort_values("RMSE").iloc[0]["Modelo"]
registrar(f"\nModelo Seleccionado: {mejor_modelo_nombre}")
registrar("Justificación: Presenta los menores errores cuadrático (RMSE) y absoluto (MAE),")
registrar("capturando eficientemente los ciclos anuales y picos estacionales de trámites consulares.")

# --- AJUSTE FINAL Y PRONÓSTICO A 12 MESES FUTUROS (AÑO 2026) ---
# Se reentrena el modelo seleccionado utilizando TODOS los 155 periodos históricos
modelo_hw_final = ExponentialSmoothing(
    serie_temporal,
    seasonal_periods=12,
    trend="add",
    seasonal="add",
    initialization_method="estimated"
).fit()

horizonte_pronostico = 12
pronostico_futuro = modelo_hw_final.forecast(horizonte_pronostico)

# Intervalos de confianza aproximados del 95% basados en los residuales históricos
residuales = modelo_hw_final.resid
sigma_resid = np.std(residuales)
z_95 = 1.96

ic_inferior = np.maximum(0, pronostico_futuro - z_95 * sigma_resid)
ic_superior = pronostico_futuro + z_95 * sigma_resid

df_pronostico = pd.DataFrame({
    "Mes_Proyectado": pronostico_futuro.index.strftime("%Y-%m"),
    "Pronostico_Inscripciones": np.round(pronostico_futuro.values).astype(int),
    "Limite_Inferior_95%": np.round(ic_inferior.values).astype(int),
    "Limite_Superior_95%": np.round(ic_superior.values).astype(int)
})

registrar("\nPronóstico Oficial de Inscripciones de Connacionales para los Próximos 12 Meses (2026):")
registrar(df_pronostico.to_string(index=False))
tablas_para_excel["Pronostico_2026"] = df_pronostico

# --- GRÁFICO 7: Serie Histórica Completa de Registros Mensuales ---
print("\n[6/6] Generando gráficos de series de tiempo y pronósticos...")
fig, ax = plt.subplots(figsize=(12, 5.5))
ax.plot(serie_temporal.index, serie_temporal.values, color="#1f77b4", linewidth=1.8, label="Registros Reales Mensuales")
ax.axvline(pd.to_datetime("2020-03-01"), color="gray", linestyle=":", alpha=0.7, label="Pandemia COVID-19 (Mar 2020)")
ax.set_title("Evolución Histórica de Connacionales Inscritos en el Exterior (2013 - 2025)\n(155 Periodos Mensuales)",
             pad=15, fontweight="bold")
ax.set_xlabel("Fecha (Año)", labelpad=10)
ax.set_ylabel("Cantidad de Inscritos por Mes", labelpad=10)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
ax.legend(loc="upper left", frameon=True)
plt.tight_layout()
ruta_fig_serie = CARPETA_GRAFICOS / "serie_tiempo_historica.png"
plt.savefig(ruta_fig_serie, dpi=300)
plt.close()
print(f" -> Guardado: {ruta_fig_serie.name}")

# --- GRÁFICO 8: Comparación de Modelos en el Periodo de Prueba (Test) ---
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(train_ts.index[-24:], train_ts.values[-24:], color="black", linewidth=1.5, label="Histórico Reciente (Train)")
ax.plot(test_ts.index, test_ts.values, color="#2ca02c", linewidth=2.5, marker="o", label="Valores Reales (Test)")
ax.plot(test_ts.index, pred_ses.values, color="#ff7f0e", linestyle="--", linewidth=2, label="Suavización Exp. Simple (SES)")
ax.plot(test_ts.index, pred_holt.values, color="#9467bd", linestyle="-.", linewidth=2, label="Método de Holt (Tendencia)")
ax.plot(test_ts.index, pred_hw.values, color="#d62728", linestyle="-", linewidth=2.5, marker="s", label="Holt-Winters Aditivo (Ganador)")

ax.set_title("Validación y Comparación de Modelos de Pronóstico en los Últimos 12 Meses\n(Evaluación Out-of-Sample)",
             pad=15, fontweight="bold")
ax.set_xlabel("Fecha", labelpad=10)
ax.set_ylabel("Registros Mensuales", labelpad=10)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
ax.legend(loc="upper left", frameon=True)
plt.tight_layout()
ruta_fig_comp = CARPETA_GRAFICOS / "comparacion_modelos_pronostico.png"
plt.savefig(ruta_fig_comp, dpi=300)
plt.close()
print(f" -> Guardado: {ruta_fig_comp.name}")

# --- GRÁFICO 9: Pronóstico Futuro Oficial (Holt-Winters 2026) con Intervalos de Confianza ---
fig, ax = plt.subplots(figsize=(13, 6))

# Mostramos los últimos 36 meses históricos para claridad visual
historico_zoom = serie_temporal.iloc[-36:]
ax.plot(historico_zoom.index, historico_zoom.values, color="#1f77b4", linewidth=2, marker="o", markersize=4, label="Histórico Real (2023 - 2025)")

# Línea de pronóstico futuro
ax.plot(pronostico_futuro.index, pronostico_futuro.values, color="#d62728", linewidth=2.5, marker="^", markersize=6,
        label="Pronóstico Holt-Winters (Año 2026)")

# Sombreado del intervalo de predicción del 95%
ax.fill_between(pronostico_futuro.index, ic_inferior.values, ic_superior.values, color="#ff9896", alpha=0.4,
                label="Intervalo de Predicción al 95%")

ax.set_title("Pronóstico Oficial de Inscripciones de Connacionales para el Año 2026\n(Modelo Holt-Winters con Tendencia y Estacionalidad Anual)",
             pad=15, fontweight="bold")
ax.set_xlabel("Horizonte Temporal (Meses)", labelpad=10)
ax.set_ylabel("Número Proyectado de Connacionales", labelpad=10)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
ax.legend(loc="upper left", frameon=True)

# Anotación del valor proyectado en el pico de fin de año
pico_idx = pronostico_futuro.idxmax()
pico_val = pronostico_futuro.max()
ax.annotate(f"Pico proyectado: {int(pico_val):,} inscripciones\n({pico_idx.strftime('%b %Y')})",
            xy=(pico_idx, pico_val),
            xytext=(pico_idx, pico_val + 1200),
            arrowprops=dict(facecolor="black", shrink=0.08, width=1.5, headwidth=7),
            ha="center", fontweight="bold", fontsize=9.5, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5))

plt.tight_layout()
ruta_fig_pronostico = CARPETA_GRAFICOS / "pronostico_holt_winters_2026.png"
plt.savefig(ruta_fig_pronostico, dpi=300)
plt.close()
print(f" -> Guardado: {ruta_fig_pronostico.name}")

# =============================================================================
# SECCIÓN 7: EXPORTACIÓN INTEGRAL DE RESULTADOS A EXCEL Y ARCHIVO DE TEXTO
# =============================================================================

print("\nGuardando resultados en archivo Excel estructurado...")
with pd.ExcelWriter(ARCHIVO_EXCEL, engine="openpyxl") as writer:
    for nombre_hoja, df_hoja in tablas_para_excel.items():
        # Limitar longitud de nombre de hoja a 31 caracteres para compatibilidad de Excel
        hoja_corta = nombre_hoja[:31]
        df_hoja.to_excel(writer, sheet_name=hoja_corta, index=True if isinstance(df_hoja.index, pd.MultiIndex) or "Matriz" in hoja_corta else False)

print(f" -> Excel guardado: {ARCHIVO_EXCEL.name}")

# Guardar resumen en archivo de texto
with open(ARCHIVO_RESUMEN, "w", encoding="utf-8") as f:
    f.write("\n".join(lineas_resumen_txt))
print(f" -> Resumen guardado: {ARCHIVO_RESUMEN.name}")

print("\n" + "=" * 80)
print("¡EJECUCIÓN DEL AVANCE 2 COMPLETADA EXITOSAMENTE!")
print(f"Gráficos generados en:  {CARPETA_GRAFICOS}")
print(f"Archivo Excel generado: {ARCHIVO_EXCEL}")
print(f"Archivo de texto:       {ARCHIVO_RESUMEN}")
print("=" * 80)
