from pydantic import BaseModel


class ErrorResponse(BaseModel):
    STATUS: str
    ERROR_TYPE: str
    ERROR_MESSAGE: str
    CODE: int


class PropertyListResponse(BaseModel):
    STATUS: str
    DATA: list[dict[str, str | int | None]] | None
    ERROR: None
    CODE: int


class TypeListResponse(BaseModel):
    STATUS: str
    DATA: list[dict[str, str | int | bool]] | None
    ERROR: None
    CODE: int


class EntityListResponse(BaseModel):
    STATUS: str
    DATA: list[dict[str, str]] | None
    ERROR: None
    CODE: int


class ContainmentRuleListResponse(BaseModel):
    STATUS: str
    DATA: list[dict[str, int]] | None
    ERROR: None
    CODE: int


class ContainmentListResponse(BaseModel):
    STATUS: str
    DATA: list[dict[str, str | None]] | None
    ERROR: None
    CODE: int


class TypePropertyListResponse(BaseModel):
    STATUS: str
    DATA: list[dict[str, int | bool]] | None
    ERROR: None
    CODE: int


class EntityPropertyListResponse(BaseModel):
    STATUS: str
    DATA: list[dict[str, str | int]] | None
    ERROR: None
    CODE: int


class NetworkInterfaceListResponse(BaseModel):
    STATUS: str
    DATA: list[dict[str, str | int]] | None
    ERROR: None
    CODE: int


class NetworkLinkListResponse(BaseModel):
    STATUS: str
    DATA: list[dict[str, int]] | None
    ERROR: None
    CODE: int


class SuccessResponse(BaseModel):
    STATUS: str
    ERROR: None
    CODE: int
