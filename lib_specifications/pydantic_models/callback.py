"""Pydantic model for callback information."""

from pydantic import BaseModel, ConfigDict, Field

from .parameter_schema import PydanticSignatureSchema


class PydanticCallbackInfo(BaseModel):
    """Information about a callback for serialization."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "is_weekend",
                "signature": {
                    "parameters": {
                        "date": {
                            "name": "date",
                            "data_type": "date",
                            "required": True,
                            "default": None,
                        }
                    }
                },
            }
        },
    )

    name: str = Field(..., description="Callback name")
    signature: PydanticSignatureSchema = Field(..., description="Callback signature schema")
