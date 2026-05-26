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
- identifica horarios ocupados
- considera responsabilidades personales
- considera energía
- genera múltiples horarios posibles
- mantiene proporcionalidad entre ramos
""")

RAMOS = {
    "Introducción al Cálculo": (6, 2),
    "Introducción al Álgebra": (6, 2),
    "Introducción a la Ingeniería": (4, 0),
    "Taller de Estrategias de Aprendizaje para Ingeniería": (0, 4),
    "Cálculo Diferencial e Integral": (6, 0),
    "Cálculo Integral": (6, 0),
    "Álgebra Lineal": (6, 0),
    "Física Newtoniana": (6, 2),
    "Física Newtoniana para Ingenieros": (6, 2),
    "Taller de Habilidades Comunicativas para Ingeniería": (0, 2),
    "Taller de Habilidades Comunicativas para Ingenieros": (0, 4),
    "Dibujo de Ingeniería": (2, 2),
    "Herramientas Computacionales para Ingeniería": (0, 2),
    "Fundamentos de Programación y Computación": (2, 2),
    "Cálculo en Varias Variables": (4, 0),
    "Cálculo Vectorial": (6, 0),
    "Ecuaciones Diferenciales": (4, 0),
    "Electromagnetismo M2024": (4, 2),
    "Electromagnetismo M2023": (6, 2),
    "Química General": (4, 2),
    "Programación para Ingeniería": (0, 4),
    "Termodinámica": (4, 0),
    "Probabilidad y Estadística": (4, 0),
    "Estadística Aplicada": (6, 0),
    "Óptica y Ondas": (4, 2),
    "Mecánica": (4, 2),
    "Mecánica Estática": (6, 0),
    "Desafío de Proyecto de Ingeniería I": (0, 4),
    "Inglés para Ingeniería I": (2, 2),
    "Métodos Numéricos para Ingeniería": (4, 0),
    "Métodos Numéricos": (6, 0),
    "Ciencias de Materiales": (4, 2),
    "Ingeniería de Materiales": (2, 2),
    "Fundamentos de Economía": (4, 0),
    "Mecánica de Sólidos M2024": (4, 2),
    "Mecánica de Sólidos M2023": (6, 0),
    "Investigación de Operaciones": (4, 0),
    "Inglés para Ingeniería II": (2, 2),
    "Filosofía de las Ciencias de la Ingeniería": (4, 0),
    "Taller de Creatividad": (0, 2)
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

HORAS = list(range(0, 24))
st.header("1. Información universitaria")

uls = st.radio(
    "¿Eres estudiante de la Universidad de La Serena?",
    ["Sí", "No"]
)

if uls == "Sí":

    universidad = "Universidad de La Serena"
    ct = 27
    horas_credito = "Automático"

else:

    universidad = st.text_input(
        "Nombre de tu universidad"
    )

    horas_credito = st.text_input(
        "¿A cuántas horas equivale 1 crédito transferible en tu universidad?"
    )

    if horas_credito.strip() == "":
        horas_credito = "Estimado"

    ct = st.number_input(
        "Cantidad de créditos transferibles",
        min_value=1,
        step=1
    )

st.header("2. Selección de ramos")

opciones_ramos = []

for nombre, datos in RAMOS.items():

    t, l = datos

    opciones_ramos.append(
        f"{nombre} (T{t},L{l})"
    )

seleccion_ramos = st.multiselect(
    "Selecciona tus ramos",
    opciones_ramos
)

ramos = []

for seleccion in seleccion_ramos:

    for nombre, datos in RAMOS.items():

        t, l = datos

        texto = f"{nombre} (T{t},L{l})"

        if seleccion == texto:

            ramos.append({
                "nombre": nombre,
                "teoria": t,
                "laboratorio": l
            })

st.subheader("Agregar ramo personalizado")

agregar_otro = st.checkbox(
    "Agregar ramo OTRO"
)

if agregar_otro:

    nombre_otro = st.text_input(
        "Nombre ramo"
    )

    teoria_otro = st.number_input(
        "Horas teoría",
        min_value=0,
        step=1
    )

    laboratorio_otro = st.number_input(
        "Horas laboratorio/práctica",
        min_value=0,
        step=1
    )

    if nombre_otro:

        ramos.append({
            "nombre": nombre_otro,
            "teoria": teoria_otro,
            "laboratorio": laboratorio_otro
        })

# ==================================================
# 3. ACTIVIDADES PERSONALES
# ==================================================

st.header("3. Actividades y responsabilidades")

st.write("""
Selecciona las actividades que forman parte de tu rutina.
""")

ACTIVIDADES = {
    "Clase": {
        "energia": 2,
        "permite_estudio": False,
        "descanso": False
    },

    "Trabajo": {
        "energia": 5,
        "permite_estudio": False,
        "descanso": False
    },

    "Transporte": {
        "energia": 2,
        "permite_estudio": True,
        "descanso": False
    },

    "Descanso": {
        "energia": -2,
        "permite_estudio": False,
        "descanso": True
    },

    "Gimnasio": {
        "energia": 4,
        "permite_estudio": False,
        "descanso": False
    },

    "Tiempo personal": {
        "energia": 1,
        "permite_estudio": False,
        "descanso": True
    },

    "Almuerzo": {
        "energia": 1,
        "permite_estudio": False,
        "descanso": True
    },

    "Libre": {
        "energia": 0,
        "permite_estudio": False,
        "descanso": False
    }
}

# ==================================================
# AGREGAR RAMOS COMO ACTIVIDADES
# ==================================================

for ramo in ramos:

    ACTIVIDADES[ramo["nombre"]] = {
        "energia": 3,
        "permite_estudio": False,
        "descanso": False
    }

# ==================================================
# 4. ENERGÍA GENERAL
# ==================================================

st.header("4. Energía durante el día")

energia = {}

columnas = st.columns(3)

for i, hora in enumerate(range(6, 24)):

    with columnas[i % 3]:

        energia[hora] = st.slider(
            f"{hora}:00",
            1,
            5,
            3
        )

# ==================================================
# 5. SUEÑO
# ==================================================

st.header("5. Horario de sueño")

hora_dormir = st.slider(
    "Hora de dormir",
    0,
    23,
    23
)

hora_despertar = st.slider(
    "Hora de despertar",
    0,
    23,
    7
)

horas_sueno = []

if hora_dormir > hora_despertar:

    for h in range(hora_dormir, 24):
        horas_sueno.append(h)

    for h in range(0, hora_despertar):
        horas_sueno.append(h)

else:

    for h in range(hora_dormir, hora_despertar):
        horas_sueno.append(h)

# ==================================================
# 6. AGENDA SEMANAL
# ==================================================

st.header("6. Agenda semanal")

st.write("""
Completa tu semana seleccionando actividades.
""")

opciones = list(ACTIVIDADES.keys())

agenda = pd.DataFrame(
    "Libre",
    index=[f"{h}:00" for h in HORAS],
    columns=DIAS
)

for hora in horas_sueno:

    agenda.loc[f"{hora}:00"] = "Dormir"

agenda_final = st.data_editor(
    agenda,
    use_container_width=True,
    column_config={
        dia: st.column_config.SelectboxColumn(
            dia,
            options=opciones + ["Dormir"]
        )
        for dia in DIAS
    }
)

# ==================================================
# 7. DETECTAR BLOQUES DISPONIBLES
# ==================================================

st.header("7. Disponibilidad detectada")

bloques_disponibles = []

for dia in DIAS:

    for hora in HORAS:

        actividad = agenda_final.loc[f"{hora}:00", dia]

        energia_hora = energia.get(hora, 1)

        if actividad == "Libre" and energia_hora >= 2:

            bloques_disponibles.append({
                "día": dia,
                "hora": hora,
                "energía": energia_hora
            })

        elif actividad == "Transporte":

            bloques_disponibles.append({
                "día": dia,
                "hora": hora,
                "energía": energia_hora,
                "tipo": "Estudio ligero"
            })

st.success(
    f"Se detectaron {len(bloques_disponibles)} bloques potenciales de estudio."
)
