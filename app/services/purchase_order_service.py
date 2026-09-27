from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from app.dao.product_dao import ProductDAO
from app.dao.purchase_order_dao import PurchaseOrderDAO, PurchaseOrderItemDAO
from app.dao.supplier_dao import SupplierDAO
from app.models.purchase_order import PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus
from app.models.stock_movement import MovementType
from app.services.stock_movement_service import StockMovementService


class PurchaseOrderService:
    def __init__(self, db: Session):
        self.dao = PurchaseOrderDAO(db)
        self.item_dao = PurchaseOrderItemDAO(db)
        self.supplier_dao = SupplierDAO(db)
        self.product_dao = ProductDAO(db)
        self.stock_movement_service = StockMovementService(db)

    def list_orders(self, skip: int = 0, limit: int = 100) -> list[PurchaseOrder]:
        return self.dao.get_all_with_details(skip=skip, limit=limit)

    def get_order(self, order_id: int) -> PurchaseOrder | None:
        return self.dao.get_by_id_with_details(order_id)

    def get_orders_by_status(
        self, status: PurchaseOrderStatus, skip: int = 0, limit: int = 100
    ) -> list[PurchaseOrder]:
        return self.dao.get_by_status(status, skip=skip, limit=limit)

    def _generate_order_number(self) -> str:
        return f"PO-{uuid4().hex[:8].upper()}"

    def create_order(
        self,
        supplier_id: int,
        items: list[dict],
        expected_date: datetime | None = None,
    ) -> PurchaseOrder:
        if not self.supplier_dao.get_by_id(supplier_id):
            raise ValueError(f"Supplier {supplier_id} not found")
        if not items:
            raise ValueError("Purchase order must have at least one item")

        order = PurchaseOrder(
            order_number=self._generate_order_number(),
            supplier_id=supplier_id,
            status=PurchaseOrderStatus.DRAFT,
            expected_date=expected_date,
        )
        total = Decimal("0")

        for item in items:
            product = self.product_dao.get_by_id(item["product_id"])
            if not product:
                raise ValueError(f"Product {item['product_id']} not found")
            quantity = item["quantity"]
            unit_price = Decimal(str(item.get("unit_price", product.unit_price)))
            if quantity <= 0:
                raise ValueError("Item quantity must be positive")
            total += unit_price * quantity
            order.items.append(
                PurchaseOrderItem(
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                )
            )

        order.total_amount = total
        return self.dao.create(order)

    def update_status(self, order_id: int, status: PurchaseOrderStatus) -> PurchaseOrder:
        order = self.dao.get_by_id(order_id)
        if not order:
            raise ValueError(f"Purchase order {order_id} not found")
        order.status = status
        return self.dao.update(order)

    def receive_order(self, order_id: int, warehouse_id: int) -> PurchaseOrder:
        order = self.dao.get_by_id_with_details(order_id)
        if not order:
            raise ValueError(f"Purchase order {order_id} not found")
        if order.status == PurchaseOrderStatus.CANCELLED:
            raise ValueError("Cannot receive a cancelled order")
        if order.status == PurchaseOrderStatus.RECEIVED:
            raise ValueError("Order already received")

        for item in order.items:
            remaining = item.quantity - item.received_quantity
            if remaining <= 0:
                continue
            self.stock_movement_service.record_movement(
                product_id=item.product_id,
                warehouse_id=warehouse_id,
                movement_type=MovementType.IN,
                quantity=remaining,
                reference=order.order_number,
                notes="Purchase order receipt",
            )
            item.received_quantity = item.quantity

        order.status = PurchaseOrderStatus.RECEIVED
        return self.dao.update(order)
