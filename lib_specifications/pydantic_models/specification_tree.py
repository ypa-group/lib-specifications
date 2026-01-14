"""Pydantic models for specification trees."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from .parameter import PydanticParameterValue


class PydanticSpecificationNode(BaseModel):
    """Base node in specification tree."""

    type: Literal["leaf", "and", "or", "not"] = Field(..., description="Node type")


class PydanticSpecificationFieldLeafNode(PydanticSpecificationNode):
    """Field comparison leaf node.

    Compares a field (always a path) against either another field (path) or a literal value.
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.age",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 18,
                },
            }
        },
    )

    type: Literal["leaf"] = "leaf"
    subtype: Literal["field"] = "field"
    name: str = Field(..., description="Operator name (e.g., 'equal', 'greater_than')")
    field: str = Field(..., description="Field name (path), supports dot notation (e.g., 'user.profile.age')")
    compare_to: PydanticParameterValue = Field(
        ..., description="What to compare against - can be path or literal value"
    )


class PydanticSpecificationCallbackLeafNode(PydanticSpecificationNode):
    """Callback leaf node.

    Each parameter can be either a path (to extract from data) or a literal value.
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "type": "leaf",
                "subtype": "callback",
                "name": "is_weekend",
                "params": {
                    "date": {
                        "parameter_type": "path",
                        "data_type": "date",
                        "value": "event.date",
                    },
                },
            }
        },
    )

    type: Literal["leaf"] = "leaf"
    subtype: Literal["callback"] = "callback"
    name: str = Field(..., description="Callback name (e.g., 'isWeekend')")
    params: dict[str, PydanticParameterValue] = Field(
        ...,
        description="Parameters for callback function, key is the parameter name, "
        "value is either path or literal value",
    )


PydanticSpecificationLeafNode = Annotated[
    PydanticSpecificationFieldLeafNode | PydanticSpecificationCallbackLeafNode,
    Field(discriminator="subtype"),
]


class PydanticSpecificationAndNode(PydanticSpecificationNode):
    """AND combinator node.

    Both left and right must be satisfied.
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "type": "and",
                "left": {
                    "type": "leaf",
                    "subtype": "field",
                    "name": "greater_than_or_equal",
                    "field": "user.age",
                    "compare_to": {
                        "parameter_type": "value",
                        "data_type": "int",
                        "value": 18,
                    },
                },
                "right": {
                    "type": "leaf",
                    "subtype": "field",
                    "name": "equal",
                    "field": "user.status",
                    "compare_to": {
                        "parameter_type": "value",
                        "data_type": "str",
                        "value": "active",
                    },
                },
            }
        },
    )

    type: Literal["and"] = "and"
    left: "PydanticSpecificationTree" = Field(..., description="Left specification tree")
    right: "PydanticSpecificationTree" = Field(..., description="Right specification tree")


class PydanticSpecificationOrNode(PydanticSpecificationNode):
    """OR combinator node.

    Either left or right must be satisfied.
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "type": "or",
                "left": {
                    "type": "leaf",
                    "subtype": "field",
                    "name": "equal",
                    "field": "user.status",
                    "compare_to": {
                        "parameter_type": "value",
                        "data_type": "str",
                        "value": "active",
                    },
                },
                "right": {
                    "type": "leaf",
                    "subtype": "field",
                    "name": "equal",
                    "field": "user.status",
                    "compare_to": {
                        "parameter_type": "value",
                        "data_type": "str",
                        "value": "premium",
                    },
                },
            }
        },
    )

    type: Literal["or"] = "or"
    left: "PydanticSpecificationTree" = Field(..., description="Left specification tree")
    right: "PydanticSpecificationTree" = Field(..., description="Right specification tree")


class PydanticSpecificationNotNode(PydanticSpecificationNode):
    """NOT combinator node.

    Negates the child specification.
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "type": "not",
                "child": {
                    "type": "leaf",
                    "subtype": "field",
                    "name": "equal",
                    "field": "user.banned",
                    "compare_to": {
                        "parameter_type": "value",
                        "data_type": "bool",
                        "value": True,
                    },
                },
            }
        },
    )

    type: Literal["not"] = "not"
    child: "PydanticSpecificationTree" = Field(..., description="Child specification tree to negate")


PydanticSpecificationTree = Annotated[
    PydanticSpecificationLeafNode
    | PydanticSpecificationAndNode
    | PydanticSpecificationOrNode
    | PydanticSpecificationNotNode,
    Field(discriminator="type"),
]

# Update forward references
PydanticSpecificationAndNode.model_rebuild()
PydanticSpecificationOrNode.model_rebuild()
PydanticSpecificationNotNode.model_rebuild()
