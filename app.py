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
st.header("Pregunta 2")

seleccionados = st.multiselect(
    "Selecciona tus ramos",
    list(ramos.keys())
)

usar_otro = st.checkbox("Agregar ramo OTRO")

otros_ramos = []
cantidad_otros = 0

if usar_otro:

    cantidad_otros = st.number_input(
        "¿Cuántos ramos OTRO deseas agregar?",
        min_value=1,
        step=1
    )

    for i in range(cantidad_otros):

        st.subheader(f"OTRO {i+1}")

        nombre = st.text_input(
            f"Nombre del ramo {i+1}"
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

if st.button("Generar diagnóstico"):

    st.divider()

    st.subheader("Resultado")

    st.write(f"Universidad: {universidad}")
    st.write(f"CT: {ct}")

    st.write("### Ramos")

    total_horas = 0

    for ramo in seleccionados:

        T = ramos[ramo]["T"]
        L = ramos[ramo]["L"]

        st.write(f"- {ramo} (T{T}, L{L})")

    for ramo in otros_ramos:

        st.write(
            f"- {ramo['nombre']} (T{ramo['T']}, L{ramo['L']})"
        )

    st.write("### Horas autónomas")

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

    st.write(
        f"## Horas autónomas semanales totales: {total_horas} horas"
    )

    st.info(
        "IMPORTANTE: La cantidad de horas puede parecer alta al principio, "
        "pero no significa que debas estudiar exactamente esas horas de manera rígida todas las semanas. "
        "Este diagnóstico entrega una referencia aproximada de dedicación académica según la carga de tus ramos "
        "y puede ajustarse a tu realidad personal, ritmo de aprendizaje, hábitos de estudio, experiencia previa "
        "y disponibilidad semanal. El objetivo es ayudarte a visualizar tu carga académica de manera más clara "
        "y organizada, no asustarte."
    )
