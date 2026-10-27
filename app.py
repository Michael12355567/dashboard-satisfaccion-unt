"""Gestor SIRIES–UNT. Prototipo funcional LOCAL con login y extracción autorizada.

No publicar esta instancia en internet con datos personales: para producción requiere
SSO institucional, MFA, HTTPS, revisión de seguridad y alojamiento autorizado.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from reportes import tabla, calidad, resumen, excel
from seguridad import verificar, bloqueado, registrar, ultimos_movimientos
from ura_api import URAClient, URAError

st.set_page_config(page_title="Gestor Estadístico SIRIES | UNT", page_icon="🎓", layout="wide")


def conf(nombre, defecto=""):
    # secretos opcionales: la pantalla informa si falta configurar
    try:
        return str(st.secrets.get(nombre, defecto))
    except (FileNotFoundError, Exception):
        return str(defecto)


def mensaje_error(e):
    if isinstance(e, URAError):
        st.error(str(e))
    else:
        st.error("Ocurrió un error durante el procesamiento. Comprueba la configuración y los datos.")


def iniciar_sesion():
    user = conf("ADMIN_USERNAME")
    pwdhash = conf("ADMIN_PASSWORD_HASH")
    if not user or not pwdhash:
        st.error("Aún no configuraste el usuario administrador.")
        st.info("En la carpeta del proyecto, ejecuta: `py configurar.py` y luego reinicia Streamlit.")
        st.stop()
    if st.session_state.get("autorizado", False):
        if st.session_state.get("usuario") != user or (time.monotonic() - st.session_state.get("actividad", 0) > 20 * 60):
            st.session_state.clear()
            st.warning("La sesión ha caducado. Vuelve a iniciar sesión.")
            st.rerun()
        st.session_state["actividad"] = time.monotonic()
        return
    st.title("🔐 Acceso restringido · SIRIES UNT")
    st.caption("Unidad de Estadística – Oficina de Planeamiento y Presupuesto")
    st.warning("Sistema local. No está autorizado para publicarse en internet ni compartir registros personales.")
    with st.form("form_login", clear_on_submit=True):
        entrada_usuario = st.text_input("Usuario", max_chars=32)
        entrada_clave = st.text_input("Contraseña", type="password")
        enviar = st.form_submit_button("Ingresar", use_container_width=True)
    if enviar:
        if not entrada_usuario or not entrada_clave:
            st.error("Ingresa usuario y contraseña.")
        elif bloqueado(entrada_usuario):
            st.error("Acceso temporalmente bloqueado por intentos fallidos. Prueba después de 15 minutos.")
        elif verificar(entrada_usuario, entrada_clave, user, pwdhash):
            st.session_state["autorizado"] = True
            st.session_state["usuario"] = user
            st.session_state["actividad"] = time.monotonic()
            registrar(user, "LOGIN", "Inicio de sesión")
            st.rerun()
        else:
            st.error("Credenciales incorrectas o cuenta temporalmente bloqueada.")
    st.stop()


def cierre():
    registrar(st.session_state.get("usuario", ""), "LOGOUT", "Cierre de sesión")
    st.session_state.clear()
    st.rerun()


def conectarse():
    token = conf("URA_API_TOKEN")
    if not token:
        raise URAError("No está configurado el token de la URA. Ejecuta `py configurar.py` con un token renovado.")
    return URAClient(token)


def consulta(func, accion, descripcion):
    try:
        valor = func()
        registrar(st.session_state.get("usuario", ""), accion, descripcion)
        return valor
    except Exception as err:
        mensaje_error(err)
        registrar(st.session_state.get("usuario", ""), "ERROR", f"{accion}: {type(err).__name__}")
        return None


def registro_resultado(filas, advertencias, metadata):
    st.session_state["resultado"] = {"filas": filas, "advertencias": advertencias, "metadata": metadata}


def mostrar_resultados():
    r = st.session_state.get("resultado")
    if not r:
        st.info("Todavía no hay un reporte descargado en esta sesión.")
        return
    df = tabla(r["filas"])
    qc = calidad(df, r["advertencias"])
    st.subheader("Reporte obtenido")
    col1, col2, col3 = st.columns(3)
    col1.metric("Filas recibidas", f"{qc['filas']:,}")
    col2.metric("Columnas", qc["columnas"])
    col3.metric("DNI con formato inválido", qc["dni_invalidos"])
    st.caption("Las filas no necesariamente equivalen a personas distintas. No se eliminan duplicados automáticamente.")
    st.info("Los datos corresponden a la fecha de extracción. No son necesariamente una fotografía al cierre del semestre.")
    st.write("**Resumen agregado por categoría (conteos de filas)**")
    res = resumen(df)
    if not res.empty:
        st.dataframe(res, hide_index=True, use_container_width=True, height=260)
    else:
        st.write("El reporte no contiene registros.")
    st.write("**Advertencias de calidad de la URA (agrupadas)**")
    if not r["metadata"].get("advertencias_consultadas", True):
        st.warning("La consulta de advertencias no está disponible para esta extracción. No significa que no existan problemas.")
    if not qc["advertencias"].empty:
        st.dataframe(qc["advertencias"], hide_index=True, use_container_width=True)
    else:
        st.success("No se recibieron advertencias o no están disponibles para este tipo de reporte.")
    st.write("**Campos vacíos (sin contar campos que la guía indica siempre nulos)**")
    if not qc["nulos"].empty:
        st.dataframe(qc["nulos"], hide_index=True, use_container_width=True, height=220)
    else:
        st.write("No se detectaron campos vacíos adicionales.")
    with st.expander("Ver metadatos de esta extracción"):
        st.json(r["metadata"])
    if st.button("Preparar Excel para descarga", key="build_excel"):
        with st.spinner("Preparando el libro Excel..."):
            try:
                st.session_state["excel_preparado"] = excel(r["filas"], r["advertencias"], r["metadata"])
                st.success("Excel preparado. Haz clic en el botón de descarga.")
            except Exception as e:
                mensaje_error(e)
    if st.session_state.get("excel_preparado"):
        nombre = f"UNT_SIRIES_{r['metadata'].get('tipo','reporte')}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        st.download_button("⬇️ Descargar Excel (datos personales)",
                           st.session_state["excel_preparado"],
                           file_name=nombre, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)
    st.caption("Guarda el Excel únicamente en una carpeta institucional protegida. No publiques registros identificables en Power BI web.")


def lista_filtrada(items, campo_id, campo_nombre, titulo):
    opciones = {}
    for a in items or []:
        if isinstance(a, dict) and campo_id in a:
            nombre = str(a.get(campo_nombre) or "Sin descripción")
            valor = a[campo_id]
            opciones[f"{nombre} — ID {valor}"] = valor
    elegir = st.multiselect(titulo, list(opciones), help="Sin selección significa todas.")
    return [opciones[v] for v in elegir]


def pregrado():
    st.subheader("1. Reportes SIRIES de pregrado")
    st.write("Consulta los catálogos primero. Los filtros vienen del servidor de la URA, no de ejemplos inventados.")
    if st.button("🔍 Consultar períodos, escuelas y sedes disponibles"):
        resultado = consulta(lambda: conectarse().catalogos(), "CATALOGOS", "Catálogos de pregrado")
        if resultado is not None:
            st.session_state["catalogos"] = resultado
            st.success("Catálogos recibidos correctamente.")
    cat = st.session_state.get("catalogos")
    if cat:
        periods = cat.get("periodos") or {}
        opciones = sorted(periods.keys(), reverse=True) if isinstance(periods, dict) else []
        if not opciones:
            st.warning("La URA no devolvió períodos válidos.")
            return
        st.metric("Períodos disponibles", len(opciones))
        tipo = st.radio("Reporte", ["Matriculados", "Egresados"], horizontal=True)
        escogidos = st.multiselect("Períodos académicos (hasta 20)", opciones, default=opciones[:1])
        escuelas = lista_filtrada(cat.get("escuelas"), "idEscuela", "nombre", "Escuelas profesionales")
        sedes = lista_filtrada(cat.get("sedes"), "idSede", "nombre", "Sedes")
        if st.button("📨 Solicitar generación del reporte", type="primary"):
            if not (1 <= len(escogidos) <= 20):
                st.error("Selecciona entre 1 y 20 períodos.")
            else:
                codigo = "siries_matriculados_pregrado" if tipo == "Matriculados" else "siries_egresados_pregrado"
                with st.spinner("Enviando la solicitud a la URA..."):
                    valor = consulta(lambda: conectarse().crear_pregrado(codigo, escogidos, escuelas, sedes),
                                     "SOLICITAR", f"{codigo} / {','.join(escogidos)}")
                if valor:
                    st.session_state["job"] = {"id": valor["id"], "tipo": codigo, "periodos": escogidos,
                                               "solicitado_en": datetime.now(timezone.utc).isoformat()}
                    st.session_state["estado"] = valor.get("estado", "pendiente")
                    st.session_state.pop("resultado", None)
                    st.session_state.pop("excel_preparado", None)
                    st.success("Solicitud creada. No es necesario solicitar nuevamente para consultar el avance.")
    else:
        st.info("Haz clic en el botón de catálogos para comenzar.")

    job = st.session_state.get("job")
    if not job:
        return
    st.divider()
    st.write("**Seguimiento de la solicitud activa**")
    st.code(job["id"], language=None)
    st.write("Períodos solicitados:", ", ".join(job["periodos"]))
    st.write("Estado conocido:", st.session_state.get("estado", "pendiente"))
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Consultar estado"):
            val = consulta(lambda: conectarse().estado(job["id"]), "ESTADO", "Consulta de estado")
            if val:
                st.session_state["estado"] = val.get("estado", "desconocido")
                progreso = val.get("avance") or {}
                st.write("Avance:", progreso)
                st.info("Estado: " + str(val.get("estado", "desconocido")))
    with col2:
        if st.button("⬇️ Descargar reporte completado"):
            # Verificación contra API, no confiamos solo en un estado anterior de la pantalla.
            actual = consulta(lambda: conectarse().estado(job["id"]), "ESTADO", "Verificar antes de descargar")
            if actual and actual.get("estado") == "completado":
                with st.spinner("Descargando los registros y las advertencias..."):
                    api = conectarse()
                    filas = consulta(lambda: api.descargar_pregrado(job["id"]), "DESCARGA", job["tipo"])
                    if filas is not None:
                        avisos = consulta(lambda: api.advertencias(job["id"]), "ADVERTENCIAS", "Control de calidad")
                        aviso_disponible = avisos is not None
                        if avisos is None:
                            st.warning("No se pudieron obtener las advertencias. Los datos no se marcarán como validados.")
                            avisos = []
                        registro_resultado(filas, avisos, {**job, "estado": "completado",
                            "advertencias_consultadas": aviso_disponible,
                            "fecha_descarga_utc": datetime.now(timezone.utc).isoformat(),
                            "fuente": "API URA UNT"})
                        st.session_state.pop("excel_preparado", None)
                        st.success("Reporte descargado para esta sesión.")
            elif actual:
                st.warning("El reporte todavía no está completado. Estado: " + str(actual.get("estado")))
    if st.session_state.get("estado") == "fallido":
        if st.button("Reintentar reporte fallido"):
            val = consulta(lambda: conectarse().reintentar(job["id"]), "REINTENTAR", "Reporte fallido")
            if val is not None:
                st.success("Reintento solicitado a la URA.")


def segunda():
    st.subheader("2. Reportes de Segunda Especialidad")
    st.caption("Dos formatos: SIRIES (respuesta inmediata) o sistema de Segunda Especialidad (paginado).")
    if st.button("🔍 Consultar filtros de Segunda Especialidad"):
        val = consulta(lambda: conectarse().filtros_segunda(), "FILTROS_SE", "Catálogo Segunda Especialidad")
        if val is not None:
            st.session_state["filtros_segunda"] = val
    cat = st.session_state.get("filtros_segunda")
    if not cat:
        st.info("Consulta primero los semestres y las especialidades disponibles.")
        return
    sem = cat.get("semestres") or []
    sem_dict = {str(d.get("descripcion", "Semestre")) + " — ID " + str(d["idAnio_Semestre"]): d["idAnio_Semestre"]
                for d in sem if isinstance(d, dict) and "idAnio_Semestre" in d}
    if not sem_dict:
        st.warning("El catálogo no contiene semestres de Segunda Especialidad.")
        return
    semestre = sem_dict[st.selectbox("Semestre", list(sem_dict))]
    especialidades = {str(d.get("nombre", "Sin nombre")) + " — ID " + str(d["idSegunda_Especialidad"]): d["idSegunda_Especialidad"]
                     for d in cat.get("especialidades", []) if isinstance(d, dict) and "idSegunda_Especialidad" in d}
    espec_txt = st.selectbox("Especialidad", ["Todas"] + list(especialidades))
    codigo_espec = None if espec_txt == "Todas" else especialidades[espec_txt]
    sedes = {str(d.get("nombre", "Sin nombre")) + " — ID " + str(d["idSede"]): d["idSede"]
             for d in cat.get("sedes", []) if isinstance(d, dict) and "idSede" in d}
    sede_txt = st.selectbox("Sede", ["Todas"] + list(sedes))
    codigo_sede = None if sede_txt == "Todas" else sedes[sede_txt]
    categoria = st.radio("Reporte", ["matriculados", "egresados"], horizontal=True)
    formato = st.radio("Formato", ["siries", "origen"], horizontal=True,
                       format_func=lambda x: "SIRIES" if x == "siries" else "Segunda Especialidad / paginado")
    if st.button("⬇️ Consultar y descargar Segunda Especialidad", type="primary"):
        with st.spinner("Consultando datos de Segunda Especialidad..."):
            result = consulta(lambda: conectarse().segunda_especialidad(categoria, semestre, formato, codigo_espec, codigo_sede),
                              "DESCARGA_SE", f"{categoria} / semestre {semestre} / formato {formato}")
        if result is not None:
            registro_resultado(result, [], {"tipo": f"segunda_{categoria}_{formato}", "semestre": semestre,
                "especialidad": codigo_espec or "Todas", "sede": codigo_sede or "Todas",
                "fecha_descarga_utc": datetime.now(timezone.utc).isoformat(),
                "fuente": "API URA UNT", "advertencias_consultadas": False})
            st.session_state.pop("excel_preparado", None)
            st.success("Registros descargados y disponibles para crear el Excel.")


# Solo se renderizan páginas de datos tras un control de autenticación satisfactorio.
iniciar_sesion()
with st.sidebar:
    st.title("🎓 SIRIES · UNT")
    st.caption("Unidad de Estadística – OPP")
    st.write("🔐 Usuario: " + st.session_state.get("usuario", ""))
    st.success("Sesión autenticada (acceso local)")
    if st.button("Cerrar sesión", use_container_width=True):
        cierre()
    st.divider()
    if conf("URA_API_TOKEN"):
        st.write("🔑 Credencial URA: configurada, pendiente de prueba si no has consultado")
    else:
        st.warning("🔑 Falta configurar el token URA")
    st.caption("No subir este aplicativo con datos personales a una nube pública. El login local no sustituye MFA/SSO.")

st.title("Sistema de Extracción Estadística SIRIES – UNT")
st.caption("Versión 1.0 local · Matriculados, egresados y Segunda Especialidad · Elaborado según la guía URA")
st.warning("Información de estudiantes: uso interno autorizado. Una contraseña no vuelve segura una publicación pública en internet.")
mod_pre, mod_seg, mod_datos, mod_bitacora = st.tabs(["📚 Pregrado", "🎓 Segunda Especialidad", "📊 Resultados / Excel", "🕒 Bitácora"])
with mod_pre:
    pregrado()
with mod_seg:
    segunda()
with mod_datos:
    mostrar_resultados()
with mod_bitacora:
    st.subheader("Registro local de operaciones")
    try:
        log = pd.DataFrame(ultimos_movimientos(), columns=["Fecha UTC", "Usuario", "Acción", "Descripción"])
        st.dataframe(log, hide_index=True, use_container_width=True)
    except Exception:
        st.error("No se pudo cargar la bitácora.")
    st.caption("No se guardan números de documentos, nombres de estudiantes, contraseñas ni tokens en la bitácora.")
