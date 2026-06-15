import os
import sys

# Agregar la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(".env")

from backend.database import engine
from backend.uow.unit_of_work import UnitOfWork
from backend.services import ingrediente_service
from backend.schemas.ingrediente import IngredienteUpdate

def run_seed():
    with UnitOfWork() as uow:
        ingredientes = uow.ingredientes.get_all()
        for ing in ingredientes:
            update_data = IngredienteUpdate()
            needs_update = False
            
            if ing.stock_cantidad < 15:
                update_data.stock_cantidad = 15
                needs_update = True
                
            if ing.stock_cantidad < 15:
                update_data.stock_cantidad = 15
                needs_update = True
            elif ing.stock_cantidad > 60:
                update_data.stock_cantidad = 60
                needs_update = True
                
            if needs_update:
                ingrediente_service.update(uow, ing.id, update_data, usuario_id=None)
                print(f"Actualizado ingrediente: {ing.nombre}")
        
        print("Seed de stock completado.")

if __name__ == "__main__":
    run_seed()
