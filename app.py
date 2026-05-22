import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================
# CONFIGURACIÓN INICIAL
# =====================================================

st.set_page_config(
    page_title="Diagnóstico Académico",
    layout="wide"
)

# =====================================================
# FUNCIONES
# =====================================================

def calcular_horas_autonomas(teoria, laboratorio):

    HT = teoria * 2
    HL = laboratorio * 1

    return HT + HL


def mostrar_ramos(seleccionados, ramos, otros_ramos):

    st.subheader("📖 Ramos")

    for ramo in seleccionados:

        T = ramos[ramo]["T"]
        L = ramos[ramo]["L"]

        st.write(f"- {ramo} (T{T}, L{L})")

    for ramo in otros_ramos:

        st.write(
            f"- {ramo['nombre']} (T{ramo['T']}, L{ramo['L']})"
        )


def mostrar_horas_autonomas(seleccionados, ramos, otros_ramos):

    total_horas = 0

    st.subheader("⏰ Horas Autónomas Estimadas")

    for ramo in seleccionados:

        T = ramos[ramo]["T"]
        L = ramos[ramo]["L"]

        horas = calcular_horas_autonomas(T, L)

        total_horas += horas

        st.write(f"### {ramo}")

        if T > 0:
            st.write(f"- Teoría: {T * 2} horas")

        if L > 0:
            st.write(f"- Laboratorio/práctica: {L * 1} horas")

    for ramo in otros_ramos:

        horas = calcular_horas_autonomas(
            ramo["T"],
            ramo["L"]
        )

        total_horas += horas

        st.write(f"### {ramo['nombre']}")

        if ramo["T"] > 0:
            st.write(f"- Teoría: {ramo['T'] * 2} horas")

        if ramo["L"] > 0:
            st.write(f"- Laboratorio/práctica: {ramo['L'] * 1} horas")

    st.divider()

    st.write(
        f"## 📌 Horas autónomas semanales totales: {total_horas} horas"
    )

    return total_horas


def detectar_espacios_libres(bloques):

    dias = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo"
    ]

    espacios = []

    inicio_jornada = 8
    fin_jornada = 22

    for dia in dias:

        actividades = []

        for bloque in bloques:

            if bloque["Día"] == dia:

                inicio = datetime.strptime(
                    bloque["Inicio"],
                    "%H:%M:%S"
                )

                fin = datetime.strptime(
                    bloque["Fin"],
                    "%H:%M:%S"
                )

                actividades.append((inicio, fin))

        actividades.sort()

        tiempo_actual = datetime.strptime(
            f"{inicio_jornada}:00:00",
            "%H:%M:%S"
        )

        fin_dia = datetime.strptime(
            f"{fin_jornada}:00:00",
            "%H:%M:%S"
        )

        for actividad in actividades:

            inicio, fin = actividad

            if inicio > tiempo_actual:

                diferencia = inicio - tiempo_actual

                horas_libres = diferencia.total_seconds() / 3600

                if horas_libres >= 1:

                    espacios.append({
                        "Día": dia,
                        "Inicio Libre": str(tiempo_actual.time()),
                        "Fin Libre": str(inicio.time()),
                        "Horas libres": round(horas_libres, 1)
                    })

            if fin > tiempo_actual:
                tiempo_actual = fin

        if tiempo_actual < fin_dia:

            diferencia = fin_dia - tiempo_actual

            horas_libres = diferencia.total_seconds() / 3600

            if horas_libres >= 1:

                espacios.append({
                    "Día": dia,
                    "Inicio Libre": str(tiempo_actual.time()),
                    "Fin Libre": str(fin_dia.time()),
                    "Horas libres": round(horas_libres, 1)
                })

    return espacios


# =====================================================
# TÍTULO
# =====================================================

st.title("📚 Diagnóstico Académico para Ingeniería")

st.markdown("""
Esta herramienta permite recopilar información académica
y personal para construir una planificación semanal inteligente.

Especialmente pensada para estudiantes de ingeniería.
""")

st.divider()

# =====================================================
# CAPA 1 — RECOLECCIÓN DE DATOS
# =====================================================

st.header("1️⃣ Información Universitaria")

universidad = st.radio(
    "¿Eres estudiante de la Universidad de La Serena?",
    ["Sí", "No"]
)

if universidad == "Sí":

    ct = 27

    st.success(
        "Se utilizará automáticamente el sistema SCT ULS."
    )

else:

    ct = st.number_input(
        "Horas equivalentes por crédito transferible:",
        min_value=1,
        max_value=100,
        value=27
    )

st.write(f"📌 CT actual: {ct} horas")

st.divider()

# =====================================================
# MATERIAS
# =====================================================

st.header("2️⃣ Materias del Semestre")

ramos = {
    "Cálculo I": {"T": 5, "L": 0},
    "Cálculo II": {"T": 5, "L": 0},
    "Álgebra": {"T": 4, "L": 0},
    "Física I": {"T": 4, "L": 2},
    "Física II": {"T": 4, "L": 2},
    "Química": {"T": 3, "L": 2},
    "Programación": {"T": 3, "L": 2},
    "Estática": {"T": 4, "L": 1},
    "Inglés": {"T": 2, "L": 0}
}

seleccionados = st.multiselect(
    "Selecciona tus materias:",
    list(ramos.keys())
)

st.divider()

# =====================================================
# OTROS RAMOS
# =====================================================

st.header("3️⃣ Agregar Otros Ramos")

cantidad_otros = st.number_input(
    "¿Cuántos ramos adicionales deseas agregar?",
    min_value=0,
    max_value=10,
    step=1
)

otros_ramos = []

for i in range(cantidad_otros):

    st.subheader(f"Ramo Extra {i+1}")

    nombre = st.text_input(
        f"Nombre del ramo {i+1}",
        key=f"nombre_{i}"
    )

    teoria = st.number_input(
        f"Horas de teoría semanales {i+1}",
        min_value=0,
        step=1,
        key=f"teoria_{i}"
    )

    laboratorio = st.number_input(
        f"Horas de laboratorio/práctica semanales {i+1}",
        min_value=0,
        step=1,
        key=f"lab_{i}"
    )

    otros_ramos.append({
        "nombre": nombre,
        "T": teoria,
        "L": laboratorio
    })

st.divider()

# =====================================================
# CAPA 2 — ORGANIZACIÓN SEMANAL
# =====================================================

st.header("4️⃣ Organización Semanal")

if "bloques" not in st.session_state:
    st.session_state.bloques = []

with st.form("formulario_bloques"):

    dia = st.selectbox(
        "Día",
        [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo"
        ]
    )

    hora_inicio = st.time_input("Hora de inicio")

    hora_fin = st.time_input("Hora de término")

    tipo = st.selectbox(
        "Tipo de actividad",
        [
            "Clase",
            "Laboratorio",
            "Transporte",
            "Trabajo",
            "Estudio",
            "Descanso",
            "Deporte",
            "Responsabilidad Familiar"
        ]
    )

    materia = st.text_input(
        "Materia o descripción"
    )

    agregar = st.form_submit_button("Agregar bloque")

    if agregar:

        nuevo_bloque = {
            "Día": dia,
            "Inicio": str(hora_inicio),
            "Fin": str(hora_fin),
            "Tipo": tipo,
            "Materia": materia
        }

        st.session_state.bloques.append(nuevo_bloque)

        st.success("Bloque agregado correctamente ✅")

st.divider()

# =====================================================
# MOSTRAR ACTIVIDADES
# =====================================================

st.header("5️⃣ Resumen de Actividades")

if len(st.session_state.bloques) > 0:

    df = pd.DataFrame(st.session_state.bloques)

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info("Aún no has agregado actividades.")

st.divider()

# =====================================================
# CAPA 3 — DETECCIÓN DE ESPACIOS LIBRES
# =====================================================

st.header("6️⃣ Espacios Libres Detectados")

espacios = detectar_espacios_libres(
    st.session_state.bloques
)

if len(espacios) > 0:

    df_espacios = pd.DataFrame(espacios)

    st.dataframe(
        df_espacios,
        use_container_width=True
    )

else:

    st.warning("No se detectaron espacios libres.")

st.divider()

# =====================================================
# CAPA 4 — DIAGNÓSTICO
# =====================================================

if st.button("Generar diagnóstico"):

    st.header("📊 Resultado del Diagnóstico")

    st.write(f"### Universidad: {universidad}")
    st.write(f"### CT utilizado: {ct}")

    st.divider()

    mostrar_ramos(
        seleccionados,
        ramos,
        otros_ramos
    )

    st.divider()

    total_horas = mostrar_horas_autonomas(
        seleccionados,
        ramos,
        otros_ramos
    )

    st.info(
        "IMPORTANTE: Estas horas son solo una estimación aproximada "
        "de dedicación académica semanal y pueden variar según "
        "tu experiencia, hábitos de estudio y dificultad personal."
    )

# =====================================================
# CAPA 5 — FUTURO MOTOR INTELIGENTE
# =====================================================

st.divider()

st.header("🚧 Futuras Funcionalidades")

st.markdown("""
Próximamente el sistema podrá:

- Detectar sobrecarga académica
- Recomendar horarios de estudio
- Analizar fatiga semanal
- Sugerir descansos
- Priorizar materias difíciles
- Generar horarios automáticos
""")


