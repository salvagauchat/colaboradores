from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from config.db import conn
from models.colaborador import colaboradores
from schemas.Colaborador import Colaborador

router = APIRouter(prefix="/colaborador",
                    tags=["Colaborador"],
                    responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado."}})

@router.get("/listado", status_code= status.HTTP_200_OK)
def getColaboradores():
    lista = conn.execute(colaboradores.select()).fetchall()
    
    #Verifica si se encontró algún colaborador
    if not lista:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No existe ningun colaborador")
    
    rows:Colaborador = []
    for t in lista:
        id = t[0]
        fullname = t[1]
        nombre = t[2]
        apellido = t[3]
        email = t[4]
        userAD = t[5]
        rows.append(
            {"id": id, "fullname":fullname, "nombre": nombre, "apellido": apellido, "email": email, "userAD": userAD})
    return rows

@router.get("/buscarColaborador/{id}", status_code= status.HTTP_200_OK)
def getColaborador(id:str):
    
    lista = conn.execute(colaboradores.select().where(colaboradores.c.id == id)).fetchall()
    
    # Verificar si se encontró algún colaborador
    if not lista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
    
    rows = []
    for t in lista:
        id = t[0]
        fullname = t[1]
        nombre = t[2]
        apellido = t[3]
        email = t[4]
        userAD = t[5]
        rows.append(
            {"id": id, "fullname":fullname, "nombre": nombre, "apellido": apellido, "email": email, "userAD": userAD})
    return rows

@router.delete("/delete/{id}", status_code= status.HTTP_204_NO_CONTENT)
def deleteColaborador(id:str):
    lista = conn.execute(colaboradores.delete().where(colaboradores.c.id == id))
    
    # Verifica si se encontró algún colaborador
    if not lista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.post("/create", status_code= status.HTTP_201_CREATED)
def createColaborador(colaboradorDb: Colaborador):
    
    # Verifica si alguna de las propiedades requeridas está vacía
    if not colaboradorDb.nombre or not colaboradorDb.apellido or not colaboradorDb.email:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Se requieren nombre, apellido y email")
    
    new_colaborador = dict()

    new_colaborador['fullname'] = colaboradorDb.fullname
    new_colaborador['nombre'] = colaboradorDb.nombre if colaboradorDb.nombre else None
    new_colaborador['apellido'] = colaboradorDb.apellido if colaboradorDb.apellido else None
    new_colaborador['email'] = colaboradorDb.email if colaboradorDb.email else None
    new_colaborador['userAD'] = colaboradorDb.userAD if colaboradorDb.userAD else None  # Asigna None si userAD no está definido

    print(new_colaborador) 
    
    result = conn.execute(colaboradores.insert().values(new_colaborador))
    print(f"Record # {result.inserted_primary_key}")

    ultimo = colaboradores.select().where(colaboradores.c.id == result.inserted_primary_key[0])
    lista = conn.execute(ultimo).fetchall()
    rows = []
    for t in lista: #Estas líneas asignan los valores de cada columna de la fila actual a variables separadas
        id = t[0]
        fullname = t[1]
        nombre = t[2]
        apellido = t[3]
        email = t[4]
        userAD = t[5]
        rows.append(
            {"id": id, "fullname":fullname, "nombre": nombre, "apellido": apellido, "email": email, "userAD": userAD})
    return rows

@router.put("/edit/{id}", status_code= status.HTTP_200_OK)
def editColaborador(id:str, colaboradorDb:Colaborador):
    updated_rows = conn.execute(
        colaboradores.update()
        .where(colaboradores.c.id == id)
        .values(
            fullname=colaboradorDb.fullname,
            nombre=colaboradorDb.nombre if colaboradorDb.nombre else None,
            apellido=colaboradorDb.apellido if colaboradorDb.apellido else None,
            email=colaboradorDb.email if colaboradorDb.email else None,
            userAD = colaboradorDb.userAD if colaboradorDb.userAD else None
        )
    )

    # Verifica si se actualizó algún registro
    if updated_rows.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
    
    lista = conn.execute(colaboradores.select().where(colaboradores.c.id == id)).fetchall()
    rows = []
    for t in lista:
        fullname = t[1]
        nombre = t[2]
        apellido = t[3]
        email = t[4]
        userAD = t[5]
        rows.append(
            {"id": id, "fullname":fullname, "nombre": nombre, "apellido": apellido, "email": email, "userAD": userAD})
    return rows