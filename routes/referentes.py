from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from config.db import conn
from models.colaborador import referentes
from schemas.Referentes import Referentes

router = APIRouter(prefix="/referentes",
                    tags=["Referentes"],
                    responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado."}})

@router.get("/listado", status_code= status.HTTP_200_OK)
def getReferentes():
    lista = conn.execute(referentes.select()).fetchall()
    
    #Verifica si se encontraron referentes
    if not lista:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No existen referentes")
    
    rows:Referentes = []
    for t in lista:
        id = t[0]
        proyecto = t[1]
        lider_tecnico = t[2]
        lider_tribu = t[3]
        po = t[4]
        rows.append(
            {"id": id, "proyecto":proyecto, "lider_tecnico": lider_tecnico,"lider_tribu": lider_tribu, "po": po})
    return rows

@router.get("/buscarReferente/{id}", status_code= status.HTTP_200_OK)
def getReferente(id:str):
    
    lista = conn.execute(referentes.select().where(referentes.c.id == id)).fetchall()
    
    # Verificar si se encontró algún colaborador
    if not lista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto/referente no encontrado")
    
    rows = []
    for t in lista:
        id = t[0]
        proyecto = t[1]
        lider_tecnico = t[2]
        lider_tribu = t[3]
        po = t[4]
        rows.append(
            {"id": id, "proyecto":proyecto, "lider_tecnico": lider_tecnico,"lider_tribu": lider_tribu, "po": po})
    return rows

@router.delete("/delete/{id}", status_code= status.HTTP_204_NO_CONTENT)
def deleteReferente(id:str):
    lista = conn.execute(referentes.delete().where(referentes.c.id == id))
    
    # Verifica si se encontró algún colaborador
    if not lista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto/referentes no encontrado")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/create", status_code= status.HTTP_201_CREATED)
def createReferente(referente: Referentes):
    
    # Verifica si alguna de las propiedades requeridas está vacía
    if not referente.proyecto or not referente.lider_tecnico or not referente.lider_tribu or not referente.po:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Se requiere proyecto, lideres y PO.")
    
    new_referente = dict()

    new_referente['proyecto'] = referente.proyecto
    new_referente['lider_tecnico_id'] = referente.lider_tecnico
    new_referente['lider_tribu_id'] = referente.lider_tribu
    new_referente['po_id'] = referente.po 

    print(new_referente) 
    
    result = conn.execute(referentes.insert().values(new_referente))
    print(f"Record # {result.inserted_primary_key}")

    ultimo = referentes.select().where(referentes.c.id == result.inserted_primary_key[0])
    lista = conn.execute(ultimo).fetchall()
    rows = []
    for t in lista: #Estas líneas asignan los valores de cada columna de la fila actual a variables separadas
        id = t[0]
        proyecto = t[1]
        lider_tecnico = t[2]
        lider_tribu = t[3]
        po = t[4]
        rows.append(
            {"id": id, "proyecto":proyecto, "lider_tecnico_id": lider_tecnico,"lider_tribu_id": lider_tribu, "po_id": po})
    return rows

@router.put("/edit/{id}", status_code= status.HTTP_200_OK)
def editReferente(id:str, referente:Referentes):    
    updated_rows = conn.execute(
        referentes.update()
        .where(referentes.c.id == id)
        .values(
            proyecto=referente.proyecto,
            lider_tecnico_id=referente.lider_tecnico,
            lider_tribu_id=referente.lider_tribu,
            po_id = referente.po
        )
    )

    # Verifica si se actualizó algún registro
    if updated_rows.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Proyecto/referentes no encontrado")
    
    lista = conn.execute(referentes.select().where(referentes.c.id == id)).fetchall()
    rows = []
    for t in lista:
        id = t[0]
        proyecto = t[1]
        lider_tecnico = t[2]
        lider_tribu = t[3]
        po = t[4]
        rows.append(
            {"id": id, "proyecto":proyecto, "lider_tecnico_id": lider_tecnico,"lider_tribu_id": lider_tribu, "po_id": po})
    return rows