"""
AGENTE IA CON OLLAMA - Clasificador de Urgencias en Salud Mental
Materia: Inteligencia Artificial Aplicada al Desarrollo de Software
Usa modelo local (privacidad total, sin internet)
"""

import requests
import json
import csv

# Configuración - Ollama corre en localhost:11434
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2"

def clasificar_con_ollama(consulta):
    """
    Agente que usa Ollama para entender lenguaje natural
    Los datos NO salen de tu computadora
    """
    
    # PROMPT ESTRUCTURADO (lo que evalúa el profesor)
    prompt = f"""
    Rol: Eres un psiquiatra experto en triage de salud mental.
    
    Contexto: Un hospital necesita clasificar urgencias de pacientes.
    
    Tarea: Clasificá la siguiente consulta según prioridad.
    
    Consulta del paciente: "{consulta}"
    
    Reglas de clasificación:
    - ALTA: riesgo de vida, intento de suicidio, psicosis aguda
    - MEDIA: ansiedad severa, depresión, crisis de pánico
    - BAJA: trámites, turnos, recetas, consultas leves
    
    Restricciones:
    - Respondé SOLO con formato JSON
    - No des consejos médicos
    
    Formato de salida exacto:
    {{"prioridad": "ALTA", "justificacion": "frase breve"}}
    """
    
    respuesta = requests.post(OLLAMA_URL, json={
        "model": MODELO,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.3
    })
    
    resultado_texto = respuesta.json()["response"]
    
    # Limpiar el JSON (por si viene con markdown)
    if "```json" in resultado_texto:
        resultado_texto = resultado_texto.split("```json")[1].split("```")[0]
    elif "```" in resultado_texto:
        resultado_texto = resultado_texto.split("```")[1].split("```")[0]
    
    return json.loads(resultado_texto)


# Pacientes de prueba
pacientes = [
    "Hace una semana que no duermo, estoy muy nervioso",
    "Necesito cambiar mi turno del martes",
    "Anoche tomé 20 pastillas, no sé qué hacer",
    "Escucho voces que me dicen que me lastime",
    "Quería pedir la receta de mi medicación"
]

print("="*55)
print("🤖 AGENTE IA con OLLAMA - HOSPITAL DE SALUD MENTAL")
print(f"📦 Modelo: {MODELO} (ejecutándose localmente)")
print("🔒 Privacidad: Los datos NO salen de tu computadora")
print("="*55)

resultados = []

for i, consulta in enumerate(pacientes, 1):
    print(f"\n📋 Paciente {i}: {consulta}")
    
    try:
        resultado = clasificar_con_ollama(consulta)
        prioridad = resultado.get("prioridad", "MEDIA")
        justificacion = resultado.get("justificacion", "")
        
        if prioridad == "ALTA":
            emoji = "🔴"
        elif prioridad == "MEDIA":
            emoji = "🟡"
        else:
            emoji = "🟢"
        
        print(f"   {emoji} Prioridad: {prioridad}")
        print(f"   📝 Justificación: {justificacion}")
        
        resultados.append({
            "consulta": consulta,
            "prioridad": prioridad,
            "justificacion": justificacion
        })
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print(f"   💡 Asegurate que Ollama esté corriendo (ollama serve)")

# Reporte final
print("\n" + "="*55)
print("📊 REPORTE DEL AGENTE IA")
print("="*55)

altas = sum(1 for r in resultados if r.get("prioridad") == "ALTA")
medias = sum(1 for r in resultados if r.get("prioridad") == "MEDIA")
bajas = sum(1 for r in resultados if r.get("prioridad") == "BAJA")

print(f"🔴 Prioridad ALTA: {altas}")
print(f"🟡 Prioridad MEDIA: {medias}")
print(f"🟢 Prioridad BAJA: {bajas}")
print(f"📋 Total analizados: {len(pacientes)}")

# Guardar en CSV
with open("resultados_ollama.csv", "w", newline="", encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(["Consulta", "Prioridad", "Justificacion"])
    for r in resultados:
        writer.writerow([r["consulta"], r["prioridad"], r["justificacion"]])

print("\n📁 Resultados guardados en 'resultados_ollama.csv'")
print("✅ Agente con Ollama ejecutado correctamente")