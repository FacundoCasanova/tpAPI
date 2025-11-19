from typing import List, Optional
from sqlmodel import Session, select
from models import Auto, AutoCreate, AutoUpdate, Venta, VentaCreate, VentaUpdate

class AutoRepository:
    def create(self, session: Session, auto: AutoCreate) -> Auto:
        db_auto = Auto.from_orm(auto)
        session.add(db_auto)
        session.commit()
        session.refresh(db_auto)
        return db_auto

    def get_by_id(self, session: Session, auto_id: int) -> Optional[Auto]:
        return session.get(Auto, auto_id)

    def get_all(self, session: Session, skip: int, limit: int) -> List[Auto]:
        statement = select(Auto).offset(skip).limit(limit)
        return session.exec(statement).all()

    def update(self, session: Session, auto_id: int, auto_update: AutoUpdate) -> Optional[Auto]:
        db_auto = session.get(Auto, auto_id)
        if not db_auto:
            return None
        auto_data = auto_update.dict(exclude_unset=True)
        for key, value in auto_data.items():
            setattr(db_auto, key, value)
        session.add(db_auto)
        session.commit()
        session.refresh(db_auto)
        return db_auto

    def delete(self, session: Session, auto_id: int) -> bool:
        db_auto = session.get(Auto, auto_id)
        if not db_auto:
            return False
        session.delete(db_auto)
        session.commit()
        return True

    def get_by_chasis(self, session: Session, numero_chasis: str) -> Optional[Auto]:
        statement = select(Auto).where(Auto.numero_chasis == numero_chasis)
        return session.exec(statement).first()

class VentaRepository:
    def create(self, session: Session, venta: VentaCreate) -> Venta:
        db_venta = Venta.from_orm(venta)
        session.add(db_venta)
        session.commit()
        session.refresh(db_venta)
        return db_venta

    def get_by_id(self, session: Session, venta_id: int) -> Optional[Venta]:
        return session.get(Venta, venta_id)

    def get_all(self, session: Session, skip: int, limit: int) -> List[Venta]:
        statement = select(Venta).offset(skip).limit(limit)
        return session.exec(statement).all()

    def update(self, session: Session, venta_id: int, venta_update: VentaUpdate) -> Optional[Venta]:
        db_venta = session.get(Venta, venta_id)
        if not db_venta:
            return None
        venta_data = venta_update.dict(exclude_unset=True)
        for key, value in venta_data.items():
            setattr(db_venta, key, value)
        session.add(db_venta)
        session.commit()
        session.refresh(db_venta)
        return db_venta

    def delete(self, session: Session, venta_id: int) -> bool:
        db_venta = session.get(Venta, venta_id)
        if not db_venta:
            return False
        session.delete(db_venta)
        session.commit()
        return True

    def get_by_auto_id(self, session: Session, auto_id: int) -> List[Venta]:
        statement = select(Venta).where(Venta.auto_id == auto_id)
        return session.exec(statement).all()

    def get_by_comprador(self, session: Session, nombre: str) -> List[Venta]:
        statement = select(Venta).where(Venta.nombre_comprador.ilike(f"%{nombre}%"))
        return session.exec(statement).all()