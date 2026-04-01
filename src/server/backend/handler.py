import sqlite3
import os
from vshc.database.utils import detect_id_gap
from pathlib import Path


class DBHandler:
    def __init__(self) -> None:
        self.db_path: str = os.path.join(
            str(Path(__file__).resolve().parent), "..", "data", "atlas.db"
        )
        self.connection = sqlite3.Connection(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    ## get entire data-sets ##
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
    def get_values_of_entity(self, entity_id: str):
        self.cursor.execute(
            f"SELECT * FROM entity_properties WHERE entity_id = '{entity_id}'"
        )
        entity_properties: list[tuple[str, int, str]] = self.cursor.fetchall()
        # TODO: finish

    ## add Data ##
    def add_property(self, name: str, type: str) -> None:
        """
        type can be text, float, int or bool
        """
        gap: int = detect_id_gap(self.cursor, "properties", "id")
        self.cursor.execute(
            "INSERT INTO properties (id, name, data_type) VALUES (?, ?, ?)",
            (gap, name, type),
        )
        self.connection.commit()


def main() -> None:
    handler = DBHandler()
    handler.get_all_properties()


if __name__ == "__main__":
    main()
