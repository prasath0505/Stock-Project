from sqlalchemy.orm import Session, joinedload

from app.dao.base import BaseDAO
from app.models.product import Product


class ProductDAO(BaseDAO[Product]):
    def __init__(self, db: Session):
        super().__init__(db, Product)

    def get_by_sku(self, sku: str) -> Product | None:
        return self.db.query(Product).filter(Product.sku == sku).first()

    def get_all_with_category(self, skip: int = 0, limit: int = 100) -> list[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id_with_category(self, product_id: int) -> Product | None:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id == product_id)
            .first()
        )

    def search(self, query: str, skip: int = 0, limit: int = 100) -> list[Product]:
        pattern = f"%{query}%"
        return (
            self.db.query(Product)
            .filter((Product.name.ilike(pattern)) | (Product.sku.ilike(pattern)))
            .offset(skip)
            .limit(limit)
            .all()
        )
