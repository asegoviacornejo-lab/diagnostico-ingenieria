# Diagnostico Academico Inteligente

Aplicacion modular en Streamlit para estimar carga academica SCT, tiempo semanal disponible y riesgo academico inicial.

## Arquitectura

```text
app.py
modules/
    formulario.py
    calculos.py
    diagnostico.py
    dashboard.py
    recomendaciones.py
data/
    storage.py
utils/
    helpers.py
AGENTS.md
requirements.txt
```

## Flujo de datos

1. `app.py` carga datos guardados o valores por defecto.
2. `modules/formulario.py` captura informacion del estudiante.
3. `data/storage.py` guarda automaticamente los datos en JSON local.
4. `modules/calculos.py` calcula SCT, horas semestrales, horas semanales y balance.
5. `modules/diagnostico.py` clasifica el nivel de riesgo.
6. `modules/recomendaciones.py` genera recomendaciones iniciales.
7. `modules/dashboard.py` muestra metricas, estado visual, observaciones y detalle por asignatura.

## Decision de persistencia

### Session State

Ventaja: es inmediato y funciona muy bien durante una sesion de Streamlit.

Desventaja: no basta para recuperar datos despues de recargar o cerrar la aplicacion.

### JSON local

Ventaja: simple, transparente, facil de revisar y suficiente para un prototipo individual.

Desventaja: no es ideal para muchos usuarios, historiales complejos o consultas.

### SQLite

Ventaja: mejor para multiples perfiles, historiales, analitica y consultas.

Desventaja: agrega algo mas de estructura desde el inicio.

### Base de datos futura

Ventaja: permitiria usuarios reales, autenticacion, sincronizacion y despliegue.

Desventaja: requiere decisiones de seguridad, hosting y mantenimiento.

## Eleccion actual

La primera version usa JSON local para persistencia y Session State para la experiencia inmediata. SQLite queda como evolucion recomendada cuando el proyecto necesite perfiles, historiales o varios usuarios.

## Ejecucion

```powershell
pip install -r requirements.txt
streamlit run app.py
```
