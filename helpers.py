from __future__ import annotations


def generar_recomendaciones(data: dict, indicadores: dict, diagnostico: dict) -> list[str]:
    estado = data.get("estado", {})
    tiempo = data.get("tiempo", {})
    sueno = data.get("sueno", {})

    recomendaciones = []
    diferencia = float(indicadores.get("diferencia", 0.0) or 0.0)
    cobertura = float(indicadores.get("cobertura", 1.0) or 0.0)

    if diferencia < -3:
        recomendaciones.append(
            f"Reorganiza la semana para recuperar al menos {abs(diferencia):.1f} horas o reduce compromisos no criticos durante evaluaciones."
        )
    elif cobertura >= 1.1:
        recomendaciones.append(
            "Usa el superavit de tiempo para adelantar entregas, practicar ejercicios acumulativos o reforzar ramos de mayor dificultad."
        )
    else:
        recomendaciones.append(
            "Mantene bloques de estudio estables y revisa semanalmente si las horas planificadas se estan cumpliendo."
        )

    if int(estado.get("organizacion", 3) or 3) <= 2:
        recomendaciones.append(
            "Implementa una planificacion semanal con bloques por asignatura, fechas de evaluacion y una revision breve cada domingo."
        )

    if int(estado.get("comprension", 3) or 3) <= 2:
        recomendaciones.append(
            "Prioriza ayudantias, consultas docentes o grupos de estudio antes de que se acumulen vacios conceptuales."
        )

    if int(estado.get("estres", 3) or 3) >= 4:
        recomendaciones.append(
            "Reserva bloques de recuperacion y evita concentrar todo el estudio en jornadas extensas de ultima hora."
        )

    if int(estado.get("motivacion", 3) or 3) <= 2:
        recomendaciones.append(
            "Divide las tareas grandes en metas pequenas de avance visible para reducir friccion al comenzar."
        )

    if float(sueno.get("horas_recuperacion", 0.0) or 0.0) - float(sueno.get("horas_normales", 0.0) or 0.0) >= 1.5:
        recomendaciones.append(
            "Ajusta horarios de cierre del dia: la brecha de sueno puede estar afectando memoria, concentracion y tolerancia al estres."
        )

    if float(tiempo.get("horas_trabajo", 0.0) or 0.0) >= 20:
        recomendaciones.append(
            "Considera una estrategia especial para semanas con evaluaciones, porque el trabajo consume una fraccion alta de energia semanal."
        )

    if diagnostico.get("nivel") == "rojo":
        recomendaciones.append(
            "Agenda una conversacion con jefatura de carrera, docente guia o unidad de apoyo estudiantil para priorizar decisiones."
        )

    return recomendaciones[:6]
