# CalCount

## Description
CalCount is a nutrition and meal management API service. It allows users to register, log in, and manage meal logs, ingredients, and nutritional information. The backend is built with FastAPI, SQLAlchemy, and Alembic for migrations, and integrates with LLMs for recipe instructions.

---

## Features
- User registration and authentication
- Meal logging and ingredient management
- Integration with USDA food data
- LLM-powered recipe instructions

---

## Alembic Database Migration Steps

Alembic is used for managing database schema migrations. Follow these steps to set up and update your database schema:

### 1. Initialize Alembic (only once, already done in this repo)
```bash
alembic init alembic
```

### 2. Configure Alembic
- Edit `alembic.ini` to set your database URL (or use environment variables).
- In `alembic/env.py`, ensure `target_metadata` is set to your models' metadata (e.g., `from models import Base; target_metadata = Base.metadata`).

### 3. Create a New Migration After Model Changes
```bash
alembic revision --autogenerate -m "Describe your change"
```
- This will generate a migration script in `alembic/versions/`.
- Review and edit the script if needed.

### 4. Apply Migrations to the Database
```bash
alembic upgrade head
```
- This will apply all pending migrations to your database.

### 5. Other Useful Alembic Commands
- **Downgrade last migration:**
  ```bash
  alembic downgrade -1
  ```
- **Downgrade to a specific revision:**
  ```bash
  alembic downgrade <revision_id>
  ```
- **Show current revision:**
  ```bash
  alembic current
  ```
- **Show all heads (branches):**
  ```bash
  alembic heads
  ```
- **Stamp the database with a specific revision (without running migrations):**
  ```bash
  alembic stamp head
  ```
- **Verbose output for troubleshooting:**
  ```bash
  alembic downgrade -1 --verbose
  ```

### Alembic Troubleshooting
- If downgrade does not work, check that your migration script's `downgrade()` function is implemented and not empty.
- If you see errors or unexpected behavior, check the output of the above commands and ensure your `alembic_version` table is in sync with your migration files.
- If you have multiple heads, resolve them using `alembic heads` and merge as needed.

---

## Usage

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/calcount.git
cd calcount
```

### 2. Install dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment
- Copy `.env.example` to `.env` and fill in the required values (database URL, API keys, etc).
- Edit `config/db/config.json` and `config/usda/config.json` as needed.

### 4. Run Database Migrations
```bash
alembic upgrade head
```

### 5. Start the Application
```bash
uvicorn app:app --reload
```

---

## Deployment

### Docker Compose
1. Build and start the services:
   ```bash
   docker-compose up --build
   ```
2. The API will be available at `http://localhost:8003` by default.

### Manual Deployment
- Ensure PostgreSQL is running and accessible.
- Set environment variables as needed.
- Run Alembic migrations and start the app as above.

---

## Development

- Use a virtual environment (`venv`) for Python dependencies.
- Code is organized into modules: `controllers/`, `services/`, `models/`, `dtos/`, etc.
- Use Alembic for database migrations.
- Lint code with `flake8` or your preferred linter.
- Run tests from the `tests/` directory:
  ```bash
  pytest
  ```

---

## API Example (cURL)

### Register a User
```bash
curl --location 'http://0.0.0.0:8003/user/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "reference_number": "7ce053af-0e2e-4ae4-93f7-4ce6f7d40086",
    "email": "test@gmail.com",
    "password": "test@123"
}'
```

### User Login
```bash
curl --location 'http://0.0.0.0:8003/user/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "reference_number": "ecc426e3-c81a-470e-808d-3e663d504fa6",
    "email": "test@gmail.com",
    "password": "test@123"
}'
```

### Search Meal
```bash
curl --location --request GET 'http://0.0.0.0:8003/api/v1/meal/search' \
--header 'Content-Type: application/json' \
--header 'Authorization: <token>' \
--data '{
    "reference_number": "7ce053af-0e2e-4ae4-93f7-4ce6f7d40086",
    "meal_name": "chicken biryani",
    "servings": 2,
    "get_instructions": false
}'
```

### Add a Meal
```bash
curl --location 'http://0.0.0.0:8003/api/v1/meal/add' \
--header 'Content-Type: application/json' \
--header 'Authorization: <token>' \
--data '{
    "reference_number": "7ce053af-0e2e-4ae4-93f7-4ce6f7d40086",
    "meal_name": "chicken biryani",
    "servings": 2,
    "get_instructions": false
}'
```

---

## Contributing
- Fork the repo and create a feature branch.
- Submit a pull request with a clear description of your changes.

---

## License
MIT License
