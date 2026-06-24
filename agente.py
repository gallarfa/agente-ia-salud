"""
Agente IA por Reglas - Clasificador de Urgencias en Salud Mental
Materia: Inteligencia Artificial Aplicada al Desarrollo de Software
Instituto: Instituto Superior Combate de Mbororé
Estudiante: Gallardo Fernando Andrés
Fecha: Junio 2026
"""

import json
import csv
import os
from datetime import datetime

# Definición de palabras clave expandida (incluye localismos de Argentina y sinónimos)
PALABRAS_ALTA = [
    "suicidio", "suicidar", "matar", "matarme", "morirme", "muerte", "pastillas", 
    "intoxicado", "sobredosis", "cortarme", "cortar", "lastimarme", "lastimar", 
    "voces", "escucho voces", "delirio", "alucinación", "alucinaciones", "brote", 
    "psicótico", "brote psicotico", "emergencia", "guardia", "colapsar", "ahorcar", 
    "no quiero vivir", "terminar con todo", "acabar con mi vida"
]

PALABRAS_MEDIA = [
    "nervioso", "nerviosa", "duermo", "dormir", "insomnio", "ansiedad", "pánico", 
    "panico", "llorar", "angustia", "angustiado", "angustiada", "depresión", 
    "depresion", "depre", "bajón", "bajon", "triste", "estrés", "estres", "crisis", 
    "fobia", "obsesión", "obsesion", "ritmo cardiaco", "palpitaciones", "asustado",
    "asustada", "ansioso", "ansiosa", "adicción", "consumo", "droga", "alcohol"
]

PACIENTES_EJEMPLO = [
    {"nombre": "Paciente A", "consulta": "Hace una semana que no duermo, estoy muy nervioso"},
    {"nombre": "Paciente B", "consulta": "Necesito cambiar mi turno del martes"},
    {"nombre": "Paciente C", "consulta": "Anoche tomé 20 pastillas, no sé qué hacer"},
    {"nombre": "Paciente D", "consulta": "Escucho voces que me dicen que me lastime"},
    {"nombre": "Paciente E", "consulta": "Quería pedir la receta de mi medicación"},
    {"nombre": "Paciente F", "consulta": "Me siento muy triste, con mucho bajón y lloro todo el tiempo"},
    {"nombre": "Paciente G", "consulta": "No le encuentro sentido a la vida, no quiero seguir viviendo"}
]

def clasificar_urgencia_reglas(consulta):
    """
    Analiza el texto de la consulta buscando palabras clave y devuelve la clasificación.
    """
    consulta_clean = consulta.lower()
    
    # Evaluar prioridad ALTA primero (riesgo de vida)
    for palabra in PALABRAS_ALTA:
        if palabra in consulta_clean:
            return {
                "prioridad": "ALTA",
                "derivacion": "Guardia de Emergencias Médicas",
                "tiempo": "Inmediato (atención de urgencia 24hs)",
                "color": "🔴",
                "criterio": f"Palabra clave de riesgo detectada: '{palabra}'"
            }
            
    # Evaluar prioridad MEDIA
    for palabra in PALABRAS_MEDIA:
        if palabra in consulta_clean:
            return {
                "prioridad": "MEDIA",
                "derivacion": "Consultorio de Terapia Ambulatoria / Psiquiatría",
                "tiempo": "Dentro de las 24 horas",
                "color": "🟡",
                "criterio": f"Palabra clave de sintomatología detectada: '{palabra}'"
            }
            
    # Por defecto es prioridad BAJA (trámites, turnos, consultas generales)
    return {
        "prioridad": "BAJA",
        "derivacion": "Consultorio Externo de Salud Mental / Área Administrativa",
        "tiempo": "Dentro de las 72 horas",
        "color": "🟢",
        "criterio": "No se detectaron palabras clave de riesgo o síntomas de alarma. Derivación de rutina."
    }

def ejecutar_lote(pacientes_lista=PACIENTES_EJEMPLO):
    print("\n" + "="*70)
    print("📋 PROCESANDO LOTE DE PACIENTES REGISTRADOS")
    print("="*70)
    
    resultados = []
    for paciente in pacientes_lista:
        nombre = paciente["nombre"]
        consulta = paciente["consulta"]
        clasificacion = clasificar_urgencia_reglas(consulta)
        
        resultados.append({
            "nombre": nombre,
            "consulta": consulta,
            "prioridad": clasificacion["prioridad"],
            "derivacion": clasificacion["derivacion"],
            "tiempo": clasificacion["tiempo"],
            "criterio": clasificacion["criterio"]
        })
        
        print(f"\n{clasificacion['color']} {nombre}")
        print(f"   Consulta: \"{consulta}\"")
        print(f"   → Clasificación: {clasificacion['prioridad']}")
        print(f"   → Derivación: {clasificacion['derivacion']} (Plazo: {clasificacion['tiempo']})")
        print(f"   → Justificación Técnica: {clasificacion['criterio']}")
        print("-" * 50)
        
    guardar_resultados_csv(resultados)
    mostrar_resumen(resultados)
    return resultados

def guardar_resultados_csv(resultados, filename="resultados.csv"):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Paciente", "Consulta", "Prioridad", "Derivacion", "Tiempo", "Criterio_Clasificacion"])
            for r in resultados:
                escritor.writerow([r["nombre"], r["consulta"], r["prioridad"], r["derivacion"], r["tiempo"], r["criterio"]])
        print(f"\n💾 Resultados guardados correctamente en '{filename}'")
    except Exception as e:
        print(f"\n❌ Error al guardar en CSV: {e}")

def mostrar_resumen(resultados):
    altas = sum(1 for r in resultados if r["prioridad"] == "ALTA")
    medias = sum(1 for r in resultados if r["prioridad"] == "MEDIA")
    bajas = sum(1 for r in resultados if r["prioridad"] == "BAJA")
    
    print("\n" + "="*70)
    print("📊 RESUMEN ESTADÍSTICO - CLASIFICACIÓN POR REGLAS")
    print("="*70)
    print(f"🔴 Urgencias ALTAS (Inmediato):  {altas}")
    print(f"🟡 Urgencias MEDIAS (24 horas):  {medias}")
    print(f"🟢 Urgencias BAJAS (72 horas):   {bajas}")
    print(f"📊 Total de casos analizados:     {len(resultados)}")
    print("="*70)

def main():
    print("="*70)
    print("🤖 SISTEMA DE CLASIFICACIÓN DE TRIAGE POR REGLAS (SALUD MENTAL)")
    print("Materia: Inteligencia Artificial Aplicada al Desarrollo de Software")
    print("Estudiante: Gallardo Fernando Andrés - Instituto Combate de Mbororé")
    print("="*70)
    
    while True:
        print("\nSeleccione una opción de ejecución:")
        print("1. Ejecutar lote de pacientes predefinidos (Checklist de examen)")
        print("2. Evaluar una consulta personalizada por teclado")
        print("3. Salir")
        
        opcion = input("Opción (1-3): ").strip()
        
        if opcion == "1":
            ejecutar_lote()
        elif opcion == "2":
            print("\n--- EVALUAR CONSULTA PERSONALIZADA ---")
            nombre = input("Ingrese el nombre/ID del paciente ficticio: ").strip()
            if not nombre:
                nombre = "Paciente Anónimo"
            consulta = input("Describa el motivo de la consulta/crisis: ").strip()
            if not consulta:
                print("Consulta vacía. Operación cancelada.")
                continue
                
            clasificacion = clasificar_urgencia_reglas(consulta)
            print(f"\n{clasificacion['color']} RESULTADO DEL TRIAGE (REGLAS):")
            print(f"   Paciente: {nombre}")
            print(f"   Consulta: \"{consulta}\"")
            print(f"   → Prioridad: {clasificacion['prioridad']}")
            print(f"   → Derivación Recomendada: {clasificacion['derivacion']}")
            print(f"   → Plazo Máximo: {clasificacion['tiempo']}")
            print(f"   → Criterio Aplicado: {clasificacion['criterio']}")
            
            # Guardar opcionalmente
            guardar = input("\n¿Desea agregar este caso al archivo resultados.csv? (s/n): ").strip().lower()
            if guardar == 's':
                # Cargar existentes
                resultados_existentes = []
                if os.path.exists("resultados.csv"):
                    try:
                        with open("resultados.csv", "r", encoding="utf-8") as f:
                            reader = csv.reader(f)
                            header = next(reader)
                            for row in reader:
                                if len(row) >= 6:
                                    resultados_existentes.append({
                                        "nombre": row[0],
                                        "consulta": row[1],
                                        "prioridad": row[2],
                                        "derivacion": row[3],
                                        "tiempo": row[4],
                                        "criterio": row[5]
                                    })
                    except Exception:
                        pass
                
                resultados_existentes.append({
                    "nombre": nombre,
                    "consulta": consulta,
                    "prioridad": clasificacion["prioridad"],
                    "derivacion": clasificacion["derivacion"],
                    "tiempo": clasificacion["tiempo"],
                    "criterio": clasificacion["criterio"]
                })
                guardar_resultados_csv(resultados_existentes)
                
        elif opcion == "3":
            print("\nSaliendo del sistema de reglas. ¡Hasta luego!")
            break
        else:
            print("\n⚠️ Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
