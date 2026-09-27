from sqlalchemy.orm import Session, joinedload

from app.dao.base import BaseDAO
from app.models.inventory import Inventory


class InventoryDAO(BaseDAO[Inventory]):
    def __init__(self, db: Session):
        super().__init__(db, Inventory)

    def get_by_product_and_warehouse(self, product_id: int, warehouse_id: int) -> Inventory | None:
        return (
            self.db.query(Inventory)
            .filter(Inventory.product_id == product_id, Inventory.warehouse_id == warehouse_id)
            .first()
        )

    def get_all_with_details(self, skip: int = 0, limit: int = 100) -> list[Inventory]:
        return (
            self.db.query(Inventory)
            .options(joinedload(Inventory.product), joinedload(Inventory.warehouse))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_low_stock(self, skip: int = 0, limit: int = 100) -> list[Inventory]:
        return (
            self.db.query(Inventory)
            .options(joinedload(Inventory.product), joinedload(Inventory.warehouse))
            .filter(Inventory.quantity <= Inventory.reorder_level)
            .offset(skip)
            .limit(limit)
            .all()
        )
