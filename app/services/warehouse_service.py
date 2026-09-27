from sqlalchemy.orm import Session

from app.dao.warehouse_dao import WarehouseDAO
from app.models.warehouse import Warehouse


class WarehouseService:
    def __init__(self, db: Session):
        self.dao = WarehouseDAO(db)

    def list_warehouses(self, skip: int = 0, limit: int = 100) -> list[Warehouse]:
        return self.dao.get_all(skip=skip, limit=limit)

    def get_warehouse(self, warehouse_id: int) -> Warehouse | None:
        return self.dao.get_by_id(warehouse_id)

    def create_warehouse(
        self, name: str, location: str | None = None, description: str | None = None
    ) -> Warehouse:
        if self.dao.get_by_name(name):
            raise ValueError(f"Warehouse '{name}' already exists")
        return self.dao.create(Warehouse(name=name, location=location, description=description))

    def update_warehouse(
        self,
        warehouse_id: int,
        name: str | None = None,
        location: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> Warehouse:
        warehouse = self.dao.get_by_id(warehouse_id)
        if not warehouse:
            raise ValueError(f"Warehouse {warehouse_id} not found")
        if name is not None:
            existing = self.dao.get_by_name(name)
            if existing and existing.id != warehouse_id:
                raise ValueError(f"Warehouse '{name}' already exists")
            warehouse.name = name
        if location is not None:
            warehouse.location = location
        if description is not None:
            warehouse.description = description
        if is_active is not None:
            warehouse.is_active = is_active
        return self.dao.update(warehouse)

    def delete_warehouse(self, warehouse_id: int) -> None:
        warehouse = self.dao.get_by_id(warehouse_id)
        if not warehouse:
            raise ValueError(f"Warehouse {warehouse_id} not found")
        self.dao.delete(warehouse)
