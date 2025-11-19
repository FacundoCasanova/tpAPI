from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import validator
import re



class AutoBase(SQLModel):
    marca: str
    modelo: str
    anio: int = Field(..., ge=1900, le=datetime.now().year)
    numero_chasis: str = Field(unique=True, index=True)

    @validator("numero_chasis")
    def validar_chasis(cls, v):
        if not re.match(r"^[a-zA-Z0-9]+$", v):
            raise ValueError("El número de chasis debe ser alfanumérico")
        return v

class Auto(AutoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ventas: List["Venta"] = Relationship(back_populates="auto")

class AutoCreate(AutoBase):
    pass

class AutoUpdate(SQLModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    anio: Optional[int] = None
    numero_chasis: Optional[str] = None

class AutoResponse(AutoBase):
    id: int

class AutoResponseWithVentas(AutoResponse):
    ventas: List["VentaResponse"] = []




class VentaBase(SQLModel):
    nombre_comprador: str
    precio: float = Field(gt=0)
    fecha_venta: datetime
    auto_id: int = Field(foreign_key="auto.id")

    @validator("nombre_comprador")
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El nombre del comprador no puede estar vacío")
        return v
    
    @validator("fecha_venta")
    def fecha_no_futura(cls, v):
        if v > datetime.now():
            raise ValueError("La fecha de venta no puede ser futura")
        return v

class Venta(VentaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    auto: Optional[Auto] = Relationship(back_populates="ventas")

class VentaCreate(VentaBase):
    pass

class VentaUpdate(SQLModel):
    nombre_comprador: Optional[str] = None
    precio: Optional[float] = None
    fecha_venta: Optional[datetime] = None

class VentaResponse(VentaBase):
    id: int

class VentaResponseWithAuto(VentaResponse):
    auto: Optional[AutoResponse] = None


AutoResponseWithVentas.update_forward_refs()