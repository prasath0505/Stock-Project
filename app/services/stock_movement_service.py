from sqlalchemy.orm import Session

from app.dao.inventory_dao import InventoryDAO
from app.dao.product_dao import ProductDAO
from app.dao.stock_movement_dao import StockMovementDAO
from app.dao.warehouse_dao import WarehouseDAO
from app.models.stock_movement import MovementType, StockMovement
from app.services.inventory_service import InventoryService


class StockMovementService:
    def __init__(self, db: Session):
        self.dao = StockMovementDAO(db)
        self.product_dao = ProductDAO(db)
        self.warehouse_dao = WarehouseDAO(db)
        self.inventory_dao = InventoryDAO(db)
        self.inventory_service = InventoryService(db)

    def list_movements(self, skip: int = 0, limit: int = 100) -> list[StockMovement]:
        return self.dao.get_all_with_details(skip=skip, limit=limit)

    def get_movements_by_product(self, product_id: int, skip: int = 0, limit: int = 100) -> list[StockMovement]:
        return self.dao.get_by_product(product_id, skip=skip, limit=limit)

    def record_movement(
        self,
        product_id: int,
        warehouse_id: int,
        movement_type: MovementType,
        quantity: int,
        reference: str | None = None,
        notes: str | None = None,
    ) -> StockMovement:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if not self.product_dao.get_by_id(product_id):
            raise ValueError(f"Product {product_id} not found")
        if not self.warehouse_dao.get_by_id(warehouse_id):
            raise ValueError(f"Warehouse {warehouse_id} not found")

        inventory = self.inventory_dao.get_by_product_and_warehouse(product_id, warehouse_id)
        if not inventory:
            inventory = self.inventory_service.set_inventory(product_id, warehouse_id, 0)

        if movement_type == MovementType.IN:
            inventory.quantity += quantity
        elif movement_type == MovementType.OUT:
            if inventory.quantity < quantity:
                raise ValueError("Insufficient stock for outbound movement")
            inventory.quantity -= quantity
        elif movement_type == MovementType.ADJUSTMENT:
            inventory.quantity = quantity
        elif movement_type == MovementType.TRANSFER:
            raise ValueError("Use transfer_stock for TRANSFER movements")

        self.inventory_dao.update(inventory)

        return self.dao.create(
            StockMovement(
                product_id=product_id,
                warehouse_id=warehouse_id,
                movement_type=movement_type,
                quantity=quantity,
                reference=reference,
                notes=notes,
            )
        )

    def transfer_stock(
        self,
        product_id: int,
        from_warehouse_id: int,
        to_warehouse_id: int,
        quantity: int,
        reference: str | None = None,
        notes: str | None = None,
    ) -> list[StockMovement]:
        if from_warehouse_id == to_warehouse_id:
            raise ValueError("Source and destination warehouses must differ")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        out_movement = self.record_movement(
            product_id=product_id,
            warehouse_id=from_warehouse_id,
            movement_type=MovementType.OUT,
            quantity=quantity,
            reference=reference,
            notes=f"Transfer out: {notes or ''}".strip(),
        )
        in_movement = self.record_movement(
            product_id=product_id,
            warehouse_id=to_warehouse_id,
            movement_type=MovementType.IN,
            quantity=quantity,
            reference=reference,
            notes=f"Transfer in: {notes or ''}".strip(),
        )
        return [out_movement, in_movement]
