"""Comprobación sencilla de las librerías de este proyecto; no conecta a la API."""
import importlib
import importlib.metadata as metadata

for paquete, modulo in [
    ("streamlit", "streamlit"),
    ("requests", "requests"),
    ("pandas", "pandas"),
    ("openpyxl", "openpyxl"),
    ("argon2-cffi", "argon2"),
]:
    importlib.import_module(modulo)
    print(f"OK: {paquete} {metadata.version(paquete)}")

print("Dependencias disponibles. Esto NO confirma la conexión a la URA.")
