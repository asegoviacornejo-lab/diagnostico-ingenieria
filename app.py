import streamlit as st

st.title("Hola Antonia 👋")

st.write("Mi primera app usando Streamlit y GitHub desde el teléfono.")
st.button("Presiona aquí")
import streamlit as st

st.set_page_config(
    page_title="Diagnóstico Académico Ingeniería",
    layout="centered"
)

st.title("Diagnóstico Académico")

st.markdown("""
Este diagnóstico está enfocado principalmente en estudiantes de Ingeniería Civil Industrial hasta quinto nivel y estudiantes de otras Ingenierías Civiles en etapa de plan común de la Universidad de La Serena.

Esto no impide que estudiantes de otras carreras o universidades puedan utilizarlo. En esos casos, simplemente deberán ingresar manualmente los datos solicitados mediante la opción “OTRO”.

El objetivo es recopilar información de manera ordenada para visualizar tu carga académica semanal.
""")

ramos = {
    "Introducción al Cálculo": {"T": 6, "L": 2},
    "Introducción al Álgebra": {"T": 6, "L": 2},
}

st.header("Pregunta 1")

uls = st.radio(
    "¿Eres estudiante de la Universidad de La Serena?",
    ["Sí", "No"]
)

estimado = False

if uls == "Sí":
    universidad = "Universidad de La Serena"
    ct = 27

else:
    universidad = st.text_input(
        "Nombre de tu universidad"
    )

    sabe_credito = st.radio(
        "¿Sabes a cuántas horas equivale 1 crédito transferible en tu universidad?",
        ["Sí", "No"]
    )

    if sabe_credito == "Sí":
        ct = st.number_input(
            "Ingresa equivalencia de créditos",
            min_value=1,
            step=1
        )

    else:
        ct = "Estimado"
        estimado = True
