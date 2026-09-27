from sqlalchemy.orm import Session

from app.dao.base import BaseDAO
from app.models.category import Category


class CategoryDAO(BaseDAO[Category]):
    def __init__(self, db: Session):
        super().__init__(db, Category)

    def get_by_name(self, name: str) -> Category | None:
        return self.db.query(Category).filter(Category.name == name).first()
