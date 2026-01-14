import inspect
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any, Literal, TypedDict


# Parameter value types
class ParameterPathValue(TypedDict):
    """Parameter that extracts value from data using a path."""

    parameter_type: Literal["path"]
    data_type: str  # ParameterTypeEnum label (e.g., "int", "str")
    value: str  # Path to extract from data (e.g., "user.id")


class ParameterLiteralValue(TypedDict):
    """Parameter that uses a literal value."""

    parameter_type: Literal["value"]
    data_type: str  # ParameterTypeEnum label (e.g., "int", "str")
    value: Any  # Literal value (e.g., 18, "hello")


ParameterValue = ParameterPathValue | ParameterLiteralValue


class ParameterTypeEnum(Enum):
    """Enum for parameter types.

    Each enum member stores a tuple of (string_value, python_type).
    You can access:
    - The string value via .value[0] or str(enum_member)
    - The Python type via .type or .value[1]

    Example:
        >>> ParameterTypeEnum.STR.value[0]  # "str"
        >>> ParameterTypeEnum.STR.type       # <class 'str'>
        >>> str(ParameterTypeEnum.STR)       # "str"
    """

    STR = ("str", str)
    INT = ("int", int)
    FLOAT = ("float", float)
    BOOL = ("bool", bool)
    DATE = ("date", date)
    DATETIME = ("datetime", datetime)
    LIST = ("list", list)
    DICT = ("dict", dict)

    def __str__(self) -> str:
        return self.label

    @property
    def python_type(self) -> type:
        """Return the Python type of the parameter type."""
        return self.value[1]

    @property
    def label(self) -> str:
        """Return the string value of the parameter type."""
        return self.value[0]

    @classmethod
    def from_string(cls, value: str) -> "ParameterTypeEnum":
        """Get enum member from string value."""
        for member in cls:
            if member.value[0] == value:
                return member
        raise ValueError(f"No ParameterTypeEnum member with string value '{value}'")

    @classmethod
    def from_type(cls, python_type: type) -> "ParameterTypeEnum":
        """Get enum member from Python type."""
        for member in cls:
            if member.value[1] == python_type:
                return member
        raise ValueError(f"No ParameterTypeEnum member with type '{python_type}'")

    def get_dummy_value(self) -> Any:
        """Get a dummy value for this parameter type.

        Used to instantiate callbacks for abstract detection when required
        parameters don't have defaults.

        Returns:
            A dummy value appropriate for the type

        Example:
            >>> ParameterTypeEnum.INT.get_dummy_value()  # 1
            >>> ParameterTypeEnum.STR.get_dummy_value()  # ""
        """
        if self == ParameterTypeEnum.INT:
            return 1
        elif self == ParameterTypeEnum.STR:
            return ""
        elif self == ParameterTypeEnum.FLOAT:
            return 0.0
        elif self == ParameterTypeEnum.BOOL:
            return False
        elif self == ParameterTypeEnum.DICT:
            return {}
        elif self == ParameterTypeEnum.LIST:
            return []
        elif self == ParameterTypeEnum.DATE:
            return date(2025, 1, 1)
        elif self == ParameterTypeEnum.DATETIME:
            return datetime(2025, 1, 1)
        else:
            # Fallback to None for unknown types
            return None


@dataclass
class ParameterSchema:
    """Schema for a single parameter which should be extracted from a callable.

    Example:
        >>> ParameterSchema(
        ...    name="age",
        ...    data_type=ParameterTypeEnum.INT,
        ...    required=True,
        ...    default=18,
        ... )
    """

    name: str  # Parameter name
    data_type: ParameterTypeEnum  # Parameter data type
    required: bool = True  # Whether the parameter is required
    default: Any | None = None  # Default value for the parameter

    def __post_init__(self):
        # If a default value is provided, the parameter should be optional
        if self.required and self.default is not None:
            raise ValueError("Default value is not allowed for required parameters")

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "data_type": self.data_type.label,
            "required": self.required,
            "default": self.default,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ParameterSchema":
        data_type = data.get("data_type")
        if not data_type:
            raise ValueError("data_type is required")
        try:
            data_type = ParameterTypeEnum.from_string(data_type)
        except ValueError:
            raise ValueError(f"Invalid data_type: {data_type}") from None

        # If default is provided, parameter is optional unless explicitly required=True
        default = data.get("default")
        required = data.get("required", default is None)

        return cls(
            name=data["name"],
            data_type=data_type,
            required=required,
            default=default,
        )


@dataclass
class SignatureSchema:
    """Schema for parameters which should be extracted from a callable.

    Example:
        >>> SignatureSchema(
        ...    parameters={
        ...        "age": ParameterSchema(
        ...            name="age",
        ...            data_type=ParameterTypeEnum.INT,
        ...            required=True,
        ...            default=18,
        ...        ),
        ...        "name": ParameterSchema(
        ...            name="name",
        ...            data_type=ParameterTypeEnum.STR,
        ...            required=False,
        ...            default="John Doe",
        ...        ),
        ...    },
        ... )
    """

    parameters: dict[str, ParameterSchema]

    def get_parameter(self, parameter_name: str) -> ParameterSchema | None:
        return self.parameters.get(parameter_name)

    def has_parameter(self, parameter_name: str) -> bool:
        return self.get_parameter(parameter_name) is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "parameters": {name: parameter.to_dict() for name, parameter in self.parameters.items()},
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SignatureSchema":
        parameters_data = data.get("parameters", {})
        if not isinstance(parameters_data, dict):
            raise ValueError("parameters must be a dictionary")
        parameters = {}
        for name, parameter_data in parameters_data.items():
            if not isinstance(parameter_data, dict):
                raise ValueError(f"parameter {name} must be a dictionary")
            parameters[name] = ParameterSchema.from_dict(parameter_data)
        return cls(parameters=parameters)


def generate_signature_from_callable(callable: Callable) -> SignatureSchema:
    """
    Automatically generate SignatureSchema from a callable using inspect.

    This function extracts parameter information from the callable's signature:
    - Parameter names become the name
    - Parameter types are mapped to ParameterTypeEnum
    - Required flag is used to determine if the parameter is required
    - Default values are used to determine default value

    Args:
        callable: The callable to analyze

    Returns:
        SignatureSchema with automatically generated ParameterSchema entries

    Raises:
        ValueError: If the callable contains **kwargs or *args parameters

    Example:
        >>> def is_adult(age: int, min_age: int = 18) -> bool:
        ...     return age >= min_age
        ...
        >>> schema = generate_signature_from_callable(is_adult)
        >>> # schema.parameters["age"] has name="age", required=True, default=18
        >>> # schema.parameters["min_age"] has name="min_age", required=False, default=18
    """
    sig = inspect.signature(callable)
    parameters = {}

    for param_name, param in sig.parameters.items():
        # Skip 'self' parameter (for bound methods)
        if param_name == "self":
            continue

        # Disallow VAR_KEYWORD parameters (**kwargs) - only fixed, typed params allowed
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            raise ValueError(
                f"Callable {callable.__name__} contains **kwargs parameter '{param_name}'. "
                "Only fixed, typed parameters are allowed."
            )

        # Disallow VAR_POSITIONAL parameters (*args) - only fixed, typed params allowed
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            raise ValueError(
                f"Callable {callable.__name__} contains *args parameter '{param_name}'. "
                "Only fixed, typed parameters are allowed."
            )

        # Get parameter type from annotation
        param_type = param.annotation
        if param_type == inspect.Parameter.empty:
            raise ValueError(f"No annotation for parameter {param_name}")

        # Map Python type to ParameterTypeEnum
        try:
            data_type = ParameterTypeEnum.from_type(param_type)
        except ValueError:
            raise ValueError(f"Invalid type for parameter {param_name}: {param_type}") from None

        # Check if parameter is required
        required = True
        default = None
        if param.default != inspect.Parameter.empty:
            required = False
            default = param.default

        parameters[param_name] = ParameterSchema(
            name=param_name,
            data_type=data_type,
            required=required,
            default=default,
        )

    return SignatureSchema(parameters=parameters)


@dataclass
class ContextSchema:
    """Schema for a context which should be extracted from a callable.
    Allow paths for parameters.
    Example:
        >>> context = {
        ...     "user": {
        ...         "age": 18,
        ...         "name": "John Doe",
        ...     },
        ... }
        >>> ContextSchema(
        ...    parameters={
        ...        "user.age": ParameterSchema(
        ...            name="user.age",
        ...            data_type=ParameterTypeEnum.INT,
        ...            required=True,
        ...            default=18,
        ...        ),
        ...        "user.name": ParameterSchema(
        ...            name="user.name",
        ...            data_type=ParameterTypeEnum.STR,
        ...            required=False,
        ...            default="John Doe",
        ...        ),
        ...    },
        ... )
    """

    parameters: dict[str, ParameterSchema]

    def to_dict(self) -> dict[str, Any]:
        return {
            "parameters": {name: parameter.to_dict() for name, parameter in self.parameters.items()},
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContextSchema":
        parameters_data = data.get("parameters", {})
        if not isinstance(parameters_data, dict):
            raise ValueError("parameters must be a dictionary")
        parameters = {}
        for name, parameter_data in parameters_data.items():
            if not isinstance(parameter_data, dict):
                raise ValueError(f"parameter {name} must be a dictionary")
            parameters[name] = ParameterSchema.from_dict(parameter_data)
        return cls(parameters=parameters)
