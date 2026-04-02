from typing import TypedDict


class ErrorResponse(TypedDict):
    STATUS: str
    ERROR: Exception
    CODE: int


class PropertyListResponse(TypedDict):
    STATUS: str
    DATA: list[dict[str, str | int | None]] | None
    ERROR: None
    CODE: int


class TypeListResponse(TypedDict):
    STATUS: str
    DATA: list[dict[str, str | int | bool]] | None
    ERROR: None
    CODE: int


class EntityListResponse(TypedDict):
    STATUS: str
    DATA: list[dict[str, str]] | None
    ERROR: None
    CODE: int


class EntityValueListResponse(TypedDict):
    STATUS: str
    DATA: list[dict[str, str | int]] | None
    ERROR: None
    CODE: int


class SuccessResponse(TypedDict):
    STATUS: str
    ERROR: None
    CODE: int
