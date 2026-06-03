from __future__ import annotations


def diagnosticar(data: dict, indicadores: dict) -> dict:
    estado = data.get("estado", {})
    sueno = data.get("sueno", {})

    cobertura = float(indicadores.get("cobertura", 1.0) or 0.0)
    deficit_horas = min(0.0, float(indicadores.get("diferencia", 0.0) or 0.0))
    comprension = int(estado.get("comprension", 3) or 3)
    organizacion = int(estado.get("organizacion", 3) or 3)
    motivacion = int(estado.get("motivacion", 3) or 3)
    estres = int(estado.get("estres", 3) or 3)
    sueno_normal = float(sueno.get("horas_normales", 0.0) or 0.0)
    sueno_recuperacion = float(sueno.get("horas_recuperacion", 0.0) or 0.0)

    puntos_riesgo = 0
    factores = []

    if cobertura < 0.75:
        puntos_riesgo += 3
        factores.append("La disponibilidad semanal cubre menos del 75% de la carga SCT estimada.")
    elif cobertura < 0.95:
        puntos_riesgo += 2
        factores.append("La disponibilidad semanal queda ajustada frente a la carga SCT.")
    elif cobertura < 1.1:
        puntos_riesgo += 1
        factores.append("La disponibilidad y la carga esperada estan cerca del equilibrio.")

    if deficit_horas <= -10:
        puntos_riesgo += 2
        factores.append("Existe un deficit semanal relevante de horas.")
    elif deficit_horas <= -3:
        puntos_riesgo += 1
        factores.append("Existe un deficit semanal moderado.")

    if estres >= 4:
        puntos_riesgo += 2
        factores.append("El nivel de estres percibido es alto.")

    if comprension <= 2:
        puntos_riesgo += 2
        factores.append("La comprension percibida de contenidos requiere apoyo temprano.")

    if organizacion <= 2:
        puntos_riesgo += 1
        factores.append("La organizacion percibida puede estar limitando el rendimiento.")

    if motivacion <= 2:
        puntos_riesgo += 1
        factores.append("La motivacion percibida esta baja y puede afectar la continuidad del estudio.")

    if sueno_recuperacion - sueno_normal >= 1.5:
        puntos_riesgo += 1
        factores.append("Hay una brecha importante entre el sueno actual y el sueno reparador.")

    if puntos_riesgo >= 7:
        nivel = "rojo"
        titulo = "Riesgo alto"
        resumen = "La carga academica muestra senales de tension importante y conviene intervenir pronto."
    elif puntos_riesgo >= 4:
        nivel = "amarillo"
        titulo = "Riesgo moderado"
        resumen = "La carga parece manejable solo con ajustes claros de tiempo, organizacion o apoyo."
    else:
        nivel = "verde"
        titulo = "Carga sostenible"
        resumen = "La relacion entre carga, tiempo y estado percibido se ve razonablemente sostenible."

    return {
        "nivel": nivel,
        "titulo": titulo,
        "resumen": resumen,
        "puntos_riesgo": puntos_riesgo,
        "factores": factores,
    }
