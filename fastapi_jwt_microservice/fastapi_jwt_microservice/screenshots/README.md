# Swagger Screenshot

Run the API:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

For assignment proof, capture a screenshot showing the Swagger/OpenAPI endpoints and the Authorize button.

Suggested screenshots:
1. Swagger `/docs` page showing Authentication and Items routes.
2. Successful `/auth/register` response.
3. Successful `/auth/login` response containing the bearer token.
4. Authorized CRUD request/response.
