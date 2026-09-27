from sqlalchemy.orm import Session, joinedload

from app.dao.base import BaseDAO
from app.models.stock_movement import StockMovement


class StockMovementDAO(BaseDAO[StockMovement]):
    def __init__(self, db: Session):
        super().__init__(db, StockMovement)

    def get_by_product(self, product_id: int, skip: int = 0, limit: int = 100) -> list[StockMovement]:
        return (
            self.db.query(StockMovement)
            .options(joinedload(StockMovement.product), joinedload(StockMovement.warehouse))
            .filter(StockMovement.product_id == product_id)
            .order_by(StockMovement.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_with_details(self, skip: int = 0, limit: int = 100) -> list[StockMovement]:
        return (
            self.db.query(StockMovement)
            .options(joinedload(StockMovement.product), joinedload(StockMovement.warehouse))
            .order_by(StockMovement.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
