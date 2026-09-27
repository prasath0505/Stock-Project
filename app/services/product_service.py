from decimal import Decimal

from sqlalchemy.orm import Session

from app.dao.product_dao import ProductDAO
from app.models.product import Product


class ProductService:
    def __init__(self, db: Session):
        self.dao = ProductDAO(db)

    def list_products(self, skip: int = 0, limit: int = 100) -> list[Product]:
        return self.dao.get_all_with_category(skip=skip, limit=limit)

    def get_product(self, product_id: int) -> Product | None:
        return self.dao.get_by_id_with_category(product_id)

    def search_products(self, query: str, skip: int = 0, limit: int = 100) -> list[Product]:
        return self.dao.search(query, skip=skip, limit=limit)

    def create_product(
        self,
        sku: str,
        name: str,
        unit_price: Decimal,
        description: str | None = None,
        category_id: int | None = None,
    ) -> Product:
        if self.dao.get_by_sku(sku):
            raise ValueError(f"Product with SKU '{sku}' already exists")
        return self.dao.create(
            Product(
                sku=sku,
                name=name,
                description=description,
                unit_price=unit_price,
                category_id=category_id,
            )
        )

    def update_product(
        self,
        product_id: int,
        name: str | None = None,
        description: str | None = None,
        unit_price: Decimal | None = None,
        category_id: int | None = None,
        is_active: bool | None = None,
    ) -> Product:
        product = self.dao.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if unit_price is not None:
            product.unit_price = unit_price
        if category_id is not None:
            product.category_id = category_id
        if is_active is not None:
            product.is_active = is_active
        return self.dao.update(product)

    def delete_product(self, product_id: int) -> None:
        product = self.dao.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        self.dao.delete(product)
