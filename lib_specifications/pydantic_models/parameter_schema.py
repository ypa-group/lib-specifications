"""Pydantic models for parameter schemas."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from ..core import ParameterSchema, ParameterTypeEnum, SignatureSchema


class PydanticParameterSchema(BaseModel):
    """Schema for a single parameter extracted from a callable."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "age",
                "data_type": "int",
                "required": True,
                "default": None,
            }
        },
    )

    name: str = Field(..., description="Parameter name")
    data_type: ParameterTypeEnum = Field(..., description="Parameter data type label (e.g., 'int', 'str')")
    required: bool = Field(default=True, description="Whether the parameter is required")
    default: Any | None = Field(default=None, description="Default value for the parameter")

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

    def to_internal(self):
        """Convert to ParameterSchema dataclass."""

        return ParameterSchema(
            name=self.name,
            data_type=self.data_type,  # Already a ParameterTypeEnum
            required=self.required,
            default=self.default,
        )


class PydanticSignatureSchema(BaseModel):
    """Schema for parameters extracted from a callable."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "parameters": {
                    "age": {
                        "name": "age",
                        "data_type": "int",
                        "required": True,
                        "default": None,
                    },
                    "name": {
                        "name": "name",
                        "data_type": "str",
                        "required": False,
                        "default": "John Doe",
                    },
                }
            }
        },
    )

    parameters: dict[str, PydanticParameterSchema] = Field(
        ..., description="Dictionary mapping parameter names to parameter schemas"
    )

    def to_internal(self):
        """Convert to internal SignatureSchema dataclass."""

        return SignatureSchema(parameters={name: param.to_internal() for name, param in self.parameters.items()})
