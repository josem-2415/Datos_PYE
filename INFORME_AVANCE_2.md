# INFORME TÉCNICO - AVANCE 2
## PROYECTO DE PROBABILIDAD Y ESTADÍSTICA (CUARTO SEMESTRE)
### ANÁLISIS BIVARIADO Y MODELOS DE PRONÓSTICO PARA SERIES TEMPORALES

---

**Asignatura:** Probabilidad y Estadística  
**Nivel Académico:** Cuarto Semestre  
**Conjunto de Datos:** Registro de Connacionales en el Exterior (Cancillería de Colombia / Datos Abiertos)  
**Población Objetivo:** Connacionales entre 25 y 40 años de edad  
**Tamaño Muestral Analizado:** $N = 590,879$ registros depurados  
**Periodo Temporal:** Febrero de 2013 a Diciembre de 2025 (155 periodos mensuales)  

---

## 1. INTRODUCCIÓN Y OBJETIVOS DEL AVANCE

El presente documento constituye el **Avance 2** del proyecto semestral de Probabilidad y Estadística. Una vez realizada la depuración y el análisis univariado exploratorio en la primera fase, esta entrega tiene como finalidad profundizar en las relaciones intervariables y en la dinámica longitudinal de los datos mediante dos ejes analíticos fundamentales:

1. **Análisis Bivariado (Estadística Descriptiva e Inferencial Bivariada):**
   - Evaluar la correlación lineal de Pearson entre variables cuantitativas, construyendo la matriz de correlación completa e interpretando los coeficientes $r$, el coeficiente de determinación $R^2$, el $p$-valor y los gráficos de dispersión.
   - Contrastar una variable cuantitativa frente a una cualitativa a través de diagramas de caja y bigotes agrupados (*boxplots by groups*), evaluando medidas de posición, dispersión y pruebas de hipótesis (ANOVA).
   - Analizar la interdependencia entre dos variables cualitativas mediante tablas de contingencia (cruzadas) de frecuencias absolutas y relativas marginales, acompañadas de diagramas de barras apiladas y prueba de independencia Chi-cuadrado ($\chi^2$).
2. **Pronósticos de Series de Tiempo:**
   - Comprobar la existencia de una dimensión temporal con más de 30 periodos continuos (el dataset cuenta con 155 periodos mensuales).
   - Implementar y comparar metodologías de pronóstico: Suavización Exponencial Simple (SES), Modelo de Holt (Tendencia Lineal) y Modelo Holt-Winters (Tendencia y Estacionalidad).
   - Evaluar los modelos en un horizonte de validación fuera de muestra (*out-of-sample*) empleando métricas de error: RMSE, MAE y MAPE.
   - Proyectar el comportamiento de inscripciones de connacionales para los próximos 12 meses (año 2026).

---

## 2. CLASIFICACIÓN Y TAXONOMÍA DE LAS VARIABLES

Antes de proceder a los modelos estadísticos, se clasificaron rigurosamente las variables presentes en el conjunto de datos limpio (`Connacionales_limpios.csv`), diferenciando su naturaleza matemática, subtipo y escala de medición:

| # | Nombre de la Variable | Naturaleza | Subtipo | Escala de Medición | Descripción / Valores |
|---|---|---|---|---|---|
| **1** | **Edad (años)** | **Cuantitativa** | Continua / Discreta | De Razón | Edad cumplida del connacional. Rango acotado en el proyecto de 25 a 40 años. |
| **2** | **Cantidad de personas** | **Cuantitativa** | Discreta | De Razón | Conteo de personas declaradas en el trámite consular (Valores enteros: 1 a 5). |
| **3** | **Latitud** *(extraída)* | **Cuantitativa** | Continua | De Intervalo | Coordenada geográfica norte-sur en grados decimales ([-90.0, +90.0]). |
| **4** | **Longitud** *(extraída)* | **Cuantitativa** | Continua | De Intervalo | Coordenada geográfica este-oeste en grados decimales ([-180.0, +180.0]). |
| **5** | **Fecha de Registro** | **Temporal / Cronológica** | Periodo mensual | De Intervalo | Año y mes de inscripción consular (`AAAA-MM`). Abarca 155 meses (2013-02 a 2025-12). Genera la serie temporal $Y_t$. |
| **6** | **Nivel Académico** | **Cualitativa** | Ordinal | Ordinal | Grado de escolaridad alcanzado con orden intrínseco: Primaria < Bachillerato < Técnica < Tecnológica < Profesional < Especialización < Maestría < Doctorado. |
| **7** | **Estado civil** | **Cualitativa** | Nominal | Nominal | Situación conyugal: Soltero, Casado, Unión libre, Divorciado, Separado, Viudo. |
| **8** | **Sexo** | **Cualitativa** | Nominal (Dicotómica) | Nominal | Género registrado: Femenino, Masculino. |
| **9** | **País** | **Cualitativa** | Nominal (Politómica) | Nominal | País de residencia actual en el extranjero (e.g., Estados Unidos, España, etc.). |
| **10** | **Código ISO país** | **Cualitativa** | Nominal | Nominal | Identificador internacional alfanumérico estándar de 3 letras (e.g., USA, ESP, CAN). |
| **11** | **Ciudad de Residencia** | **Cualitativa** | Nominal | Nominal | Ciudad de asentamiento reportada en el país receptor. |
| **12** | **Oficina consular** | **Cualitativa** | Nominal | Nominal | Consulado o misión diplomática que atiende la circunscripción territorial. |
| **13** | **Área Conocimiento** | **Cualitativa** | Nominal | Nominal | Campo profesional o disciplina del saber del connacional. |
| **14** | **Pertenencia étnica** | **Cualitativa** | Nominal | Nominal | Autoidentificación étnica declarada (Indígena, Afrocolombiano, Raizal, Rom, Ninguna). |
| **15** | **Ciudad de Nacimiento** | **Cualitativa** | Nominal | Nominal | Municipio y departamento de origen en Colombia. |

> **Balance del Dataset:** Se identificaron **4 variables cuantitativas individuales**, **1 variable temporal con 155 periodos mensuales**, y **10 variables cualitativas** (9 nominales y 1 ordinal jerarquizada).

---

## 3. ANÁLISIS CON DOS VARIABLES CUANTITATIVAS: CORRELACIÓN DE PEARSON

### 3.1. Fundamentación Teórica
El coeficiente de correlación lineal de Pearson ($r$) cuantifica la fuerza y dirección de una relación lineal entre dos variables continuas $X$ e $Y$:

$$r = \frac{\sum_{i=1}^{n} (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum_{i=1}^{n} (X_i - \bar{X})^2} \sqrt{\sum_{i=1}^{n} (Y_i - \bar{Y})^2}}$$

Donde:
- $r \in [-1, +1]$. Un valor cercano a $+1$ indica correlación lineal positiva perfecta; $-1$ correlación negativa perfecta; y $0$ ausencia de relación lineal.
- $R^2 = r^2$ es el **coeficiente de determinación**, el cual cuantifica la proporción de la varianza de $Y$ explicada linealmente por $X$.
- La significancia estadística se evalúa con el estadístico $t$ bajo $H_0: \rho = 0$:

$$t = r \sqrt{\frac{n - 2}{1 - r^2}} \sim t_{n-2}$$

### 3.2. Matriz de Correlación de Pearson
Dado que se disponen de 4 variables cuantitativas (`Edad`, `Cantidad de personas`, `Latitud`, `Longitud`), se calculó la matriz de correlación completa sobre $N = 590,872$ observaciones completas:

| Variable | Edad (años) | Cantidad de personas | Latitud | Longitud |
|---|:---:|:---:|:---:|:---:|
| **Edad (años)** | **1.00000** | -0.03293 | -0.03873 | -0.00379 |
| **Cantidad de personas** | -0.03293 | **1.00000** | -0.01965 | +0.01050 |
| **Latitud** | -0.03873 | -0.01965 | **1.00000** | -0.02691 |
| **Longitud** | -0.00379 | +0.01050 | -0.02691 | **1.00000** |

*Figura guardada:* `resultados/graficos/matriz_correlacion_pearson.png`

### 3.3. Estudio Detallado: Edad vs Cantidad de Personas
Al seleccionar las dos variables demográficas principales (`Edad` vs `Cantidad de personas`), se obtuvieron los siguientes resultados paramétricos:

- **Coeficiente de correlación ($r$):** $-0.03293$
- **Coeficiente de determinación ($R^2$):** $0.001084$ ($0.1084\%$)
- **Ecuación de Regresión:** $\hat{Y} = -0.0008 \cdot X + 1.033$
- **Valor $p$ ($p$-value):** $1.939 \times 10^{-141}$
- **Tamaño muestral ($N$):** $590,872$

### 3.4. Interpretación Estadística y Académica
1. **Diferenciación entre Significancia Estadística y Significancia Práctica:**
   - Debido a que el tamaño de la muestra es masivo ($N \approx 591,000$), la prueba de hipótesis rechaza la hipótesis nula ($p < 0.0001$). Sin embargo, esto es un efecto clásico del poder estadístico con muestras enormes (*p-value problem*).
   - En términos prácticos y de tamaño del efecto, $|r| = 0.0329 < 0.10$, lo que clasifica la correlación como **prácticamente nula o despreciable**.
2. **Capacidad Explicativa ($R^2$):**
   - El coeficiente $R^2 = 0.11\%$ demuestra que la edad del connacional (en la franja de 25 a 40 años) prácticamente no explica nada de la variabilidad en la cantidad de personas registradas. La inmensa mayoría de las personas se inscribe de manera individual ($1$ persona, $99.4\%$), con independencia de tener 25 o 40 años.
3. **Gráfico de Dispersión:** En `resultados/graficos/dispersion_edad_vs_personas.png` se observa que la línea de tendencia es casi horizontal con una pendiente prácticamente de cero, confirmando la independencia lineal entre ambas magnitudes.

---

## 4. ANÁLISIS BIVARIADO: VARIABLE CUANTITATIVA VS CUALITATIVA (DIAGRAMA DE CAJAS)

### 4.1. Variables Seleccionadas
- **Variable Cuantitativa ($Y$):** `Edad (años)` (Eje Vertical)
- **Variable Cualitativa ($X$):** `Nivel Académico` (Eje Horizontal, ordenado educativamente)
- *Comparación secundaria complementaria:* `Edad (años)` frente a `Estado civil`.

### 4.2. Estadísticas Descriptivas por Grupo Educativo
Se consideraron las 8 categorías formativas ordenadas, abarcando $N = 361,850$ registros con nivel educativo formal reportado:

| Nivel Académico | Registros ($N$) | Media ($\bar{x}$) | Mediana ($Me$) | Desv. Est. ($s$) | Q1 (25%) | Q3 (75%) | IQR | Mínimo | Máximo |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **PRIMARIA** | 13,069 | 33.26 | 34.0 | 4.42 | 30.0 | 37.0 | 7.0 | 25 | 40 |
| **BACHILLERATO** | 158,977 | 32.62 | 33.0 | 4.38 | 29.0 | 36.0 | 7.0 | 25 | 40 |
| **TÉCNICA PROFESIONAL**| 38,778 | 32.92 | 33.0 | 4.26 | 30.0 | 36.0 | 6.0 | 25 | 40 |
| **TECNOLÓGICA** | 20,474 | 32.97 | 33.0 | 4.17 | 30.0 | 36.0 | 6.0 | 25 | 40 |
| **PROFESIONAL** | 94,355 | 33.51 | 34.0 | 4.02 | 30.0 | 37.0 | 7.0 | 25 | 40 |
| **ESPECIALIZACIÓN** | 10,461 | 35.15 | 36.0 | 3.61 | 33.0 | 38.0 | 5.0 | 25 | 40 |
| **MAESTRÍA** | 22,419 | 34.43 | 35.0 | 3.92 | 31.0 | 38.0 | 7.0 | 25 | 40 |
| **DOCTORADO** | 3,288 | 35.64 | 36.0 | 3.49 | 33.0 | 39.0 | 6.0 | 25 | 40 |

*Figuras guardadas:*
- `resultados/graficos/boxplot_edad_por_nivel_academico.png`
- `resultados/graficos/boxplot_edad_por_estado_civil.png`

### 4.3. Prueba de Hipótesis ANOVA de Una Vía
Para verificar si la edad promedio difiere significativamente entre los niveles académicos, se formuló la prueba ANOVA:
- $H_0: \mu_{\text{Prim}} = \mu_{\text{Bach}} = \dots = \mu_{\text{Doc}}$ (Las medias de edad son iguales en todos los niveles).
- $H_1: \text{Al menos una media es diferente}$.

**Resultados del contraste:**
- **Estadístico $F$ de Snedecor:** $F = 1,281.67$
- **Valor $p$:** $p < 1.0 \times 10^{-300}$ (Prácticamente $0.000$)
- **Decisión:** Se rechaza contundentemente $H_0$.

### 4.4. Interpretación del Diagrama de Cajas
1. **Gradiente Formativo de Edad:**
   - Se evidencia un claro incremento en la edad mediana y promedio a medida que se escala en la jerarquía académica: los connacionales con **Bachillerato** registran una media de $32.62$ años ($Me = 33$), mientras que en **Maestría** asciende a $34.43$ años ($Me = 35$) y en **Doctorado** alcanza $35.64$ años ($Me = 36$).
   - Este comportamiento refleja la trayectoria natural del ciclo de vida y formación profesional, donde la culminación de estudios avanzados de cuarto nivel requiere años adicionales de escolarización y experiencia.
2. **Dispersión y Variabilidad (IQR):**
   - El grupo de Doctorado presenta la menor desviación estándar ($s = 3.49$ años) y una caja más compacta, concentrándose fuertemente entre los 33 y 39 años.
   - En contraste, los niveles de Primaria y Bachillerato presentan mayor dispersión ($s \approx 4.4$ años) cubriendo uniformemente todo el rango de 25 a 40 años.
3. **Análisis de Estado Civil (Gráfico Secundario):**
   - Los connacionales **Solteros** son los más jóvenes (media $32.28$ años, $Me = 32$), mientras que los connacionales **Casados** ($\bar{x} = 35.16$ años) y **Divorciados** ($\bar{x} = 36.13$ años) se ubican sistemáticamente en las cohortes superiores del rango etario.

---

## 5. ANÁLISIS BIVARIADO: DOS VARIABLES CUALITATIVAS (TABLA CRUZADA Y BARRAS APILADAS)

### 5.1. Variables Seleccionadas
- **Variable Cualitativa 1:** `Nivel Académico` (Categorías formativas ordenadas)
- **Variable Cualitativa 2:** `Sexo` (Femenino vs Masculino)

### 5.2. Tabla de Contingencia Cruzada (Frecuencias Absolutas)

| Nivel Académico | Femenino | Masculino | Total Nivel |
|---|:---:|:---:|:---:|
| **PRIMARIA** | 5,193 | 7,867 | 13,060 |
| **BACHILLERATO** | 73,972 | 84,960 | 158,932 |
| **TÉCNICA PROFESIONAL** | 22,853 | 15,915 | 38,768 |
| **TECNOLÓGICA** | 10,738 | 9,735 | 20,473 |
| **PROFESIONAL** | 56,154 | 38,182 | 94,336 |
| **ESPECIALIZACIÓN** | 6,503 | 3,958 | 10,461 |
| **MAESTRÍA** | 13,369 | 9,038 | 22,407 |
| **DOCTORADO** | 1,517 | 1,770 | 3,287 |
| **TOTAL** | **190,299** | **171,425** | **361,724** |

### 5.3. Tabla Cruzada Porcentual (Distribución Condicional por Fila)

| Nivel Académico | % Femenino | % Masculino | Total Fila |
|---|:---:|:---:|:---:|
| **PRIMARIA** | 39.76% | **60.24%** | 100.0% |
| **BACHILLERATO** | 46.54% | **53.46%** | 100.0% |
| **TÉCNICA PROFESIONAL** | **58.95%** | 41.05% | 100.0% |
| **TECNOLÓGICA** | **52.45%** | 47.55% | 100.0% |
| **PROFESIONAL** | **59.53%** | 40.47% | 100.0% |
| **ESPECIALIZACIÓN** | **62.16%** | 37.84% | 100.0% |
| **MAESTRÍA** | **59.66%** | 40.34% | 100.0% |
| **DOCTORADO** | 46.15% | **53.85%** | 100.0% |

*Figuras guardadas:*
- `resultados/graficos/barras_apiladas_nivel_vs_sexo_absoluto.png`
- `resultados/graficos/barras_apiladas_nivel_vs_sexo_porcentaje.png`

### 5.4. Prueba Chi-Cuadrado de Independencia
- $H_0$: El Nivel Académico y el Sexo son estadísticamente independientes.
- $H_1$: Existe asociación entre el Nivel Académico y el Sexo.

**Resultados de la prueba:**
- **Estadístico Chi-cuadrado ($\chi^2$):** $6,530.53$
- **Grados de libertad ($gl$):** $(8 - 1) \times (2 - 1) = 7$
- **Valor $p$:** $p < 1.0 \times 10^{-300}$
- **Coeficiente V de Cramér:** $V = 0.1344$ (Asociación moderada-baja pero estadísticamente muy significativa).
- **Decisión:** Se rechaza categóricamente la hipótesis nula de independencia.

### 5.5. Interpretación del Diagrama de Barras Apiladas
1. **Brecha Educativa Femenina Positiva en la Emigración:**
   - El diagrama de barras apiladas al 100% revela un patrón de género sumamente interesante: en los niveles de educación superior universitaria y posgrados, las mujeres ostentan una ventaja proporcional sustancial.
   - En **Especialización**, las mujeres representan el **62.16%** de los connacionales registrados; en **Maestría**, el **59.66%**; y en pregrado **Profesional**, el **59.53%**.
2. **Predominio Masculino en Niveles Básicos:**
   - Por el contrario, los hombres concentran mayores proporciones en los niveles de escolaridad básica: representan el **60.24%** de quienes reportan únicamente **Primaria** y el **53.46%** en **Bachillerato**.
   - En el nivel de **Doctorado**, la participación se equilibra con una ligera ventaja masculina (53.85% vs 46.15%).
3. **Implicación Sociodemográfica:** Las mujeres colombianas entre 25 y 40 años que se radican en el exterior y formalizan su registro consular cuentan con un perfil de cualificación académica superior al promedio masculino, lo cual puede asociarse a procesos de migración calificada por estudios de posgrado o inserción laboral técnica especializada.

---

## 6. PRONÓSTICOS DE SERIES DE TIEMPO

### 6.1. Validación de la Dimensión Temporal
La variable `Fecha de Registro` permite agregar las inscripciones en intervalos mensuales discretos desde **Febrero de 2013** hasta **Diciembre de 2025**:
- **Número total de periodos mensuales:** **155 meses continuos** ($T = 155$).
- **Requisito del avance:** Mínimo 30 periodos en el tiempo.
- **Cumplimiento:** El dataset excede ampliamente la condición requerida ($155 > 30$, más de 5 veces el umbral estipulado).

*Figura guardada:* `resultados/graficos/serie_tiempo_historica.png`

### 6.2. Metodologías de Pronóstico Implementadas
Se programaron y evaluaron tres métodos formales de suavización y series temporales:

#### 1. Suavización Exponencial Simple (SES)
Modela series con nivel local constante y sin tendencia pronunciada:
$$\hat{Y}_{t+1} = \alpha Y_t + (1 - \alpha) \hat{Y}_t, \quad \alpha \in (0, 1)$$

#### 2. Método de Holt (Suavización Exponencial Doble)
Incorpora una ecuación para el nivel ($l_t$) y otra para la pendiente o tendencia lineal ($b_t$):
$$l_t = \alpha Y_t + (1 - \alpha)(l_{t-1} + b_{t-1})$$
$$b_t = \beta (l_t - l_{t-1}) + (1 - \beta) b_{t-1}$$
$$\hat{Y}_{t+h} = l_t + h b_t$$

#### 3. Método Holt-Winters (Triple Suavización Exponencial con Estacionalidad)
Captura el nivel ($l_t$), la tendencia ($b_t$) y el patrón estacional recurrente de ciclo anual ($s_t$, con periodo estacional $m = 12$ meses):
$$l_t = \alpha (Y_t - s_{t-m}) + (1 - \alpha)(l_{t-1} + b_{t-1})$$
$$b_t = \beta (l_t - l_{t-1}) + (1 - \beta) b_{t-1}$$
$$s_t = \gamma (Y_t - l_{t-1} - b_{t-1}) + (1 - \gamma) s_{t-m}$$
$$\hat{Y}_{t+h} = l_t + h b_t + s_{t+h-m(k+1)}$$

### 6.3. Validación Fuera de Muestra (*Out-of-Sample*)
Para garantizar una evaluación rigurosa y no incurrir en sobreajuste (*overfitting*), se dividió la serie histórica:
- **Conjunto de Entrenamiento (*Train*):** Primeros 143 meses (2013-02 a 2024-12).
- **Conjunto de Prueba (*Test*):** Últimos 12 meses observados (2025-01 a 2025-12).

Las métricas de error calculadas en el conjunto de prueba fueron:
- **RMSE (Raíz del Error Cuadrático Medio):** $\text{RMSE} = \sqrt{\frac{1}{H} \sum (Y_t - \hat{Y}_t)^2}$
- **MAE (Error Absoluto Medio):** $\text{MAE} = \frac{1}{H} \sum |Y_t - \hat{Y}_t|$
- **MAPE (Error Porcentual Absoluto Medio):** $\text{MAPE} = \frac{100\%}{H} \sum \left|\frac{Y_t - \hat{Y}_t}{Y_t}\right|$

### 6.4. Tabla Comparativa de Rendimiento

| Modelo de Pronóstico | RMSE (Inscripciones) | MAE (Inscripciones) | MAPE (%) | Desempeño / Rango |
|---|:---:|:---:|:---:|:---:|
| **Suavización Exponencial Simple (SES)** | 2,872.10 | 2,001.78 | 113.65% | Modelo base (sin tendencia ni ciclos) |
| **Método de Holt (Tendencia Lineal)** | 2,763.97 | 1,746.58 | 119.94% | Captura crecimiento general |
| **Método Holt-Winters (Tendencia + Estacionalidad Aditiva)** | **2,545.29** | **1,563.89** | **108.74%** | **MEJOR MODELO (Ganador)** |

*Figura guardada:* `resultados/graficos/comparacion_modelos_pronostico.png`

> **Selección del Modelo Óptimo:** El **Método Holt-Winters** superó a los demás algoritmos, reduciendo el RMSE en más de **326 registros mensuales** frente al modelo SES y obteniendo el menor error absoluto medio ($\text{MAE} = 1,563.89$). Su ventaja radica en que es el único modelo capaz de anticipar los picos estacionales de trámites consulares recurrentes en ciertos meses del año.

### 6.5. Pronóstico Oficial para los Próximos 12 Meses (Año 2026)
Habiendo seleccionado el modelo Holt-Winters, se reentrenó con los 155 periodos históricos completos para proyectar los 12 meses del **año 2026**, calculando intervalos de predicción al 95%:

| Mes Proyectado | Pronóstico Puntual ($\hat{Y}_t$) | Límite Inferior (95%) | Límite Superior (95%) | Comportamiento Esperado |
|---|:---:|:---:|:---:|---|
| **2026-01** | 7,191 | 5,023 | 9,358 | Nivel base de inicio de año |
| **2026-02** | 7,399 | 5,232 | 9,566 | Crecimiento moderado |
| **2026-03** | **7,927** | 5,760 | 10,095 | **Pico estacional del primer trimestre** |
| **2026-04** | 6,711 | 4,544 | 8,878 | Descenso post-temporada |
| **2026-05** | 7,073 | 4,906 | 9,240 | Nivel estable de mitad de año |
| **2026-06** | 7,002 | 4,834 | 9,169 | Nivel estable |
| **2026-07** | 7,129 | 4,962 | 9,296 | Incremento vacacional |
| **2026-08** | 7,077 | 4,910 | 9,244 | Estabilidad |
| **2026-09** | 7,388 | 5,221 | 9,555 | Reactivación otoñal/académica |
| **2026-10** | 7,783 | 5,616 | 9,950 | Fase ascendente de cierre |
| **2026-11** | **8,427** | 6,260 | 10,595 | **Pico máximo proyectado del año** |
| **2026-12** | 6,480 | 4,313 | 8,647 | Reducción por receso decembrino |

*Figura guardada:* `resultados/graficos/pronostico_holt_winters_2026.png`

### 6.6. Interpretación Práctica del Pronóstico
1. **Picos de Demanda Consular:**
   - El pronóstico proyecta que el mes con mayor volumen de inscripciones en 2026 será **Noviembre (8,427 connacionales)**, seguido por **Marzo (7,927 connacionales)**.
   - Estos momentos coinciden históricamente con los cierres de vigencias fiscales y trámites previos a convocatorias académicas internacionales y procesos migratorios.
2. **Aplicación para la Gestión Pública:**
   - La Cancillería y las oficinas consulares pueden utilizar estas proyecciones para planificar la capacidad operativa de los servidores web del Registro Ciudadano en Línea y asignar personal de apoyo en las fechas de máxima afluencia estimada.

---

## 7. CONCLUSIONES GENERALES DEL AVANCE 2

1. **Independencia Cuantitativa:** La correlación de Pearson entre la edad y la cantidad de personas registradas es prácticamente inexistente ($r = -0.0329, R^2 = 0.11\%$). Esto comprueba que el comportamiento de registro de grupos familiares en el exterior no depende linealmente de la edad del solicitante en la cohorte analizada.
2. **Diferenciación Educativa por Edad:** La prueba ANOVA ($F = 1,281.67, p < 0.0001$) y los diagramas de cajas confirmaron que a mayor nivel de escolaridad formal (Especialización, Maestría, Doctorado), la mediana de edad se desplaza sistemáticamente hacia los 35-36 años, mientras que los niveles técnicos y de bachillerato se concentran en los 32-33 años.
3. **Liderazgo Femenino en Educación Superior:** La tabla cruzada y el diagrama de barras apiladas al 100% evidenciaron una marcada ventaja femenina en educación superior (más del 59% de los registros en profesional y maestría son mujeres), frente a una mayor concentración masculina en niveles de primaria y bachillerato. La prueba Chi-cuadrado ($\chi^2 = 6,530.53, p < 0.0001$) descartó la independencia entre ambas variables.
4. **Superioridad de Holt-Winters en Pronósticos:** Con 155 periodos mensuales observados, el modelo Holt-Winters capturó exitosamente los componentes de tendencia y estacionalidad anual, logrando el menor error cuadrático ($\text{RMSE} = 2,545.29$) frente a los métodos de suavización simple y lineal. Se proyecta un total aproximado de **88,000 inscripciones de connacionales en 2026**, alcanzando su cúspide en noviembre.

---

## 8. ÍNDICE DE ARCHIVOS Y EVIDENCIAS ENTREGADAS

Todos los recursos se encuentran disponibles en la carpeta del proyecto:
- **Script Principal del Avance:** `avance_2_bivariado_y_pronosticos.py` (código completamente comentado y ejecutable).
- **Libro de Trabajo en Excel:** `resultados/analisis_bivariado_y_pronosticos.xlsx` (con todas las hojas de datos tabuladas: Matriz de correlación, ANOVA, Tablas de contingencia y Proyecciones 2026).
- **Resumen en Texto Plano:** `resultados/resumen_avance_2.txt`.
- **Galería de Gráficos en Alta Resolución (300 DPI):**
  1. `resultados/graficos/matriz_correlacion_pearson.png`
  2. `resultados/graficos/dispersion_edad_vs_personas.png`
  3. `resultados/graficos/boxplot_edad_por_nivel_academico.png`
  4. `resultados/graficos/boxplot_edad_por_estado_civil.png`
  5. `resultados/graficos/barras_apiladas_nivel_vs_sexo_absoluto.png`
  6. `resultados/graficos/barras_apiladas_nivel_vs_sexo_porcentaje.png`
  7. `resultados/graficos/serie_tiempo_historica.png`
  8. `resultados/graficos/comparacion_modelos_pronostico.png`
  9. `resultados/graficos/pronostico_holt_winters_2026.png`
