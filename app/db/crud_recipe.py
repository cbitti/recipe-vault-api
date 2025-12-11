from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate
from typing import Optional


def get(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


def get_multi(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[int] = None,
    keyword: Optional[str] = None,
):
    query = db.query(Recipe)

    # 1. Filter by Owner if provided
    if owner_id:
        query = query.filter(Recipe.owner_id == owner_id)

    # 2. Filter by Keyword if provided (Case-insensitive partial match)
    if keyword:
        query = query.filter(Recipe.title.ilike(f"%{keyword}%"))

    return query.offset(skip).limit(limit).all()


def create(db: Session, obj_in: RecipeCreate, owner_id: int):
    # Convert Pydantic model to DB model
    db_obj = Recipe(**obj_in.model_dump(), owner_id=owner_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Recipe, obj_in: RecipeUpdate):
    # 1. Convert update data to dict, excluding unset values
    update_data = obj_in.model_dump(exclude_unset=True)

    # 2. Update the DB object attributes
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, recipe_id: int):
    obj = db.query(Recipe).get(recipe_id)
    db.delete(obj)
    db.commit()
    return obj
