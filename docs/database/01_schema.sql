PRAGMA foreign_keys = ON;

CREATE TABLE entity_types (
    id INTEGER PRIMARY KEY CHECK(id BETWEEN 0 AND 999),
    name TEXT NOT NULL,
    network_relevant INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE entities (
    id TEXT PRIMARY KEY,
    type_id INTEGER NOT NULL,
    serial INTEGER NOT NULL,
    name TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(type_id) REFERENCES entity_types(id),
    UNIQUE(type_id, serial)
);

CREATE TABLE containment (
    parent_id TEXT NOT NULL,
    child_id TEXT NOT NULL,
    slot TEXT,
    PRIMARY KEY(parent_id, child_id)
);

CREATE TABLE properties (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    data_type TEXT NOT NULL
);

CREATE TABLE type_properties (
    type_id INTEGER,
    property_id INTEGER,
    required INTEGER DEFAULT 0,
    PRIMARY KEY(type_id,property_id)
);

CREATE TABLE entity_properties (
    entity_id TEXT,
    property_id INTEGER,
    value TEXT,
    PRIMARY KEY(entity_id,property_id)
);

CREATE TABLE network_interfaces (
    id INTEGER PRIMARY KEY,
    entity_id TEXT NOT NULL,
    name TEXT,
    mac TEXT,
    ip TEXT
);

CREATE TABLE network_links (
    id INTEGER PRIMARY KEY,
    interface_a INTEGER,
    interface_b INTEGER
);

CREATE TABLE type_containment_rules (
    parent_type INTEGER NOT NULL,
    child_type INTEGER NOT NULL,
    PRIMARY KEY(parent_type, child_type),
    FOREIGN KEY(parent_type) REFERENCES entity_types(id),
    FOREIGN KEY(child_type) REFERENCES entity_types(id)
);
