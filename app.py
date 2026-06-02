import streamlit as st
import json
import os

# ======================================================
# CONFIGURACIÓN DE LA PÁGINA
# ======================================================

st.set_page_config(
    page_title="Diagnóstico Académico",
    page_icon="📚",
    layout="wide"
)

# ======================================================
# ESTRUCTURA BASE DEL PROYECTO
# ======================================================

ARCHIVO_DATOS = "usuario.json"

DATOS_INICIALES = {
    "perfil": {
        "nombre": "",
        "correo": "",
        "universidad": "",
        "carrera": "",
        "valor_sct": 27
    },

    "asignaturas": [],

    "sueno": {
        "sueno_real": None,
        "sueno_recuperacion": None
    },

    "actividades": [],

    "horario": [],

    "resultados_nivel1": {},

    "horario_estudio": [],

    "evaluaciones": [],

    "registro_estudio": [],

    "rendimiento": [],

    "configuracion": {}
}

# ======================================================
# FUNCIONES DE PERSISTENCIA
# ======================================================

def crear_archivo_si_no_existe():
    if not os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(
                DATOS_INICIALES,
                archivo,
                indent=4,
                ensure_ascii=False
            )


def cargar_datos():
    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )

# ======================================================
# CONTROL DE COMPLETITUD
# ======================================================

def obtener_estado(datos):

    estado = {
        "Perfil": False,
        "Asignaturas": False,
        "Sueño": False,
        "Actividades": False,
        "Horario": False
    }

    perfil = datos["perfil"]

    if (
        perfil["nombre"]
        and perfil["universidad"]
        and perfil["carrera"]
    ):
        estado["Perfil"] = True

    if len(datos["asignaturas"]) > 0:
        estado["Asignaturas"] = True

    if (
        datos["sueno"]["sueno_real"] is not None
        and
        datos["sueno"]["sueno_recuperacion"] is not None
    ):
        estado["Sueño"] = True

    if len(datos["actividades"]) > 0:
        estado["Actividades"] = True

    if len(datos["horario"]) > 0:
        estado["Horario"] = True

    return estado


def calcular_porcentaje(estado):

    total = len(estado)
    completas = sum(estado.values())

    return int((completas / total) * 100)

# ======================================================
# INICIO
# ======================================================

crear_archivo_si_no_existe()

datos = cargar_datos()

# ======================================================
# BARRA LATERAL
# ======================================================

with st.sidebar:

    st.title("📚 Diagnóstico")

    estado = obtener_estado(datos)

    porcentaje = calcular_porcentaje(estado)

    st.progress(porcentaje / 100)

    st.write(f"**Perfil completado: {porcentaje}%**")

    st.divider()

    for seccion, completa in estado.items():

        if completa:
            st.success(f"✓ {seccion}")
        else:
            st.warning(f"✗ {seccion}")

# ======================================================
# PERFIL
# ======================================================

st.title("Diagnóstico Académico")

st.header("Perfil Académico")

nombre = st.text_input(
    "Nombre o apodo",
    value=datos["perfil"]["nombre"]
)

correo = st.text_input(
    "Correo electrónico (opcional)",
    value=datos["perfil"]["correo"]
)

universidad = st.text_input(
    "Universidad",
    value=datos["perfil"]["universidad"]
)

carrera = st.text_input(
    "Carrera",
    value=datos["perfil"]["carrera"]
)

valor_sct = st.number_input(
    "Valor de 1 SCT (horas)",
    min_value=1,
    value=datos["perfil"]["valor_sct"]
)

# ======================================================
# GUARDADO AUTOMÁTICO
# ======================================================

datos["perfil"]["nombre"] = nombre
datos["perfil"]["correo"] = correo
datos["perfil"]["universidad"] = universidad
datos["perfil"]["carrera"] = carrera
datos["perfil"]["valor_sct"] = valor_sct

guardar_datos(datos)

st.success("✓ Cambios guardados automáticamente")

# ======================================================
# RESUMEN
# ======================================================

st.divider()

st.subheader("Resumen actual")

st.write("### Perfil")

st.write(f"**Nombre:** {nombre}")
st.write(f"**Correo:** {correo}")
st.write(f"**Universidad:** {universidad}")
st.write(f"**Carrera:** {carrera}")
st.write(f"**Valor SCT:** {valor_sct}")

# ======================================================
# SALIDA ESPERADA
# ======================================================

# Al completar:
#
# Nombre: Antonia
# Universidad: Universidad de La Serena
# Carrera: Ingeniería Civil Industrial
# Valor SCT: 27
#
# La barra lateral mostrará:
#
# Perfil: ✓
# Asignaturas: ✗
# Sueño: ✗
# Actividades: ✗
# Horario: ✗
#
# Perfil completado: 20%
#
# Y toda la información quedará guardada en usuario.json
