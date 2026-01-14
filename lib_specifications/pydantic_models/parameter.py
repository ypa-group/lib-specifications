"""Pydantic models for parameter values."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, field_serializer, field_validator

from ..core import ParameterTypeEnum


class PydanticParameterPathValue(BaseModel):
    """Parameter that extracts value from data using a path."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "parameter_type": "path",
                "data_type": "int",
                "value": "user.age",
            }
        },
    )

    parameter_type: Literal["path"] = "path"
    data_type: ParameterTypeEnum = Field(..., description="Parameter data type")
    value: str = Field(..., description="Path to extract from data (e.g., 'user.id')")

    @field_validator("data_type", mode="before")
    @classmethod
    def validate_data_type(cls, v):
        """Convert string to ParameterTypeEnum if needed."""
        if isinstance(v, str):
            return ParameterTypeEnum.from_string(v)
        return v

    @field_serializer("data_type", when_used="json")
    def serialize_data_type(self, value: ParameterTypeEnum, _info):
        """Serialize ParameterTypeEnum to its string label (only in JSON mode)."""
        return value.label


class PydanticParameterLiteralValue(BaseModel):
    """Parameter that uses a literal value."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "parameter_type": "value",
                "data_type": "int",
                "value": 18,
            }
        },
    )

    parameter_type: Literal["value"] = "value"
    data_type: ParameterTypeEnum = Field(..., description="Parameter data type")
    value: Any = Field(..., description="Literal value (e.g., 18, 'hello')")

    @field_validator("data_type", mode="before")
    @classmethod
    def validate_data_type(cls, v):
        """Convert string to ParameterTypeEnum if needed."""
        if isinstance(v, str):
            return ParameterTypeEnum.from_string(v)
        return v

    @field_serializer("data_type", when_used="json")
    def serialize_data_type(self, value: ParameterTypeEnum, _info):
        """Serialize ParameterTypeEnum to its string label (only in JSON mode)."""
        return value.label


# Union type for parameter values
_PydanticParameterValueUnion = PydanticParameterPathValue | PydanticParameterLiteralValue

# TypeAdapter for validation with discriminator
_PydanticParameterValueAdapter = TypeAdapter(
    Annotated[
        _PydanticParameterValueUnion,
        Field(discriminator="parameter_type"),
    ]
)

# PydanticParameterValue: Annotated union type for use in type annotations
PydanticParameterValue = Annotated[
    _PydanticParameterValueUnion,
    Field(discriminator="parameter_type"),
]
