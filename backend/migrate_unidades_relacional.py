import os
from dotenv import load_dotenv
load_dotenv(".env")
from sqlmodel import Session, text
from backend.database import engine, create_db_and_tables

# Ensure tables are created (including unidades_medida)
create_db_and_tables()

with Session(engine) as session:
    try:
        # 1. Fetch unique unidades
        result = session.exec(text("SELECT DISTINCT unidad_medida FROM ingredientes"))
        unidades = [row[0] for row in result.all() if row[0]]

        # 2. Insert units and get map
        unidad_map = {}
        for u in unidades:
            session.exec(text("INSERT INTO unidades_medida (nombre) VALUES (:n) ON CONFLICT DO NOTHING"), params={"n": u})
        
        # refresh to get IDs
        res_unidades = session.exec(text("SELECT id, nombre FROM unidades_medida")).all()
        for row in res_unidades:
            unidad_map[row[1]] = row[0]
            
        print(f"Unidades map: {unidad_map}")

        # 3. Add column to ingredientes
        try:
            session.exec(text("ALTER TABLE ingredientes ADD COLUMN unidad_medida_id INTEGER;"))
        except:
            session.rollback() # column might exist
            
        # 4. Update ingredientes
        for nombre, u_id in unidad_map.items():
            session.exec(text("UPDATE ingredientes SET unidad_medida_id = :uid WHERE unidad_medida = :n"), params={"uid": u_id, "n": nombre})
            
        # Handle ingredients that might have null unidad_medida (just in case)
        if len(unidad_map) > 0:
            first_id = list(unidad_map.values())[0]
            session.exec(text("UPDATE ingredientes SET unidad_medida_id = :uid WHERE unidad_medida_id IS NULL"), params={"uid": first_id})
            
        # 5. Set column as not null and drop old column
        session.exec(text("ALTER TABLE ingredientes ALTER COLUMN unidad_medida_id SET NOT NULL;"))
        
        try:
            session.exec(text("ALTER TABLE ingredientes ADD CONSTRAINT fk_unidad_medida FOREIGN KEY (unidad_medida_id) REFERENCES unidades_medida(id);"))
        except:
            session.rollback() # FK might exist

        session.exec(text("ALTER TABLE ingredientes DROP COLUMN unidad_medida;"))

        session.commit()
        print("Migración a tabla relacional exitosa.")
    except Exception as e:
        print(f"Error en migración: {e}")
        session.rollback()
