from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# Shared properties
class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    ingredients: List[str] = []


# Properties to receive on item creation
class RecipeCreate(RecipeBase):
    pass


# Properties to receive on item update
class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[str]] = None


# Properties to return to client
class Recipe(RecipeBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
