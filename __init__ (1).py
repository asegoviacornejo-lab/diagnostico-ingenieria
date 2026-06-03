from __future__ import annotations

import streamlit as st


def _asignatura_vacia() -> dict:
    return {"nombre": "", "sct": 0.0}


def _normalizar_asignaturas(asignaturas: list[dict]) -> list[dict]:
    limpias = []
    for asignatura in asignaturas:
        nombre = str(asignatura.get("nombre", "")).strip()
        sct = float(asignatura.get("sct", 0.0) or 0.0)
        if nombre or sct > 0:
            limpias.append({"nombre": nombre, "sct": sct})
    return limpias or [_asignatura_vacia()]


def render_formulario(data: dict) -> dict:
    updated = {
        "configuracion": dict(data["configuracion"]),
        "asignaturas": list(data["asignaturas"]),
        "sueno": dict(data["sueno"]),
        "tiempo": dict(data["tiempo"]),
        "estado": dict(data["estado"]),
    }

    st.subheader("Ingreso de informacion")

    with st.expander("Configuracion SCT", expanded=True):
        col_sct, col_sem = st.columns(2)
        with col_sct:
            updated["configuracion"]["valor_sct_horas"] = st.number_input(
                "Valor de 1 SCT en horas",
                min_value=1.0,
                max_value=60.0,
                value=float(updated["configuracion"].get("valor_sct_horas", 27.0)),
                step=0.5,
            )
        with col_sem:
            updated["configuracion"]["semanas_semestre"] = st.number_input(
                "Semanas del semestre",
                min_value=1,
                max_value=30,
                value=int(updated["configuracion"].get("semanas_semestre", 18)),
                step=1,
            )

    with st.expander("Asignaturas", expanded=True):
        asignaturas = _normalizar_asignaturas(updated["asignaturas"])
        nuevas_asignaturas = []

        for index, asignatura in enumerate(asignaturas):
            cols = st.columns([3, 1, 0.9])
            with cols[0]:
                nombre = st.text_input(
                    "Nombre",
                    value=asignatura.get("nombre", ""),
                    key=f"asignatura_nombre_{index}",
                    label_visibility="collapsed",
                    placeholder="Nombre de la asignatura",
                )
            with cols[1]:
                sct = st.number_input(
                    "SCT",
                    min_value=0.0,
                    max_value=20.0,
                    value=float(asignatura.get("sct", 0.0)),
                    step=0.5,
                    key=f"asignatura_sct_{index}",
                    label_visibility="collapsed",
                )
            with cols[2]:
                eliminar = st.button(
                    "Eliminar",
                    key=f"eliminar_asignatura_{index}",
                    use_container_width=True,
                )

            if not eliminar:
                nuevas_asignaturas.append({"nombre": nombre.strip(), "sct": sct})

        if st.button("Agregar asignatura", use_container_width=True):
            nuevas_asignaturas.append(_asignatura_vacia())

        updated["asignaturas"] = nuevas_asignaturas or [_asignatura_vacia()]

    col_a, col_b = st.columns(2)
    with col_a:
        with st.expander("Sueno", expanded=True):
            updated["sueno"]["horas_normales"] = st.slider(
                "Horas que duermes normalmente",
                min_value=0.0,
                max_value=12.0,
                value=float(updated["sueno"].get("horas_normales", 6.5)),
                step=0.5,
            )
            updated["sueno"]["horas_recuperacion"] = st.slider(
                "Horas que necesitas para recuperarte completamente",
                min_value=0.0,
                max_value=12.0,
                value=float(updated["sueno"].get("horas_recuperacion", 8.0)),
                step=0.5,
            )

    with col_b:
        with st.expander("Tiempo disponible", expanded=True):
            updated["tiempo"]["horas_disponibles"] = st.number_input(
                "Horas semanales disponibles fuera de clases",
                min_value=0.0,
                max_value=120.0,
                value=float(updated["tiempo"].get("horas_disponibles", 30.0)),
                step=1.0,
            )
            updated["tiempo"]["horas_trabajo"] = st.number_input(
                "Horas semanales de trabajo",
                min_value=0.0,
                max_value=80.0,
                value=float(updated["tiempo"].get("horas_trabajo", 0.0)),
                step=1.0,
            )
            updated["tiempo"]["horas_traslado"] = st.number_input(
                "Horas semanales de traslado",
                min_value=0.0,
                max_value=50.0,
                value=float(updated["tiempo"].get("horas_traslado", 5.0)),
                step=1.0,
            )
            updated["tiempo"]["actividades_personales"] = st.text_area(
                "Actividades personales relevantes",
                value=str(updated["tiempo"].get("actividades_personales", "")),
                placeholder="Ej.: deporte, cuidados familiares, ayudantias, salud, voluntariado.",
            )

    with st.expander("Estado academico percibido", expanded=True):
        cols = st.columns(4)
        labels = {
            "comprension": "Comprension de contenidos",
            "organizacion": "Organizacion",
            "motivacion": "Motivacion",
            "estres": "Estres",
        }
        for index, key in enumerate(labels):
            with cols[index]:
                updated["estado"][key] = st.slider(
                    labels[key],
                    min_value=1,
                    max_value=5,
                    value=int(updated["estado"].get(key, 3)),
                    step=1,
                )

    return updated
