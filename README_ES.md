# Portafolio de Automatización y Analítica

[![Tests](https://github.com/Erkzucr/automation-analytics-portfolio/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Erkzucr/automation-analytics-portfolio/actions/workflows/python-tests.yml)

Trece casos de estudio sobre conciliación, controles, automatización, análisis e IA aplicada a finanzas. Cada uno tiene código que corre y pruebas que lo verifican. Todo, salvo el caso 10, usa datos inventados para el repo: no hay archivos de producción, nombres de procesos internos ni nada que apunte a un empleador. Los problemas son los que aparecen en un cierre de verdad; las cifras, los códigos, los SOPs y los umbrales se armaron desde cero. El caso 10 es una app real construida para una escuela, publicada sin la configuración de Firebase ni los datos de la escuela.

**[Si estás revisando esto para una vacante](RECRUITER_START_HERE_ES.md)** · [English version](README.md) · [PDF de una página](assets/Erick_Zuniga_Automation_Analytics_Portfolio_OnePager.pdf) · [LinkedIn](https://www.linkedin.com/in/erick-zuniga-finance)

![Resumen del portafolio](assets/portfolio_at_a_glance.png)

## Qué contiene

Los casos 01 a 09 tratan los problemas que se repiten en conciliación y controles: fuentes que no cuadran, excepciones sin dueño, un flux que necesita un umbral escrito, evidencia que un auditor pueda seguir, y documentación redactada con IA pero verificada por una persona antes de usarse. El caso 11 es un agente en Copilot Studio que responde preguntas de política financiera y no tiene forma de tocar el libro mayor. El caso 12 descompone la variación de costo de personal en headcount, tarifa, mix y one-offs. El caso 13 sigue un proyecto de mejora del cierre con valor ganado y genera su propio reporte de estado. El caso 10 es la app de inventario escolar.

Cada caso trae el escrito, un diagrama, datos de muestra con su diccionario, casos de prueba, una matriz de controles y el código que produce el resultado esperado. Las pruebas corren en GitHub Actions con cada push.

```
# Pipeline compartido de los casos 01 a 09: regenera cada expected-output y lo compara
cd demo/case-pipeline
python run_case.py all --check
python -m unittest discover -s tests -v

# Demo de conciliación independiente
cd demo/python-reconciliation-demo
python run_demo.py

# Evaluación del agente, análisis de variaciones, tracker del proyecto
cd case-studies/11-copilot-studio-finance-agent/evaluation && python evaluate_agent.py
cd case-studies/12-people-cost-variance-analysis/analysis && python variance_analysis.py
cd case-studies/13-close-improvement-project-tracker/tracker && python project_tracker.py

# Lógica de la app de inventario, sin React ni Firebase
cd case-studies/10-school-inventory-webapp
node --test tests/*.test.js
```

Hay además un workflow de Alteryx en `demo/alteryx-reconciliation-demo/Synthetic_Reconciliation_Demo.yxmd` que solo lee los archivos sintéticos de su carpeta.

![Resultados de las demos](assets/demo_outputs.png)

## Casos

| # | Caso | Qué muestra |
|---|---|---|
| 01 | [Análisis periódico de una estimación](case-studies/01-periodic-estimate-analysis/README.md) | Validar una estimación contra una referencia y un techo por categoría |
| 02 | [Armonización de múltiples fuentes](case-studies/02-multi-source-harmonization/README.md) | Dos fuentes, un esquema, y el mapa con versión |
| 03 | [Preparación de salidas balanceadas](case-studies/03-balanced-output-preparation/README.md) | Un resumen que no se publica si no cuadra con el detalle |
| 04 | [Monitoreo y priorización de excepciones](case-studies/04-exception-monitoring/README.md) | Qué ve primero quien revisa |
| 05 | [Conciliación fuente contra registro](case-studies/05-source-to-record-reconciliation/README.md) | Full outer match para que nada desaparezca en el join |
| 06 | [Análisis periodo contra periodo](case-studies/06-period-over-period-analysis/README.md) | Flux con umbral escrito |
| 07 | [Gobierno de cálculos por política](case-studies/07-policy-driven-calculation-governance/README.md) | Tasas en un archivo con versión; sin política, excepción |
| 08 | [Ciclo de evidencia de controles](case-studies/08-control-evidence-lifecycle/README.md) | Evidencia que un revisor encuentra después |
| 09 | [Documentación asistida por IA](case-studies/09-ai-assisted-knowledge-capture/README.md) | La IA redacta, una persona verifica |
| 10 | [App de inventario escolar](case-studies/10-school-inventory-webapp/README.md) | Una app real con su lógica bajo prueba |
| 11 | [Agente de finanzas en Copilot Studio](case-studies/11-copilot-studio-finance-agent/README.md) | Agente de solo lectura sobre SOPs, con set de pruebas en CI |
| 12 | [Variaciones de costo de personal](case-studies/12-people-cost-variance-analysis/README.md) | Headcount, tarifa, mix y one-offs; materialidad por monto y porcentaje; KPIs y puente |
| 13 | [Tracker de proyecto de mejora del cierre](case-studies/13-close-improvement-project-tracker/README.md) | Valor ganado, hitos, riesgos con puntaje, reporte generado |

Los escritos de cada caso están en inglés. Los casos 01 a 09 comparten un pipeline en [`demo/case-pipeline`](demo/case-pipeline/README.md); cada uno tiene un `case.json` con su bloque de lógica y sus parámetros. Los datos de muestra incluyen un campo vacío, una clave duplicada, una referencia que no existe y un monto con una letra, para que los casos de prueba documentados se ejecuten y no solo se describan.

En `demo/` hay un [dashboard de Power BI de tres páginas](demo/power-bi-portfolio-dashboard/README.md) sobre los datos del propio portafolio, con los CSV, las medidas DAX y la especificación para reconstruirlo.

![Cobertura de pruebas](assets/portfolio_capability_coverage.png)

Cada caso se califica contra una [rúbrica escrita](docs/IMPACT_MEASUREMENT_FRAMEWORK.md). Para llegar a profundidad 5 se necesita código ejecutable, pruebas y CI. Los trece cumplen, y el badge de arriba es la verificación.

## Cómo se aborda el trabajo

Primero estandarizar, luego automatizar, con los controles diseñados desde el inicio y un dueño con nombre después de salir a producción. Las herramientas han sido Alteryx, Power Query, VBA, Python, Power Automate y Copilot Studio, según la pieza. El orden no cambia con la herramienta.

En los casos con IA (09 y 11) aplica una regla más: el modelo redacta o explica, una persona decide, y lo que la herramienta puede tocar se define en la configuración y no en el prompt. Las [notas de decisión](docs/decisions/) explican el razonamiento.

## Datos

Los CSV, las cifras, las "empresas", los SOPs y el plan de proyecto se crearon para este repo. Nada viene de un sistema productivo ni de un proceso de un empleador.
