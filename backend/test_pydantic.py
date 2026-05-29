import os
from dotenv import load_dotenv
load_dotenv(".env")
from backend.database import engine
from sqlmodel import Session, select
from backend.models.ingrediente import Ingrediente
from backend.schemas.ingrediente import IngredienteRead

with Session(engine) as session:
    try:
        ings = session.exec(select(Ingrediente)).all()
        for i in ings:
            print(f"Ingrediente: {i.nombre}, Unidad: {i.unidad_medida}")
            try:
                ir = IngredienteRead.model_validate(i)
                print("Valid:", ir)
            except Exception as e:
                print("Pydantic Error:", e)
    except Exception as e:
        print("DB Error:", e)
