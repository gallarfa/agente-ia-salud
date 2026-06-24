# 🧠 Agente Inteligente de Clasificación de Urgencias (Triage) en Salud Mental

**Materia:** Inteligencia Artificial Aplicada al Desarrollo de Software  
**Estudiante:** Gallardo Fernando Andrés  
**Carrera:** 3° año de Analista de Sistemas  
**Profesora:** Miriam Elena Coronel  
**Instituto:** Instituto Superior Combate de Mbororé  
**Fecha:** Junio de 2026  

---

## 📌 Descripción General del Proyecto

Este proyecto consiste en una solución de software inteligente en Python diseñada para optimizar los procesos de admisión y triage en centros y hospitales de salud mental. El sistema analiza los textos o motivos de consulta ingresados por los pacientes (o sus acompañantes) y clasifica automáticamente la prioridad de atención en tres niveles de urgencia clínica:

- 🔴 **ALTA:** Casos con riesgo inminente de vida, ideaciones activas de autolesión/suicidio, delirios severos, agresiones incontroladas o brotes psicóticos agudos.
- 🟡 **MEDIA:** Crisis agudas pero estables, episodios de pánico severos, llanto desmedido recurrente, angustia invalidante o problemas de consumos problemáticos sin sobredosis.
- 🟢 **BAJA:** Consultas netamente administrativas como pedido y renovación de recetas médicas, consultas o cambios de turnos, y trámites generales.

---

## ❗ Problema Clínico que Resuelve

En las salas de espera y mesas de entradas de salud mental, la recepción física o digital suele congestionarse. Un administrativo sin conocimientos clínicos puede demorar la detección de una crisis de autolesión inminente por estar procesando pedidos rutinarios de recetas o turnos.

Este sistema asiste al personal en la pre-clasificación, logrando:
1. **Detección inmediata:** Identificación instantánea de discursos clínicos graves.
2. **Priorización de guardia:** Desvío inmediato de casos 🔴 a la guardia médica especializada.
3. **Eficiencia administrativa:** Automatización de la derivación de trámites programados 🟢.
4. **Privacidad garantizada:** Seguridad legal de la información del paciente al procesar todo de manera local.

---

## 🚀 Arquitectura y Versiones del Sistema

El proyecto cuenta con dos enfoques de desarrollo para demostrar la evolución de un sistema de software tradicional hacia la integración de Inteligencia Artificial:

### 1️⃣ Agente por Reglas Rígidas (`agente.py`)
Utiliza una lógica de programación clásica estructurada en Python basada en búsquedas condicionales de palabras clave e incorporación de sinónimos dialectales locales (ej. *"bajón"*, *"crisis"*, *"pastillas"*).
- **Ventajas:** Extremadamente rápido, cero consumo de hardware, no requiere conexión externa ni librerías adicionales.
- **Desventajas:** Vulnerable a falsos negativos si el paciente expresa su dolor de forma indirecta sin utilizar palabras clave explícitas (ej. *"no quiero despertar mañana"*).

### 2️⃣ Agente IA Semántico Local (`agente_ollama.py`)
Utiliza la API HTTP local de **Ollama** para comunicarse con el modelo de lenguaje de gran tamaño **Llama 3.2** de Meta (3 mil millones de parámetros), procesando toda la información semántica en lenguaje natural dentro del propio hardware local de la institución.
- **Ventajas:** Comprensión profunda del contexto y lenguaje figurado, flexibilidad ante sinónimos y modismos, y explicación razonada de la prioridad.
- **Desventajas:** Requiere mayor capacidad de cómputo (CPU/GPU) y la instalación local de Ollama.

---

## ⚙️ Características Destacadas de la Nueva Versión

El sistema ha sido mejorado significativamente, incorporando:
- **Consola Interactiva:** Menú interactivo para ejecutar lotes de prueba preestablecidos o evaluar consultas personalizadas escritas en tiempo real por teclado.
- **Triage Clínico Manchester Adaptado:** El System Prompt ha sido refinado con criterios formales y objetivos de evaluación psiquiátrica.
- **Parser Robustecido de JSON:** Limpieza y reparación de respuestas mediante expresiones regulares de Python para evitar fallas ante errores de sintaxis del modelo.
- **Generador de Reportes HTML:** Exportación automática de un dashboard gráfico web interactivo (`reporte_triage.html`) que resume la estadística del lote analizado mediante tarjetas de colores y listas organizadas de pacientes.
- **Exportación CSV:** Ambos agentes exportan sus clasificaciones a archivos CSV estructurados (`resultados.csv` y `resultados_ollama.csv`) para permitir auditorías posteriores del equipo de salud humana.

---

## 💻 Requisitos del Sistema

- **Python 3.8 o superior**
- **Librería de Requests** (instalable mediante `pip install requests`)
- **Ollama** (para la ejecución local del agente semántico avanzado)
- **Modelo Llama 3.2** (descargable localmente)

---

## 🛠️ Guía de Instalación y Configuración

### Paso 1: Clonar el Proyecto
Descarga el proyecto en tu entorno local.

### Paso 2: Instalar Dependencias de Python
Instala las dependencias necesarias indicadas en `requirements.txt` ejecutando en tu consola:
```bash
pip install -r requirements.txt
```

### Paso 3: Instalar Ollama
1. Descarga e instala Ollama en tu sistema operativo desde [ollama.com](https://ollama.com).
2. Abre tu terminal y descarga el modelo Llama 3.2:
   ```bash
   ollama pull llama3.2
   ```
3. Asegúrate de tener Ollama ejecutándose en segundo plano (puedes verificarlo levantando la terminal e ingresando `ollama serve`).

---

## ▶️ Instrucciones de Ejecución

### Ejecución del Agente por Reglas
En tu terminal de comandos, dirígete a la carpeta del proyecto y ejecuta:
```bash
python agente.py
```

### Ejecución del Agente con Ollama (IA Local)
Asegúrate de que Ollama está activo y ejecuta en tu terminal:
```bash
python agente_ollama.py
```

---

## 📊 Ejemplo de Funcionamiento y Resultados de Salida

### Entrada del Paciente:
> *"Estoy muy nervioso, me late rápido el corazón y me cuesta respirar."*

### Salida del Agente Ollama (JSON Procesado):
```json
{
  "prioridad": "MEDIA",
  "justificacion": "El paciente presenta sintomatología compatible con un cuadro agudo de ansiedad o crisis de pánico (taquicardia, disnea) sin indicios inminentes de autolesión."
}
```

- **Derivación recomendada:** Consultorio de Urgencia Ambulatoria / Psiquiatría.
- **Plazo máximo:** Dentro de las 24 horas.
- **Emoji visual en consola:** 🟡

---

## 📂 Contenido del Proyecto (`FINAL/`)

- `agente.py`: Script del agente clasificador basado en reglas rígidas y condicionales.
- `agente_ollama.py`: Script del agente avanzado que integra Ollama local y genera reportes HTML/CSV.
- `informe_etica.md`: Documento de análisis ético, mitigación de sesgos, privacidad de datos y marco legal de Argentina.
- `requirements.txt`: Archivo de configuración de dependencias de Python.
- `README.md`: Este archivo instructivo de documentación del proyecto.
