from __future__ import annotations


def calcular_indicadores(data: dict) -> dict:
    asignaturas = data.get("asignaturas", [])
    configuracion = data.get("configuracion", {})
    tiempo = data.get("tiempo", {})

    valor_sct = float(configuracion.get("valor_sct_horas", 27.0) or 27.0)
    semanas = int(configuracion.get("semanas_semestre", 18) or 18)
    semanas = max(semanas, 1)

    sct_total = sum(float(asignatura.get("sct", 0.0) or 0.0) for asignatura in asignaturas)
    horas_semestrales = sct_total * valor_sct
    horas_semanales_esperadas = horas_semestrales / semanas
    horas_disponibles = float(tiempo.get("horas_disponibles", 0.0) or 0.0)
    diferencia = horas_disponibles - horas_semanales_esperadas

    if diferencia >= 3:
        balance = "Superavit"
    elif diferencia <= -3:
        balance = "Deficit"
    else:
        balance = "Equilibrio"

    cobertura = 1.0
    if horas_semanales_esperadas > 0:
        cobertura = horas_disponibles / horas_semanales_esperadas

    return {
        "sct_total": sct_total,
        "horas_semestrales": horas_semestrales,
        "horas_semanales_esperadas": horas_semanales_esperadas,
        "horas_disponibles": horas_disponibles,
        "diferencia": diferencia,
        "balance": balance,
        "cobertura": cobertura,
    }
