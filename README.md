# Optimización de Flujos en Redes Ferroviarias

## Descripción

Este proyecto implementa un modelo para analizar flujos de pasajeros en una red ferroviaria y evaluar el impacto de distintas configuraciones de demanda, capacidad y frecuencia del servicio.

A partir de distintas instancias de la red (por ejemplo Retiro–Tigre y Victoria–Cardales), el modelo permite estudiar cómo varía el flujo de pasajeros bajo distintos escenarios operativos.

---

## Componentes del proyecto

- Modelado de la red ferroviaria como un grafo.
- Definición de demandas de pasajeros entre estaciones.
- Simulación de flujos bajo distintas capacidades y frecuencias.
- Evaluación de distintos escenarios operativos.

---

## Estructura del repositorio

- `src/main_alu.py` – Implementación principal del modelo de flujos en la red.
- `instances/` – Instancias del problema con diferentes configuraciones de demanda, capacidad y frecuencia.
- `tools/instance_converter.py` – Herramienta para generar o convertir instancias del problema.
- `tools/toy_instance.csv` – Datos de ejemplo para generación de instancias.
- `enunciado/` – Material teórico y enunciado del trabajo.
- `tdv_tp2_cauzzo_dolhare_squillari.pdf` – Informe técnico del proyecto.

---

## Resultados

El modelo permite analizar cómo distintas configuraciones de capacidad, frecuencia y demanda afectan el comportamiento de los flujos en la red ferroviaria.

Las simulaciones permiten comparar escenarios y evaluar el impacto de cambios operativos en el sistema.

---

## Autoría

- Catalina Dolhare   
- camila Cauzzo  
- Renata Squillari
