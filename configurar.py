"""Asistente LOCAL para crear contraseña de administrador y configurar token URA.
No publica credenciales, ni imprime las entradas privadas.
"""
from pathlib import Path
from getpass import getpass
from argon2 import PasswordHasher
import json
import os
import re
import sys

RUTA = Path(__file__).resolve().parent / ".streamlit" / "secrets.toml"


def main():
    print("\nGESTOR SIRIES UNT — CONFIGURACIÓN LOCAL")
    print("NO utilices aquí una contraseña de tu correo, Windows u otros servicios.")
    print("Solicita un token URA renovado si compartiste uno anteriormente.")
    print("El archivo de secretos permanece SOLO en tu computadora y nunca debe subirse a GitHub.\n")
    if RUTA.exists():
        confirma = input("Ya hay configuración. ¿Reemplazarla? (escribe SI): ").strip()
        if confirma != "SI":
            print("Sin cambios.")
            return
    nombre = input("Elige usuario administrador (4-32 caracteres, letras/números/._-): ").strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9._-]{3,31}", nombre):
        sys.exit("Nombre de usuario no válido.")
    clave = getpass("Crea una CONTRASEÑA NUEVA de mínimo 14 caracteres: ")
    repite = getpass("Repítela: ")
    if clave != repite or len(clave) < 14 or clave.lower() == clave or not any(x.isdigit() for x in clave):
        sys.exit("Las contraseñas no coinciden o no cumplen las condiciones (14 caracteres, mayúscula y número).")
    token = getpass("TOKEN URA RENOVADO (puedes dejar vacío para configurarlo después): ").strip()
    if token and (len(token) < 16 or '\n' in token or '\r' in token):
        sys.exit("Formato de token no esperado. Confirma con la URA.")
    pwd_hash = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2).hash(clave)
    # JSON quoted strings son válidas como cadenas TOML.
    contenido = "# ARCHIVO PRIVADO. NO SUBIR A INTERNET O GITHUB.\n"
    contenido += "ADMIN_USERNAME = " + json.dumps(nombre) + "\n"
    contenido += "ADMIN_PASSWORD_HASH = " + json.dumps(pwd_hash) + "\n"
    contenido += "URA_API_TOKEN = " + json.dumps(token) + "\n"
    contenido += "PERMITIR_EXTRACCION = true\n"  # Solo configuración local explícita.
    RUTA.parent.mkdir(exist_ok=True)
    # Crear atomicamente y con permisos restrictivos donde el sistema lo permite.
    tmp = RUTA.with_suffix(".tmp")
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(contenido)
        os.replace(tmp, RUTA)
        if os.name == "posix":
            os.chmod(RUTA, 0o600)
    finally:
        if tmp.exists():
            tmp.unlink()
    print("\nConfiguración guardada. NO compartas ni subas .streamlit/secrets.toml")
    print("Inicia con: py -m streamlit run app.py")


if __name__ == "__main__":
    main()
