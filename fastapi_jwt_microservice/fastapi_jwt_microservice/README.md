# FastAPI JWT Authentication Microservice

A complete REST API microservice built with **FastAPI + SQLite + SQLAlchemy + Pydantic + bcrypt + JWT**.

## Features

- User registration
- User login
- Password hashing with bcrypt
- JWT Bearer authentication
- Protected CRUD API for items
- Pydantic request/response validation
- SQLite persistence
- Interactive Swagger/OpenAPI documentation at `/docs`
- ReDoc documentation at `/redoc`
- Postman collection included
- CORS middleware
- Clean modular project structure

## Project Structure

```text
fastapi_jwt_microservice/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       └── items.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── screenshots/
│   └── README.md
├── postman/
│   └── FastAPI_JWT_Microservice.postman_collection.json
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 1. Create virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Run

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## API Routes

### Authentication

| Method | Endpoint | Auth |
|---|---|---|
| POST | `/auth/register` | No |
| POST | `/auth/login` | No |
| GET | `/auth/me` | JWT |

### Items CRUD

| Method | Endpoint | Auth |
|---|---|---|
| POST | `/items/` | JWT |
| GET | `/items/` | JWT |
| GET | `/items/{item_id}` | JWT |
| PUT | `/items/{item_id}` | JWT |
| DELETE | `/items/{item_id}` | JWT |

## Example registration

```json
{
  "username": "prem",
  "email": "prem@example.com",
  "password": "StrongPass123"
}
```

## Example login

Swagger's `/auth/login` endpoint uses OAuth2-style form data:

```text
username = prem
password = StrongPass123
```

The response contains:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

Click **Authorize** in Swagger and enter:

```text
Bearer JWT_TOKEN
```

Then protected CRUD routes can be tested.

## Security

- Passwords are never stored as plain text.
- Passwords are hashed with bcrypt.
- JWT access tokens are signed with a secret key.
- Protected routes require `Authorization: Bearer <token>`.
- Request bodies are validated with Pydantic.
- Users can only access their own items.

For production, replace the development `SECRET_KEY` with a strong secret stored in an environment variable and use PostgreSQL if required.

## Testing

Run:

```bash
pytest -q
```

The test suite covers registration, duplicate users, login, invalid login, protected CRUD operations, and unauthorized access.

## Expected Proof

The repository contains:

- FastAPI source code
- `requirements.txt`
- Swagger/OpenAPI support
- Postman collection
- Tests
- README instructions

For the assignment screenshot proof, open `/docs` in a browser after starting the server and capture the Swagger UI.
