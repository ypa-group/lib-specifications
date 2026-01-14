from abc import ABC, abstractmethod
from typing import Any

from .parameters import ParameterTypeEnum

__all__ = [
    "Operator",
    "OperatorRegistry",
    "EqualOperator",
    "NotEqualOperator",
    "GreaterThanOperator",
    "LessThanOperator",
    "GreaterThanOrEqualOperator",
    "LessThanOrEqualOperator",
    "ContainsOperator",
    "StartsWithOperator",
    "EndsWithOperator",
    "get_operator",
    "list_operators",
]


class Operator(ABC):
    """Base class for comparison operators.

    Operators define how to compare two values in specifications.
    Each operator has a name, symbol, and compatible parameter types.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Operator name (e.g., 'equal', 'greater_than')."""
        pass

    @property
    @abstractmethod
    def symbol(self) -> str:
        """Operator symbol for display (e.g., '==', '>')."""
        pass

    @property
    @abstractmethod
    def compatible_types(self) -> list[ParameterTypeEnum]:
        """List of parameter types this operator is compatible with."""
        pass

    @abstractmethod
    def compare(self, left: Any, right: Any) -> bool:
        """Compare two values.

        Args:
            left: Left operand value
            right: Right operand value

        Returns:
            True if comparison is satisfied
        """
        pass

    def is_compatible_with(self, parameter_type: ParameterTypeEnum) -> bool:
        """Check if operator is compatible with parameter type.

        Args:
            parameter_type: Parameter type to check

        Returns:
            True if compatible
        """
        return parameter_type in self.compatible_types


class EqualOperator(Operator):
    """Equality comparison operator (==)."""

    @property
    def name(self) -> str:
        return "equal"

    @property
    def symbol(self) -> str:
        return "=="

    @property
    def compatible_types(self) -> list[ParameterTypeEnum]:
        return [
            ParameterTypeEnum.STR,
            ParameterTypeEnum.INT,
            ParameterTypeEnum.FLOAT,
            ParameterTypeEnum.BOOL,
            ParameterTypeEnum.DATE,
            ParameterTypeEnum.DATETIME,
        ]

    def compare(self, left: Any, right: Any) -> bool:
        """Check if left equals right."""
        return left == right


class NotEqualOperator(Operator):
    """Inequality comparison operator (!=)."""

    @property
    def name(self) -> str:
        return "not_equal"

    @property
    def symbol(self) -> str:
        return "!="

    @property
    def compatible_types(self) -> list[ParameterTypeEnum]:
        return [
            ParameterTypeEnum.STR,
            ParameterTypeEnum.INT,
            ParameterTypeEnum.FLOAT,
            ParameterTypeEnum.BOOL,
            ParameterTypeEnum.DATE,
            ParameterTypeEnum.DATETIME,
        ]

    def compare(self, left: Any, right: Any) -> bool:
        """Check if left does not equal right."""
        return left != right


class GreaterThanOperator(Operator):
    """Greater than comparison operator (>)."""

    @property
    def name(self) -> str:
        return "greater_than"

    @property
    def symbol(self) -> str:
        return ">"

    @property
    def compatible_types(self) -> list[ParameterTypeEnum]:
        return [
            ParameterTypeEnum.INT,
            ParameterTypeEnum.FLOAT,
            ParameterTypeEnum.DATE,
            ParameterTypeEnum.DATETIME,
        ]

    def compare(self, left: Any, right: Any) -> bool:
        """Check if left is greater than right."""
        return left > right


class LessThanOperator(Operator):
    """Less than comparison operator (<)."""

    @property
    def name(self) -> str:
        return "less_than"

    @property
    def symbol(self) -> str:
        return "<"

    @property
    def compatible_types(self) -> list[ParameterTypeEnum]:
        return [
            ParameterTypeEnum.INT,
            ParameterTypeEnum.FLOAT,
            ParameterTypeEnum.DATE,
            ParameterTypeEnum.DATETIME,
        ]

    def compare(self, left: Any, right: Any) -> bool:
        """Check if left is less than right."""
        return left < right


class GreaterThanOrEqualOperator(Operator):
    """Greater than or equal comparison operator (>=)."""

    @property
    def name(self) -> str:
        return "greater_than_or_equal"

    @property
    def symbol(self) -> str:
        return ">="

    @property
    def compatible_types(self) -> list[ParameterTypeEnum]:
        return [
            ParameterTypeEnum.INT,
            ParameterTypeEnum.FLOAT,
            ParameterTypeEnum.DATE,
            ParameterTypeEnum.DATETIME,
        ]

    def compare(self, left: Any, right: Any) -> bool:
        """Check if left is greater than or equal to right."""
        return left >= right


class LessThanOrEqualOperator(Operator):
    """Less than or equal comparison operator (<=)."""

    @property
    def name(self) -> str:
        return "less_than_or_equal"

    @property
    def symbol(self) -> str:
        return "<="

    @property
    def compatible_types(self) -> list[ParameterTypeEnum]:
        return [
            ParameterTypeEnum.INT,
            ParameterTypeEnum.FLOAT,
            ParameterTypeEnum.DATE,
            ParameterTypeEnum.DATETIME,
        ]

    def compare(self, left: Any, right: Any) -> bool:
        """Check if left is less than or equal to right."""
        return left <= right


class ContainsOperator(Operator):
    """Contains comparison operator (in)."""

    @property
    def name(self) -> str:
        return "contains"

    @property
    def symbol(self) -> str:
        return "IN"

    @property
    def compatible_types(self) -> list[ParameterTypeEnum]:
        return [ParameterTypeEnum.STR, ParameterTypeEnum.LIST]

    def compare(self, left: Any, right: Any) -> bool:
        """Check if left contains right."""
        if left is None:
            return False
        return right in left


class StartsWithOperator(Operator):
    """Starts with comparison operator."""

    @property
    def name(self) -> str:
        return "starts_with"

    @property
    def symbol(self) -> str:
        return "STARTS WITH"

    @property
    def compatible_types(self) -> list[ParameterTypeEnum]:
        return [ParameterTypeEnum.STR]

    def compare(self, left: Any, right: Any) -> bool:
        """Check if left starts with right."""
        if not isinstance(left, str):
            return False
        return left.startswith(right)


class EndsWithOperator(Operator):
    """Ends with comparison operator."""

    @property
    def name(self) -> str:
        return "ends_with"

    @property
    def symbol(self) -> str:
        return "ENDS WITH"

    @property
    def compatible_types(self) -> list[ParameterTypeEnum]:
        return [ParameterTypeEnum.STR]

    def compare(self, left: Any, right: Any) -> bool:
        """Check if left ends with right."""
        if not isinstance(left, str):
            return False
        return left.endswith(right)


class OperatorRegistry:
    """Registry for managing operators."""

    def __init__(self):
        """Initialize empty registry."""
        self._operators: dict[str, Operator] = {}

    def register(self, operator: Operator) -> None:
        """Register an operator.

        Args:
            operator: Operator instance to register
        """
        self._operators[operator.name] = operator

    def get(self, name: str) -> Operator | None:
        """Get operator by name.

        Args:
            name: Operator name

        Returns:
            Operator instance or None if not found
        """
        return self._operators.get(name)

    def list_names(self) -> list[str]:
        """List all registered operator names.

        Returns:
            List of operator names
        """
        return list(self._operators.keys())

    def get_compatible_operators(self, parameter_type: ParameterTypeEnum) -> list[str]:
        """Get operators compatible with a parameter type.

        Args:
            parameter_type: Parameter type to check

        Returns:
            List of compatible operator names
        """
        return [op.name for op in self._operators.values() if op.is_compatible_with(parameter_type)]


# Registry instance
_operator_registry = OperatorRegistry()

# Register all operators
_operator_registry.register(EqualOperator())
_operator_registry.register(NotEqualOperator())
_operator_registry.register(GreaterThanOperator())
_operator_registry.register(LessThanOperator())
_operator_registry.register(GreaterThanOrEqualOperator())
_operator_registry.register(LessThanOrEqualOperator())
_operator_registry.register(ContainsOperator())
_operator_registry.register(StartsWithOperator())
_operator_registry.register(EndsWithOperator())


# Public API
def get_operator(name: str) -> Operator | None:
    """Get operator by name.

    Args:
        name: Operator name (e.g., "equal", "greater_than")

    Returns:
        Operator instance or None if not found
    """
    return _operator_registry.get(name)


def list_operators() -> list[str]:
    """List all registered operator names.

    Returns:
        List of operator names
    """
    return _operator_registry.list_names()
