import sqlite3
import os
from vshc.database.utils import detect_id_gap
from pathlib import Path
from .helper import get_first_free_serial


class DBHandler:
    def __init__(self) -> None:
        """
        Initializes a new DBHandler instance and establishes a connection to the SQLite database.

        This function sets the path to the database file, connects to it, and creates a cursor object
        for interacting with the database. The database path is resolved relative to this file's location.

        Example:
            handler = DBHandler()
            # handler.connection and handler.cursor are now available.

        Args:
            self:
                The instance of the class.

        Returns:
            None
                This function does not return any value.

        Optional notes:
            `check_same_thread=False` is required as the handler may be called from multiple threads (e.g., by the API server).
        """
        self.db_path: str = os.path.join(
            str(Path(__file__).resolve().parent), "..", "data", "atlas.db"
        )
        self.connection = sqlite3.Connection(self.db_path, check_same_thread=False)
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    ## get data ##
    def get_all_properties(self) -> list[dict[str, str | int | None]]:
        """
        Retrieves all defined properties from the database.

        This function executes a SELECT query on the `properties` table and formats the results
        as a list of dictionaries, each representing a property with its metadata.
        The first two entries in the result list are static dictionaries for "ID" and "Name",
        serving as default fields for properties.

        Example:
            handler = DBHandler()
            properties = handler.get_all_properties()
            # properties would look like this:
            # [
            #   {"ID": None, "NAME": "ID", "TYPE": "text"},
            #   {"ID": None, "NAME": "Name", "TYPE": "text"},
            #   {"ID": 1, "NAME": "Manufacturer", "TYPE": "text"}
            # ]

        Args:
            self:
                The instance of the class.

        Returns:
            list[dict[str, str | int | None]]:
                A list of dictionaries, each representing a property, including its ID, NAME, and TYPE.
                `ID` and `Name` are always the first two elements.
        """
        self.cursor.execute("SELECT * FROM properties")
        raw_data: list[tuple[int, str, str]] = self.cursor.fetchall()
        result: list[dict[str, str | int | None]] = [
            {"ID": None, "NAME": "ID", "TYPE": "text"},
            {"ID": None, "NAME": "Name", "TYPE": "text"},
        ]
        for id, name, type in raw_data:
            result.append({"ID": id, "NAME": name, "TYPE": type})
        return result

    def get_all_types(self) -> list[dict[str, str | int | bool]]:
        """
        Retrieves all defined entity types from the database.

        This function executes a SELECT query on the `entity_types` table and formats the results
        as a list of dictionaries, each representing an entity type with its metadata.

        Example:
            handler = DBHandler()
            entity_types = handler.get_all_types()
            # entity_types would look like this:
            # [
            #   {"ID": 1, "NAME": "Server", "NETWORK_RELEVANT": True},
            #   {"ID": 2, "NAME": "Switch", "NETWORK_RELEVANT": True}
            # ]

        Args:
            self:
                The instance of the class.

        Returns:
            list[dict[str, str | int | bool]]:
                A list of dictionaries, each representing an entity type, including ID, NAME, and NETWORK_RELEVANT.
        """
        self.cursor.execute("SELECT * FROM entity_types")
        raw_data: list[tuple[int, str, int]] = self.cursor.fetchall()
        result: list[dict[str, str | int | bool]] = []
        for id, name, network_relevant in raw_data:
            result.append(
                {"ID": id, "NAME": name, "NETWORK_RELEVANT": network_relevant == 1}
            )
        return result

    def get_all_entities(self) -> list[dict[str, str]]:
        """
        Retrieves all defined entities from the database.

        This function executes a SELECT query on the `entities` table and formats the results
        as a list of dictionaries, each representing an entity with its metadata.
        Only the ID and NAME of the entity are returned.

        Example:
            handler = DBHandler()
            entities = handler.get_all_entities()
            # entities would look like this:
            # [
            #   {"ID": "001-000001", "NAME": "Server-01"},
            #   {"ID": "002-000001", "NAME": "Switch-01"}
            # ]

        Args:
            self:
                The instance of the class.

        Returns:
            list[dict[str, str]]:
                A list of dictionaries, each representing an entity, including ID and NAME.
        """
        self.cursor.execute("SELECT * FROM entities")
        raw_data: list[tuple[str, int, int, str, str]] = self.cursor.fetchall()
        result: list[dict[str, str]] = []
        for entry in raw_data:
            result.append({"ID": entry[0], "NAME": entry[3]})
        return result

    ## add Data ##
    def add_property(self, name: str, data_type: str) -> None:
        """
        Adds a new property to the database.

        This function inserts a new entry into the `properties` table after detecting a missing ID.
        It validates the `data_type` to ensure it is a valid type.

        Example:
            handler = DBHandler()
            handler.add_property(name="Manufacturer", data_type="text")
            # A new property will be added to the database.

        Args:
            self:
                The instance of the class.
            name (str):
                The name of the property to add.
            data_type (str):
                The data type of the property. Valid types are "text", "float", "int", or "bool".

        Returns:
            None
                This function does not return any value.

        Optional notes:
            Raises a `ValueError` if the `data_type` is invalid.
        """
        if data_type not in ["text", "float", "int", "bool"]:
            raise ValueError(f"{data_type=} is not a valid data type")
        gap: int = detect_id_gap(self.cursor, "properties", "id")
        self.cursor.execute(
            "INSERT INTO properties (id, name, data_type) VALUES (?, ?, ?)",
            (gap, name, data_type),
        )
        self.connection.commit()

    def add_type(self, name: str, is_network_relevant: bool) -> None:
        """
        Adds a new entity type to the database.

        This function inserts a new entry into the `entity_types` table after detecting a missing ID.
        The `is_network_relevant` parameter is converted to an integer (1 or 0).

        Example:
            handler = DBHandler()
            handler.add_type(name="Server", is_network_relevant=True)
            # A new entity type will be added to the database.

        Args:
            self:
                The instance of the class.
            name (str):
                The name of the entity type to add.
            is_network_relevant (bool):
                Indicates whether the entity type is network relevant.

        Returns:
            None
                This function does not return any value.
        """
        gap: int = detect_id_gap(self.cursor, "entity_types", "id")
        self.cursor.execute(
            "INSERT INTO entity_types (id, name, network_relevant) VALUES (?, ?, ?)",
            (gap, name, 1 if is_network_relevant else 0),
        )
        self.connection.commit()

    def add_entity(self, type_id: int, name: str) -> None:
        """
        Adds a new entity to the database.

        This function generates a unique entity ID based on the `type_id` and a free serial number.
        Then, it inserts a new entry into the `entities` table.

        Example:
            handler = DBHandler()
            handler.add_entity(type_id=1, name="Server-01")
            # A new entity with an ID like "001-000001" will be added to the database.

        Args:
            self:
                The instance of the class.
            type_id (int):
                The ID of the type to which the entity belongs.
            name (str):
                The name of the entity to add.

        Returns:
            None
                This function does not return any value.
        """
        serial: int = get_first_free_serial(self.cursor, type_id)
        entity_id: str = f"{type_id:03}-{serial:06}"
        self.cursor.execute(
            "INSERT INTO entities (id, type_id, serial, name) VALUES (?, ?, ?, ?)",
            (entity_id, type_id, serial, name),
        )
        self.connection.commit()

    ## update Data ##
    def update_property(
        self, property_id: int, new_name: str, new_data_type: str
    ) -> None:
        """
        Updates an existing property in the database.

        This function modifies the name and data type of a property identified by its ID.
        It ensures that the new data type is valid and that no records are using the property
        before making changes.

        Args:
            property_id (int):
                The ID of the property to update.
            new_name (str):
                The new name for the property.
            new_data_type (str):
                The new data type for the property. Valid types are "text", "float", "int", or "bool".

        Returns:
            None
                This function does not return any value.

        Raises:
            ValueError: If the new data type is invalid.
            RuntimeError: If records using this property already exist.
        """
        if new_data_type not in ["text", "float", "int", "bool"]:
            raise ValueError(f"{new_data_type=} is not a valid data type.")
        self.cursor.execute(
            f"SELECT * FROM entity_properties WHERE property_id={property_id}"
        )
        if self.cursor.fetchall() != []:
            raise RuntimeError(
                "Cannot change property data while records using this type already exist."
            )
        self.cursor.execute(
            f"UPDATE properties SET name='{new_name}', data_type='{new_data_type}' WHERE id={property_id}"
        )
        self.connection.commit()

    def update_type(
        self, type_id: int, new_name: str, new_is_network_relevant: bool
    ) -> None:
        """
        Updates an existing entity type in the database.

        This function modifies the name and network relevance of an entity type identified by its ID.
        It ensures that no records are using the entity type before making changes.

        Args:
            type_id (int):
                The ID of the entity type to update.
            new_name (str):
                The new name for the entity type.
            new_is_network_relevant (bool):
                The new network relevance status for the entity type.

        Returns:
            None
                This function does not return any value.

        Raises:
            RuntimeError: If records using this entity type already exist.
        """
        queries: list[str] = [
            "SELECT 1 FROM entities WHERE type_id=? LIMIT 1",
            "SELECT 1 FROM type_properties WHERE type_id=? LIMIT 1",
            "SELECT 1 FROM type_containment_rules WHERE parent_type=? OR child_type=? LIMIT 1",
        ]

        params: list[tuple[int] | tuple[int, int]] = [
            (type_id,),
            (type_id,),
            (type_id, type_id),
        ]

        for query, param in zip(queries, params):
            self.cursor.execute(query, param)

            if self.cursor.fetchone() is not None:
                raise RuntimeError(
                    "Cannot change type while records using this type already exist."
                )
        self.cursor.execute(
            f"UPDATE entity_types SET name='{new_name}', network_relevant='{1 if new_is_network_relevant else 0}' WHERE id={type_id}"
        )
        self.connection.commit()

    def update_entity(self, entity_id: str, new_name: str) -> None:
        """
        Updates an existing entity in the database.

        This function modifies the name of an entity identified by its ID.

        Args:
            entity_id (str):
                The ID of the entity to update.
            new_name (str):
                The new name for the entity.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(
            f"UPDATE entities SET name='{new_name}' WHERE id='{entity_id}'"
        )
        self.connection.commit()

    ## delete Data ##
    def delete_property(self, property_id: int) -> None:
        """
        Deletes a property from the database.

        This function removes a property identified by its ID from the `properties` table.
        It ensures that no records are using the property before deletion.

        Args:
            property_id (int):
                The ID of the property to delete.

        Returns:
            None
                This function does not return any value.

        Raises:
            RuntimeError: If records using this property already exist.
        """
        queries: list[str] = [
            "SELECT 1 FROM type_properties WHERE property_id=? LIMIT 1",
            "SELECT 1 FROM entity_properties WHERE property_id=? LIMIT 1",
        ]

        params: list[tuple[int]] = [
            (property_id,),
            (property_id,),
        ]

        for query, param in zip(queries, params):
            self.cursor.execute(query, param)

            if self.cursor.fetchone() is not None:
                raise RuntimeError(
                    "Cannot delete property while records using this property already exist."
                )
        self.cursor.execute(f"DELETE FROM properties WHERE id={property_id}")
        self.connection.commit()

    def delete_type(self, type_id: int) -> None:
        """
        Deletes an entity type from the database.

        This function removes an entity type identified by its ID from the `entity_types` table.
        It ensures that no records are using the entity type before deletion.

        Args:
            type_id (int):
                The ID of the entity type to delete.

        Returns:
            None
                This function does not return any value.

        Raises:
            RuntimeError: If records using this entity type already exist.
        """
        queries: list[str] = [
            "SELECT 1 FROM entities WHERE type_id=? LIMIT 1",
            "SELECT 1 FROM type_properties WHERE type_id=? LIMIT 1",
            "SELECT 1 FROM type_containment_rules WHERE parent_type=? OR child_type=? LIMIT 1",
        ]

        params: list[tuple[int] | tuple[int, int]] = [
            (type_id,),
            (type_id,),
            (type_id, type_id),
        ]

        for query, param in zip(queries, params):
            self.cursor.execute(query, param)

            if self.cursor.fetchone() is not None:
                raise RuntimeError(
                    "Cannot delete type while records using this type already exist."
                )
        self.cursor.execute(f"DELETE FROM entity_types WHERE id={type_id}")
        self.connection.commit()

    def delete_entity(self, entity_id: str) -> None:
        """
        Deletes an entity from the database.

        This function removes an entity identified by its ID from the `entities` table.
        It ensures that no records are using the entity before deletion.

        Args:
            entity_id (str):
                The ID of the entity to delete.

        Returns:
            None
                This function does not return any value.

        Raises:
            RuntimeError: If records using this entity already exist.
        """
        queries: list[str] = [
            "SELECT 1 FROM containment WHERE parent_id=? OR child_id=? LIMIT 1",
            "SELECT 1 FROM entity_properties WHERE entity_id=? LIMIT 1",
            "SELECT 1 FROM network_interfaces WHERE entity_id=? LIMIT 1",
        ]

        params: list[tuple[str, str] | tuple[str]] = [
            (entity_id, entity_id),
            (entity_id,),
            (entity_id,),
        ]

        for query, param in zip(queries, params):
            self.cursor.execute(query, param)

            if self.cursor.fetchone() is not None:
                raise RuntimeError(
                    "Cannot delete entity while records using this entity already exist."
                )
        self.cursor.execute(f"DELETE FROM entities WHERE id='{entity_id}'")
        self.connection.commit()

    #######################################
    ############## Properties #############
    #######################################

    ## Type-Property ##
    def add_type_property(self, type_id: int, property_id: int, required: bool) -> None:
        """
        Adds a property to a specific entity type in the database.

        This function associates a property with an entity type and marks it as required or optional.

        Args:
            type_id (int):
                The ID of the entity type to associate the property with.
            property_id (int):
                The ID of the property to add.
            required (bool):
                Indicates whether the property is required for the entity type.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(
            "INSERT INTO type_properties (type_id, property_id, required) VALUES (?, ?, ?)",
            (type_id, property_id, 1 if required else 0),
        )
        self.connection.commit()

    def delete_type_property(self, type_id: int, property_id: int) -> None:
        """
        Deletes a property from a specific entity type in the database.

        This function removes the association between a property and an entity type.
        It ensures that no records are using the property before deletion.

        Args:
            type_id (int):
                The ID of the entity type to remove the property from.
            property_id (int):
                The ID of the property to delete.

        Returns:
            None
                This function does not return any value.

        Raises:
            RuntimeError: If records using this property already exist.
        """
        self.cursor.execute(
            "SELECT 1 FROM entity_properties WHERE property_id=? AND entity_id IN (SELECT id FROM entities WHERE type_id=?) LIMIT 1",
            (property_id, type_id),
        )
        if self.cursor.fetchone() is not None:
            raise RuntimeError(
                "Cannot delete type property while records using this property already exist."
            )
        self.cursor.execute(
            f"DELETE FROM type_properties WHERE type_id={type_id} AND property_id={property_id}"
        )
        self.connection.commit()

    def get_type_properties(self) -> list[dict[str, int | bool]]:
        """
        Retrieves all type-property associations from the database.

        This function fetches all associations between entity types and properties,
        including whether each property is required.

        Args:
            None:
                This function does not take any parameters.

        Returns:
            list[dict[str, int | bool]]:
                A list of dictionaries, each representing a type-property association,
                including TYPE_ID, PROPERTY_ID, and REQUIRED status.
        """
        self.cursor.execute("SELECT * FROM type_properties")
        raw_data: list[tuple[int, int, int]] = self.cursor.fetchall()

        result: list[dict[str, int | bool]] = []
        for type_id, property_id, required in raw_data:
            result.append(
                {
                    "TYPE_ID": type_id,
                    "PROPERTY_ID": property_id,
                    "REQUIRED": required == 1,
                }
            )
        return result

    ## Entity-Property ##
    def add_entity_property(self, entity_id: str, property_id: int, value: str) -> None:
        """
        Adds a property to a specific entity in the database.

        This function associates a property with an entity and assigns it a value.

        Args:
            entity_id (str):
                The ID of the entity to associate the property with.
            property_id (int):
                The ID of the property to add.
            value (str):
                The value of the property for the entity.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(
            "INSERT INTO entity_properties (entity_id, property_id, value) VALUES (?, ?, ?)",
            (entity_id, property_id, value),
        )
        self.connection.commit()

    def update_entity_property(
        self, entity_id: str, property_id: int, new_value: str
    ) -> None:
        """
        Updates the value of a property for a specific entity in the database.

        This function modifies the value of an existing property associated with an entity.

        Args:
            entity_id (str):
                The ID of the entity whose property value is to be updated.
            property_id (int):
                The ID of the property to update.
            new_value (str):
                The new value for the property.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(
            f"UPDATE entity_properties SET value='{new_value}' WHERE entity_id='{entity_id}' AND property_id={property_id}"
        )
        self.connection.commit()

    def delete_entity_property(self, entity_id: str, property_id: int) -> None:
        """
        Deletes a property from a specific entity in the database.

        This function removes the association between a property and an entity.

        Args:
            entity_id (str):
                The ID of the entity to remove the property from.
            property_id (int):
                The ID of the property to delete.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(
            f"DELETE FROM entity_properties WHERE entity_id='{entity_id}' AND property_id={property_id}"
        )
        self.connection.commit()

    def get_entity_properties(self) -> list[dict[str, str | int]]:
        """
        Retrieves all entity-property associations from the database.

        This function fetches all associations between entities and their properties,
        including the values assigned to each property.

        Args:
            None:
                This function does not take any parameters.

        Returns:
            list[dict[str, str | int]]:
                A list of dictionaries, each representing an entity-property association,
                including ENTITY_ID, PROPERTY_ID, and VALUE.
        """
        self.cursor.execute("SELECT * FROM entity_properties")
        raw_data: list[tuple[str, int, str]] = self.cursor.fetchall()

        result: list[dict[str, str | int]] = []
        for entity_id, property_id, value in raw_data:
            result.append(
                {"ENTITY_ID": entity_id, "PROPERTY_ID": property_id, "VALUE": value}
            )
        return result

    #######################################
    ############## Cointainment ###########
    #######################################

    ## rules ##
    def add_containment_rule(self, parent_type_id: int, child_type_id: int) -> None:
        """
        Adds a containment rule between two entity types in the database.

        This function creates a new rule specifying that entities of the parent type
        can contain entities of the child type.

        Args:
            parent_type_id (int):
                The ID of the parent entity type.
            child_type_id (int):
                The ID of the child entity type.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(
            "INSERT INTO type_containment_rules (parent_type, child_type) VALUES (?, ?)",
            (parent_type_id, child_type_id),
        )
        self.connection.commit()

    def delete_containment_rule(self, parent_type_id: int, child_type_id: int) -> None:
        """
        Deletes a containment rule between two entity types in the database.

        This function removes the rule specifying that entities of the parent type
        can contain entities of the child type. It ensures that no records are using
        the rule before deletion.

        Args:
            parent_type_id (int):
                The ID of the parent entity type.
            child_type_id (int):
                The ID of the child entity type.

        Returns:
            None
                This function does not return any value.

        Raises:
            RuntimeError: If records using this rule already exist.
        """
        queries: list[str] = [
            "SELECT 1 FROM containment WHERE parent_id IN (SELECT id FROM entities WHERE type_id=?) AND child_id IN (SELECT id FROM entities WHERE type_id=?) LIMIT 1",
        ]

        params: list[tuple[int, int]] = [
            (parent_type_id, child_type_id),
        ]

        for query, param in zip(queries, params):
            self.cursor.execute(query, param)

            if self.cursor.fetchone() is not None:
                raise RuntimeError(
                    "Cannot delete containment rule while records using this rule already exist."
                )
        self.cursor.execute(
            f"DELETE FROM type_containment_rules WHERE parent_type={parent_type_id} AND child_type={child_type_id}"
        )
        self.connection.commit()

    def get_containment_rules(self) -> list[dict[str, int]]:
        """
        Retrieves all containment rules from the database.

        This function fetches all rules specifying which entity types can contain others.

        Args:
            None:
                This function does not take any parameters.

        Returns:
            list[dict[str, int]]:
                A list of dictionaries, each representing a containment rule,
                including PARENT and CHILD entity type IDs.
        """
        self.cursor.execute("SELECT * FROM type_containment_rules")
        raw_data: list[tuple[int, int]] = self.cursor.fetchall()

        result: list[dict[str, int]] = []
        for parent, child in raw_data:
            result.append({"PARENT": parent, "CHILD": child})
        return result

    ## Containment-Register ##
    def add_containment(
        self, parent_entity_id: str, child_entity_id: str, slot: str | None = None
    ) -> None:
        """
        Adds a containment relationship between two entities in the database.

        This function specifies that a parent entity contains a child entity,
        optionally assigning the child to a specific slot.

        Args:
            parent_entity_id (str):
                The ID of the parent entity.
            child_entity_id (str):
                The ID of the child entity.
            slot (str | None):
                The slot to assign the child entity to, if applicable.

        Returns:
            None
                This function does not return any value.

        Raises:
            RuntimeError: If the child entity is already contained by another parent.
        """
        self.cursor.execute(
            f"SELECT * FROM containment WHERE child_id='{child_entity_id}'"
        )
        if self.cursor.fetchall() != []:
            raise RuntimeError(
                "Can't add entry, since child is already bound in another parent."
            )
        self.cursor.execute(
            "INSERT INTO containment (parent_id, child_id, slot) VALUES (?, ?, ?)",
            (parent_entity_id, child_entity_id, slot),
        )
        self.connection.commit()

    def update_containment(
        self, parent_entity_id: str, child_entity_id: str, new_slot: str | None
    ) -> None:
        """
        Updates the slot assignment for a containment relationship in the database.

        This function modifies the slot assignment for a child entity contained by a parent entity.

        Args:
            parent_entity_id (str):
                The ID of the parent entity.
            child_entity_id (str):
                The ID of the child entity.
            new_slot (str | None):
                The new slot to assign the child entity to.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(
            f"UPDATE containment SET slot='{new_slot}' WHERE parent_id='{parent_entity_id}' AND child_id='{child_entity_id}'"
        )
        self.connection.commit()

    def delete_containment(self, parent_entity_id: str, child_entity_id: str) -> None:
        """
        Deletes a containment relationship between two entities in the database.

        This function removes the relationship specifying that a parent entity contains a child entity.

        Args:
            parent_entity_id (str):
                The ID of the parent entity.
            child_entity_id (str):
                The ID of the child entity.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(
            f"DELETE FROM containment WHERE parent_id='{parent_entity_id}' AND child_id='{child_entity_id}'"
        )
        self.connection.commit()

    def get_containment(self) -> list[dict[str, str | None]]:
        """
        Retrieves all containment relationships from the database.

        This function fetches all relationships specifying which entities contain others,
        including optional slot assignments.

        Args:
            None:
                This function does not take any parameters.

        Returns:
            list[dict[str, str | None]]:
                A list of dictionaries, each representing a containment relationship,
                including PARENT, CHILD, and SLOT information.
        """
        self.cursor.execute("SELECT * FROM containment")
        raw_data: list[tuple[str, str, str | None]] = self.cursor.fetchall()

        result: list[dict[str, str | None]] = []
        for parent, child, slot in raw_data:
            result.append({"PARENT_ID": parent, "CHILD_ID": child, "SLOT": slot})
        return result

    ###################################
    ############## Network ############
    ###################################

    ## Network Interfaces ##
    def add_network_interface(
        self, entity_id: str, interface_name: str, mac: str, ip: str
    ) -> None:
        """
        Adds a new network interface to the database.

        This function creates a new network interface associated with a specific entity,
        including its name, MAC address, and IP address.

        Args:
            entity_id (str):
                The ID of the entity to associate the network interface with.
            interface_name (str):
                The name of the network interface.
            mac (str):
                The MAC address of the network interface.
            ip (str):
                The IP address of the network interface.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(
            "INSERT INTO network_interfaces (id, entity_id, interface_name, mac, ip) VALUES (?, ?, ?, ?, ?)",
            (
                detect_id_gap(self.cursor, "network_interfaces"),
                entity_id,
                interface_name,
                mac,
                ip,
            ),
        )
        self.connection.commit()

    def update_network_interface(
        self,
        interface_id: int,
        new_entity_id: str,
        new_interface_name: str,
        new_mac: str,
        new_ip: str,
    ) -> None:
        """
        Updates an existing network interface in the database.

        This function modifies the details of a network interface identified by its ID,
        including its associated entity, name, MAC address, and IP address.

        Args:
            interface_id (int):
                The ID of the network interface to update.
            new_entity_id (str):
                The new entity ID to associate the network interface with.
            new_interface_name (str):
                The new name for the network interface.
            new_mac (str):
                The new MAC address for the network interface.
            new_ip (str):
                The new IP address for the network interface.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(
            f"UPDATE network_interfaces SET entity_id='{new_entity_id}', interface_name='{new_interface_name}', mac='{new_mac}', ip='{new_ip}' WHERE id={interface_id}"
        )
        self.connection.commit()

    def delete_network_interface(self, interface_id: int) -> None:
        """
        Deletes a network interface from the database.

        This function removes a network interface identified by its ID.
        It ensures that no network links are associated with the interface before deletion.

        Args:
            interface_id (int):
                The ID of the network interface to delete.

        Returns:
            None
                This function does not return any value.

        Raises:
            RuntimeError: If network links are associated with the interface.
        """
        self.cursor.execute(
            "SELECT 1 FROM network_links WHERE interface_a=? OR interface_b=? LIMIT 1",
            (interface_id, interface_id),
        )
        if self.cursor.fetchone() is not None:
            raise RuntimeError(
                "Cannot delete network interface while links to this interface exist."
            )
        self.cursor.execute(f"DELETE FROM network_interfaces WHERE id={interface_id}")
        self.connection.commit()

    def get_network_interfaces(self) -> list[dict[str, str | int]]:
        """
        Retrieves all network interfaces from the database.

        This function fetches all network interfaces, including their IDs, associated entity IDs,
        interface names, MAC addresses, and IP addresses.

        Args:
            None:
                This function does not take any parameters.

        Returns:
            list[dict[str, str | int]]:
                A list of dictionaries, each representing a network interface with its metadata.
        """
        self.cursor.execute("SELECT * FROM network_interfaces")
        raw_data: list[tuple[int, str, str, str, str]] = self.cursor.fetchall()

        result: list[dict[str, str | int]] = []
        for interface_id, entity_id, interface_name, mac, ip in raw_data:
            result.append(
                {
                    "ID": interface_id,
                    "ENTITY_ID": entity_id,
                    "NAME": interface_name,
                    "MAC_ADDRESS": mac,
                    "IP_ADDRESS": ip,
                }
            )
        return result

    ## Network Links ##
    def add_network_link(self, interface_a: int, interface_b: int) -> None:
        """
        Adds a network link between two interfaces in the database.

        This function creates a new link between two network interfaces, identified by their IDs.

        Args:
            interface_a (int):
                The ID of the first network interface.
            interface_b (int):
                The ID of the second network interface.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(
            "INSERT INTO network_links (id, interface_a, interface_b) VALUES (?, ?, ?)",
            (detect_id_gap(self.cursor, "network_links"), interface_a, interface_b),
        )
        self.connection.commit()

    def delete_network_link(self, link_id: int) -> None:
        """
        Deletes a network link from the database.

        This function removes a network link identified by its ID.

        Args:
            link_id (int):
                The ID of the network link to delete.

        Returns:
            None
                This function does not return any value.
        """
        self.cursor.execute(f"DELETE FROM network_links WHERE id={link_id}")
        self.connection.commit()

    def get_network_links(self) -> list[dict[str, int]]:
        """
        Retrieves all network links from the database.

        This function fetches all network links, including their IDs and the IDs of the connected interfaces.

        Args:
            None:
                This function does not take any parameters.

        Returns:
            list[dict[str, int]]:
                A list of dictionaries, each representing a network link with its metadata.
        """
        self.cursor.execute("SELECT * FROM network_links")
        raw_data: list[tuple[int, int, int]] = self.cursor.fetchall()

        result: list[dict[str, int]] = []
        for link_id, interface_a, interface_b in raw_data:
            result.append(
                {"ID": link_id, "INTERFACE_A": interface_a, "INTERFACE_B": interface_b}
            )
        return result


def main() -> None:
    handler = DBHandler()
    handler.get_all_properties()


if __name__ == "__main__":
    main()
