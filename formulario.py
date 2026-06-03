from __future__ import annotations

import streamlit as st

from utils.helpers import clamp


def _format_hours(value: float) -> str:
    return f"{value:.1f} h"


def _status_color(nivel: str) -> str:
    return {
        "verde": "#15803d",
        "amarillo": "#b45309",
        "rojo": "#b91c1c",
    }.get(nivel, "#334155")


def render_dashboard(data: dict, indicadores: dict, diagnostico: dict, recomendaciones: list[str]) -> None:
    st.divider()
    st.subheader("Resultados del diagnostico")

    metric_cols = st.columns(4)
    metric_cols[0].metric("SCT totales", f"{indicadores['sct_total']:.1f}")
    metric_cols[1].metric("Horas semestrales", _format_hours(indicadores["horas_semestrales"]))
    metric_cols[2].metric("Horas semanales esperadas", _format_hours(indicadores["horas_semanales_esperadas"]))
    metric_cols[3].metric(
        "Balance semanal",
        indicadores["balance"],
        delta=_format_hours(indicadores["diferencia"]),
    )

    nivel = diagnostico["nivel"]
    color = _status_color(nivel)
    st.markdown(
        f"""
        <div class="status-card status-{nivel}">
            <h3 style="margin:0;color:{color};">{diagnostico["titulo"]}</h3>
            <p style="margin:0.35rem 0 0 0;">{diagnostico["resumen"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cobertura = clamp(float(indicadores.get("cobertura", 0.0) or 0.0), 0.0, 1.5)
    st.write("Cobertura de horas disponibles frente a carga esperada")
    st.progress(int(min(cobertura, 1.0) * 100), text=f"{indicadores['cobertura'] * 100:.0f}%")

    col_left, col_right = st.columns([1.05, 0.95])
    with col_left:
        st.markdown("#### Observaciones automaticas")
        if diagnostico["factores"]:
            for factor in diagnostico["factores"]:
                st.write(f"- {factor}")
        else:
            st.write("- No se observan alertas importantes con los datos actuales.")

        actividades = data.get("tiempo", {}).get("actividades_personales", "").strip()
        if actividades:
            st.markdown("#### Actividades personales consideradas")
            st.write(actividades)

    with col_right:
        st.markdown("#### Recomendaciones iniciales")
        for recomendacion in recomendaciones:
            st.write(f"- {recomendacion}")

    with st.expander("Detalle por asignatura"):
        asignaturas = data.get("asignaturas", [])
        if not asignaturas:
            st.write("Aun no hay asignaturas registradas.")
            return

        valor_sct = float(data.get("configuracion", {}).get("valor_sct_horas", 27.0) or 27.0)
        semanas = int(data.get("configuracion", {}).get("semanas_semestre", 18) or 18)
        semanas = max(semanas, 1)

        rows = []
        for asignatura in asignaturas:
            sct = float(asignatura.get("sct", 0.0) or 0.0)
            rows.append(
                {
                    "Asignatura": asignatura.get("nombre", "Sin nombre") or "Sin nombre",
                    "SCT": sct,
                    "Horas semestre": round(sct * valor_sct, 1),
                    "Horas semana": round((sct * valor_sct) / semanas, 1),
                }
            )

        st.dataframe(rows, use_container_width=True, hide_index=True)
