import sqlite3
import os
from vshc.database.utils import detect_id_gap
from pathlib import Path
from .helper import get_first_free_serial


class DBHandler:
    def __init__(self) -> None:
        self.db_path: str = os.path.join(
            str(Path(__file__).resolve().parent), "..", "data", "atlas.db"
        )
        self.connection = sqlite3.Connection(self.db_path, check_same_thread=False)
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    ## get data ##
    def get_all_properties(self) -> list[dict[str, str | int | None]]:
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
        self.cursor.execute("SELECT * FROM entity_types")
        raw_data: list[tuple[int, str, int]] = self.cursor.fetchall()
        result: list[dict[str, str | int | bool]] = []
        for id, name, network_relevant in raw_data:
            result.append(
                {"ID": id, "NAME": name, "NETWORK_RELEVANT": network_relevant == 1}
            )
        return result

    def get_all_entities(self) -> list[dict[str, str]]:
        self.cursor.execute("SELECT * FROM entities")
        raw_data: list[tuple[str, int, int, str, str]] = self.cursor.fetchall()
        result: list[dict[str, str]] = []
        for entry in raw_data:
            result.append({"ID": entry[0], "NAME": entry[3]})
        return result

    ## add Data ##
    def add_property(self, name: str, data_type: str) -> None:
        """
        type can be text, float, int or bool
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
        gap: int = detect_id_gap(self.cursor, "entity_types", "id")
        self.cursor.execute(
            "INSERT INTO entity_types (id, name, network_relevant) VALUES (?, ?, ?)",
            (gap, name, 1 if is_network_relevant else 0),
        )
        self.connection.commit()

    def add_entity(self, type_id: int, name: str) -> None:
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
        self.cursor.execute(
            f"UPDATE entities SET name='{new_name}' WHERE id='{entity_id}'"
        )
        self.connection.commit()

    ## delete Data ##
    def delete_property(self, property_id: int) -> None:
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
        self.cursor.execute(
            "INSERT INTO type_properties (type_id, property_id, required) VALUES (?, ?, ?)",
            (type_id, property_id, 1 if required else 0),
        )
        self.connection.commit()

    def delete_type_property(self, type_id: int, property_id: int) -> None:
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
        self.cursor.execute(
            "INSERT INTO entity_properties (entity_id, property_id, value) VALUES (?, ?, ?)",
            (entity_id, property_id, value),
        )
        self.connection.commit()

    def update_entity_property(
        self, entity_id: str, property_id: int, new_value: str
    ) -> None:
        self.cursor.execute(
            f"UPDATE entity_properties SET value='{new_value}' WHERE entity_id='{entity_id}' AND property_id={property_id}"
        )
        self.connection.commit()

    def delete_entity_property(self, entity_id: str, property_id: int) -> None:
        self.cursor.execute(
            f"DELETE FROM entity_properties WHERE entity_id='{entity_id}' AND property_id={property_id}"
        )
        self.connection.commit()

    def get_entity_properties(self) -> list[dict[str, str | int]]:
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
        self.cursor.execute(
            "INSERT INTO type_containment_rules (parent_type, child_type) VALUES (?, ?)",
            (parent_type_id, child_type_id),
        )
        self.connection.commit()

    def delete_containment_rule(self, parent_type_id: int, child_type_id: int) -> None:
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
        self.cursor.execute(
            f"SELECT * FROM containment WHERE child_id='{child_entity_id}'"
        )
        if self.cursor.fetchall() != []:
            raise RuntimeError(
                "Can't add entry, since child is allready bind in another parent."
            )
        self.cursor.execute(
            "INSERT INTO containment (parent_id, child_id, slot) VALUES (?, ?, ?)",
            (parent_entity_id, child_entity_id, slot),
        )
        self.connection.commit()

    def update_containment(
        self, parent_entity_id: str, child_entity_id: str, new_slot: str | None
    ) -> None:
        self.cursor.execute(
            f"UPDATE containment SET slot='{new_slot}' WHERE parent_id='{parent_entity_id}' AND child_id='{child_entity_id}'"
        )
        self.connection.commit()

    def delete_containment(self, parent_entity_id: str, child_entity_id: str) -> None:
        self.cursor.execute(
            f"DELETE FROM containment WHERE parent_id='{parent_entity_id}' AND child_id='{child_entity_id}'"
        )
        self.connection.commit()

    def get_containment(self) -> list[dict[str, str | None]]:
        self.cursor.execute("SELECT * FROM containment")
        raw_data: list[tuple[str, str, str | None]] = self.cursor.fetchall()

        result: list[dict[str, str | None]] = []
        for parent, child, slot in raw_data:
            result.append({"PARENT": parent, "CHILD": child, "SLOT": slot})
        return result

    ###################################
    ############## Network ############
    ###################################

    ## Network Interfaces ##
    def add_network_interface(
        self, entity_id: str, interface_name: str, mac: str, ip: str
    ) -> None:
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
        self.cursor.execute(
            f"UPDATE network_interfaces SET entity_id='{new_entity_id}', interface_name='{new_interface_name}', mac='{new_mac}', ip='{new_ip}' WHERE id={interface_id}"
        )
        self.connection.commit()

    def delete_network_interface(self, interface_id: int) -> None:
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
        self.cursor.execute("SELECT * FROM network_interfaces")
        raw_data: list[tuple[int, str, str, str, str]] = self.cursor.fetchall()

        result: list[dict[str, str | int]] = []
        for interface_id, entity_id, interface_name, mac, ip in raw_data:
            result.append(
                {
                    "ID": interface_id,
                    "ENTITY_ID": entity_id,
                    "INTERFACE_NAME": interface_name,
                    "MAC": mac,
                    "IP": ip,
                }
            )
        return result

    ## Network Links ##
    def add_network_link(self, interface_a: int, interface_b: int) -> None:
        self.cursor.execute(
            "INSERT INTO network_links (id, interface_a, interface_b) VALUES (?, ?, ?)",
            (detect_id_gap(self.cursor, "network_links"), interface_a, interface_b),
        )
        self.connection.commit()

    def delete_network_link(self, link_id: int) -> None:
        self.cursor.execute(f"DELETE FROM network_links WHERE id={link_id}")
        self.connection.commit()

    def get_network_links(self) -> list[dict[str, int]]:
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
