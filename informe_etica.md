# Informe Ético – Agente de Clasificación de Urgencias en Salud Mental

## Introducción

Este proyecto consiste en un agente desarrollado en Python que clasifica consultas de salud mental según su nivel de prioridad:

- Alta
- Media
- Baja

Actualmente, el sistema funciona mediante reglas simples basadas en palabras clave detectadas dentro del motivo de consulta ingresado por el usuario.

Ejemplo:

- "suicidio"
- "autolesión"
- "ansiedad"
- "estrés"

En futuras versiones se planea integrar modelos de inteligencia artificial local mediante **Ollama**, lo que aumentará la capacidad de análisis del agente.

Debido a que trabaja con información sensible relacionada con la salud mental, es importante analizar los aspectos éticos del sistema.

---

# 1. Sesgos

## Riesgo de sesgos

El agente actual puede presentar sesgos porque utiliza palabras clave predefinidas por los desarrolladores.

Por ejemplo:

- Puede detectar correctamente la palabra "suicidio"
- Pero podría no detectar expresiones similares como:
  - "no quiero seguir viviendo"
  - "quiero desaparecer"
  - "no tengo razones para vivir"

Esto puede generar errores de clasificación debido a limitaciones en el vocabulario utilizado.

También pueden existir sesgos culturales o lingüísticos:

- Diferentes regiones utilizan distintas expresiones
- Algunos pacientes pueden describir su situación de manera indirecta

---

## Cómo mitigamos los sesgos

Para reducir estos problemas se propone:

- Ampliar constantemente la base de palabras clave
- Validar el sistema con profesionales de salud mental
- Realizar pruebas con distintos tipos de lenguaje
- Evitar depender únicamente de una sola palabra
- Incorporar supervisión humana

Cuando se implemente Ollama:

- Entrenar/promptear cuidadosamente al modelo
- Revisar resultados periódicamente
- Detectar posibles patrones discriminatorios

---

# 2. Alucinaciones o errores de clasificación

## Situación actual

El sistema actual no utiliza IA generativa, por lo tanto no produce alucinaciones tradicionales como inventar información.

Sin embargo, sí puede cometer errores de clasificación:

Ejemplo:

Un paciente escribe:

"Estoy cansado de vivir"

Si esa frase no coincide con palabras clave críticas, el sistema podría clasificar incorrectamente como prioridad media o baja.

---

## Riesgos

Una clasificación incorrecta puede provocar:

- Retraso en atención urgente
- Riesgo para el paciente
- Mala asignación de recursos
- Decisiones equivocadas

---

## Solución propuesta

El agente debe funcionar únicamente como herramienta de apoyo.

La decisión final debe ser tomada por:

- Psicólogos
- Psiquiatras
- Médicos
- Personal capacitado

En futuras versiones con Ollama:

- Implementar revisión humana obligatoria
- Registrar decisiones del sistema
- Permitir auditorías

---

# 3. Privacidad de datos

La información de pacientes de salud mental es altamente sensible.

Ejemplos:

- Diagnósticos
- Síntomas
- Historial emocional
- Riesgos de autolesión

---

## Medidas de protección

Para proteger los datos se recomienda:

- No almacenar datos innecesarios
- Encriptar bases de datos
- Restringir accesos
- Utilizar autenticación segura
- Anonymizar información cuando sea posible
- Cumplir normativas de protección de datos

Si se utiliza Ollama local:

Esto mejora la privacidad porque los datos pueden procesarse en servidores locales sin enviarlos a servicios externos.

---

# 4. Responsabilidad

El agente no debe reemplazar a profesionales de salud.

Es una herramienta de apoyo para clasificación inicial.

Si ocurre un error:

- La institución debe supervisar su implementación
- Los desarrolladores deben mantener el sistema
- Los profesionales deben validar decisiones críticas

---

## Responsabilidad compartida

### Desarrolladores
Responsables de diseñar correctamente el sistema y minimizar errores.

### Institución médica
Responsable de implementar protocolos adecuados.

### Profesionales de salud
Responsables de la decisión final sobre el paciente.

---

# Conclusión

La inteligencia artificial puede ayudar a mejorar procesos en salud mental, pero debe utilizarse de manera responsable.

Este proyecto demuestra una aplicación inicial sencilla mediante reglas en Python, pero reconoce que cualquier evolución hacia modelos más avanzados como Ollama requerirá mayores controles éticos, técnicos y humanos.

La tecnología debe complementar al profesional, nunca reemplazarlo.