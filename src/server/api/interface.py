from fastapi import FastAPI
import uvicorn
from backend.handler import DBHandler

app = FastAPI()
handler = DBHandler()


@app.get("/properties")
def list_properties() -> dict[str, str | list[dict[str, str | int | None]] | None]:
    data: list[dict[str, str | int | None]] = handler.get_all_properties()
    return {"status": "success", "data": data, "error": None}


@app.get("/entities")
def list_entities() -> dict[str, str | list[dict[str, str]] | None]:
    data: list[dict[str, str]] = handler.get_all_entities()
    return {"status": "success", "data": data, "error": None}


def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
