# API Overview

This API provides access to entities, properties, and types. It is built with FastAPI and uses a database handler on the backend.

The API follows a simple JSON response format for both successful and failed requests.

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
  "CODE": 200
}
```

Failed response:

```json
{
  "STATUS": "fail",
  "ERROR_TYPE": "<error_type>",
  "ERROR_MESSAGE": "<error_message>",
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

### Get all types

```http
GET /types
```

Returns a list of all available types.

### Get all entities

```http
GET /entities
```

Returns a list of all entities.

### Get all type properties

```http
GET /type_properties
```

Returns a list of all type-property relationships.

### Get all entity properties

```http
GET /entity_properties
```

Returns a list of all entity-property relationships.

### Get all containment rules

```http
GET /containment_rules
```

Returns a list of all containment rules.

### Get all containment relationships

```http
GET /containment
```

Returns a list of all containment relationships.

### Get all network interfaces

```http
GET /network_interfaces
```

Returns a list of all network interfaces.

### Get all network links

```http
GET /network_links
```

Returns a list of all network links.

---

## POST Endpoints

### Create a new property

```http
POST /property
```

Request body:

```json
{
  "NAME": "<property_name>",
  "TYPE": "<property_type>"
}
```

### Create a new type

```http
POST /types
```

Request body:

```json
{
  "NAME": "<type_name>",
  "IS_NETWORK_RELEVANT": true
}
```

### Create a new entity

```http
POST /entity
```

Request body:

```json
{
  "NAME": "<entity_name>",
  "TYPE_ID": 1
}
```

### Create a new type-property relationship

```http
POST /type_property
```

Request body:

```json
{
  "TYPE_ID": 1,
  "PROPERTY_ID": 2,
  "REQUIRED": true
}
```

### Create a new entity-property relationship

```http
POST /entity_property
```

Request body:

```json
{
  "ENTITY_ID": "<entity_id>",
  "PROPERTY_ID": 2,
  "VALUE": "<value>"
}
```

### Create a new containment rule

```http
POST /containment_rule
```

Request body:

```json
{
  "PARENT_TYPE_ID": 1,
  "CHILD_TYPE_ID": 2
}
```

### Create a new containment relationship

```http
POST /containment
```

Request body:

```json
{
  "PARENT_ID": "<parent_entity_id>",
  "CHILD_ID": "<child_entity_id>",
  "SLOT": "<slot>"
}
```

### Create a new network interface

```http
POST /network_interface
```

Request body:

```json
{
  "ENTITY_ID": "<entity_id>",
  "INTERFACE_NAME": "<interface_name>",
  "MAC": "<mac_address>",
  "IP": "<ip_address>"
}
```

### Create a new network link

```http
POST /network_link
```

Request body:

```json
{
  "INTERFACE_A": 1,
  "INTERFACE_B": 2
}
```

---

## PUT Endpoints

### Update a property

```http
PUT /property/{property_id}
```

Request body:

```json
{
  "NAME": "<new_property_name>",
  "DATA_TYPE": "<new_property_type>"
}
```

### Update a type

```http
PUT /type/{type_id}
```

Request body:

```json
{
  "NAME": "<new_type_name>",
  "NETWORK_RELEVANT": true
}
```

### Update an entity

```http
PUT /entity/{entity_id}
```

Request body:

```json
{
  "NAME": "<new_entity_name>"
}
```

### Update an entity-property relationship

```http
PUT /entity_property/{entity_id}/{property_id}
```

Request body:

```json
{
  "VALUE": "<new_value>"
}
```

### Update a containment relationship

```http
PUT /containment/{parent_entity_id}/{child_entity_id}
```

Request body:

```json
{
  "SLOT": "<new_slot>"
}
```

### Update a network interface

```http
PUT /network_interface/{interface_id}
```

Request body:

```json
{
  "ENTITY_ID": "<new_entity_id>",
  "INTERFACE_NAME": "<new_interface_name>",
  "MAC": "<new_mac_address>",
  "IP": "<new_ip_address>"
}
```

---

## DELETE Endpoints

### Delete a property

```http
DELETE /property/{property_id}
```

### Delete a type

```http
DELETE /type/{type_id}
```

### Delete an entity

```http
DELETE /entity/{entity_id}
```

### Delete a type-property relationship

```http
DELETE /type_property/{type_id}/{property_id}
```

### Delete an entity-property relationship

```http
DELETE /entity_property/{entity_id}/{property_id}
```

### Delete a containment rule

```http
DELETE /containment_rule/{parent_type_id}/{child_type_id}
```

### Delete a containment relationship

```http
DELETE /containment/{parent_entity_id}/{child_entity_id}
```

### Delete a network interface

```http
DELETE /network_interface/{interface_id}
```

### Delete a network link

```http
DELETE /network_link/{link_id}
```
