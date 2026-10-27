"""Cliente de solo lectura de reportes URA (excepto solicitudes de generación/reintento).

Implementación basada en Guía de uso de la API SIRIES para OPP, 8 páginas.
Nunca registrar tokens, datos personales ni respuestas completas.
"""
from __future__ import annotations

import json
import time
import uuid
from urllib.parse import urljoin
from typing import Any

import requests

BASE_URL = "https://api-tramites.unitru.edu.pe"
MAX_JSON_BYTES = 80 * 1024 * 1024


class URAError(Exception):
    """Error amigable que no revela credenciales ni datos personales."""


class URAClient:
    def __init__(self, token: str):
        if not token or not token.strip():
            raise URAError("No se ha configurado el token institucional de la URA.")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": "Bearer " + token.strip(),
            "Accept": "application/json",
            "User-Agent": "Unidad-Estadistica-UNT/1.0",
        })

    def _json(self, method: str, path: str, *, params=None, payload=None, headers=None) -> Any:
        if not path.startswith("/api/") or "//" in path or ".." in path:
            raise URAError("Ruta de consulta no permitida.")
        url = BASE_URL + path
        for intento in range(4):
            try:
                with self.session.request(
                    method, url, params=params, json=payload, headers=headers,
                    timeout=(10, 70), stream=True, allow_redirects=False,
                    verify=True,
                ) as respuesta:
                    code = respuesta.status_code
                    if code == 429 and intento < 3:
                        raw = respuesta.headers.get("Retry-After", "5")
                        try:
                            esperar = float(raw)
                        except (TypeError, ValueError):
                            esperar = 5
                        time.sleep(max(1, min(30, esperar)))
                        continue
                    if code in (500, 503) and intento < 3:
                        time.sleep(min(2 ** intento, 8))
                        continue
                    if code == 401:
                        raise URAError("Acceso rechazado (401): el token falta, caducó o no es válido.")
                    if code == 403:
                        raise URAError("Acceso no autorizado (403). Contacta con Informática de la URA.")
                    if code == 404:
                        raise URAError("Recurso o reporte inexistente (404).")
                    if code == 409:
                        raise URAError("Conflicto (409): reporte no listo o solicitud incompatible.")
                    if code == 410:
                        raise URAError("El reporte caducó (410). Genera una nueva solicitud.")
                    if code == 422:
                        raise URAError("La URA rechazó los filtros (422). Revisa los períodos seleccionados.")
                    if code == 429:
                        raise URAError("Límite de solicitudes alcanzado (429). Vuelve a intentarlo más tarde.")
                    if not (200 <= code < 300):
                        raise URAError(f"La URA respondió con el código HTTP {code}.")
                    total = 0
                    partes = []
                    longitud = respuesta.headers.get("Content-Length")
                    if longitud and longitud.isdigit() and int(longitud) > MAX_JSON_BYTES:
                        raise URAError("El reporte supera el tamaño máximo de esta versión (80 MB). Divide los períodos.")
                    for bloque in respuesta.iter_content(chunk_size=1024 * 256):
                        total += len(bloque)
                        if total > MAX_JSON_BYTES:
                            raise URAError("La respuesta excede 80 MB. Solicita menos períodos.")
                        partes.append(bloque)
                    try:
                        return json.loads(b"".join(partes))
                    except (ValueError, UnicodeError):
                        raise URAError("La respuesta del servicio no es un JSON válido.") from None
            except (requests.Timeout, requests.ConnectionError):
                if intento == 3:
                    raise URAError("No se pudo contactar con la API de la URA. Comprueba la red o el servicio.") from None
                time.sleep(min(2 ** intento, 8))
        raise URAError("No se pudo completar la consulta.")

    def catalogos(self) -> dict:
        data = self._json("GET", "/api/reportes/siries/catalogos")
        if not isinstance(data, dict):
            raise URAError("La respuesta de catálogos tiene un formato inesperado.")
        return data

    def crear_pregrado(self, tipo: str, periodos: list[str], escuelas=None, sedes=None) -> dict:
        permitidos = ("siries_matriculados_pregrado", "siries_egresados_pregrado")
        if tipo not in permitidos or not (1 <= len(periodos) <= 20):
            raise URAError("Selecciona un tipo válido y entre 1 y 20 períodos.")
        filtro = {"periodos": periodos}
        if escuelas:
            filtro["escuelas"] = escuelas
        if sedes:
            filtro["sedes"] = sedes
        clave = str(uuid.uuid4())  # idempotencia: se conserva para reintentos de red
        resultado = self._json(
            "POST", "/api/reportes", payload={"tipo": tipo, "filtros": filtro},
            headers={"Content-Type": "application/json", "Idempotency-Key": clave},
        )
        if not isinstance(resultado, dict) or not resultado.get("id"):
            raise URAError("La URA no devolvió el identificador del reporte.")
        return resultado

    @staticmethod
    def validar_reporte_id(reporte_id: str) -> str:
        try:
            return str(uuid.UUID(str(reporte_id)))
        except (ValueError, AttributeError, TypeError):
            raise URAError("Identificador de reporte inválido.") from None

    def estado(self, reporte_id: str) -> dict:
        rid = self.validar_reporte_id(reporte_id)
        data = self._json("GET", f"/api/reportes/{rid}")
        if not isinstance(data, dict):
            raise URAError("Estado de reporte no reconocido.")
        return data

    def descargar_pregrado(self, reporte_id: str) -> list[dict]:
        rid = self.validar_reporte_id(reporte_id)
        filas = self._json("GET", f"/api/reportes/{rid}/descarga")
        if not isinstance(filas, list):
            raise URAError("El reporte no contiene la lista JSON esperada.")
        return filas

    def advertencias(self, reporte_id: str) -> list[dict]:
        rid = self.validar_reporte_id(reporte_id)
        todas = []
        pagina = 1
        while True:
            bloque = self._json("GET", f"/api/reportes/{rid}/advertencias", params={"page": pagina, "size": 500})
            todas.extend(bloque.get("data", []))
            meta = bloque.get("meta", {})
            if pagina >= int(meta.get("last_page", pagina)):
                return todas
            if pagina >= 200:
                raise URAError("Hay más de 200 páginas de advertencias. Consulta con Informática.")
            pagina += 1
            time.sleep(1.1)

    def reintentar(self, reporte_id: str) -> dict:
        rid = self.validar_reporte_id(reporte_id)
        return self._json("POST", f"/api/reportes/{rid}/reintentar")

    def filtros_segunda(self) -> dict:
        result = self._json("GET", "/api/segunda-especialidad/filtros")
        if not isinstance(result, dict):
            raise URAError("Formato de filtros de Segunda Especialidad inesperado.")
        return result

    def segunda_especialidad(self, categoria: str, semestre: Any, formato: str = "siries", especialidad=None, sede=None) -> list[dict]:
        if categoria not in ("matriculados", "egresados") or formato not in ("siries", "origen"):
            raise URAError("Tipo de consulta de Segunda Especialidad no admitido.")
        ruta = f"/api/segunda-especialidad/reportes/{categoria}"
        params = {"semestre": semestre}
        if especialidad is not None:
            params["especialidad"] = especialidad
        if sede is not None:
            params["sede"] = sede
        if formato == "siries":
            params["formato"] = "siries"
            filas = self._json("GET", ruta, params=params)
            if not isinstance(filas, list):
                raise URAError("Segunda Especialidad no devolvió una lista JSON.")
            return filas
        acumulado = []
        pagina = 1
        while True:
            bloque = self._json("GET", ruta, params={**params, "page": pagina, "size": 500})
            if not isinstance(bloque, dict):
                raise URAError("Paginación inválida en Segunda Especialidad.")
            acumulado.extend(bloque.get("data", []))
            if pagina >= int(bloque.get("meta", {}).get("last_page", pagina)):
                break
            if pagina >= 200:
                raise URAError("La consulta supera 200 páginas. Aplica más filtros.")
            pagina += 1
            time.sleep(1.1)
        return acumulado
