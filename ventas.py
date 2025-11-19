from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from database import get_session
from models import VentaCreate, VentaResponse, VentaUpdate, VentaResponseWithAuto
from repository import VentaRepository, AutoRepository


router = APIRouter(prefix="/ventas", tags=["Ventas"])

venta_repo = VentaRepository()
auto_repo = AutoRepository()

@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(venta: VentaCreate, session: Session = Depends(get_session)):
  
    if not auto_repo.get_by_id(session, venta.auto_id):
        raise HTTPException(status_code=404, detail="El auto especificado no existe")
    return venta_repo.create(session, venta)

@router.get("/", response_model=List[VentaResponse])
def listar_ventas(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return venta_repo.get_all(session, skip, limit)

@router.get("/{venta_id}", response_model=VentaResponse)
def obtener_venta(venta_id: int, session: Session = Depends(get_session)):
    venta = venta_repo.get_by_id(session, venta_id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@router.put("/{venta_id}", response_model=VentaResponse)
def actualizar_venta(venta_id: int, venta_update: VentaUpdate, session: Session = Depends(get_session)):
    venta = venta_repo.update(session, venta_id, venta_update)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@router.delete("/{venta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_venta(venta_id: int, session: Session = Depends(get_session)):
    if not venta_repo.delete(session, venta_id):
        raise HTTPException(status_code=404, detail="Venta no encontrada")

@router.get("/auto/{auto_id}", response_model=List[VentaResponse])
def listar_ventas_por_auto(auto_id: int, session: Session = Depends(get_session)):
    # Verificamos que el auto exista para dar un mejor error
    if not auto_repo.get_by_id(session, auto_id):
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return venta_repo.get_by_auto_id(session, auto_id)

@router.get("/comprador/{nombre}", response_model=List[VentaResponse])
def buscar_ventas_por_comprador(nombre: str, session: Session = Depends(get_session)):
    return venta_repo.get_by_comprador(session, nombre)

@router.get("/{venta_id}/with-auto", response_model=VentaResponseWithAuto)
def obtener_venta_con_auto(venta_id: int, session: Session = Depends(get_session)):
    venta = venta_repo.get_by_id(session, venta_id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta