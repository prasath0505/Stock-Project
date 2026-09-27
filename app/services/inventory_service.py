from sqlalchemy.orm import Session

from app.dao.inventory_dao import InventoryDAO
from app.dao.product_dao import ProductDAO
from app.dao.warehouse_dao import WarehouseDAO
from app.models.inventory import Inventory


class InventoryService:
    def __init__(self, db: Session):
        self.dao = InventoryDAO(db)
        self.product_dao = ProductDAO(db)
        self.warehouse_dao = WarehouseDAO(db)

    def list_inventory(self, skip: int = 0, limit: int = 100) -> list[Inventory]:
        return self.dao.get_all_with_details(skip=skip, limit=limit)

    def get_inventory(self, inventory_id: int) -> Inventory | None:
        return self.dao.get_by_id(inventory_id)

    def get_low_stock(self, skip: int = 0, limit: int = 100) -> list[Inventory]:
        return self.dao.get_low_stock(skip=skip, limit=limit)

    def set_inventory(
        self,
        product_id: int,
        warehouse_id: int,
        quantity: int,
        reorder_level: int = 10,
    ) -> Inventory:
        if not self.product_dao.get_by_id(product_id):
            raise ValueError(f"Product {product_id} not found")
        if not self.warehouse_dao.get_by_id(warehouse_id):
            raise ValueError(f"Warehouse {warehouse_id} not found")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        existing = self.dao.get_by_product_and_warehouse(product_id, warehouse_id)
        if existing:
            existing.quantity = quantity
            existing.reorder_level = reorder_level
            return self.dao.update(existing)

        return self.dao.create(
            Inventory(
                product_id=product_id,
                warehouse_id=warehouse_id,
                quantity=quantity,
                reorder_level=reorder_level,
            )
        )

    def adjust_quantity(self, product_id: int, warehouse_id: int, delta: int) -> Inventory:
        inventory = self.dao.get_by_product_and_warehouse(product_id, warehouse_id)
        if not inventory:
            raise ValueError(
                f"No inventory record for product {product_id} in warehouse {warehouse_id}"
            )
        new_quantity = inventory.quantity + delta
        if new_quantity < 0:
            raise ValueError("Insufficient stock")
        inventory.quantity = new_quantity
        return self.dao.update(inventory)
