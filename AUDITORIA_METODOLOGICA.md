# Auditoría metodológica Word → Excel → Dashboard

## 1. Qué define el Word

El documento separa tres niveles de lectura:

1. **Ítems P1–P17:** respuestas en escala Likert 1–5.
2. **Dimensiones D1–D4:** satisfacción determinada por el promedio individual de cuatro ítems; promedio >=4 = satisfecho.
3. **Satisfacción general:** P17; 4 o 5 = satisfecho, 1, 2 o 3 = no satisfecho.

Después de clasificar a los estudiantes se calcula el porcentaje N/D × 100. La tabla 0–59 / 60–74 / 75–89 / 90–100 interpreta ese porcentaje resultante.

## 2. Punto crítico: 1, 2 y 3 en las dimensiones

No es correcto decir que una dimensión se calcula sumando directamente todas las respuestas 1, 2 y 3 de sus cuatro preguntas. La unidad de clasificación es el estudiante:

- se promedian sus cuatro respuestas de la dimensión;
- si el promedio >=4, queda clasificado como satisfecho;
- si el promedio <4, queda clasificado como no satisfecho.

Por ejemplo, respuestas 5, 5, 3, 3 producen promedio 4.0 y, por la regla del Word, ese estudiante es satisfecho en la dimensión aunque dos ítems tengan respuesta 3.

## 3. Cómo se interpretan los ítems

El documento formula el indicador “por dimensión y global”; por ello el dashboard no presenta P1–P16 como 16 indicadores institucionales independientes. Para cada ítem se reporta:

- porcentaje de respuestas 4–5;
- porcentaje de respuestas 1–3;
- distribución completa 1, 2, 3, 4, 5;
- promedio del ítem;
- posición descriptiva del ítem dentro de su dimensión.

No se coloca una etiqueta institucional Insatisfactorio/Regular/Satisfactorio/Muy satisfactorio a cada P1–P16. Esa etiqueta se reserva para D1–D4 y P17, que son las medidas definidas por el documento para cálculo dimensional/global.

## 4. Verificación de la base Excel

Registros: 7,677.

La revisión directa de las respuestas P1–P17 confirma que las columnas calculadas del archivo coinciden con las reglas del Word:

- `D1_Promedio`, `D2_Promedio`, `D3_Promedio`, `D4_Promedio`: 0 diferencias.
- `D1_Satisfecho`, `D2_Satisfecho`, `D3_Satisfecho`, `D4_Satisfecho`: 0 diferencias.
- `Global_Satisfecho`: 0 diferencias.
- `Categoria_Global`: coincide con P17 (4–5 satisfecho; 1–3 no satisfecho).

## 5. Resultados institucionales calculados

| Medida | Satisfechos | Porcentaje | Nivel |
|---|---:|---:|---|
| P17 Satisfacción general | 5,482 / 7,677 | 71.4% | Regular |
| D1 Calidad del proceso académico | 4,222 / 7,677 | 55.0% | Insatisfactorio |
| D2 Desempeño docente y estrategias pedagógicas | 4,647 / 7,677 | 60.5% | Regular |
| D3 Servicios y gestión educativa | 3,182 / 7,677 | 41.4% | Insatisfactorio |
| D4 Formación integral y desarrollo personal | 4,989 / 7,677 | 65.0% | Regular |

La clasificación se realiza con el porcentaje sin redondear y luego se muestra redondeado a una decimal.

## 6. Correcciones frente a versiones previas

- Eliminado el supuesto indicador global P1–P16 = 44.6%, porque no está definido como regla global en el Word.
- P17 vuelve a su función documental de satisfacción general, sin presentarlo con una jerarquía tipográfica exagerada.
- Eliminadas las categorías “Favorable / Neutral / Desfavorable”.
- Conservados los semáforos 3D y el diseño tipográfico de la fórmula N/D × 100.
- Eliminado el bloque visual “Marco documental / PEI”.
- Eliminadas del tablero principal pruebas inferenciales que no forman parte de la definición del instrumento.
- Añadida interpretación explícita para cada dimensión y lectura descriptiva para cada ítem.

## 7. Confiabilidad y validez

Alfa de Cronbach en la base:

- P1–P16: ≈0.968
- D1: ≈0.917
- D2: ≈0.942
- D3: ≈0.913
- D4: ≈0.942

Estos resultados describen consistencia interna y no prueban validez. El propio documento señala V de Aiken como siguiente paso; esa prueba requiere evaluaciones de jueces expertos y no puede calcularse a partir de la base de respuestas estudiantiles.
