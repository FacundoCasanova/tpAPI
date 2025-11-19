from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from database import get_session
from models import AutoCreate, AutoResponse, AutoUpdate, AutoResponseWithVentas
from repository import AutoRepository

router = APIRouter(prefix="/autos", tags=["Autos"])
repo = AutoRepository()

@router.post("/", response_model=AutoResponse, status_code=status.HTTP_201_CREATED)
def crear_auto(auto: AutoCreate, session: Session = Depends(get_session)):
   
    if repo.get_by_chasis(session, auto.numero_chasis):
        raise HTTPException(status_code=400, detail="El número de chasis ya existe")
    return repo.create(session, auto)

@router.get("/", response_model=List[AutoResponse])
def listar_autos(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return repo.get_all(session, skip, limit)

@router.get("/{auto_id}", response_model=AutoResponse)
def obtener_auto(auto_id: int, session: Session = Depends(get_session)):
    auto = repo.get_by_id(session, auto_id)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto

@router.put("/{auto_id}", response_model=AutoResponse)
def actualizar_auto(auto_id: int, auto_update: AutoUpdate, session: Session = Depends(get_session)):
    auto = repo.update(session, auto_id, auto_update)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto

@router.delete("/{auto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_auto(auto_id: int, session: Session = Depends(get_session)):
    if not repo.delete(session, auto_id):
        raise HTTPException(status_code=404, detail="Auto no encontrado")

@router.get("/chasis/{numero_chasis}", response_model=AutoResponse)
def buscar_por_chasis(numero_chasis: str, session: Session = Depends(get_session)):
    auto = repo.get_by_chasis(session, numero_chasis)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto

@router.get("/{auto_id}/with-ventas", response_model=AutoResponseWithVentas)
def obtener_auto_con_ventas(auto_id: int, session: Session = Depends(get_session)):
    auto = repo.get_by_id(session, auto_id)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto