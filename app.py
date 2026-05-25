import streamlit as st
import pandas as pd
import random
from collections import defaultdict

st.set_page_config(
    page_title="Planificador Académico",
    layout="wide"
)

st.title("Planificador Académico Adaptativo")

st.write("""
Este sistema:
- calcula horas autónomas
- identifica horario ocupado
- considera responsabilidades
- considera energía
- genera múltiples horarios posibles
- mantiene proporcionalidad entre ramos
""")

RAMOS = {
    1: ("Introducción al Cálculo", 6, 2),
    2: ("Introducción al Álgebra", 6, 2),
    3: ("Introducción a la Ingeniería", 4, 0),
    4: ("Taller de Estrategias de Aprendizaje para Ingeniería", 0, 4),
    5: ("Cálculo Diferencial e Integral", 6, 0),
    6: ("Cálculo Integral", 6, 0),
    7: ("Álgebra Lineal", 6, 0),
    8: ("Física Newtoniana", 6, 2),
    9: ("Física Newtoniana para Ingenieros", 6, 2),
    10: ("Taller de Habilidades Comunicativas para Ingeniería", 0, 2),
    11: ("Taller de Habilidades Comunicativas para Ingenieros", 0, 4),
    12: ("Dibujo de Ingeniería", 2, 2),
    13: ("Herramientas Computacionales para Ingeniería", 0, 2),
    14: ("Fundamentos de Programación y Computación", 2, 2),
    15: ("Cálculo en Varias Variables", 4, 0),
    16: ("Cálculo Vectorial", 6, 0),
    17: ("Ecuaciones Diferenciales", 4, 0),
    18: ("Electromagnetismo M2024", 4, 2),
    19: ("Electromagnetismo M2023", 6, 2),
    20: ("Química General", 4, 2)
}

DIAS = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo"
]

HORAS = list(range(8, 23))

st.header("1. Universidad")

uls = st.radio(
    "¿Eres estudiante de la Universidad de La Serena?",
    ["Sí", "No"]
)

if uls == "Sí":
    universidad = "Universidad de La Serena"
    ct = 27

else:
    universidad = st.text_input("Nombre universidad")
    ct = st.number_input(
        "Cantidad créditos transferibles",
        min_value=1,
        step=1
    )

st.header("2. Selección de ramos")

for codigo, datos in RAMOS.items():

    nombre, t, l = datos

    st.write(f"{codigo}. {nombre}(T{t},L{l})")

seleccion = st.text_input(
    "Selecciona números separados por coma"
)

ramos = []

if seleccion:

    numeros = [
        int(x.strip())
        for x in seleccion.split(",")
        if x.strip().isdigit()
    ]

    for n in numeros:

        if n in RAMOS:
            ramos.append(RAMOS[n])

st.header("3. Horario fijo")

cantidad_fijos = st.number_input(
    "Cantidad de actividades fijas",
    min_value=0,
    step=1
)

bloques_fijos = []

for i in range(cantidad_fijos):

    st.subheader(f"Actividad fija {i+1}")

    nombre = st.text_input(
        f"Nombre {i+1}",
        key=f"nombre_{i}"
    )

    dia = st.selectbox(
        f"Día {i+1}",
        DIAS,
        key=f"dia_{i}"
    )

    inicio = st.number_input(
        f"Hora inicio {i+1}",
        min_value=0,
        max_value=23,
        key=f"inicio_{i}"
    )

    fin = st.number_input(
        f"Hora fin {i+1}",
        min_value=0,
        max_value=23,
        key=f"fin_{i}"
    )

    bloques_fijos.append({
        "nombre": nombre,
        "dia": dia,
        "inicio": inicio,
        "fin": fin
    })

st.header("4. Responsabilidades personales")

responsabilidad = st.selectbox(
    "Nivel de responsabilidades personales/familiares",
    ["Baja", "Media", "Alta"]
)

st.header("5. Energía")

energia = {}

for dia in DIAS:

    energia[dia] = st.selectbox(
        f"Energía predominante {dia}",
        ["Alta", "Media", "Baja"],
        key=f"energia_{dia}"
    )

st.header("6. Restricciones")

descanso = st.number_input(
    "Horas mínimas entre bloques de estudio",
    min_value=1,
    max_value=6,
    value=2
)

maximo_diario = st.number_input(
    "Máximo horas de estudio por día",
    min_value=1,
    max_value=12,
    value=6
)

cantidad_horarios = st.slider(
    "Cantidad de horarios a generar",
    1,
    10,
    3
)

def calcular_horas(ramos):

    datos = []

    total = 0

    for ramo in ramos:

        nombre, t, l = ramo

        ht = t * 2
        hl = l * 1

        horas = ht + hl

        datos.append({
            "ramo": nombre,
            "horas_originales": horas
        })

        total += horas

    return datos, total

def ajustar_por_responsabilidad(datos):

    factor = 1.0

    if responsabilidad == "Media":
        factor = 0.85

    elif responsabilidad == "Alta":
        factor = 0.70

    for d in datos:

        nuevas = round(
            d["horas_originales"] * factor
        )

        if nuevas < 1:
            nuevas = 1

        d["horas_ajustadas"] = nuevas

    return datos

def ocupado(dia, hora, calendario):

    for bloque in calendario:

        if bloque["dia"] == dia:

            if hora >= bloque["inicio"] and hora < bloque["fin"]:
                return True

    return False

def generar_horario(datos):

    calendario = []

    for b in bloques_fijos:
        calendario.append(b)

    horas_dia = defaultdict(int)

    for ramo in datos:

        nombre = ramo["ramo"]

        horas_restantes = ramo["horas_ajustadas"]

        intentos = 0

        while horas_restantes > 0 and intentos < 500:

            intentos += 1

            dia = random.choice(DIAS)

            hora = random.choice(HORAS[:-1])

            energia_dia = energia[dia]

            if energia_dia == "Baja" and hora >= 20:
                continue

            if horas_dia[dia] >= maximo_diario:
                continue

            conflicto = False

            for h in range(
                hora - descanso,
                hora + descanso + 1
            ):

                if ocupado(dia, h, calendario):
                    conflicto = True
                    break

            if conflicto:
                continue

            calendario.append({
                "nombre": f"Estudio - {nombre}",
                "dia": dia,
                "inicio": hora,
                "fin": hora + 1
            })

            horas_dia[dia] += 1
            horas_restantes -= 1

    return calendario

if st.button("Generar horarios"):

    datos, total_original = calcular_horas(ramos)

    datos = ajustar_por_responsabilidad(datos)

    st.header("Resumen académico")

    st.write(f"Universidad: {universidad}")
    st.write(f"CT: {ct}")

    st.subheader("Ramos")

    for d in datos:

        st.write(
            f"- {d['ramo']} | "
            f"Horas originales: {d['horas_originales']} | "
            f"Horas ajustadas: {d['horas_ajustadas']}"
        )

    st.subheader("Responsabilidades")

    st.write(
        f"Nivel seleccionado: {responsabilidad}"
    )

    st.subheader("Horarios generados")

    for i in range(cantidad_horarios):

        st.markdown(f"## Horario {i+1}")

        calendario = generar_horario(datos)

        filas = []

        for bloque in calendario:

            filas.append({
                "Día": bloque["dia"],
                "Inicio": f"{bloque['inicio']}:00",
                "Fin": f"{bloque['fin']}:00",
                "Actividad": bloque["nombre"]
            })

        df = pd.DataFrame(filas)

        if not df.empty:

            orden_dias = {
                "Lunes": 0,
                "Martes": 1,
                "Miércoles": 2,
                "Jueves": 3,
                "Viernes": 4,
                "Sábado": 5,
                "Domingo": 6
            }

            df["orden"] = df["Día"].map(orden_dias)

            df = df.sort_values(
                by=["orden", "Inicio"]
            )

            df = df.drop(columns=["orden"])

            st.dataframe(
                df,
                use_container_width=True
            )

    st.write("""
IMPORTANTE:
Los horarios generados son alternativas posibles que cumplen las restricciones ingresadas por el estudiante.

Las horas autónomas pueden ajustarse según:
- disponibilidad real
- energía
- responsabilidades personales
- carga académica

El objetivo es entregar distintas opciones para que el estudiante pueda elegir la que mejor se adapte a su realidad.
""") 


