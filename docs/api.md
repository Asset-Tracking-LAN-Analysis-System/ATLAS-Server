# API Design Pattern Guide

## Purpose

This document defines a **reproducible, generic API pattern** that can be reused across projects. It is intentionally abstract so different teams can implement their own logic while following the same structure.

The goal:

- Consistent communication between client and server
- Clear request/response contracts
- Easy extensibility

---

## Architecture Overview

Client and server are **independent systems**:

- Client → sends HTTP requests
- Server → processes logic + database
- Communication → JSON over HTTP

The server **does NOT need to run on the same machine** as the client.

Example:

```
Client (Desktop / Web) → Internet → Server (API)
```

---

## Base URL Pattern

```
https://api.your-domain.com/v1
```

Always version your API.

---

## Generic Request Pattern

### GET (read data)

```
GET /resources
GET /resources/{id}
```

### POST (create)

```
POST /resources
```

### PUT / PATCH (update)

```
PUT /resources/{id}
```

### DELETE (remove)

```
DELETE /resources/{id}
```

---

## Generic Query Pattern (Filtering & Pagination)

```
GET /resources?limit=10&offset=0&filter=name:value
```

### Parameters

- `limit` → number of results
- `offset` → starting point
- `filter` → optional filtering logic

---

## Standard Response Schema

All endpoints should follow a consistent structure:

```json
{
  "status": "success",
  "data": [],
  "meta": {
    "count": 0,
    "limit": 10,
    "offset": 0
  },
  "error": null
}
```

### Error Example

```json
{
  "status": "error",
  "data": null,
  "meta": null,
  "error": {
    "message": "Resource not found",
    "code": 404
  }
}
```

---

## Server Skeleton (Python / FastAPI)

```python
from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

# Mock database
DATABASE = []

@app.get("/resources")
def list_resources(limit: int = Query(10), offset: int = Query(0)):
    data = DATABASE[offset: offset + limit]
    return {
        "status": "success",
        "data": data,
        "meta": {
            "count": len(DATABASE),
            "limit": limit,
            "offset": offset
        },
        "error": None
    }

@app.get("/resources/{resource_id}")
def get_resource(resource_id: int):
    for item in DATABASE:
        if item["id"] == resource_id:
            return {
                "status": "success",
                "data": item,
                "meta": None,
                "error": None
            }
    return {
        "status": "error",
        "data": None,
        "meta": None,
        "error": {"message": "Not found", "code": 404}
    }

@app.post("/resources")
def create_resource(data: dict):
    data["id"] = len(DATABASE) + 1
    DATABASE.append(data)
    return {
        "status": "success",
        "data": data,
        "meta": None,
        "error": None
    }
```

---

## Client Skeleton (Python)

```python
import requests

BASE_URL = "https://api.your-domain.com/v1"

# Get list
res = requests.get(f"{BASE_URL}/resources", params={
    "limit": 10,
    "offset": 0
})
print(res.json())

# Get single
res = requests.get(f"{BASE_URL}/resources/1")
print(res.json())

# Create
res = requests.post(
    f"{BASE_URL}/resources",
    json={"name": "Example"}
)
print(res.json())
```

---

## Client Skeleton (JavaScript)

```javascript
const BASE_URL = "https://api.your-domain.com/v1";

// Get list
fetch(`${BASE_URL}/resources?limit=10&offset=0`)
  .then((res) => res.json())
  .then((data) => console.log(data));

// Get single
fetch(`${BASE_URL}/resources/1`)
  .then((res) => res.json())
  .then((data) => console.log(data));

// Create
fetch(`${BASE_URL}/resources`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ name: "Example" }),
})
  .then((res) => res.json())
  .then((data) => console.log(data));
```

---

## Design Principles

### 1. Consistency

Every endpoint follows the same structure.

### 2. Separation of Concerns

- Client → UI + requests
- Server → logic + database

### 3. Scalability

Always assume data will grow.

### 4. Extensibility

New features = new endpoints, not hacks.

---

## Naming Conventions

- Use plural nouns: `/resources`
- Use lowercase + hyphens if needed
- Avoid verbs in URLs

---

## Documentation Strategy

- Provide OpenAPI (`/docs`)
- Provide this Markdown as human-readable guide
- Keep examples minimal and reproducible

---

## Summary

This skeleton defines a **universal API pattern**:

- Predictable endpoints
- Standardized responses
- Language-independent clients

If every developer follows this, integration becomes trivial and maintenance stays manageable.
