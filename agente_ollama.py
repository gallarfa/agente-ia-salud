"""
Agente Inteligente con IA Local (Ollama) - Triage de Salud Mental
Materia: Inteligencia Artificial Aplicada al Desarrollo de Software
Instituto: Instituto Superior Combate de Mbororé
Estudiante: Gallardo Fernando Andrés
Fecha: Junio 2026
"""

import requests
import json
import csv
import os
import re
from datetime import datetime

# Configuración del servidor local de Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO_OLLAMA = "llama3.2"

PACIENTES_EJEMPLO = [
    {"nombre": "Paciente A", "consulta": "Hace una semana que no duermo, estoy muy nervioso"},
    {"nombre": "Paciente B", "consulta": "Necesito cambiar mi turno del martes"},
    {"nombre": "Paciente C", "consulta": "Anoche tomé 20 pastillas, no sé qué hacer"},
    {"nombre": "Paciente D", "consulta": "Escucho voces que me dicen que me lastime"},
    {"nombre": "Paciente E", "consulta": "Quería pedir la receta de mi medicación"},
    {"nombre": "Paciente F", "consulta": "Me siento muy triste, con mucho bajón y lloro todo el tiempo"},
    {"nombre": "Paciente G", "consulta": "No le encuentro sentido a la vida, no quiero seguir viviendo"}
]

def limpiar_y_cargar_json(texto_respuesta):
    """
    Intenta limpiar y parsear la respuesta del modelo de lenguaje.
    Maneja bloques de código markdown ```json ... ``` y repara errores comunes.
    """
    texto_limpio = texto_respuesta.strip()
    
    # 1. Quitar bloques de formato markdown ```json y ```
    if "```json" in texto_limpio:
        texto_limpio = texto_limpio.split("```json")[1].split("```")[0].strip()
    elif "```" in texto_limpio:
        texto_limpio = texto_limpio.split("```")[1].split("```")[0].strip()
        
    # 2. Extraer solo el contenido dentro de las llaves {} mediante expresiones regulares si hay texto alrededor
    match = re.search(r"\{.*\}", texto_limpio, re.DOTALL)
    if match:
        texto_limpio = match.group(0)
        
    # 3. Intentar parsear el JSON
    try:
        data = json.loads(texto_limpio)
        # Validar campos requeridos
        if "prioridad" not in data or "justificacion" not in data:
            raise KeyError("Faltan campos obligatorios en el JSON retornado.")
        return data
    except Exception as e:
        # Intento de reparación manual básico si falló
        print(f"   ⚠️ Error de parseo JSON. Intentando reparar respuesta cruda...")
        
        # Buscar prioridad estimada mediante texto
        prioridad_reparada = "MEDIA"
        if "ALTA" in texto_respuesta.upper() or "🔴" in texto_respuesta:
            prioridad_reparada = "ALTA"
        elif "BAJA" in texto_respuesta.upper() or "🟢" in texto_respuesta:
            prioridad_reparada = "BAJA"
            
        # Extraer justificación aproximada
        justificacion_reparada = "Reparación automática: Error en estructura JSON de Ollama."
        match_just = re.search(r'"justificacion"\s*:\s*"([^"]+)"', texto_respuesta)
        if match_just:
            justificacion_reparada = match_just.group(1)
        else:
            # Buscar una frase descriptiva simple
            frases = [line.strip() for line in texto_respuesta.split("\n") if len(line.strip()) > 10 and not line.startswith("{") and not line.startswith("}")]
            if frases:
                justificacion_reparada = frases[0]
                
        return {
            "prioridad": prioridad_reparada,
            "justificacion": justificacion_reparada,
            "reparado": True
        }

def clasificar_con_ollama(consulta):
    """
    Envía la consulta del paciente al modelo Llama 3.2 local usando un prompt estructurado
    con guías clínicas de salud mental adaptadas del Sistema Manchester.
    """
    
    # Prompt de Sistema estructurado y restrictivo
    prompt_sistema = f"""
    Rol: Eres un psiquiatra y enfermero de salud mental senior experto en triage clínico (Manchester Triage System).
    
    Contexto: Trabajas en la mesa de entrada de emergencias de un Hospital Psiquiátrico. Tu labor es analizar de forma objetiva y empática la consulta del paciente y determinar la prioridad de derivación.
    
    Consulta a clasificar: "{consulta}"
    
    Reglas de clasificación (Manchester Adaptado):
    1. PRIORIDAD: "ALTA" (Riesgo de vida o integridad de terceros)
       - Criterios: Intento de suicidio reciente, ideación suicida activa, autolesión en curso o reciente, alucinaciones auditivas/visuales imperativas (escuchar voces que ordenan daño), agresividad física descontrolada, psicosis aguda o delirio severo.
       - Derivación: Guardia Médica / Psiquiátrica. Plazo: Inmediato.
       
    2. PRIORIDAD: "MEDIA" (Trastorno clínico agudo sin riesgo vital inmediato)
       - Criterios: Crisis de pánico en curso, ansiedad generalizada severa, insomnio de varios días con labilidad emocional, depresión severa sin planes de suicidio, llanto desconsolado recurrente, angustia invalidante, recaída en consumos problemáticos (adicciones) sin sobredosis.
       - Derivación: Consultorio de Urgencia Ambulatoria. Plazo: Dentro de las 24 horas.
       
    3. PRIORIDAD: "BAJA" (Consultas administrativas y sintomatología leve o crónica)
       - Criterios: Solicitud de renovación de recetas, cambio o pedido de turnos médicos programados, consultas sobre horarios de atención, trámites de certificados, controles crónicos estables.
       - Derivación: Administración / Consultorio Externo Programado. Plazo: Dentro de las 72 horas.

    Restricciones de seguridad y formato:
    - Tu respuesta debe ser EXCLUSIVAMENTE un objeto JSON válido. No incluyas explicaciones de bienvenida ni introducciones.
    - No brindes consejos médicos, diagnósticos terapéuticos ni tratamientos farmacéuticos en la justificación.
    - La justificación técnica debe ser una sola frase corta y objetiva centrada en los síntomas detectados.
    
    Formato de salida obligatorio:
    {{
        "prioridad": "ALTA" | "MEDIA" | "BAJA",
        "justificacion": "Explicación breve y técnica del porqué de la decisión"
    }}
    """
    
    try:
        respuesta = requests.post(OLLAMA_URL, json={
            "model": MODELO_OLLAMA,
            "prompt": prompt_sistema,
            "stream": False,
            "options": {
                "temperature": 0.3  # Baja temperatura para mitigar alucinaciones y forzar JSON
            }
        }, timeout=15)
        
        if respuesta.status_code == 200:
            resultado_texto = respuesta.json().get("response", "")
            return limpiar_y_cargar_json(resultado_texto)
        else:
            raise requests.exceptions.HTTPError(f"Código de estado de Ollama: {respuesta.status_code}")
            
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "No se pudo establecer conexión con Ollama. "
            "Asegúrate de ejecutar la aplicación de Ollama localmente "
            "o correr el comando 'ollama serve' en la terminal."
        )

def generar_reporte_html(resultados, filename="reporte_triage.html"):
    """
    Genera un panel web interactivo para visualizar los resultados clasificados por la IA.
    """
    ahora = datetime.now().strftime("%d/%m/%Y a las %H:%M")
    
    altas = sum(1 for r in resultados if r["prioridad"] == "ALTA")
    medias = sum(1 for r in resultados if r["prioridad"] == "MEDIA")
    bajas = sum(1 for r in resultados if r["prioridad"] == "BAJA")
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Triage Inteligente - Ollama</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --color-alta: #ef4444;
            --color-media: #f59e0b;
            --color-baja: #10b981;
            --accent: #6366f1;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 2px solid #334155;
            padding-bottom: 20px;
        }}
        h1 {{
            margin: 0;
            color: var(--text-main);
            font-size: 2.2em;
            letter-spacing: -0.5px;
        }}
        .meta {{
            color: var(--text-muted);
            margin-top: 10px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border-top: 4px solid var(--accent);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .stat-card.alta {{ border-top-color: var(--color-alta); }}
        .stat-card.media {{ border-top-color: var(--color-media); }}
        .stat-card.baja {{ border-top-color: var(--color-baja); }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0 5px 0;
        }}
        .stat-label {{
            color: var(--text-muted);
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 1px;
        }}
        .triage-table {{
            width: 100%;
            border-collapse: collapse;
            background-color: var(--card-bg);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .triage-table th {{
            background-color: #334155;
            text-align: left;
            padding: 16px;
            font-weight: 600;
        }}
        .triage-table td {{
            padding: 16px;
            border-bottom: 1px solid #334155;
        }}
        .triage-table tr:last-child td {{
            border-bottom: none;
        }}
        .badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 50px;
            font-size: 0.85em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .badge.alta {{
            background-color: rgba(239, 68, 68, 0.15);
            color: var(--color-alta);
            border: 1px solid var(--color-alta);
        }}
        .badge.media {{
            background-color: rgba(245, 158, 11, 0.15);
            color: var(--color-media);
            border: 1px solid var(--color-media);
        }}
        .badge.baja {{
            background-color: rgba(16, 185, 129, 0.15);
            color: var(--color-baja);
            border: 1px solid var(--color-baja);
        }}
        .paciente-nombre {{
            font-weight: bold;
        }}
        .consulta-texto {{
            font-style: italic;
            color: var(--text-muted);
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            color: var(--text-muted);
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🧠 Panel de Control - Triage IA Local</h1>
            <p class="meta">Reporte de Auditoría Generado el {ahora} | Modelo: {MODELO_OLLAMA}</p>
        </header>
        
        <div class="stats">
            <div class="stat-card alta">
                <div class="stat-value">{altas}</div>
                <div class="stat-label">Urgencia Alta 🔴</div>
            </div>
            <div class="stat-card media">
                <div class="stat-value">{medias}</div>
                <div class="stat-label">Prioridad Media 🟡</div>
            </div>
            <div class="stat-card baja">
                <div class="stat-value">{bajas}</div>
                <div class="stat-label">Prioridad Baja 🟢</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(resultados)}</div>
                <div class="stat-label">Total Pacientes</div>
            </div>
        </div>
        
        <table class="triage-table">
            <thead>
                <tr>
                    <th style="width: 15%">Paciente</th>
                    <th style="width: 35%">Consulta</th>
                    <th style="width: 15%">Prioridad</th>
                    <th style="width: 35%">Justificación Clínica (IA)</th>
                </tr>
            </thead>
            <tbody>
"""
    for r in resultados:
        badge_class = r['prioridad'].lower()
        html += f"""
                <tr>
                    <td><span class="paciente-nombre">{r['nombre']}</span></td>
                    <td><span class="consulta-texto">"{r['consulta']}"</span></td>
                    <td><span class="badge {badge_class}">{r['prioridad']}</span></td>
                    <td>{r['justificacion']}</td>
                </tr>
"""
    html += """
            </tbody>
        </table>
        
        <div class="footer">
            <p>Trabajo Final - Inteligencia Artificial Aplicada al Desarrollo de Software</p>
            <p><strong>Estudiante:</strong> Gallardo Fernando Andrés | Instituto Superior Combate de Mbororé</p>
        </div>
    </div>
</body>
</html>
"""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)
        print(f"📊 Reporte gráfico interactivo generado en '{filename}'")
    except Exception as e:
        print(f"⚠️ No se pudo generar el HTML: {e}")

def guardar_resultados_csv(resultados, filename="resultados_ollama.csv"):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Paciente", "Consulta", "Prioridad", "Justificacion"])
            for r in resultados:
                escritor.writerow([r["nombre"], r["consulta"], r["prioridad"], r["justificacion"]])
        print(f"💾 Resultados guardados correctamente en '{filename}'")
    except Exception as e:
        print(f"❌ Error al guardar en CSV: {e}")

def ejecutar_lote_ollama(pacientes_lista=PACIENTES_EJEMPLO):
    print("\n" + "="*70)
    print(f"🧠 PROCESANDO CON IA LOCAL ({MODELO_OLLAMA.upper()})")
    print("="*70)
    print("Conectando con el servidor local de Ollama... (Espere unos segundos)")
    
    resultados = []
    
    for i, paciente in enumerate(pacientes_lista, 1):
        nombre = paciente["nombre"]
        consulta = paciente["consulta"]
        
        print(f"\n📋 [{i}/{len(pacientes_lista)}] Paciente: {nombre}")
        print(f"   Consulta: \"{consulta}\"")
        
        try:
            clasificacion = clasificar_con_ollama(consulta)
            prioridad = clasificacion["prioridad"]
            justificacion = clasificacion["justificacion"]
            
            if prioridad == "ALTA":
                emoji = "🔴"
            elif prioridad == "MEDIA":
                emoji = "🟡"
            else:
                emoji = "🟢"
                
            print(f"   → Clasificación: {emoji} {prioridad}")
            print(f"   → Justificación: {justificacion}")
            
            resultados.append({
                "nombre": nombre,
                "consulta": consulta,
                "prioridad": prioridad,
                "justificacion": justificacion
            })
        except Exception as e:
            print(f"   ❌ Error procesando este caso: {e}")
            
    if resultados:
        guardar_resultados_csv(resultados)
        generar_reporte_html(resultados)
        
        # Resumen rápido por consola
        altas = sum(1 for r in resultados if r["prioridad"] == "ALTA")
        medias = sum(1 for r in resultados if r["prioridad"] == "MEDIA")
        bajas = sum(1 for r in resultados if r["prioridad"] == "BAJA")
        
        print("\n" + "="*70)
        print("📊 RESUMEN ESTADÍSTICO - CLASIFICACIÓN IA (OLLAMA)")
        print("="*70)
        print(f"🔴 Urgencia ALTA (Inmediato):  {altas}")
        print(f"🟡 Prioridad MEDIA (24hs):     {medias}")
        print(f"🟢 Prioridad BAJA (72hs):      {bajas}")
        print(f"📊 Total analizados con éxito:  {len(resultados)}")
        print("="*70)
    else:
        print("\n⚠️ No se pudieron generar resultados. Verifique la conexión a Ollama.")

def main():
    print("="*75)
    print("🤖 SISTEMA DE CLASIFICACIÓN DE TRIAGE SEMÁNTICO POR IA (OLLAMA)")
    print("Materia: Inteligencia Artificial Aplicada al Desarrollo de Software")
    print("Estudiante: Gallardo Fernando Andrés - Instituto Combate de Mbororé")
    print(f"Modelo: {MODELO_OLLAMA} (Procesamiento 100% Local y Privado)")
    print("="*75)
    
    # Intento de verificación rápida de conexión a Ollama
    try:
        res = requests.get("http://localhost:11434/", timeout=2)
        if res.status_code == 200:
            print("✅ Conexión con servidor Ollama establecida correctamente.")
    except Exception:
        print("❌ ADVERTENCIA: El servidor de Ollama no responde en http://localhost:11434")
        print("   Asegúrate de abrir la aplicación Ollama y que esté corriendo.")
        print("   Comando sugerido en terminal: ollama run llama3.2")
        print("-" * 75)

    while True:
        print("\nSeleccione una opción de ejecución:")
        print("1. Procesar lote de pacientes predefinidos (Para el reporte final)")
        print("2. Evaluar una consulta personalizada con Ollama en tiempo real")
        print("3. Salir")
        
        opcion = input("Opción (1-3): ").strip()
        
        if opcion == "1":
            ejecutar_lote_ollama()
        elif opcion == "2":
            print("\n--- EVALUAR CONSULTA CON IA LOCAL ---")
            nombre = input("Ingrese el nombre/ID del paciente ficticio: ").strip()
            if not nombre:
                nombre = "Paciente Anónimo"
            consulta = input("Describa el motivo de la consulta/crisis: ").strip()
            if not consulta:
                print("Consulta vacía. Operación cancelada.")
                continue
                
            print("\nAnalizando con Llama 3.2...")
            try:
                clasificacion = clasificar_con_ollama(consulta)
                prioridad = clasificacion["prioridad"]
                justificacion = clasificacion["justificacion"]
                
                if prioridad == "ALTA":
                    emoji = "🔴"
                elif prioridad == "MEDIA":
                    emoji = "🟡"
                else:
                    emoji = "🟢"
                    
                print(f"\n{emoji} RESULTADO DEL TRIAGE (IA LOCAL):")
                print(f"   Paciente: {nombre}")
                print(f"   Consulta: \"{consulta}\"")
                print(f"   → Prioridad Estimada: {prioridad}")
                print(f"   → Justificación Técnica: {justificacion}")
                
                guardar = input("\n¿Desea agregar este caso al archivo resultados_ollama.csv? (s/n): ").strip().lower()
                if guardar == 's':
                    resultados_existentes = []
                    if os.path.exists("resultados_ollama.csv"):
                        try:
                            with open("resultados_ollama.csv", "r", encoding="utf-8") as f:
                                reader = csv.reader(f)
                                header = next(reader)
                                for row in reader:
                                    if len(row) >= 4:
                                        resultados_existentes.append({
                                            "nombre": row[0],
                                            "consulta": row[1],
                                            "prioridad": row[2],
                                            "justificacion": row[3]
                                        })
                        except Exception:
                            pass
                    
                    resultados_existentes.append({
                        "nombre": nombre,
                        "consulta": consulta,
                        "prioridad": prioridad,
                        "justificacion": justificacion
                    })
                    guardar_resultados_csv(resultados_existentes)
                    generar_reporte_html(resultados_existentes)
                    
            except Exception as e:
                print(f"\n❌ Error en la clasificación: {e}")
                
        elif opcion == "3":
            print("\nSaliendo del sistema de IA. ¡Hasta luego!")
            break
        else:
            print("\n⚠️ Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
