# API Overview

This API provides access to entities, properties, and types. It is built with FastAPI and uses a database handler on the backend.

The API follows a simple JSON response format for both successful and failed requests. Humanity keeps inventing new ways to wrap database calls in HTTP, and somehow this is still one of the cleaner ones.

---

# Base URL

```text
http://localhost:8000
```

---

# Standard Response Format

Successful response:

```json
{
  "STATUS": "success",
  "DATA": [],
  "ERROR": null,
  "CODE": 200
}
```

Failed response:

```json
{
  "STATUS": "fail",
  "ERROR": "Internal server error",
  "CODE": 500
}
```

---

# Available Endpoints

## GET Endpoints

### Get all properties

```http
GET /properties
```

Returns a list of all available properties.

Example response:

```json
{
  "STATUS": "success",
  "DATA": [
    {
      "ID": 1,
      "NAME": "color",
      "TYPE": "string"
    }
  ],
  "ERROR": null,
  "CODE": 200
}
```

---

### Get all types

```http
GET /types
```

Returns a list of all available types.

---

### Get all entities

```http
GET /entities
```

Returns a list of all entities.

---

### Get values of a specific entity

```http
GET /entity/{entity_id}
```

Path parameters:

| Name      | Type   | Description                    |
| --------- | ------ | ------------------------------ |
| entity_id | string | The ID of the requested entity |

Example:

```http
GET /entity/001-000001
```

---

## POST Endpoints

### Create a new property

```http
POST /property
```

Request body:

```json
{
  "NAME": "weight",
  "TYPE": "integer"
}
```

Example success response:

```json
{
  "STATUS": "success",
  "ERROR": null,
  "CODE": 201
}
```

---

## PUT Endpoint Example

The current API does not include an update route yet, but a common pattern would look like this:

```http
PUT /property/{property_id}
```

Example request body:

```json
{
  "NAME": "updated_weight",
  "TYPE": "float"
}
```

Example response:

```json
{
  "STATUS": "success",
  "ERROR": null,
  "CODE": 200
}
```

---

## DELETE Endpoint Example

The current API does not include a delete route yet, but a common pattern would look like this:

```http
DELETE /property/{property_id}
```

Example response:

```json
{
  "STATUS": "success",
  "ERROR": null,
  "CODE": 200
}
```

---

# Server-Side Python Skeleton

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items")
def get_items():
    return {
        "STATUS": "success",
        "DATA": [],
        "ERROR": None,
        "CODE": 200,
    }


@app.post("/item")
def create_item(data: dict):
    return {
        "STATUS": "success",
        "ERROR": None,
        "CODE": 201,
    }


@app.put("/item/{item_id}")
def update_item(item_id: int, data: dict):
    return {
        "STATUS": "success",
        "ERROR": None,
        "CODE": 200,
    }


@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    return {
        "STATUS": "success",
        "ERROR": None,
        "CODE": 200,
    }
```

---

# Python Client Skeleton

```python
import requests

BASE_URL = "http://localhost:8000"


def get_properties() -> dict:
    response = requests.get(f"{BASE_URL}/properties")
    return response.json()


def create_property(name: str, property_type: str) -> dict:
    payload = {
        "NAME": name,
        "TYPE": property_type,
    }

    response = requests.post(f"{BASE_URL}/property", json=payload)
    return response.json()


def update_property(property_id: int, name: str, property_type: str) -> dict:
    payload = {
        "NAME": name,
        "TYPE": property_type,
    }

    response = requests.put(
        f"{BASE_URL}/property/{property_id}",
        json=payload,
    )
    return response.json()


def delete_property(property_id: int) -> dict:
    response = requests.delete(f"{BASE_URL}/property/{property_id}")
    return response.json()
```

---

# JavaScript Client Skeleton

```javascript
const BASE_URL = "http://localhost:8000";

async function getProperties() {
  const response = await fetch(`${BASE_URL}/properties`);
  return await response.json();
}

async function createProperty(name, type) {
  const response = await fetch(`${BASE_URL}/property`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      NAME: name,
      TYPE: type,
    }),
  });

  return await response.json();
}

async function updateProperty(propertyId, name, type) {
  const response = await fetch(`${BASE_URL}/property/${propertyId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      NAME: name,
      TYPE: type,
    }),
  });

  return await response.json();
}

async function deleteProperty(propertyId) {
  const response = await fetch(`${BASE_URL}/property/${propertyId}`, {
    method: "DELETE",
  });

  return await response.json();
}
```

---

# Notes

- Use HTTP status codes consistently.
- Keep response structures identical across all endpoints.
- Prefer singular endpoint names for single resources and plural names for collections.
- Add validation models with Pydantic for production use.
- Consider adding authentication if the API will be public. Because eventually every harmless little internal API turns into "temporary production" and then survives for seven years through fear and duct tape.
