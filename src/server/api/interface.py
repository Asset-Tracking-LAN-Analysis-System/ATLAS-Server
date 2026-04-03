from fastapi import FastAPI
import uvicorn
from backend.handler import DBHandler
from .types import (
    ErrorResponse,
    PropertyListResponse,
    TypeListResponse,
    EntityListResponse,
    EntityValueListResponse,
    SuccessResponse,
)

app = FastAPI()
handler = DBHandler()


## get entire datasets ##
@app.get("/properties")
def list_properties() -> PropertyListResponse | ErrorResponse:
    try:
        data: list[dict[str, str | int | None]] = handler.get_all_properties()
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None:
            return PropertyListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=204,
            )
        else:
            return PropertyListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=200,
            )


@app.get("/types")
def list_types() -> TypeListResponse | ErrorResponse:
    try:
        data: list[dict[str, str | int | bool]] = handler.get_all_types()
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None:
            return TypeListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=204,
            )
        else:
            return TypeListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=200,
            )


@app.get("/entities")
def list_entities() -> EntityListResponse | ErrorResponse:
    try:
        data: list[dict[str, str]] = handler.get_all_entities()
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None:
            return EntityListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=204,
            )
        else:
            return EntityListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=200,
            )


## get specific data ##
@app.get("/entity/{entity_id}")
def list_values_of_entity(entity_id: str) -> EntityValueListResponse | ErrorResponse:
    try:
        data: list[dict[str, str | int]] = handler.get_values_of_entity(entity_id)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None:
            return EntityValueListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=204,
            )
        else:
            return EntityValueListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=200,
            )


## add Data ##
@app.post("/property")
def add_property(data: dict[str, str]) -> SuccessResponse | ErrorResponse:
    try:
        name: str = data["NAME"]
        data_type: str = data["TYPE"]
        handler.add_property(name, data_type)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(
            STATUS="success",
            ERROR=None,
            CODE=201,
        )


def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
