from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.db import crud_recipe
from app.schemas.recipe import Recipe, RecipeCreate, RecipeUpdate
from app.db.session import get_db
from app.models.user import User

router = APIRouter()


# 1. GET /recipes - List all recipes
@router.get("/", response_model=List[Recipe])
def read_recipes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    keyword: Optional[str] = Query(
        None, min_length=3, description="Search recipe titles"
    ),
) -> Any:
    """
    Retrieve recipes with optional filtering and search.
    """
    recipes = crud_recipe.get_multi(
        db, skip=skip, limit=limit, owner_id=user_id, keyword=keyword
    )
    return recipes


# 2. POST /recipes - Create a new recipe
@router.post("/", response_model=Recipe, status_code=status.HTTP_201_CREATED)
def create_recipe(
    *,
    db: Session = Depends(get_db),
    recipe_in: RecipeCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new recipe.
    """
    recipe = crud_recipe.create(db=db, obj_in=recipe_in, owner_id=current_user.id)
    return recipe


# 3. GET /recipes/{id} - Get a specific recipe
@router.get("/{recipe_id}", response_model=Recipe)
def read_recipe(
    *,
    db: Session = Depends(get_db),
    recipe_id: int,
) -> Any:
    """
    Get recipe by ID.
    """
    recipe = crud_recipe.get(db=db, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


# 4. PATCH /recipes/{id} - Update a recipe
@router.patch("/{recipe_id}", response_model=Recipe)
def update_recipe(
    *,
    db: Session = Depends(get_db),
    recipe_id: int,
    recipe_in: RecipeUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a recipe.
    """
    recipe = crud_recipe.get(db=db, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # SECURITY CHECK: Only the owner can update [cite: 27]
    if recipe.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    recipe = crud_recipe.update(db=db, db_obj=recipe, obj_in=recipe_in)
    return recipe


# 5. DELETE /recipes/{id} - Delete a recipe
@router.delete("/{recipe_id}", response_model=Recipe)
def delete_recipe(
    *,
    db: Session = Depends(get_db),
    recipe_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a recipe.
    """
    recipe = crud_recipe.get(db=db, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # SECURITY CHECK: Only the owner can delete [cite: 27]
    if recipe.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    recipe = crud_recipe.remove(db=db, recipe_id=recipe_id)
    return recipe
