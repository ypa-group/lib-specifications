"""Pydantic models for data transfer and serialization."""

from .callback import PydanticCallbackInfo
from .operator import PydanticOperatorInfo
from .parameter import (
    PydanticParameterLiteralValue,
    PydanticParameterPathValue,
    _PydanticParameterValueAdapter,
)
from .parameter import (
    PydanticParameterValue as _PydanticParameterValueType,
)
from .parameter_schema import PydanticParameterSchema, PydanticSignatureSchema
from .specification_tree import (
    PydanticSpecificationAndNode,
    PydanticSpecificationCallbackLeafNode,
    PydanticSpecificationFieldLeafNode,
    PydanticSpecificationLeafNode,
    PydanticSpecificationNode,
    PydanticSpecificationNotNode,
    PydanticSpecificationOrNode,
    PydanticSpecificationTree,
)


# Create a class that works both as a type annotation and has model_validate
# When used as a type annotation, Pydantic will use __get_pydantic_core_schema__
# When used as a class, it has model_validate for tests
class PydanticParameterValue:
    """Discriminated union type for parameter values.

    Can be used as a type annotation in Pydantic models.
    Has model_validate method for standalone validation (for tests).
    """

    @staticmethod
    def model_validate(obj, *, from_attributes=False):
        """Validate and return a PydanticParameterPathValue or PydanticParameterLiteralValue."""
        return _PydanticParameterValueAdapter.validate_python(obj, from_attributes=from_attributes)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """Tell Pydantic how to handle this type when used in annotations."""
        # Return the schema for the Annotated union type
        return handler(_PydanticParameterValueType)


__all__ = [
    # Parameters
    "PydanticParameterValue",
    "PydanticParameterPathValue",
    "PydanticParameterLiteralValue",
    # Parameter Schemas
    "PydanticParameterSchema",
    "PydanticSignatureSchema",
    # Specification Tree
    "PydanticSpecificationTree",
    "PydanticSpecificationNode",
    "PydanticSpecificationLeafNode",
    "PydanticSpecificationFieldLeafNode",
    "PydanticSpecificationCallbackLeafNode",
    "PydanticSpecificationAndNode",
    "PydanticSpecificationOrNode",
    "PydanticSpecificationNotNode",
    # Operator
    "PydanticOperatorInfo",
    # Callback
    "PydanticCallbackInfo",
]
