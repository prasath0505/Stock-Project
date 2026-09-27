from datetime import datetime

import strawberry
from sqlalchemy.orm import Session
from strawberry.types import Info

from app.database import get_db
from app.graphql.inputs import (
    CategoryInput,
    InventoryInput,
    ProductInput,
    PurchaseOrderInput,
    StockMovementInput,
    SupplierInput,
    TransferStockInput,
    UpdateOrderStatusInput,
    WarehouseInput,
)
from app.graphql.types import (
    CategoryType,
    InventoryType,
    MovementTypeEnum,
    ProductType,
    PurchaseOrderStatusEnum,
    PurchaseOrderType,
    StockMovementType,
    SupplierType,
    WarehouseType,
    map_category,
    map_inventory,
    map_product,
    map_purchase_order,
    map_stock_movement,
    map_supplier,
    map_warehouse,
)
from app.models.purchase_order import PurchaseOrderStatus
from app.models.stock_movement import MovementType
from app.services.category_service import CategoryService
from app.services.inventory_service import InventoryService
from app.services.product_service import ProductService
from app.services.purchase_order_service import PurchaseOrderService
from app.services.stock_movement_service import StockMovementService
from app.services.supplier_service import SupplierService
from app.services.warehouse_service import WarehouseService


def get_session(info: Info) -> Session:
    return info.context["db"]


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "Stock Management API is running"

    @strawberry.field
    def categories(self, info: Info, skip: int = 0, limit: int = 100) -> list[CategoryType]:
        service = CategoryService(get_session(info))
        return [map_category(c) for c in service.list_categories(skip=skip, limit=limit)]

    @strawberry.field
    def category(self, info: Info, id: int) -> CategoryType | None:
        service = CategoryService(get_session(info))
        entity = service.get_category(id)
        return map_category(entity) if entity else None

    @strawberry.field
    def products(self, info: Info, skip: int = 0, limit: int = 100) -> list[ProductType]:
        service = ProductService(get_session(info))
        return [map_product(p) for p in service.list_products(skip=skip, limit=limit)]

    @strawberry.field
    def product(self, info: Info, id: int) -> ProductType | None:
        service = ProductService(get_session(info))
        entity = service.get_product(id)
        return map_product(entity) if entity else None

    @strawberry.field
    def search_products(self, info: Info, query: str, skip: int = 0, limit: int = 100) -> list[ProductType]:
        service = ProductService(get_session(info))
        return [map_product(p) for p in service.search_products(query, skip=skip, limit=limit)]

    @strawberry.field
    def suppliers(self, info: Info, skip: int = 0, limit: int = 100, active_only: bool = False) -> list[SupplierType]:
        service = SupplierService(get_session(info))
        return [map_supplier(s) for s in service.list_suppliers(skip=skip, limit=limit, active_only=active_only)]

    @strawberry.field
    def supplier(self, info: Info, id: int) -> SupplierType | None:
        service = SupplierService(get_session(info))
        entity = service.get_supplier(id)
        return map_supplier(entity) if entity else None

    @strawberry.field
    def warehouses(self, info: Info, skip: int = 0, limit: int = 100) -> list[WarehouseType]:
        service = WarehouseService(get_session(info))
        return [map_warehouse(w) for w in service.list_warehouses(skip=skip, limit=limit)]

    @strawberry.field
    def warehouse(self, info: Info, id: int) -> WarehouseType | None:
        service = WarehouseService(get_session(info))
        entity = service.get_warehouse(id)
        return map_warehouse(entity) if entity else None

    @strawberry.field
    def inventory(self, info: Info, skip: int = 0, limit: int = 100) -> list[InventoryType]:
        service = InventoryService(get_session(info))
        return [map_inventory(i) for i in service.list_inventory(skip=skip, limit=limit)]

    @strawberry.field
    def low_stock(self, info: Info, skip: int = 0, limit: int = 100) -> list[InventoryType]:
        service = InventoryService(get_session(info))
        return [map_inventory(i) for i in service.get_low_stock(skip=skip, limit=limit)]

    @strawberry.field
    def stock_movements(self, info: Info, skip: int = 0, limit: int = 100) -> list[StockMovementType]:
        service = StockMovementService(get_session(info))
        return [map_stock_movement(m) for m in service.list_movements(skip=skip, limit=limit)]

    @strawberry.field
    def product_movements(
        self, info: Info, product_id: int, skip: int = 0, limit: int = 100
    ) -> list[StockMovementType]:
        service = StockMovementService(get_session(info))
        return [map_stock_movement(m) for m in service.get_movements_by_product(product_id, skip=skip, limit=limit)]

    @strawberry.field
    def purchase_orders(self, info: Info, skip: int = 0, limit: int = 100) -> list[PurchaseOrderType]:
        service = PurchaseOrderService(get_session(info))
        return [map_purchase_order(o) for o in service.list_orders(skip=skip, limit=limit)]

    @strawberry.field
    def purchase_order(self, info: Info, id: int) -> PurchaseOrderType | None:
        service = PurchaseOrderService(get_session(info))
        entity = service.get_order(id)
        return map_purchase_order(entity) if entity else None

    @strawberry.field
    def purchase_orders_by_status(
        self, info: Info, status: PurchaseOrderStatusEnum, skip: int = 0, limit: int = 100
    ) -> list[PurchaseOrderType]:
        service = PurchaseOrderService(get_session(info))
        orders = service.get_orders_by_status(PurchaseOrderStatus(status.value), skip=skip, limit=limit)
        return [map_purchase_order(o) for o in orders]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_category(self, info: Info, input: CategoryInput) -> CategoryType:
        service = CategoryService(get_session(info))
        return map_category(service.create_category(input.name, input.description))

    @strawberry.mutation
    def create_product(self, info: Info, input: ProductInput) -> ProductType:
        service = ProductService(get_session(info))
        entity = service.create_product(
            sku=input.sku,
            name=input.name,
            unit_price=input.unit_price,
            description=input.description,
            category_id=input.category_id,
        )
        return map_product(entity)

    @strawberry.mutation
    def create_supplier(self, info: Info, input: SupplierInput) -> SupplierType:
        service = SupplierService(get_session(info))
        entity = service.create_supplier(
            name=input.name,
            contact_name=input.contact_name,
            email=input.email,
            phone=input.phone,
            address=input.address,
        )
        return map_supplier(entity)

    @strawberry.mutation
    def create_warehouse(self, info: Info, input: WarehouseInput) -> WarehouseType:
        service = WarehouseService(get_session(info))
        entity = service.create_warehouse(input.name, input.location, input.description)
        return map_warehouse(entity)

    @strawberry.mutation
    def set_inventory(self, info: Info, input: InventoryInput) -> InventoryType:
        service = InventoryService(get_session(info))
        entity = service.set_inventory(
            product_id=input.product_id,
            warehouse_id=input.warehouse_id,
            quantity=input.quantity,
            reorder_level=input.reorder_level,
        )
        return map_inventory(entity)

    @strawberry.mutation
    def record_stock_movement(self, info: Info, input: StockMovementInput) -> StockMovementType:
        service = StockMovementService(get_session(info))
        entity = service.record_movement(
            product_id=input.product_id,
            warehouse_id=input.warehouse_id,
            movement_type=MovementType(input.movement_type.value),
            quantity=input.quantity,
            reference=input.reference,
            notes=input.notes,
        )
        return map_stock_movement(entity)

    @strawberry.mutation
    def transfer_stock(self, info: Info, input: TransferStockInput) -> list[StockMovementType]:
        service = StockMovementService(get_session(info))
        movements = service.transfer_stock(
            product_id=input.product_id,
            from_warehouse_id=input.from_warehouse_id,
            to_warehouse_id=input.to_warehouse_id,
            quantity=input.quantity,
            reference=input.reference,
            notes=input.notes,
        )
        return [map_stock_movement(m) for m in movements]

    @strawberry.mutation
    def create_purchase_order(self, info: Info, input: PurchaseOrderInput) -> PurchaseOrderType:
        service = PurchaseOrderService(get_session(info))
        items = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
            }
            for item in input.items
        ]
        entity = service.create_order(
            supplier_id=input.supplier_id,
            items=items,
            expected_date=input.expected_date,
        )
        return map_purchase_order(entity)

    @strawberry.mutation
    def update_purchase_order_status(self, info: Info, input: UpdateOrderStatusInput) -> PurchaseOrderType:
        service = PurchaseOrderService(get_session(info))
        entity = service.update_status(input.order_id, PurchaseOrderStatus(input.status.value))
        return map_purchase_order(entity)

    @strawberry.mutation
    def receive_purchase_order(self, info: Info, order_id: int, warehouse_id: int) -> PurchaseOrderType:
        service = PurchaseOrderService(get_session(info))
        entity = service.receive_order(order_id, warehouse_id)
        return map_purchase_order(entity)


schema = strawberry.Schema(query=Query, mutation=Mutation)


async def get_graphql_context():
    db = next(get_db())
    try:
        yield {"db": db}
    finally:
        db.close()
