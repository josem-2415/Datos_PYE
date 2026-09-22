import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import subprocess
import sys


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
SCRIPT_LIMPIEZA = BASE_DIR / "limpieza_datos.py"
ARCHIVO = BASE_DIR / "Connacionales_limpios.csv"

CARPETA_RESULTADOS = BASE_DIR / "resultados"
CARPETA_GRAFICOS = CARPETA_RESULTADOS / "graficos"

CARPETA_RESULTADOS.mkdir(exist_ok=True)
CARPETA_GRAFICOS.mkdir(exist_ok=True)


# ============================================================
# 0. EJECUTAR SCRIPT DE LIMPIEZA AUTOMÁTICAMENTE
# ============================================================

print("=" * 70)
print("EJECUTANDO PREPROCESAMIENTO Y LIMPIEZA DE DATOS...")
print("=" * 70)

try:
    subprocess.run([sys.executable, str(SCRIPT_LIMPIEZA)], check=True)
except Exception as e:
    print(f"\nADVERTENCIA: No se pudo ejecutar automáticamente el script de limpieza: {e}")
    print("Intentando cargar el archivo preprocesado existente...")


# ============================================================
# 1. CARGAR EL ARCHIVO CSV LIMPIO
# ============================================================

print("\n" + "=" * 70)
print("ANÁLISIS ESTADÍSTICO DE CONNACIONALES EN EL EXTERIOR")
print("=" * 70)

try:
    df = pd.read_csv(ARCHIVO, low_memory=False)

except FileNotFoundError:
    print("\nERROR: No se encontró el archivo limpio:")
    print(ARCHIVO)
    print("\nVerifica que el CSV esté en la misma carpeta que main.py.")
    exit()


print("\nArchivo cargado correctamente.")
print(f"Cantidad total de registros: {len(df):,}")


# ============================================================
# 2. MOSTRAR LAS COLUMNAS
# ============================================================

print("\n" + "=" * 70)
print("COLUMNAS DEL ARCHIVO")
print("=" * 70)

for i, columna in enumerate(df.columns, start=1):
    print(f"{i}. {columna}")


# ============================================================
# 3. CONVERTIR EDAD A VARIABLE NUMÉRICA
# ============================================================

df["Edad (años)"] = pd.to_numeric(
    df["Edad (años)"],
    errors="coerce"
)


# ============================================================
# 4. FILTRAR PERSONAS ENTRE 25 Y 40 AÑOS
# ============================================================

df = df[
    (df["Edad (años)"] >= 25) &
    (df["Edad (años)"] <= 40)
].copy()


print("\n" + "=" * 70)
print("FILTRO DE EDAD")
print("=" * 70)

print(
    f"Personas entre 25 y 40 años: {len(df):,}"
)


# ============================================================
# 5. VARIABLES CUANTITATIVAS
# ============================================================

variables_cuantitativas = [
    "Edad (años)"
]


# ============================================================
# 6. ESTADÍSTICAS DESCRIPTIVAS
# ============================================================

estadisticas = []


for variable in variables_cuantitativas:

    datos = df[variable].dropna()

    # Moda
    moda = datos.mode()

    if len(moda) > 0:
        moda = ", ".join(
            str(valor) for valor in moda.tolist()
        )
    else:
        moda = "Sin moda"


    # Estadísticas
    fila = {

        "Variable": variable,

        # Cantidad de datos
        "N": datos.count(),

        # -------------------------------
        # TENDENCIA CENTRAL
        # -------------------------------

        "Media": datos.mean(),

        "Mediana": datos.median(),

        "Moda": moda,

        # -------------------------------
        # POSICIÓN
        # -------------------------------

        "Mínimo": datos.min(),

        "Q1 (25%)": datos.quantile(0.25),

        "Q2 (50%)": datos.quantile(0.50),

        "Q3 (75%)": datos.quantile(0.75),

        "Máximo": datos.max(),

        # Percentiles adicionales

        "Percentil 10": datos.quantile(0.10),

        "Percentil 90": datos.quantile(0.90),

        # -------------------------------
        # DISPERSIÓN
        # -------------------------------

        "Rango": datos.max() - datos.min(),

        "Varianza": datos.var(),

        "Desviación estándar": datos.std(),

        "Coeficiente de variación (%)":
            (datos.std() / datos.mean()) * 100
    }

    estadisticas.append(fila)


tabla_estadisticas = pd.DataFrame(
    estadisticas
)


# ============================================================
# 7. MOSTRAR ESTADÍSTICAS
# ============================================================

print("\n" + "=" * 70)
print("ESTADÍSTICAS DESCRIPTIVAS")
print("=" * 70)

print(
    tabla_estadisticas.to_string(index=False)
)


# ============================================================
# 8. TABLA DE FRECUENCIA PARA EDAD
# ============================================================

print("\n" + "=" * 70)
print("TABLA DE FRECUENCIA - EDAD")
print("=" * 70)


frecuencia_edad = (
    df["Edad (años)"]
    .value_counts()
    .sort_index()
)


tabla_frecuencia_edad = pd.DataFrame({

    "Edad":
        frecuencia_edad.index,

    "Frecuencia absoluta":
        frecuencia_edad.values
})


# Frecuencia relativa

tabla_frecuencia_edad[
    "Frecuencia relativa"
] = (
    tabla_frecuencia_edad[
        "Frecuencia absoluta"
    ]
    /
    tabla_frecuencia_edad[
        "Frecuencia absoluta"
    ].sum()
)


# Porcentaje

tabla_frecuencia_edad[
    "Porcentaje (%)"
] = (
    tabla_frecuencia_edad[
        "Frecuencia relativa"
    ] * 100
)


# Frecuencia acumulada

tabla_frecuencia_edad[
    "Frecuencia acumulada"
] = (
    tabla_frecuencia_edad[
        "Frecuencia absoluta"
    ].cumsum()
)


print(
    tabla_frecuencia_edad.to_string(
        index=False
    )
)


# ============================================================
# 9. VARIABLES CUALITATIVAS
# ============================================================

variables_cualitativas = [

    "País",

    "Ciudad de Residencia",

    "Oficina de circunscripción consular",

    "Área Conocimiento",

    "Nivel Académico",

    "Estado civil",

    "Sexo",

    "Pertenencia étnica",

    "Ciudad de Nacimiento",

    "Localización"
]


# Diccionario donde guardaremos las tablas

tablas_cualitativas = {}


# ============================================================
# 10. CONTEO Y PORCENTAJE
# ============================================================

for variable in variables_cualitativas:

    print("\n" + "=" * 70)
    print(f"VARIABLE CUALITATIVA: {variable}")
    print("=" * 70)


    # Reemplazar valores vacíos

    datos = (
        df[variable]
        .fillna("Sin información")
    )


    # Conteo

    frecuencia = (
        datos
        .value_counts()
    )


    # Porcentaje

    porcentaje = (
        frecuencia
        /
        frecuencia.sum()
    ) * 100


    # Crear tabla

    tabla = pd.DataFrame({

        variable:
            frecuencia.index,

        "Conteo":
            frecuencia.values,

        "Porcentaje (%)":
            porcentaje.values
    })


    # Guardar

    tablas_cualitativas[
        variable
    ] = tabla


    # Mostrar solamente las primeras 20
    # categorías en consola

    print(
        tabla.head(20).to_string(
            index=False
        )
    )


    if len(tabla) > 20:

        print(
            f"\n... y {len(tabla) - 20} "
            "categorías adicionales."
        )


# ============================================================
# 11. GRÁFICO DE BARRAS DE EDAD
# ============================================================

datos_edad = df["Edad (años)"].dropna()


plt.figure(figsize=(10, 6))


plt.bar(
    tabla_frecuencia_edad["Edad"],
    tabla_frecuencia_edad[
        "Frecuencia absoluta"
    ]
)


plt.title(
    "Frecuencia de personas por edad"
)

plt.xlabel(
    "Edad (años)"
)

plt.ylabel(
    "Cantidad de personas"
)


plt.xticks(
    tabla_frecuencia_edad["Edad"]
)


plt.tight_layout()


plt.savefig(
    CARPETA_GRAFICOS /
    "frecuencia_edad.png",
    dpi=300
)


plt.close()


# ============================================================
# 12. HISTOGRAMA DE EDAD
# ============================================================

plt.figure(figsize=(10, 6))


plt.hist(
    datos_edad,
    bins=range(25, 42),
    edgecolor="black"
)


plt.title(
    "Histograma de edades"
)

plt.xlabel(
    "Edad (años)"
)

plt.ylabel(
    "Frecuencia"
)


plt.xticks(
    range(25, 41)
)


plt.tight_layout()


plt.savefig(
    CARPETA_GRAFICOS /
    "histograma_edad.png",
    dpi=300
)


plt.close()


# ============================================================
# 13. CAJA Y BIGOTES
# ============================================================

plt.figure(figsize=(10, 5))


plt.boxplot(
    datos_edad,
    vert=False
)


plt.title(
    "Diagrama de caja y bigotes - Edad"
)

plt.xlabel(
    "Edad (años)"
)


plt.tight_layout()


plt.savefig(
    CARPETA_GRAFICOS /
    "caja_y_bigotes_edad.png",
    dpi=300
)


plt.close()


# ============================================================
# 14. FRECUENCIA ACUMULADA
# ============================================================

plt.figure(figsize=(10, 6))


plt.plot(
    tabla_frecuencia_edad["Edad"],
    tabla_frecuencia_edad[
        "Frecuencia acumulada"
    ],
    marker="o"
)


plt.title(
    "Frecuencia acumulada de edades"
)

plt.xlabel(
    "Edad (años)"
)

plt.ylabel(
    "Frecuencia acumulada"
)


plt.xticks(
    tabla_frecuencia_edad["Edad"]
)


plt.grid(
    True,
    alpha=0.3
)


plt.tight_layout()


plt.savefig(
    CARPETA_GRAFICOS /
    "frecuencia_acumulada.png",
    dpi=300
)


plt.close()


# ============================================================
# 15. GRÁFICOS DE VARIABLES CUALITATIVAS
# ============================================================

for variable in variables_cualitativas:

    tabla = tablas_cualitativas[variable]


    # Tomar las 10 categorías más frecuentes

    tabla_grafico = tabla.head(10)


    plt.figure(figsize=(11, 6))


    plt.bar(
        tabla_grafico[
            variable
        ].astype(str),

        tabla_grafico[
            "Conteo"
        ]
    )


    plt.title(
        f"Distribución de {variable}"
    )

    plt.xlabel(
        variable
    )

    plt.ylabel(
        "Cantidad de personas"
    )


    plt.xticks(
        rotation=45,
        ha="right"
    )


    plt.tight_layout()


    # Crear nombre válido para archivo

    nombre_archivo = (
        variable
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "")
    )


    plt.savefig(
        CARPETA_GRAFICOS /
        f"{nombre_archivo}.png",
        dpi=300
    )


    plt.close()


# ============================================================
# 16. EXPORTAR TODO A EXCEL
# ============================================================

archivo_excel = (
    CARPETA_RESULTADOS /
    "analisis_estadistico.xlsx"
)


with pd.ExcelWriter(
    archivo_excel,
    engine="openpyxl"
) as writer:


    # --------------------------------------------
    # HOJA DE ESTADÍSTICAS CUANTITATIVAS
    # --------------------------------------------

    tabla_estadisticas.to_excel(
        writer,

        sheet_name="Cuantitativas",

        index=False
    )


    # --------------------------------------------
    # HOJA DE FRECUENCIA DE EDAD
    # --------------------------------------------

    tabla_frecuencia_edad.to_excel(
        writer,

        sheet_name="Frecuencia Edad",

        index=False
    )


    # --------------------------------------------
    # VARIABLES CUALITATIVAS
    # --------------------------------------------

    for variable, tabla in tablas_cualitativas.items():

        # Excel permite máximo 31 caracteres
        nombre_hoja = variable[:31]


        tabla.to_excel(
            writer,

            sheet_name=nombre_hoja,

            index=False
        )


# ============================================================
# 17. CREAR UN ARCHIVO TXT CON RESUMEN
# ============================================================

archivo_resumen = (
    CARPETA_RESULTADOS /
    "resumen_estadistico.txt"
)


with open(
    archivo_resumen,
    "w",
    encoding="utf-8"
) as archivo:


    archivo.write(
        "ANÁLISIS ESTADÍSTICO DE CONNACIONALES\n"
    )

    archivo.write(
        "Personas entre 25 y 40 años\n"
    )

    archivo.write(
        "=" * 60 + "\n\n"
    )


    archivo.write(
        f"Cantidad de registros analizados: "
        f"{len(df):,}\n\n"
    )


    archivo.write(
        "ESTADÍSTICAS CUANTITATIVAS\n"
    )

    archivo.write(
        "-" * 60 + "\n"
    )


    archivo.write(
        tabla_estadisticas.to_string(
            index=False
        )
    )


    archivo.write(
        "\n\n"
    )


    archivo.write(
        "TABLA DE FRECUENCIA DE EDAD\n"
    )

    archivo.write(
        "-" * 60 + "\n"
    )


    archivo.write(
        tabla_frecuencia_edad.to_string(
            index=False
        )
    )


# ============================================================
# 18. FINALIZACIÓN
# ============================================================

print("\n")
print("=" * 70)
print("ANÁLISIS TERMINADO CORRECTAMENTE")
print("=" * 70)


print(
    "\nArchivos generados:"
)


print(
    f"\nExcel:"
)

print(
    f"  {archivo_excel}"
)


print(
    f"\nResumen:"
)

print(
    f"  {archivo_resumen}"
)


print(
    f"\nGráficos:"
)

print(
    f"  {CARPETA_GRAFICOS}"
)


print("\n")
print("=" * 70)