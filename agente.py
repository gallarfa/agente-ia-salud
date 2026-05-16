"""
Agente IA - Clasificador de Urgencias en Salud Mental
Materia: Inteligencia Artificial Aplicada al Desarrollo de Software
"""

import json
import csv
from datetime import datetime

print("="*50)
print("🤖 AGENTE IA - HOSPITAL DE SALUD MENTAL")
print("="*50)

# Lista de pacientes de ejemplo (después vas a poder cambiar esto)
pacientes = [
    {"nombre": "Paciente A", "consulta": "Hace una semana que no duermo, estoy muy nervioso"},
    {"nombre": "Paciente B", "consulta": "Necesito cambiar mi turno del martes"},
    {"nombre": "Paciente C", "consulta": "Anoche tomé 20 pastillas, no sé qué hacer"},
    {"nombre": "Paciente D", "consulta": "Escucho voces que me dicen que me lastime"},
    {"nombre": "Paciente E", "consulta": "Quería pedir la receta de mi medicación"},
]

def clasificar_urgencia(consulta):
    """
    Esta función es el CEREBRO de nuestro agente.
    Analiza el texto y decide qué prioridad tiene.
    """
    consulta = consulta.lower()  # Convertimos todo a minúsculas para comparar
    
    # Palabras que indican URGENCIA ALTA (riesgo de vida)
    palabras_alta = ["pastillas", "voces", "suicidio", "muerte", "sangre", "lastime"]
    for palabra in palabras_alta:
        if palabra in consulta:
            return {
                "prioridad": "ALTA",
                "derivacion": "Guardia",
                "tiempo": "inmediato",
                "color": "🔴"
            }
    
    # Palabras que indican URGENCIA MEDIA (requiere atención pronto)
    palabras_media = ["nervioso", "duermo", "ansiedad", "pánico", "llorar", "angustia"]
    for palabra in palabras_media:
        if palabra in consulta:
            return {
                "prioridad": "MEDIA",
                "derivacion": "Ambulatorio",
                "tiempo": "24hs",
                "color": "🟡"
            }
    
    # Si no encontró nada grave, es prioridad BAJA
    return {
        "prioridad": "BAJA",
        "derivacion": "Consultorio",
        "tiempo": "72hs",
        "color": "🟢"
    }

print("\n📋 Procesando pacientes...")
print("-" * 50)

resultados = []

for paciente in pacientes:
    nombre = paciente["nombre"]
    consulta = paciente["consulta"]
    
    # El AGENTE clasifica automáticamente (esto es la IA)
    clasificacion = clasificar_urgencia(consulta)
    
    # Guardar resultado
    resultados.append({
        "nombre": nombre,
        "consulta": consulta,
        "prioridad": clasificacion["prioridad"],
        "derivacion": clasificacion["derivacion"],
        "tiempo": clasificacion["tiempo"]
    })
    
    # Mostrar en pantalla
    print(f"\n{clasificacion['color']} {nombre}")
    print(f"   Consulta: {consulta}")
    print(f"   → {clasificacion['prioridad']} - {clasificacion['derivacion']} ({clasificacion['tiempo']})")

# Mostrar resumen final
print("\n" + "="*50)
print("📊 RESUMEN DEL AGENTE")
print("="*50)

altas = sum(1 for r in resultados if r["prioridad"] == "ALTA")
medias = sum(1 for r in resultados if r["prioridad"] == "MEDIA")
bajas = sum(1 for r in resultados if r["prioridad"] == "BAJA")

print(f"🔴 Urgencia ALTA: {altas} pacientes (atención inmediata)")
print(f"🟡 Urgencia MEDIA: {medias} pacientes")
print(f"🟢 Urgencia BAJA: {bajas} pacientes")
print(f"\n📊 Total pacientes analizados: {len(resultados)}")

# Guardar resultados en un archivo CSV (para después mostrarlo en la defensa)
with open("resultados.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["Paciente", "Consulta", "Prioridad", "Derivacion", "Tiempo"])
    for r in resultados:
        escritor.writerow([r["nombre"], r["consulta"], r["prioridad"], r["derivacion"], r["tiempo"]])

print("\n📁 Resultados guardados en 'resultados.csv'")
print("\n✅ AGENTE IA EJECUTADO CORRECTAMENTE")