# UNT | Tablero diagnóstico 2026 de satisfacción académica

Versión final revisada con base en:
- ficha técnica PEI compartida por el usuario;
- propuesta del instrumento de satisfacción;
- base `basededatos.xlsx`.

## Criterios implementados
- 2026 se muestra como diagnóstico / validación, no como medición oficial PEI.
- P17 se usa como resultado global diagnóstico: 4 o 5 = satisfecho.
- D1–D4: satisfecho si el promedio de sus 4 ítems es >= 4.
- P1–P16 >=4 se muestra solo como análisis complementario, no como regla oficial del IND.01.
- La escala 0–59 / 60–74 / 75–89 / 90–100 se rotula como propuesta, porque el documento indica que puede ajustarse.
- El valor referencial PEI >=60% y las metas 2027–2030 se presentan como contexto estratégico, no como meta 2026.

## Ejecutar
```bash
python -m streamlit run app.py
```
