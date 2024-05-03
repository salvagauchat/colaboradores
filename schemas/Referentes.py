from pydantic import BaseModel
from typing import Optional

class Referentes(BaseModel):
    id: Optional[str] = None
    proyecto:str
    lider_tecnico:int
    lider_tribu:int
    po:int