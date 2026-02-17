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

def generate_question(profile: str, context: dict = None, scores: dict = None) -> str:
    # Asegúrate de que las preguntas sean variadas
    extra_context = ""

    if context:
        extra_context = f"""
        Contexto del pretest del usuario:
        {context["summary"]}
        """

    # Evitar repetir las mismas preguntas
    previous_questions = "\n".join(used_questions[profile][-5:])

    prompt = f"""
    Eres un orientador vocacional experto en RIASEC.

    {extra_context}

    Genera una pregunta en forma de afirmacion interesante y diferente para el perfil {profile}, para explorar los intereses y características de la persona sin hacer referencia directa a su perfil. 
    La pregunta debe centrarse en los intereses y motivaciones del usuario. Evita mencionar el perfil RIASEC o hacer preguntas directas sobre él.

    No repitas las mismas afirmaciones. Evita repetir ideas como:
    {previous_questions}

    - afirmacion corta
    - usa lenguaje sencillo
    - haz la afirmacion en primera persona
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    question = response.choices[0].message.content.strip()
    used_questions[profile].append(question)  # Registrar la pregunta para no repetirla

    return question
