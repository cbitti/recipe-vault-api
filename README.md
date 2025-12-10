# RecipeVault API 🍳

RecipeVault is a robust backend API for managing user-generated recipes. Built with modern Python best practices, it demonstrates a production-ready architecture using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.

## 🚀 Key Features

* **RESTful Architecture:** Clean, resource-oriented endpoints (GET, POST, PATCH, DELETE).
* **Secure Authentication:** User management with JWT (JSON Web Tokens) and secure password hashing.
* **Relational Data Modeling:** One-to-Many relationships between Users and Recipes using SQLAlchemy.
* **Robust Validation:** Data integrity ensured by Pydantic schemas (for API) and database constraints.
* **Professional Tooling:** Fully integrated with Poetry for dependency management and pre-commit hooks for code quality.

## 🛠 Tech Stack

* **Framework:** FastAPI
* **Language:** Python 3.10+
* **Database:** PostgreSQL (with `psycopg2` driver)
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **Authentication:** PyJWT + Passlib (bcrypt)
* **Testing:** Pytest

## ⚡ Quick Start

### Prerequisites
* Python 3.10 or higher
* PostgreSQL installed and running locally
* [Poetry](https://python-poetry.org/) for dependency management

### 1. Clone the Repository
```bash
git clone [https://github.com/cbitti/recipe-vault-api.git](https://github.com/cbitti/recipe-vault-api.git)
cd recipe-vault-api
