import streamlit as st

from data.storage import load_user_data, save_user_data
from modules.calculos import calcular_indicadores
from modules.diagnostico import diagnosticar
from modules.recomendaciones import generar_recomendaciones
from modules.formulario import render_formulario
from modules.dashboard import render_dashboard
from utils.helpers import apply_page_style, default_user_data


st.set_page_config(
    page_title="Diagnostico Academico Inteligente",
    page_icon=":mortar_board:",
    layout="wide",
)

apply_page_style()


def ensure_state() -> None:
    if "user_data" not in st.session_state:
        stored_data = load_user_data()
        st.session_state.user_data = stored_data or default_user_data()


def main() -> None:
    ensure_state()

    st.title("Diagnostico Academico Inteligente")
    st.caption("Herramienta de orientacion para estimar carga SCT, tiempo disponible y riesgo academico.")

    with st.sidebar:
        st.header("Configuracion")
        st.info(
            "Los datos se guardan automaticamente en este equipo mediante un archivo JSON local."
        )
        if st.button("Restablecer datos", use_container_width=True):
            st.session_state.user_data = default_user_data()
            save_user_data(st.session_state.user_data)
            st.rerun()

    updated_data = render_formulario(st.session_state.user_data)
    st.session_state.user_data = updated_data
    save_user_data(updated_data)

    indicadores = calcular_indicadores(updated_data)
    diagnostico = diagnosticar(updated_data, indicadores)
    recomendaciones = generar_recomendaciones(updated_data, indicadores, diagnostico)

    render_dashboard(updated_data, indicadores, diagnostico, recomendaciones)


if __name__ == "__main__":
    main()

