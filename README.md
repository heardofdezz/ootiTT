# Django Todolist + Notes API

A REST API built with Django + Django REST Framework exposing two cross-referencing apps: **todos** and **notes**.

---

## Quick start
Python -m venv .venv (if virtual env is needed)
```bash
# 1. Install dependencies
pip install django djangorestframework

# 2. Run migrations
python manage.py migrate

# 3. Start the server
python manage.py runserver
```

API is available at `http://localhost:8000/api/`

---

## Endpoints

### Todos

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/todos/` | List all todos (paginated) |
| POST | `/api/todos/` | Create a todo |
| GET | `/api/todos/{id}/` | Retrieve a todo |
| PUT | `/api/todos/{id}/` | Full update |
| PATCH | `/api/todos/{id}/` | Partial update |
| DELETE | `/api/todos/{id}/` | Delete |

### Notes

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/notes/` | List all notes (paginated) |
| POST | `/api/notes/` | Create a note |
| GET | `/api/notes/{id}/` | Retrieve a note |
| PUT | `/api/notes/{id}/` | Full update |
| PATCH | `/api/notes/{id}/` | Partial update |
| DELETE | `/api/notes/{id}/` | Delete |

---

## cURL examples

```bash
# Create a note
curl -X POST http://localhost:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Shopping list", "content": "Things to buy"}'

# Create a todo linked to note id=1
curl -X POST http://localhost:8000/api/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "status": "pending", "note": 1}'

# Get a note with its todos embedded
curl http://localhost:8000/api/notes/1/

# Update todo status
curl -X PATCH http://localhost:8000/api/todos/1/ \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'

# Unlink a todo from its note
curl -X PATCH http://localhost:8000/api/todos/1/ \
  -H "Content-Type: application/json" \
  -d '{"note": null}'
```

---

## Todo payload

```json
{
  "title": "Buy milk",         // required
  "description": "...",        // optional
  "status": "pending",         // pending | in_progress | done  (default: pending)
  "note": 1                    // optional FK to a Note (write-only, send Note id)
}
```

**Response** includes `note_detail` (read-only) instead of the raw FK:

```json
{
  "id": 1,
  "title": "Buy milk",
  "status": "pending",
  "note_detail": { "id": 1, "title": "Shopping list" },
  "created_at": "...",
  "updated_at": "..."
}
```

## Note payload

```json
{
  "title": "Shopping list",    // required
  "content": "..."             // optional
}
```

**Response** embeds linked todos:

```json
{
  "id": 1,
  "title": "Shopping list",
  "content": "Things to buy",
  "todos": [
    { "id": 1, "title": "Buy milk", "status": "pending" }
  ],
  "created_at": "...",
  "updated_at": "..."
}
```

---

## Run tests

```bash
python manage.py test --verbosity=2
```

---
