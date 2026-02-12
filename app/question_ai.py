import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

used_questions = {
    "R": [],
    "I": [],
    "A": [],
    "S": [],
    "E": [],
    "C": []
}


def generate_question(profile: str) -> str:

    previous = "\n".join(used_questions[profile][-5:])

    for _ in range(5):

        prompt = f"""
        Eres un orientador vocacional experto en el modelo RIASEC.

        El usuario ya realizó un pretest inicial que sugiere inclinación hacia el perfil {profile}.
        Tu tarea es profundizar en ese perfil con una afirmación que explore aspectos más específicos y variados de su comportamiento.

        Genera UNA afirmación corta en primera persona claramente relacionada con actividades del perfil {profile} del modelo RIASEC.

        La afirmación debe:
        - evaluar el perfil {profile}
        - explorar situaciones reales (trabajo, estudio de colegio, hobbies, resolución de problemas, interacción social, liderazgo o creatividad)
        - ayudar a confirmar o refinar la inclinación del usuario
        - no repetir ideas similares a estas afirmaciones previas: {previous}

        Reglas estrictas:
        - debe ser una afirmación, no una pregunta
        - no usar la palabra "o"
        - usar lenguaje cotidiano
        - escala de respuesta 1–5
        - responder solo con la afirmación

        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )

        question = response.choices[0].message.content.strip()

        if question not in used_questions[profile]:
            used_questions[profile].append(question)
            return question

    return "Me gusta aprender cosas nuevas."
