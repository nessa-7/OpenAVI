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

@app.post("/next-question", response_model=QuestionResponse)
def next_question(data: QuestionRequest):

    session = get_session(data.session_id)

    profile = choose_profile(
        data.riasec_scores,
        session["question_count"],
        session["history"]
    )

    question = generate_question(profile)

    session["question_count"] += 1
    session["history"].append(profile)

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

@app.post("/result", response_model=ResultResponse)
def final_result(scores: dict):

    sorted_profiles = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top = sorted_profiles[:3]

    programs = recommend_programs([p for p, _ in top])

    return {
        "dominant_profiles": [
            {"profile": p, "score": s}
            for p, s in top
        ],
        "recommended_programs": programs
    }
