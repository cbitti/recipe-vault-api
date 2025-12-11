from fastapi import FastAPI
from app.api.v1.endpoints import auth, users

app = FastAPI(title="RecipeVault API")

# 1. Mount Auth Router -> /api/v1/auth
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

# 2. Mount Users Router -> /api/v1/users
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
