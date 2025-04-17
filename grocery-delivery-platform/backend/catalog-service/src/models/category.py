from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl
from .product import PydanticObjectId


class Category(BaseModel):
    id: PydanticObjectId = Field(default_factory=lambda: str(PydanticObjectId()))
    store_id: PydanticObjectId
    name: str
    description: Optional[str] = None
    slug: str
    parent_id: Optional[PydanticObjectId] = None
    image_url: Optional[HttpUrl] = None
    is_active: bool = True
    display_order: int = 0
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            PydanticObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }

    def update_timestamps(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()


class CategoryTree(Category):
    children: List['CategoryTree'] = []
    product_count: int = 0

    def add_child(self, child: 'CategoryTree'):
        """Add a child category to this category"""
        self.children.append(child)

    def get_all_child_ids(self) -> List[PydanticObjectId]:
        """Get all child category IDs recursively"""
        ids = [self.id]
        for child in self.children:
            ids.extend(child.get_all_child_ids())
        return ids

    def get_breadcrumb(self, categories: dict[PydanticObjectId, 'CategoryTree']) -> List[str]:
        """Get category breadcrumb path"""
        breadcrumb = [self.name]
        current = self
        while current.parent_id and current.parent_id in categories:
            current = categories[current.parent_id]
            breadcrumb.insert(0, current.name)
        return breadcrumb

    def to_dict(self) -> dict:
        """Convert category tree to dictionary"""
        return {
            **super().dict(),
            'children': [child.to_dict() for child in self.children],
            'product_count': self.product_count
        } 