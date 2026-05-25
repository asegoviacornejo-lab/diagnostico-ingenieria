import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

st.set_page_config(page_title="Planificador Académico", layout="wide")

st.title("Planificador Académico Inteligente")

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
    20: ("Química General", 4, 2),
    21: ("Programación para Ingeniería", 0, 4),
    22: ("Termodinámica", 4, 0),
    23: ("Probabilidad y Estadística", 4, 0),
    24: ("Estadística Aplicada", 6, 0),
    25: ("Óptica y Ondas", 4, 2),
    26: ("Mecánica", 4, 2),
    27: ("Mecánica Estática", 6, 0),
    28: ("Desafío de Proyecto de Ingeniería I", 0, 4),
    29: ("Inglés para Ingeniería I", 2, 2),
    30: ("Métodos Numéricos para Ingeniería", 4, 0),
    31: ("Métodos Numéricos", 6, 0),
    32: ("Ciencias de Materiales", 4, 2),
    33: ("Ingeniería de Materiales", 2, 2),
    34: ("Fundamentos de Economía", 4, 0),
    35: ("Mecánica de Sólidos M2024", 4, 2),
    36: ("Mecánica de Sólidos M2023", 6, 0),
    37: ("Investigación de Operaciones", 4, 0),
    38: ("Inglés para Ingeniería II", 2, 2),
    39: ("Filosofía de las Ciencias de la Ingeniería", 4, 0),
    40: ("Taller de Creatividad", 0, 2)
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

st.header("1. Información general")

uls = st.radio(
    "¿Eres estudiante de la Universidad de La Serena?",
    ["Sí", "No"]
)

if uls == "Sí":
    universidad = "Universidad de La Serena"
    ct = 27
else:
    universidad = st.text_input("Universidad")
    ct = st.number_input(
        "Créditos transferibles",
        min_value=1,
        step=1
    )

st.header("2. Selección de ramos")

for codigo, datos in RAMOS.items():
    nombre, t, l = datos
    st.write(f"{codigo}. {nombre}(T{t},L{l})")

seleccion = st.text_input(
    "Ingresa números separados por coma"
)

ramos_finales = []

if seleccion:

    numeros = [
        int(x.strip())
        for x in seleccion.split(",")
        if x.strip().isdigit()
    ]

    for n in numeros:

        if n in RAMOS:
            ramos_finales.append(RAMOS[n])

st.header("3. Horario fijo")

cantidad_bloques = st.number_input(
    "Cantidad de actividades fijas",
    min_value=0,
    step=1
)

bloques_fijos = []

for i in range(cantidad_bloques):

    st.subheader(f"Actividad fija {i+1}")

    nombre = st.text_input(
        f"Nombre actividad {i+1}",
        key=f"nombre_{i}"
    )

    dia = st.selectbox(
        f"Día {i+1}",
        DIAS,
        key=f"dia_{i}"
    )

    inicio = st.time_input(
        f"Hora inicio {i+1}",
        value=time(8, 0),
        key=f"inicio_{i}"
    )

    fin = st.time_input(
        f"Hora fin {i+1}",
        value=time(10, 0),
        key=f"fin_{i}"
    )

    bloques_fijos.append({
        "nombre": nombre,
        "dia": dia,
        "inicio": inicio,
        "fin": fin
    })

st.header("4. Energía")

energia_usuario = {}

for dia in DIAS:

    energia_usuario[dia] = st.selectbox(
        f"Energía predominante {dia}",
        ["Alta", "Media", "Baja"],
        key=f"energia_{dia}"
    )

st.header("5. Restricciones")

descanso_minimo = st.number_input(
    "Horas mínimas entre bloques de estudio",
    min_value=1,
    max_value=8,
    value=2
)

duracion_bloque = st.number_input(
    "Duración de bloques de estudio (horas)",
    min_value=1,
    max_value=4,
    value=2
)

st.header("6. Generar calendario")

def calcular_horas_autonomas(ramos):

    resultado = []

    for ramo in ramos:

        nombre, t, l = ramo

        ht = t * 2
        hl = l * 1

        total = ht + hl

        resultado.append({
            "ramo": nombre,
            "horas": total
        })

    return resultado

def convertir_a_datetime(hora):

    return datetime.combine(datetime.today(), hora)

def bloque_ocupado(dia, inicio, fin, bloques):

    for bloque in bloques:

        if bloque["dia"] != dia:
            continue

        b_inicio = convertir_a_datetime(bloque["inicio"])
        b_fin = convertir_a_datetime(bloque["fin"])

        if inicio < b_fin and fin > b_inicio:
            return True

    return False

def generar_bloques_estudio(
    horas_autonomas,
    bloques_fijos,
    descanso_minimo,
    duracion_bloque
):

    calendario = []

    horas_inicio = 8
    horas_fin = 22

    for ramo in horas_autonomas:

        nombre = ramo["ramo"]
        horas_restantes = ramo["horas"]

        for dia in DIAS:

            hora_actual = horas_inicio

            while hora_actual < horas_fin and horas_restantes > 0:

                inicio = datetime.combine(
                    datetime.today(),
                    time(hora_actual, 0)
                )

                fin = inicio + timedelta(hours=duracion_bloque)

                ocupado = bloque_ocupado(
                    dia,
                    inicio,
                    fin,
                    bloques_fijos
                )

                if not ocupado:

                    calendario.append({
                        "Día": dia,
                        "Inicio": inicio.strftime("%H:%M"),
                        "Fin": fin.strftime("%H:%M"),
                        "Actividad": f"Estudio - {nombre}"
                    })

                    bloques_fijos.append({
                        "nombre": f"Estudio - {nombre}",
                        "dia": dia,
                        "inicio": inicio.time(),
                        "fin": fin.time()
                    })

                    horas_restantes -= duracion_bloque

                    hora_actual += duracion_bloque + descanso_minimo

                else:
                    hora_actual += 1

    return calendario

if st.button("Generar calendario"):

    horas_autonomas = calcular_horas_autonomas(ramos_finales)

    calendario = generar_bloques_estudio(
        horas_autonomas,
        bloques_fijos,
        descanso_minimo,
        duracion_bloque
    )

    st.header("Resumen")

    st.write(f"Universidad: {universidad}")
    st.write(f"CT: {ct}")

    st.subheader("Ramos")

    for ramo in ramos_finales:

        nombre, t, l = ramo

        st.write(f"- {nombre}(T{t},L{l})")

    st.subheader("Horas autónomas")

    total = 0

    for ramo in ramos_finales:

        nombre, t, l = ramo

        st.write(nombre)

        if t > 0:

            ht = t * 2
            total += ht

            st.write(f"- Teoría: {ht} horas")

        if l > 0:

            hl = l * 1
            total += hl

            st.write(f"- Laboratorio/práctica: {hl} horas")

    st.write(f"Horas autónomas semanales totales: {total} horas")

    st.header("Calendario generado")

    if calendario:

        df = pd.DataFrame(calendario)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning(
            "No se pudieron generar bloques."
        )

    st.header("Energía semanal")

    for dia, energia in energia_usuario.items():

        st.write(f"{dia}: {energia}")

    st.write("""
IMPORTANTE: La cantidad de horas puede parecer alta al principio, pero no significa que debas estudiar exactamente esas horas de manera rígida todas las semanas.

Este diagnóstico entrega una referencia aproximada de dedicación académica según la carga de tus ramos y puede ajustarse a tu realidad personal, ritmo de aprendizaje, hábitos de estudio, experiencia previa y disponibilidad semanal.

El objetivo es ayudarte a visualizar tu carga académica de manera más clara y organizada, no asustarte.
""")


