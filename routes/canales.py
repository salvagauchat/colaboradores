from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from config.db import conn
from models.colaborador import canales
from schemas.Canales import Canales

router = APIRouter(prefix="/canales",
                    tags=["Canales"],
                    responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado."}})

@router.get("/listado", status_code= status.HTTP_200_OK)
def getCanales():
    lista = conn.execute(canales.select()).fetchall()
    
    #Verifica si se encontró algún colaborador
    if not lista:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No existe ningun canal")
    
    rows:Canales = []
    for t in lista:
        id = t[0]
        webex = t[1]
        whatsapp = t[2]
        email = t[3]
        proyecto = t[4]
        rows.append(
            {"id": id, "webex":webex, "whatsapp": whatsapp,"email": email, "proyecto": proyecto})
    return rows

@router.get("/buscarCanal/{id}", status_code= status.HTTP_200_OK)
def getCanal(id:str):
    
    lista = conn.execute(canales.select().where(canales.c.id == id)).fetchall()
    
    # Verificar si se encontró algún colaborador
    if not lista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Canal no encontrado")
    
    rows = []
    for t in lista:
        id = t[0]
        webex = t[1]
        whatsapp = t[2]
        email = t[3]
        proyecto = t[4]
        rows.append(
            {"id": id, "webex":webex, "whatsapp": whatsapp,"email": email, "proyecto": proyecto})
    return rows

@router.delete("/delete/{id}", status_code= status.HTTP_204_NO_CONTENT)
def deleteCanal(id:str):
    lista = conn.execute(canales.delete().where(canales.c.id == id))
    
    # Verifica si se encontró algún colaborador
    if not lista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Canal no encontrado")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/create", status_code= status.HTTP_201_CREATED)
def createCanal(canal: Canales):
    
    # Verifica si alguna de las propiedades requeridas está vacía
    if not canal.webex or not canal.proyecto:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Se requieren webex y proyecto obligatoriamente")
    
    new_canal = dict()

    new_canal['webex'] = canal.webex
    new_canal['whatsapp'] = canal.whatsapp if canal.whatsapp else None  # Asigna None si userAD no está definido
    new_canal['email'] = canal.email if canal.email else None 
    new_canal['proyecto'] = canal.proyecto 

    print(new_canal) 
    
    result = conn.execute(canales.insert().values(new_canal))
    print(f"Record # {result.inserted_primary_key}")

    ultimo = canales.select().where(canales.c.id == result.inserted_primary_key[0])
    lista = conn.execute(ultimo).fetchall()
    rows = []
    for t in lista: #Estas líneas asignan los valores de cada columna de la fila actual a variables separadas
        id = t[0]
        webex = t[1]
        whatsapp = t[2]
        email = t[3]
        proyecto = t[4]
        rows.append(
            {"id": id, "webex":webex, "whatsapp": whatsapp,"email": email, "proyecto": proyecto})
    return rows

@router.put("/edit/{id}", status_code= status.HTTP_200_OK)
def editCanal(id:str, canal:Canales):
    updated_rows = conn.execute(
        canales.update()
        .where(canales.c.id == id)
        .values(
            webex=canal.webex,
            whatsapp=canal.whatsapp if canal.whatsapp else None,
            email=canal.email if canal.whatsapp else None,
            proyecto = canal.proyecto
        )
    )

    # Verifica si se actualizó algún registro
    if updated_rows.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Canal no encontrado")
    
    lista = conn.execute(canales.select().where(canales.c.id == id)).fetchall()
    rows = []
    for t in lista:
        id = t[0]
        webex = t[1]
        whatsapp = t[2]
        email = t[3]
        proyecto = t[4]
        rows.append(
            {"id": id, "webex":webex, "whatsapp": whatsapp,"email": email, "proyecto": proyecto})
    return rows