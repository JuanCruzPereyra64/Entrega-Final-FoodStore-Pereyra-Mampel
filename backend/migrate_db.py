import os
from dotenv import load_dotenv
load_dotenv(".env")
from sqlmodel import Session, text
from backend.database import engine

with Session(engine) as session:
    try:
        # Renombrar, pero si ya se renombró y falló, ignorar error
        try:
            session.exec(text("ALTER TABLE ingredientes RENAME COLUMN descripcion TO unidad_medida;"))
        except:
            session.rollback()
            
        session.exec(text("UPDATE ingredientes SET unidad_medida = 'Unidades' WHERE unidad_medida IS NULL;"))
        session.exec(text("ALTER TABLE ingredientes ALTER COLUMN unidad_medida TYPE VARCHAR(50);"))
        session.exec(text("ALTER TABLE ingredientes ALTER COLUMN unidad_medida SET NOT NULL;"))
        session.exec(text("ALTER TABLE ingredientes ALTER COLUMN unidad_medida SET DEFAULT 'Unidades';"))
        session.commit()
        print("Migración exitosa: descripcion renombrada a unidad_medida")
    except Exception as e:
        print(f"Error en migración: {e}")
        session.rollback()
