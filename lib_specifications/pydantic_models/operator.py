"""Pydantic model for operator information."""

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from ..core import ParameterTypeEnum


class PydanticOperatorInfo(BaseModel):
    """Information about an operator for serialization."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "equal",
                "symbol": "==",
                "compatible_types": ["str", "int", "float", "bool", "date", "datetime"],
            }
        },
    )

    name: str = Field(..., description="Operator name (e.g., 'equal', 'greater_than')")
    symbol: str = Field(..., description="Operator symbol for display (e.g., '==', '>')")
    compatible_types: list[ParameterTypeEnum] = Field(..., description="List of compatible parameter types")

    @field_validator("compatible_types", mode="before")
    @classmethod
    def validate_compatible_types(cls, v):
        """Convert list of strings to list of ParameterTypeEnum if needed."""
        if isinstance(v, list):
            return [ParameterTypeEnum.from_string(item) if isinstance(item, str) else item for item in v]
        return v

    @field_serializer("compatible_types", when_used="json")
    def serialize_compatible_types(self, value: list[ParameterTypeEnum], _info):
        """Serialize list of ParameterTypeEnum to list of string labels (only in JSON mode)."""
        return [item.label for item in value]
