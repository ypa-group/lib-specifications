"""Field specification for comparing field values."""

from .base import BaseSpecification
from .operators import get_operator
from .parameters import ParameterPathValue, ParameterValue


class FieldSpecification(BaseSpecification):
    """Specification for comparing a field value.

    Compares a field (always a path) against either another field (path) or a literal value.

    Args:
        field: ParameterPathValue - the field to compare (always a path)
        operator: str - operator name (e.g., "equal", "greater_than")
        compare_to: ParameterValue - what to compare against (path or literal value)
    """

    def __init__(
        self,
        field: ParameterPathValue,
        operator: str,
        compare_to: ParameterValue,
    ):
        """Initialize field specification.

        Args:
            field: ParameterPathValue - the field path to compare
            operator: Operator name (e.g., "equal", "greater_than")
            compare_to: ParameterValue - what to compare against (path or literal)
        """
        self.field = field
        self.operator = operator
        self.compare_to = compare_to

    def describe(self) -> str:
        """Return human-readable description."""
        field_path = self.field["value"]
        operator = get_operator(self.operator)
        if self.compare_to["parameter_type"] == "path":
            compare_to_path = self.compare_to["value"]
            return f"{field_path} {operator.symbol} {compare_to_path}"
        else:
            compare_to_value = self.compare_to["value"]
            return f"{field_path} {operator.symbol} {compare_to_value}"
