# Student Learning Management API (FastAPI + PostgreSQL)

A production-ready **FastAPI** backend for an EdTech use case:
user auth (JWT), courses CRUD, and enrollments. Fully async with
SQLAlchemy + asyncpg. Comes with Docker Compose, Swagger docs, and a
clean, extensible structure.

## Features
- Python 3.11+, FastAPI, Uvicorn
- Async SQLAlchemy + PostgreSQL (asyncpg)
- JWT authentication (register/login)
- Courses CRUD (create/list/get/update/delete)
- Enrollments (student ↔ course)
- Swagger UI at `/docs` and OpenAPI JSON at `/openapi.json`
- Seed script for demo data
- Docker Compose for one-command start
- Works with PostgreSQL; falls back to SQLite for quick local runs

## Quickstart (Local - PostgreSQL via Docker)
```bash
cp .env.example .env
# (Optional) edit .env values

docker compose up --build
# App runs at http://localhost:8000
# Swagger: http://localhost:8000/docs
```

## Quickstart (Local - without Docker, SQLite fallback)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Replace DATABASE_URL with: sqlite+aiosqlite:///./app.db  (optional quick mode)
uvicorn app.main:app --reload
```

## Default Users (after seeding)
- admin@example.com / Admin@123
- student@example.com / Student@123

## API Overview
- `POST /auth/register` — create user (role: "admin" or "student")
- `POST /auth/login` — obtain access token
- `GET /users/me` — current user
- `POST /courses` — create course (admin only)
- `GET /courses` — list courses (public)
- `GET /courses/{course_id}` — get course (public)
- `PUT /courses/{course_id}` — update course (admin only)
- `DELETE /courses/{course_id}` — delete course (admin only)
- `POST /enroll/{course_id}` — enroll current user (student only)
- `GET /enrollments/me` — my enrollments

## Seeding demo data
Create an admin token, then run:
```bash
python seed.py
```

## Deploy (Render/Heroku)
- Uses `Procfile` for process definition
- Set env vars: `DATABASE_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Tech stack
- FastAPI, Pydantic
- SQLAlchemy (async), asyncpg
- passlib (bcrypt), python-jose (JWT)

## License
MIT
