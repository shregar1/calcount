# CalCount

---

## Description
CalCount is a nutrition and meal management API service. It allows users to register, log in, and manage meal logs, ingredients, and nutritional information. The backend is built with FastAPI, SQLAlchemy, and Alembic for migrations, and integrates with LLMs for recipe instructions.

---

## Features
- User registration and authentication
- Meal logging and ingredient management
- Integration with USDA food data
- LLM-powered recipe instructions

---

## Project Structure

```
calcount/
├── abstractions/         # Abstract base classes and interfaces for controllers, services, repositories, and utilities. Promotes code reuse and enforces contracts.
│   ├── controller.py     # Base controller class/interface
│   ├── error.py          # Base error/exception classes
│   ├── factory.py        # Factory patterns for object creation
│   ├── model.py          # Abstract data models
│   ├── repository.py     # Base repository interface
│   ├── service.py        # Base service interface
│   └── utility.py        # Abstract utility classes
├── alembic/              # Alembic migration scripts and configuration for database schema management
│   ├── env.py            # Alembic environment setup
│   ├── versions/         # Auto-generated migration scripts
│   └── ...
├── config/               # Static configuration files (JSON, YAML, etc.)
│   ├── db/               # Database connection/configuration
│   └── usda/             # USDA API configuration
├── configurations/       # Python modules for loading and managing configuration
│   ├── db.py             # Database config loader
│   └── usda.py           # USDA config loader
├── constants/            # Constant values used throughout the app
│   ├── api_lk.py         # API lookup keys
│   ├── api_status.py     # API status codes/messages
│   ├── db/               # Database table names, etc.
│   ├── payload_type.py   # Payload type constants
│   └── regular_expression.py # Regex patterns
├── controllers/          # FastAPI route controllers (handle HTTP requests)
│   ├── apis/             # API versioned controllers (e.g., v1)
│   │   ├── meal/         # Meal-related endpoints (add, fetch, history, etc.)
│   │   └── user/         # User-related endpoints (login, register, logout, etc.)
│   └── ...
├── dependencies/         # FastAPI dependency providers (e.g., for DI, DB sessions)
├── dtos/                 # Data Transfer Objects (request/response schemas)
│   ├── requests/         # Request DTOs (organized by API and user)
│   ├── responses/        # Response DTOs
│   └── ...
├── errors/               # Custom error/exception classes for API and business logic
├── middlewares/          # FastAPI middleware (authentication, rate limiting, request context, etc.)
├── models/               # SQLAlchemy ORM models (database tables)
├── repositories/         # Database access layer (CRUD operations, queries)
│   ├── meal_log.py       # Meal log repository
│   ├── profile.py        # User profile repository
│   └── user.py           # User repository
├── services/             # Business logic layer (application services)
│   ├── apis/             # API-specific services (e.g., meal add/fetch)
│   └── user/             # User-related services (login, logout, register)
├── tests/                # Unit and integration tests
│   ├── services/         # Service layer tests
│   └── ...
├── utilities/            # Utility/helper functions and classes
│   ├── dictionary.py     # Dictionary utilities
│   └── jwt.py            # JWT token utilities
├── app.py                # FastAPI app entry point (creates app, adds routers, middleware)
├── start_utils.py        # Startup utilities (config loading, logger setup, etc.)
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker build file for containerization
├── docker-compose.yml    # Docker Compose config for multi-container setup
└── README.md             # Project documentation
```

---

## Routing Pattern

This project uses a modular, versioned routing pattern for its API endpoints:

- **Versioned API Structure:**
  - All API endpoints are grouped under versioned paths (e.g., `/api/v1/`, `/user/`).
  - This allows for easy evolution of the API without breaking existing clients.

- **Modular Controllers:**
  - Each resource (such as `meal` or `user`) has its own controller module under `controllers/apis/v1/`, `controllers/user/`.
  - Endpoints are further organized by resource and action (e.g., `add`, `fetch`, `history`, `login`, `register`, `logout`).

- **Router Aggregation:**
  - Each controller defines its own FastAPI router.
  - Routers are aggregated in the main app, so all endpoints are registered cleanly and predictably.

- **Example Endpoint Paths:**
  - `/api/v1/meal/add` — Add a new meal log
  - `/api/v1/meal/fetch` — Fetch meal details
  - `/api/v1/meal/history` — Fetch meal history for a user
  - `/user/login` — User login
  - `/user/register` — User registration
  - `/user/logout` — User logout

This pattern ensures scalability, maintainability, and clarity for both developers and API consumers.

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

---

## Made with ❤️

This project is made with love, [FastAPI](https://fastapi.tiangolo.com/), and modern web technologies. We strive for clean code, robust architecture, and a great developer experience.
