from sqlalchemy.orm import Session

from app.dao.base import BaseDAO
from app.models.supplier import Supplier


class SupplierDAO(BaseDAO[Supplier]):
    def __init__(self, db: Session):
        super().__init__(db, Supplier)

    def get_active(self, skip: int = 0, limit: int = 100) -> list[Supplier]:
        return (
            self.db.query(Supplier)
            .filter(Supplier.is_active.is_(True))
            .offset(skip)
            .limit(limit)
            .all()
        )
