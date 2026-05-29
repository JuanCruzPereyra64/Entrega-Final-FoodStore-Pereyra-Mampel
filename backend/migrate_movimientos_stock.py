import os
from dotenv import load_dotenv
load_dotenv(".env")
from sqlmodel import Session, text
from backend.database import engine

with Session(engine) as session:
    try:
        session.exec(text("""
        CREATE TABLE IF NOT EXISTS movimientos_stock (
            id SERIAL PRIMARY KEY,
            ingrediente_id INTEGER NOT NULL REFERENCES ingredientes(id) ON DELETE CASCADE,
            cantidad NUMERIC(10, 2) NOT NULL,
            tipo VARCHAR(20) NOT NULL,
            motivo VARCHAR(255) NOT NULL,
            usuario_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """))
        session.commit()
        print("Migración exitosa: tabla movimientos_stock creada.")
    except Exception as e:
        print(f"Error en migración: {e}")
        session.rollback()
