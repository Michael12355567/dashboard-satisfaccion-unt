# Auditoría metodológica — Word + Excel + Dashboard

## 1. Qué mide el indicador

El indicador es el **porcentaje de estudiantes de pregrado satisfechos con su formación académica integral**.

## 2. Regla global correcta

La satisfacción general se obtiene con **P17**:

- 4 o 5: satisfecho.
- 1, 2 o 3: no satisfecho.

Por tanto, el indicador global es:

**5,482 / 7,677 × 100 = 71.4%**.

El nivel de interpretación del porcentaje es **Regular**, porque 71.4% cae en el intervalo 60% a <75%.

## 3. Regla dimensional correcta

No se promedian porcentajes de preguntas. Primero se calcula, para cada estudiante, el promedio de los cuatro ítems de la dimensión. Si ese promedio es >=4, el estudiante se clasifica como satisfecho en esa dimensión. Después se calcula N/D × 100.

Resultados:

- D1: 4,222 / 7,677 = 55.0% — Insatisfactorio.
- D2: 4,647 / 7,677 = 60.5% — Regular.
- D3: 3,182 / 7,677 = 41.4% — Insatisfactorio.
- D4: 4,989 / 7,677 = 65.0% — Regular.

## 4. Regla por pregunta

En P1–P17:

- Satisfechos = respuestas 4 y 5.
- No satisfechos = respuestas 1, 2 y 3.

La respuesta 3 conserva el texto “Ni de acuerdo ni en desacuerdo” únicamente en el detalle de la escala Likert; no se convierte en una tercera categoría del indicador.

## 5. Qué significan los rangos 0–59 / 60–74 / 75–89 / 90–100

Son **criterios de interpretación del porcentaje de satisfacción** incluidos en la propuesta del instrumento. No son categorías de respuesta y tampoco son puntos de corte descubiertos estadísticamente en el Excel.

Para porcentajes con decimales se implementan sin huecos: <60%, 60–<75%, 75–<90% y >=90%.

## 6. Auditoría del Excel

- 7,677 registros.
- 130,509 respuestas P1–P17 esperadas.
- 0 faltantes.
- 0 respuestas fuera de 1–5.
- Los promedios D1–D4 del Excel coinciden con los recalculados.
- D1_Satisfecho, D2_Satisfecho, D3_Satisfecho y D4_Satisfecho coinciden con la regla promedio >=4.
- Global_Satisfecho y Categoria_Global coinciden con P17.
- Promedio_P1_P16 también está correctamente calculado en el Excel, pero **no se usa como sustituto del indicador global**, porque el instrumento define la satisfacción general mediante P17.

## 7. Decisiones de diseño del dashboard

Se eliminan:

- Favorable / Neutral / Desfavorable.
- Marco documental / PEI.
- Semáforos ambiguos.
- El promedio P1–P16 como resultado global.
- Pruebas estadísticas adicionales del tablero principal.

Se conserva:

- Resultado global P17.
- D1–D4 con promedio individual >=4.
- Un resultado separado para cada pregunta P1–P17.
- La distribución original 1–5 solo como detalle desplegable.
- La escala de interpretación del porcentaje, explicada de forma explícita.
