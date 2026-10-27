# Gestor SIRIES UNT — versión 1.1 corregida

## Corrige el error `No module named argon2`

El módulo importado en `seguridad.py` es `argon2`; se instala con el paquete **`argon2-cffi`**. Este ZIP trae `requirements.txt` con esa dependencia **en la misma carpeta que `app.py`**, de acuerdo con la documentación de Streamlit Community Cloud.

## ¿Cómo subirlo a GitHub?

1. Descomprime el ZIP. **Sube el contenido de la carpeta, no una carpeta adicional ni el ZIP en sí.**
2. En la raíz del repositorio deben verse juntos `app.py`, `seguridad.py`, `ura_api.py`, `reportes.py`, `requirements.txt` y `.streamlit/config.toml`.
3. Sustituye los archivos antiguos. Si existe `uv.lock`, `Pipfile`, `environment.yml` o `pyproject.toml` de otras versiones, retíralo o asegúrate de que el sistema de dependencias que Streamlit Cloud elige instala `argon2-cffi`.
4. Realiza **Commit changes**.
5. En Streamlit Cloud, configura el **Main file path** como `app.py`. Si permanece instalado un entorno anterior, desde **Manage app** reinicia la aplicación o reconstruye sus dependencias. Revisa en los logs que se instaló `argon2-cffi`.

## Configurar SOLO el inicio de sesión en Cloud (sin datos personales)

Para ver la interfaz, necesitas configurar en **App settings → Secrets**:

```toml
ADMIN_USERNAME = "administrador"
ADMIN_PASSWORD_HASH = "$argon2id$...HASH_GENERADO_EN_TU_PC..."
PERMITIR_EXTRACCION = false
```

**NO introduzcas una contraseña en texto plano ni copies literalmente el hash de ejemplo.** Obtén un hash real en tu computadora con `python generar_hash.py` después de instalar dependencias. Ese comando pide la contraseña en privado y muestra únicamente su hash. Elige una contraseña distinta de tus contraseñas institucionales.

En **Streamlit Community Cloud** NO se recomienda descargar o almacenar padrones con datos personales de estudiantes mediante este formulario de login. Por defecto, el proyecto impide las consultas a la API: podrás revisar la interfaz y la autenticación, pero no extraer registros reales. Un login casero no garantiza que una aplicación publicada sea segura.

## Para descargar datos reales

**Ejecuta la aplicación en una computadora o servidor autorizado de la UNT**, usando `01_INSTALAR_Y_CONFIGURAR.bat` y `02_ABRIR_APLICATIVO.bat`. El asistente local crea tu usuario, contraseña hash, configura un token URA válido y marca `PERMITIR_EXTRACCION = true`. El archivo `.streamlit/secrets.toml` se crea localmente y no debe subirse a GitHub.

Si deseas un despliegue institucional, pide revisión de la OTI y agrega HTTPS, autenticación institucional con MFA, control de permisos/roles, VPN o red restringida, registros centralizados y políticas de retención. No existe seguridad 100% infalible.

**ATENCIÓN:** si una credencial URA fue expuesta, solicita su rotación antes de utilizarla. No incluyas tokens, claves, nombres ni DNI en incidencias públicas de GitHub ni en capturas.

## Cómo comprobar dependencias localmente

```bash
python -m pip install -r requirements.txt
python comprobar_instalacion.py
python -m unittest discover -s tests -v
```

En Windows, usa el intérprete de tu entorno virtual (archivo `01_INSTALAR_Y_CONFIGURAR.bat`).

## Fuente de la estructura de API

`Guía de uso — API de reportes SIRIES para la Unidad de Estadística - OPP` y colección `OPP-Reportes.postman_collection.json`. Los endpoints no se han probado con un token real en este entorno.
