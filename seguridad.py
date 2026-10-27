"""Autenticación local de un usuario y bloqueo simple de intentos.
No sustituye a SSO/MFA ni a un control perimetral para publicación en internet.
"""
from __future__ import annotations
import sqlite3
import time
from pathlib import Path
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

BASE = Path(__file__).resolve().parent
DB = BASE / "datos_locales" / "seguridad.sqlite3"
HASHER = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2)
MAX_FAILURES = 5
LOCK_SECONDS = 15 * 60
WINDOW_SECONDS = 15 * 60


def _conexion():
    DB.parent.mkdir(exist_ok=True)
    db = sqlite3.connect(DB, timeout=10)
    db.execute("PRAGMA busy_timeout=10000")
    db.execute("""CREATE TABLE IF NOT EXISTS intentos (
      usuario TEXT PRIMARY KEY, fallos INTEGER NOT NULL,
      desde REAL NOT NULL, bloqueado_hasta REAL NOT NULL
    )""")
    db.execute("""CREATE TABLE IF NOT EXISTS bitacora (
      fecha_utc TEXT NOT NULL, usuario TEXT NOT NULL, accion TEXT NOT NULL,
      descripcion TEXT NOT NULL
    )""")
    db.commit()
    return db


def bloqueado(usuario: str) -> int:
    with _conexion() as db:
        fila = db.execute("SELECT bloqueado_hasta FROM intentos WHERE usuario = ?", (usuario,)).fetchone()
    faltan = (fila[0] - time.time()) if fila else 0
    return max(0, int(faltan + 0.99))


def fallo(usuario: str) -> None:
    actual = time.time()
    with _conexion() as db:
        db.execute("BEGIN IMMEDIATE")
        fila = db.execute("SELECT fallos, desde, bloqueado_hasta FROM intentos WHERE usuario = ?", (usuario,)).fetchone()
        if fila and fila[2] > actual:
            return
        n = fila[0] + 1 if fila and actual - fila[1] <= WINDOW_SECONDS else 1
        desde = fila[1] if fila and actual - fila[1] <= WINDOW_SECONDS else actual
        hasta = actual + LOCK_SECONDS if n >= MAX_FAILURES else 0
        db.execute("INSERT OR REPLACE INTO intentos VALUES (?, ?, ?, ?)", (usuario, n, desde, hasta))


def verificar(usuario: str, clave: str, usuario_esperado: str, hash_esperado: str) -> bool:
    # Siempre calcular hash de verificación para evitar diferencias evidentes de tiempo.
    if bloqueado(usuario):
        return False
    try:
        correcto = HASHER.verify(hash_esperado, clave)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        correcto = False
    valido = correcto and usuario == usuario_esperado
    if valido:
        with _conexion() as db:
            db.execute("DELETE FROM intentos WHERE usuario = ?", (usuario,))
        return True
    fallo(usuario)
    return False


def registrar(usuario: str, accion: str, descripcion: str) -> None:
    # Solo metadatos: nunca tokens, contraseñas ni contenidos individuales.
    with _conexion() as db:
        from datetime import datetime, timezone
        db.execute("INSERT INTO bitacora VALUES (?, ?, ?, ?)",
                   (datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    usuario[:40], accion[:40], descripcion[:180]))


def ultimos_movimientos(limite=100):
    with _conexion() as db:
        return db.execute("SELECT fecha_utc, usuario, accion, descripcion FROM bitacora ORDER BY rowid DESC LIMIT ?", (min(int(limite), 500),)).fetchall()
