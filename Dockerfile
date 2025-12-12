# 1. Base Image: Use a lightweight Python version
FROM python:3.10-slim

# 2. Environment Variables
# PYTHONDONTWRITEBYTECODE=1: Prevents Python from writing .pyc files
# PYTHONUNBUFFERED=1: Ensures logs are flushed immediately (easier debugging)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set Working Directory
WORKDIR /app

# 4. Install System Dependencies
# 'build-essential' is often needed to compile Python packages (like Argon2/cffi)
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Poetry
RUN pip install --no-cache-dir poetry

# 6. Install Dependencies (Leveraging Docker Cache)
# We copy ONLY the requirements files first. Docker checks if these changed.
# If not, it skips the 'poetry install' step and uses the cached layer.
COPY pyproject.toml poetry.lock ./

# --no-root: Don't install the project package itself yet (we copy code later)
# --no-dev: Don't install testing/linting tools (keeps image small)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --without dev

# 7. Copy Application Code
COPY . .

# 8. Expose the port (Documentation only, technically)
EXPOSE 8000

# 9. Run the Application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
