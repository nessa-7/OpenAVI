import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_pretest(answers: list):

    prompt = f"""
    Analiza las siguientes respuestas de un pretest vocacional:

    {answers}

    Tu tarea:

    1. Detectar inclinaciones según el modelo RIASEC
    2. Asignar puntajes del 0 al 10 a cada perfil:
       R, I, A, S, E, C
    3. Explicar brevemente el perfil dominante

    Responde SOLO en JSON:

    {{
      "scores": {{
        "R": int,
        "I": int,
        "A": int,
        "S": int,
        "E": int,
        "C": int
      }},
      "summary": "explicación corta"
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    import json
    return json.loads(response.choices[0].message.content)
