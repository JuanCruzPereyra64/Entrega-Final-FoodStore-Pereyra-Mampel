import os
from dotenv import load_dotenv
load_dotenv(".env")
from sqlmodel import Session, text
from backend.database import engine

with Session(engine) as session:
    try:
        # Añadir stock_actual y stock_minimo a ingredientes
        session.exec(text("ALTER TABLE ingredientes ADD COLUMN IF NOT EXISTS stock_actual NUMERIC(10, 2) NOT NULL DEFAULT 0.0;"))
        session.exec(text("ALTER TABLE ingredientes ADD COLUMN IF NOT EXISTS stock_minimo NUMERIC(10, 2) NOT NULL DEFAULT 0.0;"))
        
        # Añadir cantidad_requerida a producto_ingrediente
        session.exec(text("ALTER TABLE producto_ingrediente ADD COLUMN IF NOT EXISTS cantidad_requerida NUMERIC(10, 2) NOT NULL DEFAULT 1.0;"))
        
        session.commit()
        print("Migración exitosa: columnas de stock y cantidad requerida añadidas correctamente.")
    except Exception as e:
        print(f"Error en migración: {e}")
        session.rollback()
