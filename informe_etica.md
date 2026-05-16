# Informe Ético – Agente de Clasificación de Urgencias en Salud Mental

## Introducción

Este proyecto consiste en un agente desarrollado en Python que clasifica consultas de salud mental según su nivel de prioridad:

- Alta
- Media
- Baja

Inicialmente, el sistema funcionaba mediante reglas simples basadas en palabras clave.

Ejemplo:

- suicidio  
- autolesión  
- ansiedad  
- estrés  

Posteriormente el proyecto evolucionó incorporando **Ollama** ejecutando localmente el modelo **Llama 3.2**, permitiendo analizar lenguaje natural de manera más inteligente sin depender de servicios externos.

Esto mejora significativamente tanto la capacidad técnica como los aspectos éticos relacionados con privacidad.

---

# 1. Sesgos

## Riesgo de sesgos

Todo sistema de inteligencia artificial puede presentar sesgos.

En la primera versión basada en palabras clave:

- Solo detectaba términos exactos
- Podía ignorar expresiones indirectas
- Tenía limitaciones lingüísticas

Ejemplo:

"No quiero seguir viviendo"

Si la palabra "suicidio" no aparecía explícitamente, el sistema podía fallar.

---

## Con Ollama

Al incorporar **:contentReference[oaicite:2]{index=2}** y el modelo :contentReference[oaicite:3]{index=3}:

- El agente comprende mejor el contexto
- Detecta frases indirectas
- Interpreta lenguaje natural
- Reduce errores por coincidencia exacta de palabras

Ejemplo:

- "Estoy cansado de vivir"
- "No encuentro sentido a nada"

El modelo puede detectar señales de riesgo aunque no aparezcan palabras exactas.

---

## Mitigación de sesgos

Para reducir riesgos:

- Supervisión humana
- Evaluación constante
- Revisión de resultados
- Pruebas con diferentes perfiles de pacientes
- Mejora continua del sistema

---

# 2. Alucinaciones o errores de clasificación

Los modelos LLM pueden interpretar incorrectamente ciertos mensajes.

Aunque el sistema mejoró con Ollama, todavía existe riesgo de:

- Clasificación errónea
- Falsos positivos
- Falsos negativos

Esto podría afectar la atención médica.

---

## Mitigación

El sistema debe funcionar únicamente como herramienta de apoyo.

La decisión final debe ser tomada por:

- Psicólogos  
- Psiquiatras  
- Médicos  
- Profesionales capacitados  

Nunca debe reemplazar el juicio humano.

---

# 3. Privacidad de datos

La información de salud mental es extremadamente sensible.

Ejemplos:

- Diagnósticos
- Crisis emocionales
- Pensamientos suicidas
- Historial clínico

---

## Uso de Ollama local

Una gran ventaja ética del proyecto es que utiliza **:contentReference[oaicite:4]{index=4}** de manera local.

Esto significa que:

✅ Los datos de pacientes **nunca salen de la computadora o servidor local**  

✅ No se envían datos a APIs externas  

✅ No se comparte información con terceros  

✅ Se reduce el riesgo de filtraciones

---

## Cumplimiento de privacidad

Este enfoque ayuda a cumplir con buenas prácticas y normas de privacidad en sistemas de salud mental porque protege información altamente confidencial.

Además se recomienda:

- Control de acceso
- Cifrado de datos
- Auditorías de seguridad
- Almacenamiento seguro

---

# 4. Costos y acceso equitativo

Muchos sistemas de IA dependen de APIs pagas como:

- :contentReference[oaicite:5]{index=5}  
- :contentReference[oaicite:6]{index=6}  

Esto puede generar costos elevados para hospitales o instituciones pequeñas.

---

## Ventaja ética de Ollama

Con **:contentReference[oaicite:7]{index=7}**:

✅ No hay costo por uso de API  

✅ No existen pagos por cantidad de consultas  

✅ Mayor accesibilidad para instituciones con pocos recursos  

✅ Democratiza el acceso a IA en salud

---

# 5. Responsabilidad

Si ocurre un error:

- Los desarrolladores deben mantener el sistema
- La institución debe supervisar su implementación
- Los profesionales deben validar decisiones críticas

La responsabilidad es compartida.

---

# Conclusión

El proyecto evolucionó desde un sistema simple basado en reglas hacia una solución más avanzada utilizando IA local con **** y el modelo :contentReference[oaicite:9]{index=9}.

Esto mejora:

- Interpretación de lenguaje natural
- Privacidad de datos
- Reducción de costos
- Accesibilidad tecnológica

Sin embargo, sigue siendo una herramienta de apoyo y nunca debe reemplazar la evaluación de profesionales de salud mental.