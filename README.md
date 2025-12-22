# RecipeVault API 🍳

![CI/CD](https://github.com/cbitti/recipe-vault-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

RecipeVault is a production-grade backend API for managing user-generated recipes. It demonstrates a modern, scalable architecture using **FastAPI**, **PostgreSQL**, and **Docker**, featuring a complete CI/CD pipeline and comprehensive test coverage.

## 🚀 Key Features

* **RESTful Architecture:** Clean, resource-oriented endpoints following the Service-Repository pattern.
* **Secure Authentication:** OAuth2 compliant login flow with **PyJWT** (access tokens) and **Argon2** (password hashing).
* **Advanced Search:** Filtering recipes by owner and keyword search using SQLAlchemy dynamic queries.
* **Robust Validation:** Data integrity ensured by **Pydantic V2** schemas.
* **Containerized Deployment:** Fully Dockerized application ensuring consistent runtime environments.
* **CI/CD Pipeline:** Automated testing, linting, and Docker publishing via **GitHub Actions**.

---

## 🛠 Tech Stack

| Category | Technology | Reasoning |
|----------|------------|-----------|
| **Framework** | FastAPI | High performance, automatic Swagger docs, async support. |
| **Database** | PostgreSQL | Robust relational data integrity and complex querying. |
| **ORM** | SQLAlchemy | Type-safe database interactions and migration support. |
| **Auth** | PyJWT + Pwdlib | Industry standard JWT handling and Argon2id hashing. |
| **Testing** | Pytest | Fixture-based testing for both Unit and Integration suites. |
| **Infrastructure** | Docker | Consistent runtime environment from dev to prod. |

---

## 📂 Project Structure

The project follows a domain-driven structure to separate concerns:

```text
app/
├── api/             # Route handlers (Controllers)
│   ├── deps.py      # Dependency injection (Current User, DB Session)
│   └── v1/          # API Version 1 endpoints
├── core/            # Global configs and security utilities
├── db/              # Database connection and CRUD operations
├── models/          # SQLAlchemy Database Models
└── schemas/         # Pydantic Data Schemas (Input/Output)
tests/
├── api/             # Integration tests (End-to-End workflows)
├── crud/            # Database logic tests
└── unit/            # Isolated logic tests (Hashing, Utils)
