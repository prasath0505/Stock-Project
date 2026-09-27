from sqlalchemy.orm import Session

from app.dao.category_dao import CategoryDAO
from app.models.category import Category


class CategoryService:
    def __init__(self, db: Session):
        self.dao = CategoryDAO(db)

    def list_categories(self, skip: int = 0, limit: int = 100) -> list[Category]:
        return self.dao.get_all(skip=skip, limit=limit)

    def get_category(self, category_id: int) -> Category | None:
        return self.dao.get_by_id(category_id)

    def create_category(self, name: str, description: str | None = None) -> Category:
        if self.dao.get_by_name(name):
            raise ValueError(f"Category '{name}' already exists")
        return self.dao.create(Category(name=name, description=description))

    def update_category(
        self, category_id: int, name: str | None = None, description: str | None = None
    ) -> Category:
        category = self.dao.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category {category_id} not found")
        if name is not None:
            existing = self.dao.get_by_name(name)
            if existing and existing.id != category_id:
                raise ValueError(f"Category '{name}' already exists")
            category.name = name
        if description is not None:
            category.description = description
        return self.dao.update(category)

    def delete_category(self, category_id: int) -> None:
        category = self.dao.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category {category_id} not found")
        self.dao.delete(category)
