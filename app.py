from fastapi import FastAPI
from routes import colaborador, canales, referentes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="API Colaboradores, Canales y Referentes",
              description="Registro de colaboradores/referentes y canales de comunicación de cada tribu.")

#Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(colaborador.router)
app.include_router(canales.router)
app.include_router(referentes.router)