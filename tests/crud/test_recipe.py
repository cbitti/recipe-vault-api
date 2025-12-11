from sqlalchemy.orm import Session
from app.db import crud_recipe
from app.schemas.recipe import RecipeCreate


def test_create_recipe(db: Session):
    title = "Unit Test Curry"
    description = "Spicy"
    ingredients = ["chili", "rice"]
    owner_id = 1

    recipe_in = RecipeCreate(
        title=title, description=description, ingredients=ingredients
    )
    recipe = crud_recipe.create(db, obj_in=recipe_in, owner_id=owner_id)

    assert recipe.title == title
    assert recipe.owner_id == owner_id


def test_search_recipe(db: Session):
    # Setup: Create 2 recipes
    r1 = RecipeCreate(title="Apple Pie", ingredients=[])
    r2 = RecipeCreate(title="Banana Bread", ingredients=[])
    crud_recipe.create(db, r1, owner_id=1)
    crud_recipe.create(db, r2, owner_id=1)

    # Test: Search for "Apple"
    results = crud_recipe.get_multi(db, keyword="Apple")
    assert len(results) == 1
    assert results[0].title == "Apple Pie"

    # Test: Search for "Pie" (Partial match)
    results = crud_recipe.get_multi(db, keyword="pie")
    assert len(results) == 1
