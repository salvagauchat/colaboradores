from pydantic import BaseModel
from typing import Optional

class Colaborador(BaseModel):
    id: Optional[str] = None
    fullname:str
    nombre:str
    apellido:str
    email:str
    userAD:str