"""Base specification classes."""

from abc import ABCMeta, abstractmethod


class BaseSpecification(metaclass=ABCMeta):
    """Base class for all specifications.

    Provides logical combinators (AND/OR/NOT) for building complex rules.
    Specifications don't have is_satisfied_by - that's implemented in evaluators.
    """

    @abstractmethod
    def describe(self) -> str:
        """Return human-readable description of this specification.

        Returns:
            String description of the rule
        """
        pass

    def __and__(self, other: "BaseSpecification") -> "BaseSpecification":
        """Combine with AND logic."""
        return AndSpecification(self, other)

    def __or__(self, other: "BaseSpecification") -> "BaseSpecification":
        """Combine with OR logic."""
        return OrSpecification(self, other)

    def __invert__(self) -> "BaseSpecification":
        """Negate with NOT logic."""
        return NotSpecification(self)


class AndSpecification(BaseSpecification):
    """Specification combining two specs with AND logic."""

    def __init__(
        self,
        left: BaseSpecification,
        right: BaseSpecification,
    ):
        self.left = left
        self.right = right

    def describe(self):
        return f"({self.left.describe()} AND {self.right.describe()})"


class OrSpecification(BaseSpecification):
    """Specification combining two specs with OR logic."""

    def __init__(
        self,
        left: BaseSpecification,
        right: BaseSpecification,
    ):
        self.left = left
        self.right = right

    def describe(self):
        return f"({self.left.describe()} OR {self.right.describe()})"


class NotSpecification(BaseSpecification):
    """Specification negating another spec with NOT logic."""

    def __init__(self, spec: BaseSpecification):
        self.spec = spec

    def describe(self):
        return f"NOT ({self.spec.describe()})"
