from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.riasec_engine import choose_profile
from app.question_ai import generate_question
from app.schemas import (
    QuestionRequest,
    QuestionResponse,
    AnswerRequest,
    ResultResponse
)
from app.recommender import recommend_programs

from app.database import get_programs 


app = FastAPI(title="RIASEC API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"mensaje": "API RIASEC funcionando 🚀"}


# --------- sesiones ---------

sessions = {}


def get_session(session_id: str):

    if session_id not in sessions:
        sessions[session_id] = {
            "question_count": 0,
            "history": []
        }

    return sessions[session_id]


# --------- preguntas ---------

@app.post("/next-question")
def next_question(data: QuestionRequest):
    session = get_session(data.session_id)

    # Asegúrate de que el historial se esté actualizando después de cada respuesta
    profile = choose_profile(
        data.riasec_scores,
        session["question_count"],
        session["history"]
    )

    context = session.get("pretest_context")

    # Llamamos a la función para generar una pregunta y asegurarnos de que el historial se use para la variabilidad
    question = generate_question(profile, context, data.riasec_scores)

    session["question_count"] += 1
    session["history"].append(profile)  # Actualizamos el historial de respuestas

    return QuestionResponse(
        question=question,
        category=profile,
        session_id=data.session_id
    )


# --------- actualizar puntaje ---------

@app.post("/update-score")
def update_score(data: AnswerRequest):

    scores = data.riasec_scores
    scores[data.category] += data.answer

    return {"updated_scores": scores}


# --------- resultado final ---------

@app.post("/result")
def final_result(scores: dict):

    programs_from_db = get_programs()

    programs = recommend_programs(
        scores,
        programs_from_db
    )

    top_profiles = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    formatted_profiles = [
        {"profile": p[0], "score": p[1]}
        for p in top_profiles
    ]

    programs_from_db = get_programs()
    print("Programas desde DB:", programs_from_db)
    
    return {
        "top_profiles": formatted_profiles,
        "recommended_programs": programs
    }



from app.pretest_ai import analyze_pretest


@app.post("/analyze-pretest")
def analyze(data: dict):

    result = analyze_pretest(data["answers"])

    session = get_session(data["session_id"])

    session["pretest_context"] = result

    return result
