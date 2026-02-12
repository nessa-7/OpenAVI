PROGRAMS = {
    "R": [
        "Mecánica de motores diésel", 
        "Montaje y puesta en marcha de sistemas eléctricos industriales",
        "Mecánica industrial"
    ],
    "I": [
        "Análisis y desarrollo de software", 
        "Gestión de redes de datos", 
        "Desarrollo de videojuegos", 
        "Desarrollo multimedia y web"
    ],
    "A": [
        "Diseño de prendas de vestir", 
        "Diseño, desarrollo e innovación de productos de la confección", 
        "Artes gráficas"
    ],
    "S": [
        "Atención al cliente", 
        "Educación", 
        "Apoyo administrativo en salud", 
        "Auxiliar de enfermería", 
        "Guía turístico", 
        "Gestión documental"
    ],
    "E": [
        "Administración de recursos humanos", 
        "Administración y control ambiental", 
        "Gestión del talento humano", 
        "Gestión administrativa y financiera"
    ],
    "C": [
        "Contabilidad", 
        "Programación de sistemas de información", 
        "Gestión de redes de datos", 
        "Gestión documental", 
        "Seguridad informática"
    ]
}


def recommend_programs(top_profiles):
    results = []

    for profile in top_profiles:
        programs = PROGRAMS.get(profile, [])
        if programs:
            results.append(programs[0])

    return results