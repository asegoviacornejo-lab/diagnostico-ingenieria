# Diagnostico Academico Inteligente

## Contexto

Aplicacion web en Streamlit para ayudar a estudiantes universitarios a analizar carga academica, habitos de estudio, tiempo disponible y riesgo academico.

El foco inicial son estudiantes de Ingenieria Civil Industrial hasta quinto nivel y otras Ingenierias Civiles en plan comun de la Universidad de La Serena, manteniendo uso general para cualquier estudiante.

## Reglas de producto

- Priorizar claridad pedagogica sobre complejidad tecnica innecesaria.
- Explicar resultados con lenguaje directo, respetuoso y accionable.
- Evitar juicios personales; hablar de condiciones, riesgos y alternativas.
- Mantener el sistema modular y facil de ampliar.
- Separar interfaz, calculos, diagnostico, recomendaciones y persistencia.

## Reglas SCT

- El valor por defecto de 1 SCT es 27 horas.
- Las horas semestrales se calculan como: SCT totales * valor SCT.
- Las horas semanales esperadas se calculan como: horas semestrales / 18 semanas.
- La comparacion principal enfrenta horas semanales esperadas contra horas semanales disponibles fuera de clases.

## Criterios de diagnostico

- Verde: carga sostenible.
- Amarillo: riesgo moderado.
- Rojo: riesgo alto.
- El diagnostico debe considerar disponibilidad, deficit/superavit, sueno, estres, organizacion, motivacion y comprension.

## Persistencia

- En la primera version se usa JSON local para mantener datos al recargar.
- Session State se usa solo para la experiencia inmediata dentro de Streamlit.
- SQLite sera preferible cuando se requieran multiples usuarios, historiales, busqueda o analitica.

## Estilo de codigo

- Usar funciones pequenas con nombres claros.
- Mantener comentarios breves solo donde agreguen contexto.
- No concentrar toda la logica en `app.py`.
- Agregar nuevas funcionalidades en modulos especificos.
