from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_program(description: str):

    prompt = f"""
Analiza este programa académico y clasifícalo
según el modelo RIASEC.

Asigna puntajes del 1 al 5.

Devuelve SOLO JSON:

{{"R":0,"I":0,"A":0,"S":0,"E":0,"C":0}}

Programa:
{description}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)
