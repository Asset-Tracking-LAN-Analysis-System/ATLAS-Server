import sqlite3


def get_first_free_serial(cursor: sqlite3.Cursor, type_id: int) -> int:
    """
    Find the first free serial number for a given type_id.

    Example:
    Existing serials: 0, 1, 2, 4
    Result: 3
    """

    cursor.execute(
        """
        SELECT serial
        FROM entities
        WHERE type_id = ?
        ORDER BY serial ASC
        """,
        (type_id,),
    )

    expected = 0

    for (serial,) in cursor.fetchall():
        if serial != expected:
            return expected
        expected += 1

    return expected
