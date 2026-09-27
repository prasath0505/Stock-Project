from sqlalchemy.orm import Session, joinedload

from app.dao.base import BaseDAO
from app.models.purchase_order import PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus


class PurchaseOrderDAO(BaseDAO[PurchaseOrder]):
    def __init__(self, db: Session):
        super().__init__(db, PurchaseOrder)

    def get_by_order_number(self, order_number: str) -> PurchaseOrder | None:
        return self.db.query(PurchaseOrder).filter(PurchaseOrder.order_number == order_number).first()

    def get_all_with_details(self, skip: int = 0, limit: int = 100) -> list[PurchaseOrder]:
        return (
            self.db.query(PurchaseOrder)
            .options(
                joinedload(PurchaseOrder.supplier),
                joinedload(PurchaseOrder.items).joinedload(PurchaseOrderItem.product),
            )
            .order_by(PurchaseOrder.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id_with_details(self, order_id: int) -> PurchaseOrder | None:
        return (
            self.db.query(PurchaseOrder)
            .options(
                joinedload(PurchaseOrder.supplier),
                joinedload(PurchaseOrder.items).joinedload(PurchaseOrderItem.product),
            )
            .filter(PurchaseOrder.id == order_id)
            .first()
        )

    def get_by_status(
        self, status: PurchaseOrderStatus, skip: int = 0, limit: int = 100
    ) -> list[PurchaseOrder]:
        return (
            self.db.query(PurchaseOrder)
            .options(joinedload(PurchaseOrder.supplier))
            .filter(PurchaseOrder.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )


class PurchaseOrderItemDAO(BaseDAO[PurchaseOrderItem]):
    def __init__(self, db: Session):
        super().__init__(db, PurchaseOrderItem)
