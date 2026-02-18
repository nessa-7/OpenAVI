import os
import json
from openai import OpenAI
from app.riasec_keywords import RIASEC_KEYWORDS

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def score_program(program, user_scores):
    description = program["description"].lower()
    score = 0

    # Puntuación por coincidencia de palabras clave
    for profile, keywords in RIASEC_KEYWORDS.items():
        matches = sum(1 for word in keywords if word in description)
        score += matches * user_scores.get(profile, 0)  # Asegúrate de que esté usando el puntaje del perfil correctamente

    # Puntuación adicional por la relevancia de las necesidades del usuario
    for profile, score_val in user_scores.items():
        if score_val > 7:  # Si un perfil tiene un puntaje alto, agregamos un bono
            score += 2

    print(f"Programa: {program['name']} | Puntaje: {score}")  # Para depuración
    return score



def recommend_programs(user_scores, programs):
    ranked = sorted(
        programs,
        key=lambda p: score_program(p, user_scores),
        reverse=True
    )

    top_programs = ranked[:3]  # Solo toma los primeros 3 programas

    # Verificar que top_programs no esté vacío
    if not top_programs:
        print("No se encontraron programas recomendados")

    programs_text = "\n\n".join([f"Programa: {p['name']}\nDescripción: {p['description']}" for p in top_programs])

    prompt = f"""
    El perfil RIASEC del usuario es:
    {user_scores}

    Evalúa estos programas:

    {programs_text}

    Selecciona los 3 más compatibles.
    Explica brevemente cada elección.

    Responde en JSON:
    {{
        "recommendations": [
            {{
                "name": "...",
                "reason": "Razón de la recomendación basada en el perfil"
            }}
        ]
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        response_format={"type": "json_object"}
    )

    print("Respuesta de OpenAI:", response.choices[0].message.content)

    print("User scores:", user_scores)

    content = response.choices[0].message.content

    try:
        content = content.strip()

        if content.startswith("```"):
            content = content.split("```")[1]

        parsed = json.loads(content)
        return parsed.get("recommendations", [])

    except Exception as e:
        print("Error parseando respuesta de OpenAI:", e)
        print("Contenido recibido:", content)
        return []
