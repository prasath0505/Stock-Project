from datetime import datetime
from decimal import Decimal
from enum import Enum

import strawberry


@strawberry.enum
class MovementTypeEnum(Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUSTMENT = "ADJUSTMENT"
    TRANSFER = "TRANSFER"


@strawberry.enum
class PurchaseOrderStatusEnum(Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    CANCELLED = "CANCELLED"


@strawberry.type
class CategoryType:
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime


@strawberry.type
class ProductType:
    id: int
    sku: str
    name: str
    description: str | None
    unit_price: Decimal
    category_id: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    category: CategoryType | None = None


@strawberry.type
class SupplierType:
    id: int
    name: str
    contact_name: str | None
    email: str | None
    phone: str | None
    address: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


@strawberry.type
class WarehouseType:
    id: int
    name: str
    location: str | None
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


@strawberry.type
class InventoryType:
    id: int
    product_id: int
    warehouse_id: int
    quantity: int
    reorder_level: int
    created_at: datetime
    updated_at: datetime
    product: ProductType | None = None
    warehouse: WarehouseType | None = None


@strawberry.type
class StockMovementType:
    id: int
    product_id: int
    warehouse_id: int
    movement_type: MovementTypeEnum
    quantity: int
    reference: str | None
    notes: str | None
    created_at: datetime
    product: ProductType | None = None
    warehouse: WarehouseType | None = None


@strawberry.type
class PurchaseOrderItemType:
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    received_quantity: int
    product: ProductType | None = None


@strawberry.type
class PurchaseOrderType:
    id: int
    order_number: str
    supplier_id: int
    status: PurchaseOrderStatusEnum
    total_amount: Decimal
    order_date: datetime
    expected_date: datetime | None
    created_at: datetime
    updated_at: datetime
    supplier: SupplierType | None = None
    items: list[PurchaseOrderItemType] = strawberry.field(default_factory=list)


def map_category(entity) -> CategoryType:
    return CategoryType(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def map_product(entity) -> ProductType:
    return ProductType(
        id=entity.id,
        sku=entity.sku,
        name=entity.name,
        description=entity.description,
        unit_price=entity.unit_price,
        category_id=entity.category_id,
        is_active=entity.is_active,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        category=map_category(entity.category) if entity.category else None,
    )


def map_supplier(entity) -> SupplierType:
    return SupplierType(
        id=entity.id,
        name=entity.name,
        contact_name=entity.contact_name,
        email=entity.email,
        phone=entity.phone,
        address=entity.address,
        is_active=entity.is_active,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def map_warehouse(entity) -> WarehouseType:
    return WarehouseType(
        id=entity.id,
        name=entity.name,
        location=entity.location,
        description=entity.description,
        is_active=entity.is_active,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def map_inventory(entity) -> InventoryType:
    return InventoryType(
        id=entity.id,
        product_id=entity.product_id,
        warehouse_id=entity.warehouse_id,
        quantity=entity.quantity,
        reorder_level=entity.reorder_level,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        product=map_product(entity.product) if entity.product else None,
        warehouse=map_warehouse(entity.warehouse) if entity.warehouse else None,
    )


def map_stock_movement(entity) -> StockMovementType:
    return StockMovementType(
        id=entity.id,
        product_id=entity.product_id,
        warehouse_id=entity.warehouse_id,
        movement_type=MovementTypeEnum(entity.movement_type.value),
        quantity=entity.quantity,
        reference=entity.reference,
        notes=entity.notes,
        created_at=entity.created_at,
        product=map_product(entity.product) if entity.product else None,
        warehouse=map_warehouse(entity.warehouse) if entity.warehouse else None,
    )


def map_purchase_order_item(entity) -> PurchaseOrderItemType:
    return PurchaseOrderItemType(
        id=entity.id,
        product_id=entity.product_id,
        quantity=entity.quantity,
        unit_price=entity.unit_price,
        received_quantity=entity.received_quantity,
        product=map_product(entity.product) if hasattr(entity, "product") and entity.product else None,
    )


def map_purchase_order(entity) -> PurchaseOrderType:
    return PurchaseOrderType(
        id=entity.id,
        order_number=entity.order_number,
        supplier_id=entity.supplier_id,
        status=PurchaseOrderStatusEnum(entity.status.value),
        total_amount=entity.total_amount,
        order_date=entity.order_date,
        expected_date=entity.expected_date,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        supplier=map_supplier(entity.supplier) if entity.supplier else None,
        items=[map_purchase_order_item(item) for item in entity.items],
    )
