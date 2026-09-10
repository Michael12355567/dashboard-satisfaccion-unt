# Dashboard UNT — corrección KeyError

Esta versión conserva el diseño y la jerarquía visual de la versión anterior.

Corrección aplicada:
- se evita cachear el DataFrame ya transformado;
- Streamlit cachea únicamente la lectura cruda de `basededatos.xlsx`;
- las columnas derivadas (`D1_Sat`–`D4_Sat`, `Integral_P1P16_Prom`, `Integral_P1P16_Sat`, `P17_Sat`) se recalculan en cada ejecución;
- se añadió una versión de esquema a la clave de caché para impedir que sobreviva un resultado antiguo incompatible.

No se modificaron semáforos, fórmula visual, tamaños principales ni el Excel.
