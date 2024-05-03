from pydantic import BaseModel
from typing import Optional

class Canales(BaseModel):
    id: Optional[str] = None
    webex:str
    whatsapp:str
    email:str
    proyecto:str