# Informe Ético y de Impacto Social
## Agente Inteligente de Clasificación de Urgencias (Triage) en Salud Mental

**Materia:** Inteligencia Artificial Aplicada al Desarrollo de Software  
**Estudiante:** Gallardo Fernando Andrés  
**Carrera:** 3° año de Analista de Sistemas  
**Profesora:** Miriam Elena Coronel  
**Instituto:** Instituto Superior Combate de Mbororé  
**Fecha:** Junio de 2026  

---

## 1. Introducción

El presente informe analiza las implicancias éticas, técnicas y legales de la implementación de un sistema de pre-clasificación (triage) automático de consultas en centros de salud mental. El sistema cuenta con dos variantes: una basada en reglas condicionales rígidas (`agente.py`) y otra basada en un modelo de lenguaje de gran tamaño (LLM) procesado localmente mediante Ollama y el modelo Llama 3.2 (`agente_ollama.py`).

En el ámbito de la salud, y particularmente en salud mental, la confidencialidad, la precisión técnica y la equidad son derechos fundamentales protegidos por normativas nacionales e internacionales. A continuación se detallan los riesgos identificados en este proyecto y las estrategias adoptadas para mitigarlos.

---

## 2. Análisis de Sesgos Técnicos y Lingüísticos

### 2.1. Sesgo en el Enfoque por Reglas Rígidas
La primera versión del sistema (`agente.py`) utiliza una estructura clásica de comparación de subcadenas basadas en palabras clave predefinidas. Este enfoque adolece de un grave **sesgo lingüístico y de rigidez**:
- **Falsos Negativos Críticos:** Si un paciente en crisis expresa pensamientos suicidas mediante frases de sentido figurado o indirectas (por ejemplo: *"No encuentro motivos para seguir despierto mañana"* o *"Quiero apagar mi cabeza de una vez"*), el sistema condicional falla y clasifica el caso como prioridad **BAJA** por defecto al no detectar la palabra clave exacta *"suicidio"* o *"pastillas"*.
- **Falsos Positivos Administrativos:** Si un paciente realiza una consulta netamente administrativa que incluye una palabra de riesgo en un contexto no urgente (por ejemplo: *"Quiero consultar el horario de atención para retirar las pastillas de mi abuela"*), el sistema de reglas lo clasifica de forma errónea como prioridad **ALTA** (Guardia) debido a la coincidencia con la palabra clave *"pastillas"*.

### 2.2. Sesgo en el Enfoque Semántico con Ollama (Llama 3.2)
El modelo LLM posee una comprensión semántica del lenguaje natural que le permite discernir el contexto real:
- **Mejora:** Puede identificar intenciones de autolesión indirectas en expresiones coloquiales o modismos propios de la región (jerga argentina como *"estar de bajón"*, *"brote"*, *"angustiado"*).
- **Riesgo:** Los modelos fundacionales están entrenados con datasets globales que pueden contener sesgos de género, clase social, etnia o variaciones dialectales que no representan la realidad local de la provincia de Misiones o el resto de la Argentina. Esto podría llevar al modelo a interpretar de manera dispar consultas formuladas por personas de diferentes orígenes sociolingüísticos.
- **Mitigación:** Se estructuró el **System Prompt** con guías clínicas bien delimitadas y criterios específicos que anclan las decisiones del modelo a hechos observables (ej. pérdida de sueño, autolesión, delirios) en lugar de permitirle deducir de adjetivos abstractos.

---

## 3. Alucinaciones y Estructura de Salida

### 3.1. El Riesgo Clínico de las Alucinaciones
Una "alucinación" en un LLM ocurre cuando el modelo genera información coherente a nivel sintáctico pero falsa o inexistente en la realidad. En un triage de salud mental, una alucinación (como inventar un diagnóstico o minimizar la urgencia de un caso grave justificándolo con lógica falsa) puede poner en riesgo la vida de un paciente.

### 3.2. Estrategias de Mitigación en el Código
Para neutralizar la aleatoriedad del modelo Llama 3.2, se implementaron las siguientes medidas en `agente_ollama.py`:
1. **Temperatura Baja (0.3):** Se redujo la temperatura de generación a `0.3` en los parámetros de la API de Ollama. Esto limita el comportamiento creativo del modelo y lo fuerza a ser determinista y ceñirse estrictamente al prompt clínico.
2. **Restricción de Rol y Contexto:** El prompt del sistema delimita estrictamente el rol del agente como *"enfermero de triage administrativo"* y le prohíbe explícitamente prescribir tratamientos, realizar diagnósticos o emitir consejos médicos.
3. **Formato JSON Estricto y Parser de Respaldo:** Se le exige al modelo retornar únicamente un JSON con dos llaves (`prioridad` y `justificacion`). Para evitar fallas de ejecución ante pequeñas variaciones de formato, el código incluye un **parser robusto con expresiones regulares** capaz de aislar las llaves de salida y reconstruir los datos si el modelo añade texto complementario no deseado.

---

## 4. Privacidad de Datos y Confidencialidad Médica

La información manejada en consultas de psiquiatría y psicología clínica se encuadra dentro de la categoría de **datos sensibles de salud**.

### 4.1. El Peligro de las Nubes Públicas
El uso de APIs propietarias y centralizadas en la nube (como OpenAI ChatGPT o Anthropic Claude) para procesar consultas médicas presenta objeciones éticas severas:
- **Pérdida de Soberanía de Datos:** La información del paciente sale del territorio nacional y es procesada en servidores extranjeros.
- **Uso para Reentrenamiento:** Las nubes comerciales suelen utilizar las interacciones de los usuarios para entrenar futuras versiones de sus modelos, vulnerando el secreto médico.
- **Riesgo de Filtraciones (Data Breaches):** Las bases de datos centralizadas de grandes corporaciones son objetivos constantes de ciberataques.

### 4.2. El Enfoque Local con Ollama
La gran ventaja ética y técnica de esta solución avanzada es el procesamiento en un **servidor local (On-Premise)**:
- Los datos de los pacientes jamás salen de la computadora del centro de salud o el servidor del hospital.
- No se requiere conectividad a internet para clasificar las urgencias, asegurando la continuidad del servicio ante caídas de la red de comunicaciones.
- El hospital retiene el control absoluto sobre sus registros y el ciclo de vida de los datos de salud mental.

---

## 5. Marco Legal Aplicable (Argentina)

El desarrollo e implementación de este agente inteligente se alinea y debe cumplir estrictamente con las siguientes normativas argentinas:

### 5.1. Ley N° 25.326 de Protección de Datos Personales
Esta ley rige el tratamiento de datos personales asentados en archivos o bases de datos de organismos públicos y privados:
- **Art. 2 (Definición de Datos Sensibles):** Los datos sobre salud física o mental son considerados de categoría sensible y gozan de la máxima protección legal.
- **Art. 7 (Prohibición de Tratamiento):** Prohíbe la formación de archivos que almacenen información sensible que revele filiaciones o condiciones de salud de manera indiscriminada. Nuestro agente procesa los datos en memoria en tiempo de triage local y los almacena localmente en el hospital con el consentimiento adecuado, sin compartirlos con terceros externos.

### 5.2. Ley Nacional de Salud Mental N° 26.657
Esta ley tiene por objeto asegurar el derecho a la protección de la salud mental de todas las personas:
- **Art. 7:** Reconoce el derecho del paciente a recibir una atención basada en fundamentos científicos ajustados a principios éticos, a la confidencialidad de la información y al resguardo de su identidad.
- **Supervisión Obligatoria:** Dado que la ley promueve el abordaje interdisciplinario e humanizado, **el agente jamás toma decisiones de internación o tratamiento de forma autónoma**. Actúa únicamente como un asistente organizativo administrativo, derivando siempre al paciente a profesionales humanos calificados para su diagnóstico.

---

## 6. Equidad y Acceso a la Salud

En países en desarrollo y particularmente en áreas de bajos recursos, la dependencia de APIs pagas limita la adopción de tecnologías avanzadas en hospitales públicos:
- **Costos de Escala:** Pagar por cantidad de tokens procesados con APIs comerciales puede ser insostenible para un centro de salud comunitario.
- **Democratización de la Tecnología:** Al utilizar modelos locales y de código abierto (Llama 3.2), se democratiza el acceso a la inteligencia artificial, eliminando la barrera económica para brindar un servicio de triage más eficiente y rápido en el sector público de salud.

---

## 7. Conclusión: El Rol del Ser Humano (Human-in-the-Loop)

El principio rector fundamental de este desarrollo es que **la inteligencia artificial no sustituye al profesional de la salud mental**. 

El agente clasificador funciona como un **copiloto organizativo**. Su único fin es agilizar la cola de espera inicial de una mesa de entradas, alertando al personal administrativo y de guardia sobre la presencia de expresiones de riesgo de forma inmediata. La validación final de la urgencia, el diagnóstico clínico y el abordaje terapéutico siguen siendo responsabilidad exclusiva y reservada del equipo médico humano.
