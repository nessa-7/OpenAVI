import random

PROFILES = ["R", "I", "A", "S", "E", "C"]


import random

PROFILES = ["R", "I", "A", "S", "E", "C"]


def choose_profile(scores: dict, question_count: int, history: list) -> str:

    # ordenar perfiles por puntaje (del pretest + test)
    sorted_profiles = sorted(scores, key=scores.get, reverse=True)

    top3 = sorted_profiles[:3]
    others = sorted_profiles[3:]

    # ---------- FASE 1: enfocarse en intereses principales ----------
    if question_count < 10:

        # 80% probabilidad de preguntar del top 3
        if random.random() < 0.8:
            profile = random.choice(top3)
        else:
            profile = random.choice(others)

    # ---------- FASE 2: exploración equilibrada ----------
    else:

        if random.random() < 0.6:
            profile = random.choice(top3)
        else:
            profile = random.choice(PROFILES)

    # evitar repetir seguido
    if history and profile == history[-1]:
        alternatives = [p for p in PROFILES if p != profile]
        profile = random.choice(alternatives)

    return profile
