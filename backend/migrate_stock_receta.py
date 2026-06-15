import os
from dotenv import load_dotenv
load_dotenv(".env")
from sqlmodel import Session, text
from backend.database import engine

with Session(engine) as session:
    try:
        # Añadir stock_cantidad a ingredientes
        session.exec(text("ALTER TABLE ingredientes ADD COLUMN IF NOT EXISTS stock_cantidad BIGINT NOT NULL DEFAULT 0;"))
        
        # Añadir cantidad a producto_ingrediente
        session.exec(text("ALTER TABLE producto_ingrediente ADD COLUMN IF NOT EXISTS cantidad NUMERIC(10, 3) NOT NULL DEFAULT 1.0;"))
        
        session.commit()
        print("Migración exitosa: columnas de stock y cantidad requerida añadidas correctamente.")
    except Exception as e:
        print(f"Error en migración: {e}")
        session.rollback()
