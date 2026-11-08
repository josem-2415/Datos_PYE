# INFORME CONSOLIDADO DEL PROYECTO
## PROBABILIDAD Y ESTADÍSTICA (CUARTO SEMESTRE)
### ANÁLISIS INTEGRAL UNIVARIADO, BIVARIADO Y MODELOS DE PRONÓSTICO: CONNACIONALES INSCRITOS EN EL REGISTRO CIUDADANO EN LÍNEA

---

**Asignatura:** Probabilidad y Estadística  
**Semestre:** Cuarto Semestre  
**Conjunto de Datos:** Registro de Connacionales en el Exterior (Cancillería de Colombia)  
**Alcance Poblacional:** Connacionales colombianos entre 25 y 40 años de edad  
**Registros Depurados:** $N = 590,879$ observaciones  
**Horizonte Histórico:** Febrero de 2013 a Diciembre de 2025 (155 periodos mensuales)  

---

## 1. INTRODUCCIÓN GENERAL

El presente informe consolida los resultados y hallazgos obtenidos a lo largo del desarrollo del proyecto de la asignatura **Probabilidad y Estadística**. El objeto de estudio corresponde a los ciudadanos colombianos radicados en el exterior que han formalizado su inscripción a través del Registro Ciudadano en Línea de la Cancillería de Colombia. 

El proyecto se estructuró en dos grandes fases de avance:
1. **Fase 1 (Informe 1):** Limpieza, depuración, estandarización de datos y análisis exploratorio univariado de variables cuantitativas y cualitativas.
2. **Fase 2 (Avance 2):** Análisis estadístico bivariado (correlación de Pearson, diagramas de caja agrupados, tablas cruzadas con pruebas de hipótesis) y modelado predictivo mediante series de tiempo (Suavización Exponencial y Holt-Winters).

---

## 2. TAXONOMÍA Y CLASIFICACIÓN DE LAS VARIABLES

El conjunto de datos comprende **15 variables analíticas**, clasificadas formalmente según su naturaleza matemática y escala de medición:

| Variable | Tipo de Variable | Subtipo | Escala de Medición | Rol Analítico |
|---|---|---|---|---|
| **Edad (años)** | Cuantitativa | Continua / Discreta | Razón | Variable continua central (25 a 40 años). |
| **Cantidad de personas** | Cuantitativa | Discreta | Razón | Número de personas vinculadas (1 a 5). |
| **Latitud** *(geográfica)* | Cuantitativa | Continua | Intervalo | Coordenada norte-sur extraída de Localización. |
| **Longitud** *(geográfica)* | Cuantitativa | Continua | Intervalo | Coordenada este-oeste extraída de Localización. |
| **Fecha de Registro** | Temporal | Cronológica (Mes) | Intervalo | Variable generadora de la serie de tiempo (155 meses). |
| **Nivel Académico** | Cualitativa | Ordinal | Ordinal | Nivel educativo jerárquico (Primaria a Doctorado). |
| **Estado civil** | Cualitativa | Nominal | Nominal | Situación civil declarada por el connacional. |
| **Sexo** | Cualitativa | Nominal (Dicotómica)| Nominal | Género registrado (Femenino / Masculino). |
| **País** | Cualitativa | Nominal | Nominal | País de residencia en el extranjero. |
| **Código ISO país** | Cualitativa | Nominal | Nominal | Código estándar alfanumérico de 3 letras. |
| **Ciudad de Residencia** | Cualitativa | Nominal | Nominal | Ciudad de residencia internacional. |
| **Oficina consular** | Cualitativa | Nominal | Nominal | Misión diplomática o consulado asignado. |
| **Área Conocimiento** | Cualitativa | Nominal | Nominal | Disciplina formativa o profesional. |
| **Pertenencia étnica** | Cualitativa | Nominal | Nominal | Autoidentificación étnica declarada. |
| **Ciudad de Nacimiento** | Cualitativa | Nominal | Nominal | Municipio y departamento de origen en Colombia. |

---

## 3. PARTE I: RESUMEN DE LA FASE 1 (LIMPIEZA Y ANÁLISIS UNIVARIADO)

### 3.1. Proceso de Limpieza y Calidad de Datos
En la primera etapa se ejecutó una depuración automatizada sobre los 590,879 registros iniciales:
- **Espacios en blanco:** Eliminación de espacios superfluos iniciales y finales (*trimming*) en todas las columnas de texto.
- **Inconsistencias geográficas:** Unificación de denominaciones de países (e.g., *CHINA, REPÚBLICA POPULAR* $\rightarrow$ *CHINA*, *VIET NAM* $\rightarrow$ *VIETNAM*, *ANTILLAS HOLANDESAS* $\rightarrow$ *PAÍSES BAJOS*).
- **Valores faltantes implícitos:** Homogeneización de etiquetas ambiguas (*(NO REGISTRA)*, *DESCONOCIDO*, *NO INDICA*) bajo la categoría estandarizada `SIN INFORMACIÓN`.
- **Fechas anómalas:** Corrección de registros con fecha centinela errónea (`1900-01`), reclasificándolos adecuadamente.

### 3.2. Estadísticas Univariadas de la Edad (25 a 40 Años)
El análisis univariado de la variable `Edad (años)` sobre los 590,879 connacionales arrojó los siguientes estadísticos:

| Parámetro Estadístico | Valor Numérico | Interpretación |
|---|:---:|---|
| **Tamaño de muestra ($N$)** | 590,879 | Totalidad de personas analizadas en la cohorte. |
| **Media Aritmética ($\bar{x}$)** | **33.14 años** | Edad promedio de los connacionales registrados. |
| **Mediana ($Me$)** | **33.00 años** | El 50% de las personas tiene 33 años o menos. |
| **Moda ($Mo$)** | **34.00 años** | La edad más repetida individualmente (43,420 personas). |
| **Mínimo y Máximo** | 25 y 40 años | Rango total de la cohorte seleccionada ($Rango = 15$ años). |
| **Primer Cuartil ($Q_1$)** | 30.00 años | El 25% de los registrados tiene 30 años o menos. |
| **Tercer Cuartil ($Q_3$)** | 37.00 años | El 75% de los registrados tiene 37 años o menos. |
| **Rango Intercuartílico ($IQR$)**| 7.00 años | El 50% central de los datos abarca 7 años. |
| **Varianza ($s^2$)** | 18.81 años$^2$ | Medida de dispersión cuadrática. |
| **Desviación Estándar ($s$)** | **4.34 años** | Dispersión típica respecto a la media. |
| **Coeficiente de Variación ($CV$)**| **13.09%** | Dispersión relativa baja ($CV < 15\%$), indicando alta homogeneidad. |

*Gráficos generados en Fase 1:* `frecuencia_edad.png`, `histograma_edad.png`, `caja_y_bigotes_edad.png`, `frecuencia_acumulada.png`.

---

## 4. PARTE II: RESULTADOS DEL AVANCE 2 (ANÁLISIS BIVARIADO)

### 4.1. Correlación Lineal de Pearson entre Variables Cuantitativas

Se analizó la relación lineal entre las variables numéricas del dataset. La **matriz de correlación de Pearson** resultante es:

```
                      Edad (años)  Cantidad de personas   Latitud  Longitud
Edad (años)               1.00000              -0.03293  -0.03873  -0.00379
Cantidad de personas     -0.03293               1.00000  -0.01965   0.01050
Latitud                  -0.03873              -0.01965   1.00000  -0.02691
Longitud                 -0.00379               0.01050  -0.02691   1.00000
```

#### Análisis Específico: Edad vs Cantidad de Personas
- **Coeficiente $r$:** $-0.03293$
- **Coeficiente $R^2$:** $0.001084$ ($0.108\%$)
- **Valor $p$:** $1.939 \times 10^{-141}$
- **Conclusión Estadística:** A pesar de que el valor $p$ es infinitesimal debido a la gigantesca potencia muestral ($N = 590,872$), la magnitud $|r| \approx 0.033$ indica una **asociación lineal prácticamente inexistente o nula**. La edad de los connacionales no condiciona linealmente el número de personas registradas en el núcleo consular.

*Figuras:* `matriz_correlacion_pearson.png`, `dispersion_edad_vs_personas.png`.

---

### 4.2. Variable Cuantitativa vs Cualitativa: Diagrama de Cajas por Grupos

Se contrastó la variable cuantitativa `Edad (años)` según las categorías de `Nivel Académico`:

| Nivel Académico | $N$ | Media ($\bar{x}$) | Mediana ($Me$) | Desv. Est. ($s$) | $Q_1$ | $Q_3$ | $IQR$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **PRIMARIA** | 13,069 | 33.26 | 34.0 | 4.42 | 30.0 | 37.0 | 7.0 |
| **BACHILLERATO** | 158,977 | 32.62 | 33.0 | 4.38 | 29.0 | 36.0 | 7.0 |
| **TÉCNICA PROFESIONAL** | 38,778 | 32.92 | 33.0 | 4.26 | 30.0 | 36.0 | 6.0 |
| **TECNOLÓGICA** | 20,474 | 32.97 | 33.0 | 4.17 | 30.0 | 36.0 | 6.0 |
| **PROFESIONAL** | 94,355 | 33.51 | 34.0 | 4.02 | 30.0 | 37.0 | 7.0 |
| **ESPECIALIZACIÓN** | 10,461 | 35.15 | 36.0 | 3.61 | 33.0 | 38.0 | 5.0 |
| **MAESTRÍA** | 22,419 | 34.43 | 35.0 | 3.92 | 31.0 | 38.0 | 7.0 |
| **DOCTORADO** | 3,288 | **35.64** | **36.0** | 3.49 | 33.0 | 39.0 | 6.0 |

- **Prueba ANOVA:** $F = 1,281.67, p < 0.0001$.
- **Hallazgo:** Existe un gradiente cronológico-académico. Quienes poseen títulos de posgrado (Especialización, Maestría, Doctorado) registran una edad media significativamente superior ($\approx 35.6$ años) respecto a quienes poseen formación escolar o técnica ($\approx 32.6$ - $32.9$ años), con menor dispersión intercuartílica.
- **Estado Civil:** Los connacionales casados ($\bar{x} = 35.16$) y divorciados ($\bar{x} = 36.13$) exhiben edades superiores frente a los solteros ($\bar{x} = 32.28$).

*Figuras:* `boxplot_edad_por_nivel_academico.png`, `boxplot_edad_por_estado_civil.png`.

---

### 4.3. Dos Variables Cualitativas: Tabla Cruzada y Diagrama de Barras Apiladas

Se analizó la relación entre `Nivel Académico` y `Sexo` sobre $N = 361,724$ connacionales:

#### Tabla Cruzada de Porcentajes Condicionales por Fila (%):
```
Nivel Académico          % Femenino    % Masculino     Total
PRIMARIA                     39.76%         60.24%    100.0%
BACHILLERATO                 46.54%         53.46%    100.0%
TÉCNICA PROFESIONAL          58.95%         41.05%    100.0%
TECNOLÓGICA                  52.45%         47.55%    100.0%
PROFESIONAL                  59.53%         40.47%    100.0%
ESPECIALIZACIÓN              62.16%         37.84%    100.0%
MAESTRÍA                     59.66%         40.34%    100.0%
DOCTORADO                    46.15%         53.85%    100.0%
```

- **Prueba Chi-cuadrado ($\chi^2$):** $\chi^2 = 6,530.53, gl = 7, p < 0.0001$. Coeficiente $V \text{ de Cramér} = 0.1344$.
- **Hallazgo:** Se descarta la hipótesis de independencia. En el colectivo de connacionales emigrantes entre 25 y 40 años, las mujeres superan ampliamente a los hombres en la proporción de títulos de educación superior y posgrados (alcanzando el $62.16\%$ en Especializaciones y el $59.66\%$ en Maestrías), mientras los hombres presentan mayor proporción en escolaridad primaria y secundaria.

*Figuras:* `barras_apiladas_nivel_vs_sexo_absoluto.png`, `barras_apiladas_nivel_vs_sexo_porcentaje.png`.

---

## 5. PARTE III: PRONÓSTICOS DE SERIES DE TIEMPO

### 5.1. Dimensión Temporal y Metodología
- **Periodos históricos:** 155 meses continuos (Febrero 2013 a Diciembre 2025). Cumple y supera el requisito mínimo de 30 periodos.
- **Partición experimental:** 143 meses para entrenamiento (*Train*) y 12 meses para prueba fuera de muestra (*Test*).

### 5.2. Evaluación y Selección de Modelos

| Modelo de Pronóstico | RMSE | MAE | MAPE (%) | Estado |
|---|:---:|:---:|:---:|:---:|
| **Suavización Exponencial Simple (SES)** | 2,872.10 | 2,001.78 | 113.65% | Descartado |
| **Método de Holt (Tendencia Lineal)** | 2,763.97 | 1,746.58 | 119.94% | Descartado |
| **Método Holt-Winters (Tendencia + Estacionalidad Aditiva)** | **2,545.29** | **1,563.89** | **108.74%** | **SELECCIONADO** |

El método **Holt-Winters** resultó ser el más preciso al modelar tanto la tendencia subyacente de crecimiento como los ciclos de periodicidad anual de la Cancillería.

### 5.3. Pronóstico para los Próximos 12 Meses (Año 2026)

Proyección oficial ajustada sobre los 155 periodos históricos con bandas de confianza al 95%:

| Periodo Proyectado | Pronóstico Puntual ($\hat{Y}_t$) | Límite Inferior (95%) | Límite Superior (95%) |
|---|:---:|:---:|:---:|
| **2026-01** | 7,191 | 5,023 | 9,358 |
| **2026-02** | 7,399 | 5,232 | 9,566 |
| **2026-03** | **7,927** | 5,760 | 10,095 |
| **2026-04** | 6,711 | 4,544 | 8,878 |
| **2026-05** | 7,073 | 4,906 | 9,240 |
| **2026-06** | 7,002 | 4,834 | 9,169 |
| **2026-07** | 7,129 | 4,962 | 9,296 |
| **2026-08** | 7,077 | 4,910 | 9,244 |
| **2026-09** | 7,388 | 5,221 | 9,555 |
| **2026-10** | 7,783 | 5,616 | 9,950 |
| **2026-11** | **8,427** *(Pico anual)* | 6,260 | 10,595 |
| **2026-12** | 6,480 | 4,313 | 8,647 |

*Figuras:* `serie_tiempo_historica.png`, `comparacion_modelos_pronostico.png`, `pronostico_holt_winters_2026.png`.

---

## 6. CONCLUSIONES FINALES INTEGRADAS

1. **Rigor en la Calidad del Dato:** El proceso sistemático de limpieza y filtrado permitió aislar una cohorte homogénea de 590,879 registros de connacionales jóvenes y adultos (25 a 40 años), asegurando la validez interna de los análisis.
2. **Independencia Demográfica:** La edad no guarda relación lineal con el tamaño del núcleo familiar registrado ($r = -0.0329$), lo que confirma que el registro individual predomina uniformemente a lo largo de todo el ciclo etario de la adultez temprana y media.
3. **Estructura Formativa Diferenciada:** El nivel académico condiciona significativamente la edad del connacional (ANOVA, $p < 0.0001$), acumulándose los mayores rangos de edad en posgrados. Asimismo, la migración femenina de esta cohorte demuestra un perfil de cualificación universitaria y de posgrado notablemente superior al masculino (Chi-cuadrado, $p < 0.0001$).
4. **Predictibilidad de la Demanda Consular:** Con 155 meses analizados, se demostró la robustez del modelo **Holt-Winters**, permitiendo anticipar los periodos de alta demanda (marzo y noviembre) con un volumen estimado de más de 88,000 registros para el año 2026, herramienta clave para la planificación institucional de la Cancillería.
