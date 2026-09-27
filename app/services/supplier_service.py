from sqlalchemy.orm import Session

from app.dao.supplier_dao import SupplierDAO
from app.models.supplier import Supplier


class SupplierService:
    def __init__(self, db: Session):
        self.dao = SupplierDAO(db)

    def list_suppliers(self, skip: int = 0, limit: int = 100, active_only: bool = False) -> list[Supplier]:
        if active_only:
            return self.dao.get_active(skip=skip, limit=limit)
        return self.dao.get_all(skip=skip, limit=limit)

    def get_supplier(self, supplier_id: int) -> Supplier | None:
        return self.dao.get_by_id(supplier_id)

    def create_supplier(
        self,
        name: str,
        contact_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        address: str | None = None,
    ) -> Supplier:
        return self.dao.create(
            Supplier(
                name=name,
                contact_name=contact_name,
                email=email,
                phone=phone,
                address=address,
            )
        )

    def update_supplier(
        self,
        supplier_id: int,
        name: str | None = None,
        contact_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        is_active: bool | None = None,
    ) -> Supplier:
        supplier = self.dao.get_by_id(supplier_id)
        if not supplier:
            raise ValueError(f"Supplier {supplier_id} not found")
        if name is not None:
            supplier.name = name
        if contact_name is not None:
            supplier.contact_name = contact_name
        if email is not None:
            supplier.email = email
        if phone is not None:
            supplier.phone = phone
        if address is not None:
            supplier.address = address
        if is_active is not None:
            supplier.is_active = is_active
        return self.dao.update(supplier)

    def delete_supplier(self, supplier_id: int) -> None:
        supplier = self.dao.get_by_id(supplier_id)
        if not supplier:
            raise ValueError(f"Supplier {supplier_id} not found")
        self.dao.delete(supplier)
