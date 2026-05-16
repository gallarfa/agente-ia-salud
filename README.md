# 🧠 Agente Inteligente de Clasificación de Urgencias en Salud Mental

## 📌 Descripción del Proyecto

Este proyecto consiste en un agente desarrollado en Python que analiza el motivo de consulta de pacientes dentro de un sistema de salud mental y clasifica automáticamente el nivel de urgencia del caso.

El sistema asigna una prioridad:

- 🔴 ALTA
- 🟡 MEDIA
- 🟢 BAJA

El objetivo es ayudar al personal de salud a priorizar rápidamente casos críticos y mejorar los tiempos de respuesta.

---

# ❗ Problema que resuelve

En centros de salud mental pueden ingresar múltiples consultas al mismo tiempo y muchas veces no existe una clasificación automática inicial.

Este sistema ayuda a:

- Detectar casos urgentes rápidamente
- Reducir tiempos de espera
- Optimizar recursos
- Asistir al personal administrativo
- Mejorar la atención inicial al paciente

---

# 🚀 Versiones del Proyecto

Actualmente el proyecto cuenta con **dos versiones diferentes**:

---

## 1️⃣ `agente.py` → Versión básica

Esta versión utiliza reglas simples mediante palabras clave.

Ejemplo:

- suicidio
- autolesión
- ansiedad
- estrés
- depresión

Según las palabras encontradas, clasifica el caso como:

- Alta
- Media
- Baja

### Ventajas

✅ Fácil de desarrollar  
✅ Rápido de ejecutar  
✅ No requiere librerías externas  
✅ Ideal para entender la lógica inicial

### Desventajas

❌ Limitado a palabras exactas  
❌ Puede fallar con frases complejas  
❌ Menor capacidad de interpretación

---

## 2️⃣ `agente_ollama.py` → Versión avanzada con IA local

Esta versión utiliza **Ollama** ejecutando el modelo **Llama 3.2** de forma local para interpretar mejor el contexto del mensaje del paciente.

Ejemplo:

El paciente escribe:

*"No quiero seguir viviendo, estoy cansado de todo."*

Aunque no use la palabra exacta "suicidio", el modelo puede interpretar que se trata de un caso crítico.

---

# ✅ Ventajas de usar Ollama

### 🔒 Mayor privacidad

Los datos se procesan localmente en la computadora o servidor.

No se envían datos sensibles de pacientes a servicios externos.

:contentReference[oaicite:0]{index=0}

---

### 🌐 No necesita internet

Una vez descargado el modelo:

- Puede funcionar offline
- Ideal para hospitales o centros con conectividad limitada

---

### 💰 Costo cero

No requiere pagar APIs externas como:

- :contentReference[oaicite:1]{index=1}  
- :contentReference[oaicite:2]{index=2}  

El modelo funciona localmente sin costos por uso.

---

### 🧠 Mejor comprensión del lenguaje natural

Puede interpretar frases complejas, indirectas o ambiguas mejor que el sistema basado únicamente en palabras clave.

---

# ⚙️ Instalación

Requisitos:

- Python 3.x
- Ollama (solo para versión avanzada)

Verificar Python:

```bash
python --version
```

Instalar Ollama:

:contentReference[oaicite:3]{index=3}

Descargar modelo Llama 3.2:

```bash
ollama pull llama3.2
```

---

# ▶️ Ejecución

## Versión básica

```bash
py agente.py
```

o

```bash
python agente.py
```

---

## Versión avanzada con Ollama

```bash
py agente_ollama.py
```

o

```bash
python agente_ollama.py
```

---

# 💻 Ejemplo de salida

```bash
Motivo de consulta:
"Paciente presenta intento de autolesión"

Resultado:
🔴 PRIORIDAD ALTA
```

```bash
Motivo de consulta:
"Paciente tiene ansiedad por trabajo"

Resultado:
🟡 PRIORIDAD MEDIA
```

```bash
Motivo de consulta:
"Paciente desea iniciar terapia"

Resultado:
🟢 PRIORIDAD BAJA
```

---

# 🛠️ Tecnologías utilizadas

- Python
- Inteligencia Artificial
- Procesamiento de texto
- Reglas condicionales
- Ollama
- :contentReference[oaicite:4]{index=4} Llama 3.2
- Git
- GitHub

---

# 📚 Contexto académico

Proyecto desarrollado para la carrera de **Analista de Sistemas**, aplicando conceptos de:

- Inteligencia Artificial
- Ética en IA
- Automatización
- Sistemas de información
- Desarrollo de software

---

# 👨‍💻 Autor

**Fernando Gallardo**  
Estudiante de Analista de Sistemas