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
        self.cursor = self.connection.cursor()

    ## get entire datasets ##
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

    ## get specific data ##
    def get_values_of_entity(self, entity_id: str) -> list[dict[str, str | int]]:
        self.cursor.execute(
            f"SELECT * FROM entity_properties WHERE entity_id = '{entity_id}'"
        )
        entity_properties: list[tuple[str, int, str]] = self.cursor.fetchall()
        result: list[dict[str, str | int]] = []
        for entity_id, property_id, value in entity_properties:
            self.cursor.execute(f"SELECT * FROM properties WHERE id = '{property_id}'")
            property_data: tuple[int, str, str] = self.cursor.fetchone()

            result.append(
                {
                    "ENTITY_ID": entity_id,
                    "PROPERTY_ID": property_id,
                    "PROPERTY_NAME": property_data[1],
                    "PROPERTY_TYPE": property_data[2],
                    "PROPERTY_VALUE": value,
                }
            )
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
        self.cursor.execute(
            f"UPDATE entity_types SET name='{new_name}', network_relevant='{1 if new_is_network_relevant else 0}', WHERE id={type_id}"
        )
        self.connection.commit()

    def update_entity(self, entity_id: str, new_name: str) -> None:
        self.cursor.execute(
            f"UPDATE entities SET name='{new_name}' WHERE id='{entity_id}'"
        )
        self.connection.commit()

    ## delete Data ##
    def delete_property(self, property_id: int) -> None:
        self.cursor.execute(
            f"SELECT * FROM type_properties WHERE property_id={property_id}"
        )
        self.cursor.execute(
            f"SELECT * FROM entity_properties WHERE property_id={property_id}"
        )
        if self.cursor.fetchall() != []:
            raise RuntimeError(
                "Cannot delete property while records using this property already exist."
            )
        self.cursor.execute(f"DELETE FROM properties WHERE id={property_id}")
        self.connection.commit()

    def delete_type(self, type_id: int) -> None:
        self.cursor.execute(f"SELECT * FROM entities WHERE type_id={type_id}")
        self.cursor.execute(f"SELECT * FROM type_properties WHERE type_id={type_id}")
        self.cursor.execute(
            f"SELECT * FROM type_containment_rules WHERE parent_type={type_id} OR child_type={type_id}"
        )
        if self.cursor.fetchall() != []:
            raise RuntimeError(
                "Cannot delete type while records using this type already exist."
            )
        self.cursor.execute(f"DELETE FROM entity_types WHERE id={type_id}")
        self.connection.commit()

    def delete_entity(self, entity_id: str) -> None:
        self.cursor.execute(
            f"SELECT * FROM containment WHERE parent_id='{entity_id}' OR child_id='{entity_id}'"
        )
        self.cursor.execute(
            f"SELECT * FROM entity_properties WHERE entity_id='{entity_id}'"
        )
        self.cursor.execute(
            f"SELECT * FROM network_interfaces WHERE entity_id='{entity_id}'"
        )
        if self.cursor.fetchall() != []:
            raise RuntimeError(
                "Cannot delete entity while records using this entity already exist."
            )
        self.cursor.execute(f"DELETE FROM entities WHERE id='{entity_id}'")
        self.connection.commit()


def main() -> None:
    handler = DBHandler()
    handler.get_all_properties()


if __name__ == "__main__":
    main()
