from datetime import datetime
from decimal import Decimal

import strawberry

from app.graphql.types import MovementTypeEnum, PurchaseOrderStatusEnum


@strawberry.input
class CategoryInput:
    name: str
    description: str | None = None


@strawberry.input
class ProductInput:
    sku: str
    name: str
    unit_price: Decimal
    description: str | None = None
    category_id: int | None = None


@strawberry.input
class SupplierInput:
    name: str
    contact_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None


@strawberry.input
class WarehouseInput:
    name: str
    location: str | None = None
    description: str | None = None


@strawberry.input
class InventoryInput:
    product_id: int
    warehouse_id: int
    quantity: int
    reorder_level: int = 10


@strawberry.input
class StockMovementInput:
    product_id: int
    warehouse_id: int
    movement_type: MovementTypeEnum
    quantity: int
    reference: str | None = None
    notes: str | None = None


@strawberry.input
class TransferStockInput:
    product_id: int
    from_warehouse_id: int
    to_warehouse_id: int
    quantity: int
    reference: str | None = None
    notes: str | None = None


@strawberry.input
class PurchaseOrderItemInput:
    product_id: int
    quantity: int
    unit_price: Decimal | None = None


@strawberry.input
class PurchaseOrderInput:
    supplier_id: int
    items: list[PurchaseOrderItemInput]
    expected_date: datetime | None = None


@strawberry.input
class UpdateOrderStatusInput:
    order_id: int
    status: PurchaseOrderStatusEnum
