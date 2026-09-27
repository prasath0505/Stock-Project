from sqlalchemy.orm import Session

from app.dao.base import BaseDAO
from app.models.warehouse import Warehouse


class WarehouseDAO(BaseDAO[Warehouse]):
    def __init__(self, db: Session):
        super().__init__(db, Warehouse)

    def get_by_name(self, name: str) -> Warehouse | None:
        return self.db.query(Warehouse).filter(Warehouse.name == name).first()
