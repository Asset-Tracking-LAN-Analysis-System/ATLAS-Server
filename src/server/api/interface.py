from fastapi import FastAPI
import uvicorn
from server.backend.handler import DBHandler
from .types import (
    Containment,
    ContainmentListResponse,
    ContainmentRule,
    ContainmentRuleListResponse,
    Entity,
    EntityListResponse,
    EntityProperty,
    EntityPropertyListResponse,
    ErrorResponse,
    NetworkInterface,
    NetworkInterfaceListResponse,
    NetworkLink,
    NetworkLinkListResponse,
    SuccessResponse,
    Type,
    TypeListResponse,
    TypeProperty,
    TypePropertyListResponse,
    Property,
    PropertyListResponse,
)

app = FastAPI()
handler = DBHandler()


## get entire datasets ##
@app.get("/properties")
def list_properties() -> PropertyListResponse | ErrorResponse:
    try:
        data: list[Property] = [
            Property.model_validate(item) for item in handler.get_all_properties()
        ]
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None or data == [] or data == []:
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
        data: list[Type] = [
            Type.model_validate(item) for item in handler.get_all_types()
        ]
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None or data == []:
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
        data: list[Entity] = [
            Entity.model_validate(item) for item in handler.get_all_entities()
        ]
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None or data == []:
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


@app.post("/types")
def add_type(data: dict[str, str | bool]) -> SuccessResponse | ErrorResponse:
    try:
        name: str = str(data["NAME"])
        is_network_relevant: bool = bool(data["IS_NETWORK_RELEVANT"])
        handler.add_type(name, is_network_relevant)
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


@app.post("/entity")
def add_entity(data: dict[str, str | int]) -> SuccessResponse | ErrorResponse:
    try:
        name: str = str(data["NAME"])
        type_id: int = int(data["TYPE_ID"])
        handler.add_entity(type_id, name)
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


## update Data ##
@app.put("/property/{property_id}")
def update_property(
    property_id: int, data: dict[str, str]
) -> SuccessResponse | ErrorResponse:
    try:
        name: str = data["NAME"]
        data_type: str = data["DATA_TYPE"]
        handler.update_property(property_id, name, data_type)
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


@app.put("/type/{type_id}")
def update_type(
    type_id: int, data: dict[str, str | bool]
) -> SuccessResponse | ErrorResponse:
    try:
        name: str = str(data["NAME"])
        is_network_relevant: bool = bool(data["NETWORK_RELEVANT"])
        handler.update_type(type_id, name, is_network_relevant)
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


@app.put("/entity/{entity_id}")
def update_entity(
    entity_id: str, data: dict[str, str]
) -> SuccessResponse | ErrorResponse:
    try:
        name: str = data["NAME"]
        handler.update_entity(entity_id, name)
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


## delete Data ##
@app.delete("/property/{property_id}")
def delete_property(property_id: int) -> SuccessResponse | ErrorResponse:
    try:
        handler.delete_property(property_id)
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


@app.delete("/type/{type_id}")
def delete_type(type_id: int) -> SuccessResponse | ErrorResponse:
    try:
        handler.delete_type(type_id)
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


@app.delete("/entity/{entity_id}")
def delete_entity(entity_id: str) -> SuccessResponse | ErrorResponse:
    try:
        handler.delete_entity(entity_id)
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


#######################################
############## Properties #############
#######################################


## Property-Type ##
@app.post("/type_property")
def add_type_property(data: dict[str, int | bool]) -> SuccessResponse | ErrorResponse:
    try:
        type_id: int = int(data["TYPE_ID"])
        property_id: int = int(data["PROPERTY_ID"])
        required: bool = bool(data["REQUIRED"])
        handler.add_type_property(type_id, property_id, required)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.delete("/type_property/{type_id}/{property_id}")
def delete_type_property(
    type_id: int, property_id: int
) -> SuccessResponse | ErrorResponse:
    try:
        handler.delete_type_property(type_id, property_id)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.get("/type_properties")
def get_type_properties() -> TypePropertyListResponse | ErrorResponse:
    try:
        data: list[TypeProperty] = [
            TypeProperty.model_validate(item) for item in handler.get_type_properties()
        ]
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None:
            return TypePropertyListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=204,
            )
        else:
            return TypePropertyListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=200,
            )


## Entity-Property ##
@app.post("/entity_property")
def add_entity_property(data: dict[str, str | int]) -> SuccessResponse | ErrorResponse:
    try:
        entity_id: str = str(data["ENTITY_ID"])
        property_id: int = int(data["PROPERTY_ID"])
        value: str = str(data["VALUE"])
        handler.add_entity_property(entity_id, property_id, value)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.put("/entity_property/{entity_id}/{property_id}")
def update_entity_property(
    entity_id: str, property_id: int, data: dict[str, str]
) -> SuccessResponse | ErrorResponse:
    try:
        new_value: str = str(data["VALUE"])
        handler.update_entity_property(entity_id, property_id, new_value)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.delete("/entity_property/{entity_id}/{property_id}")
def delete_entity_property(
    entity_id: str, property_id: int
) -> SuccessResponse | ErrorResponse:
    try:
        handler.delete_entity_property(entity_id, property_id)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.get("/entity_properties")
def get_entity_properties() -> EntityPropertyListResponse | ErrorResponse:
    try:
        data: list[EntityProperty] = [
            EntityProperty.model_validate(item)
            for item in handler.get_entity_properties()
        ]
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None:
            return EntityPropertyListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=204,
            )
        else:
            return EntityPropertyListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=200,
            )


#######################################
############## Cointainment ###########
#######################################


## rules ##
@app.get("/containment_rules")
def list_containment_rules() -> ContainmentRuleListResponse | ErrorResponse:
    try:
        data: list[ContainmentRule] = [
            ContainmentRule.model_validate(item)
            for item in handler.get_containment_rules()
        ]
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None or data == []:
            return ContainmentRuleListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=204,
            )
        else:
            return ContainmentRuleListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=200,
            )


@app.post("/containment_rule")
def add_containment_rule(data: dict[str, int]) -> SuccessResponse | ErrorResponse:
    try:
        parent_type_id: int = int(data["PARENT_TYPE_ID"])
        child_type_id: int = int(data["CHILD_TYPE_ID"])
        handler.add_containment_rule(parent_type_id, child_type_id)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.delete("/containment_rule/{parent_type_id}/{child_type_id}")
def delete_containment_rule(
    parent_type_id: int, child_type_id: int
) -> SuccessResponse | ErrorResponse:
    try:
        handler.delete_containment_rule(parent_type_id, child_type_id)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.post("/containment")
def add_containment(data: dict[str, str | None]) -> SuccessResponse | ErrorResponse:
    try:
        parent_entity_id: str = str(data["PARENT_ID"])
        child_entity_id: str = str(data["CHILD_ID"])
        slot: str | None = data["SLOT"]
        handler.add_containment(parent_entity_id, child_entity_id, slot)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.put("/containment/{parent_entity_id}/{child_entity_id}")
def update_containment(
    parent_entity_id: str, child_entity_id: str, data: dict[str, str | None]
) -> SuccessResponse | ErrorResponse:
    try:
        new_slot: str | None = data["SLOT"]
        handler.update_containment(parent_entity_id, child_entity_id, new_slot)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.delete("/containment/{parent_entity_id}/{child_entity_id}")
def delete_containment(
    parent_entity_id: str, child_entity_id: str
) -> SuccessResponse | ErrorResponse:
    try:
        handler.delete_containment(parent_entity_id, child_entity_id)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.get("/containment")
def get_containment() -> ContainmentListResponse | ErrorResponse:
    try:
        data: list[Containment] = [
            Containment.model_validate(item) for item in handler.get_containment()
        ]
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None or data == []:
            return ContainmentListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=204,
            )
        else:
            return ContainmentListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=200,
            )


###################################
############## Network ############
###################################


## Network Interfaces ##
@app.post("/network_interface")
def add_network_interface(data: dict[str, str]) -> SuccessResponse | ErrorResponse:
    try:
        entity_id: str = str(data["ENTITY_ID"])
        interface_name: str = str(data["INTERFACE_NAME"])
        mac: str = str(data["MAC"])
        ip: str = str(data["IP"])
        handler.add_network_interface(entity_id, interface_name, mac, ip)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.put("/network_interface/{interface_id}")
def update_network_interface(
    interface_id: int, data: dict[str, str]
) -> SuccessResponse | ErrorResponse:
    try:
        new_entity_id: str = str(data["ENTITY_ID"])
        new_interface_name: str = str(data["INTERFACE_NAME"])
        new_mac: str = str(data["MAC"])
        new_ip: str = str(data["IP"])
        handler.update_network_interface(
            interface_id, new_entity_id, new_interface_name, new_mac, new_ip
        )
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.delete("/network_interface/{interface_id}")
def delete_network_interface(interface_id: int) -> SuccessResponse | ErrorResponse:
    try:
        handler.delete_network_interface(interface_id)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.get("/network_interfaces")
def get_network_interfaces() -> NetworkInterfaceListResponse | ErrorResponse:
    try:
        data: list[NetworkInterface] = [
            NetworkInterface.model_validate(item)
            for item in handler.get_network_interfaces()
        ]
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None:
            return NetworkInterfaceListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=204,
            )
        else:
            return NetworkInterfaceListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=200,
            )


## Network Links ##
@app.post("/network_link")
def add_network_link(data: dict[str, int]) -> SuccessResponse | ErrorResponse:
    try:
        interface_a: int = int(data["INTERFACE_A"])
        interface_b: int = int(data["INTERFACE_B"])
        handler.add_network_link(interface_a, interface_b)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.delete("/network_link/{link_id}")
def delete_network_link(link_id: int) -> SuccessResponse | ErrorResponse:
    try:
        handler.delete_network_link(link_id)
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        return SuccessResponse(STATUS="success", ERROR=None, CODE=201)


@app.get("/network_links")
def get_network_links() -> NetworkLinkListResponse | ErrorResponse:
    try:
        data: list[NetworkLink] = [
            NetworkLink.model_validate(item) for item in handler.get_network_links()
        ]
    except Exception as e:
        return ErrorResponse(
            STATUS="fail",
            ERROR_TYPE=type(e).__name__,
            ERROR_MESSAGE=str(e),
            CODE=500,
        )
    else:
        if data is None:
            return NetworkLinkListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=204,
            )
        else:
            return NetworkLinkListResponse(
                STATUS="success",
                DATA=data,
                ERROR=None,
                CODE=200,
            )


def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
