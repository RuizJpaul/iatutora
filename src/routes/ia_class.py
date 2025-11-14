from flask import Blueprint, request, jsonify
import os
from google import genai
from src.utils.mongo import mongo_db
from dotenv import load_dotenv
from src.utils.extract import read_pdf
from datetime import datetime

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

bp = Blueprint("ia", __name__, url_prefix="/api/ia")
PDF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "uploads", "clase01.pdf")

@bp.route("/start", methods=["POST"])
def start_class():
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id requerido"}), 400

    # Leer PDF
    clase_text = read_pdf(PDF_PATH)

    prompt = f"""
Actúa como un profesor universitario de élite, experto en computación en la nube y DevOps.
Estamos iniciando la Clase 1: Introducción a la Computación en la Nube.

Contenido base:
{clase_text}

Instrucciones:
- Explica en bloques cortos y claros.
- Mantén el flujo pedagógico de la clase.
- Termina cada bloque con una pregunta reflexiva.
- Solo genera el primer bloque y la primera pregunta.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt
    )

    # Guardar historial en MongoDB
    mongo_db.historial.insert_one({
        "user_id": user_id,
        "type": "start_class",
        "professor_response": response.text,
        "timestamp": datetime.utcnow()
    })

    # Guardar resumen inicial
    mongo_db.resumen.update_one(
        {"user_id": user_id},
        {"$set": {"summary": response.text}},
        upsert=True
    )

    return jsonify({"response": response.text})


# ----------------------------
# Preguntar a la IA
# ----------------------------
@bp.route("/ask", methods=["POST"])
def ask_gemini():
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")
    if not user_id or not message:
        return jsonify({"error": "user_id y message son requeridos"}), 400

    # Recuperar historial reciente
    historial = list(mongo_db.historial.find({"user_id": user_id}).sort("timestamp", 1))
    historial_formateado = "\n".join(
        f"{'ESTUDIANTE' if 'student_message' in h else 'PROFESOR'}: {h.get('student_message') or h.get('professor_response')}"
        for h in historial[-5:]  # últimos 5 mensajes
    )

    # Recuperar resumen acumulativo
    resumen_doc = mongo_db.resumen.find_one({"user_id": user_id})
    resumen_actual = resumen_doc.get("summary", "") if resumen_doc else ""

    clase_text = read_pdf(PDF_PATH)

    prompt = f"""
Continuación de la Clase 1: Introducción a la Computación en la Nube.
Actúa como el mismo profesor, experto y didáctico.

Contenido base:
{clase_text}

Resumen acumulativo de la clase:
{resumen_actual}

Historial reciente:
{historial_formateado}

Respuesta del estudiante:
"{message}"

Instrucciones:
1. Antes de avanzar al siguiente bloque, revisa si el estudiante tiene alguna duda o confusión en su mensaje.
2. Si hay una duda, resuélvela primero con claridad y ejemplos.
3. Solo después de resolver la duda, continúa con el siguiente bloque de la clase.
4. Mantén un tono profesional, cercano y didáctico.
5. Termina cada intervención con una pregunta breve para el estudiante.
6. No repitas contenido ya explicado ni avances a temas futuros antes de que la duda esté resuelta.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt
    )

    # Guardar interacción en MongoDB
    mongo_db.historial.insert_one({
        "user_id": user_id,
        "type": "ask",
        "student_message": message,
        "professor_response": response.text,
        "timestamp": datetime.utcnow()
    })

    # Actualizar resumen acumulativo
    nuevo_resumen = resumen_actual + "\n" + response.text
    mongo_db.resumen.update_one(
        {"user_id": user_id},
        {"$set": {"summary": nuevo_resumen}},
        upsert=True
    )

    return jsonify({"response": response.text})