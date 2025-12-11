from typing import Any, Annotated
from fastapi import APIRouter, Depends
from app.schemas.user import User
from app.models.user import User as UserModel
from app.api import deps

router = APIRouter()


@router.get("/me", response_model=User)
def read_users_me(
    current_user: Annotated[UserModel, Depends(deps.get_current_user)],
) -> Any:
    """
    Get current user.
    """
    return current_user
