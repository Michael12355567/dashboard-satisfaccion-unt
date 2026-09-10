# Auditoría Word → Excel → Dashboard

## 1. Qué dice el Word

### Escala Likert
1. Totalmente en desacuerdo  
2. En desacuerdo  
3. Ni de acuerdo ni en desacuerdo  
4. De acuerdo  
5. Totalmente de acuerdo

### Criterio de satisfacción
El documento indica que se considera satisfecho al estudiante que marca **4 o 5**.

### Dimensiones
- D1 = P1–P4
- D2 = P5–P8
- D3 = P9–P12
- D4 = P13–P16

En cada dimensión, el estudiante se considera satisfecho si su **promedio individual >= 4**.

### Satisfacción general
P17:
- **Satisfecho:** 4 o 5
- **No satisfecho:** 1, 2 o 3

### Criterios institucionales de interpretación
- 0–59%: Insatisfactorio
- 60–74%: Regular
- 75–89%: Satisfactorio
- 90–100%: Muy satisfactorio

Estos rangos interpretan el **porcentaje final**; no son categorías Likert.

## 2. Cómo se adapta al dashboard

- P17 se presenta como indicador global.
- D1–D4 se calculan por promedio individual >=4.
- P1–P16 se muestran por pregunta como:
  - respuestas 4–5, que cumplen el criterio de satisfacción;
  - respuestas 1–3, como complemento descriptivo.
- Solo P17 usa explícitamente en pantalla las etiquetas "Satisfecho / No satisfecho" porque el Word las define de forma literal para la satisfacción general.
- No se usa "Neutral" como categoría del indicador.
- No se usa "Favorable / Neutral / Desfavorable".
- No se usa el promedio P1–P16 como indicador global.
- No se muestra el bloque Marco documental / PEI.

## 3. Verificación del Excel

La base contiene 7,677 registros y P1–P17 están completos y dentro del rango 1–5.

Resultados recalculados:
- P17: 5,482 / 7,677 = 71.4% → Regular.
- D1: 4,222 / 7,677 = 55.0% → Insatisfactorio.
- D2: 4,647 / 7,677 = 60.5% → Regular.
- D3: 3,182 / 7,677 = 41.4% → Insatisfactorio.
- D4: 4,989 / 7,677 = 65.0% → Regular.

Las columnas `D1_Promedio`–`D4_Promedio`, `D1_Satisfecho`–`D4_Satisfecho`, `Global_Satisfecho` y `Categoria_Global` coinciden con el recálculo realizado a partir de las respuestas originales.
