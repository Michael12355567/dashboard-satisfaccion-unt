"""Genera un hash Argon2id local, sin mostrar ni guardar la contraseña."""
from getpass import getpass
from argon2 import PasswordHasher

if __name__ == "__main__":
    password = getpass("Contraseña NUEVA para el administrador: ")
    confirm = getpass("Repite la contraseña: ")
    if len(password) < 14 or password != confirm:
        raise SystemExit("La contraseña debe tener 14 caracteres o más y coincidir.")
    print('\nADMIN_PASSWORD_HASH = "' + PasswordHasher().hash(password) + '"')
    print("Copia solo esa línea a los secretos de Streamlit; NO copies tu contraseña a GitHub.")
