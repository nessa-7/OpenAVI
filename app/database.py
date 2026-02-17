import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


def get_programs():
    query = text("""
        SELECT nombre, descripcion
        FROM PROGRAMA
        WHERE activo = true
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        programs = [
            {
                "name": row.nombre,
                "description": row.descripcion
            }
            for row in result
        ]
        
        # Imprimir la lista de programas para depuración
        print("Programas recuperados:", programs)
        return programs

