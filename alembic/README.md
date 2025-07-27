# Alembic (Database Migrations)

## Purpose

In software engineering, **Alembic** is a database migration tool for SQLAlchemy. It manages schema changes over time, allowing for versioned, repeatable, and reversible migrations.

In this project, the `alembic` folder contains migration scripts and configuration for managing the database schema.

## Structure

```
alembic/
  env.py
  README
  script.py.mako
  versions/
    31c7fc3c6b39_schema.py
```

- `env.py`: Alembic environment setup
- `versions/`: Migration scripts
- `README`: Alembic usage documentation
- `script.py.mako`: Migration script template 