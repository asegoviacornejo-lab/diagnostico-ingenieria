import streamlit as st
import pandas as pd

# -----------------------------------
# CONFIGURACIÓN INICIAL
# -----------------------------------

st.set_page_config(
    page_title="Diagnóstico Académico",
    layout="wide"
)

# -----------------------------------
# TÍTULO
# -----------------------------------

st.title("📚 Diagnóstico Académico para Ingeniería")

st.markdown("""
Esta herramienta permite recopilar información académica
y personal para construir una planificación semanal inteligente.

Especialmente pensada para estudiantes de ingeniería.
""")

st.divider()

# -----------------------------------
# PREGUNTA 1 — UNIVERSIDAD
# -----------------------------------

st.header("1️⃣ Información Universitaria")

universidad = st.radio(
    "¿Eres estudiante de la Universidad de La Serena?",
    ["Sí", "No"]
)

if universidad == "Sí":

    ct = 27

    st.success(
        "Se utilizará automáticamente el sistema SCT ULS (27 horas por crédito)."
    )

else:

    ct = st.number_input(
        "Ingrese cuántas horas equivale un crédito transferible en tu universidad:",
        min_value=1,
        max_value=100,
        value=27
    )

st.write(f"📌 Valor actual del crédito transferible: {ct} horas")

st.divider()

# -----------------------------------
# PREGUNTA 2 — MATERIAS
# -----------------------------------

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
    "Selecciona las materias que estás cursando:",
    list(ramos.keys())
)

st.divider()

# -----------------------------------
# OTROS RAMOS
# -----------------------------------

st.header("3️⃣ Agregar Otros Ramos")

cantidad_otros = st.number_input(
    "¿Cuántos ramos quieres agregar manualmente?",
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

# -----------------------------------
# BLOQUES SEMANALES
# -----------------------------------

st.header("4️⃣ Organización Semanal")

st.markdown("""
Agrega actividades de tu semana:
- clases
- laboratorios
- transporte
- trabajo
- estudio
- descanso
""")

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
        "Materia o descripción de la actividad"
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

# -----------------------------------
# MOSTRAR TABLA
# -----------------------------------

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

# -----------------------------------
# GENERAR DIAGNÓSTICO
# -----------------------------------

if st.button("Generar diagnóstico"):

    st.divider()

    st.header("📊 Resultado del Diagnóstico")

    st.write(f"### Universidad: {universidad}")
    st.write(f"### CT utilizado: {ct}")

    st.divider()

    st.subheader("📖 Ramos")

    total_horas = 0

    for ramo in seleccionados:

        T = ramos[ramo]["T"]
        L = ramos[ramo]["L"]

        st.write(f"- {ramo} (T{T}, L{L})")

    for ramo in otros_ramos:

        st.write(
            f"- {ramo['nombre']} (T{ramo['T']}, L{ramo['L']})"
        )

    st.divider()

    st.subheader("⏰ Horas Autónomas Estimadas")

    for ramo in seleccionados:

        T = ramos[ramo]["T"]
        L = ramos[ramo]["L"]

        HT = T * 2
        HL = L * 1

        total_horas += HT + HL

        st.write(f"### {ramo}")

        if T > 0:
            st.write(f"- Teoría: {HT} horas")

        if L > 0:
            st.write(f"- Laboratorio/práctica: {HL} horas")

    for ramo in otros_ramos:

        HT = ramo["T"] * 2
        HL = ramo["L"] * 1

        total_horas += HT + HL

        st.write(f"### {ramo['nombre']}")

        if ramo["T"] > 0:
            st.write(f"- Teoría: {HT} horas")

        if ramo["L"] > 0:
            st.write(f"- Laboratorio/práctica: {HL} horas")

    st.divider()

    st.write(
        f"## 📌 Horas autónomas semanales totales: {total_horas} horas"
    )

    st.info(
        "IMPORTANTE: La cantidad de horas puede parecer alta al principio, "
        "pero no significa que debas estudiar exactamente esas horas de manera rígida todas las semanas. "
        "Este diagnóstico entrega una referencia aproximada de dedicación académica según la carga de tus ramos "
        "y puede ajustarse a tu realidad personal, ritmo de aprendizaje, hábitos de estudio, experiencia previa "
        "y disponibilidad semanal. El objetivo es ayudarte a visualizar tu carga académica de manera más clara "
        "y organizada, no asustarte."
            )


