from dataclasses import dataclass
from enum import Enum, auto

from .callback import BaseCallback
from .parameters import ContextSchema


class InterceptorContentTypeEnum(str, Enum):
    """
    Types of interceptors that can interrupt scenario flow.

    Interceptors are shown to users between node transitions based on
    conditions like time elapsed, daily limits, etc.
    """

    def _generate_next_value_(name, start, count, last_values):
        return name

    GREETINGS = auto()  # Welcome messages like "Good day" or "Hi again"
    ADVERTISING = auto()  # Promotional content or advertisements


@dataclass
class InterceptorContentType:
    name: InterceptorContentTypeEnum
    description: str | None = None
    applicable_specifications: set[BaseCallback] | None = None
    context_schema: ContextSchema | None = None

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        if self.applicable_specifications:
            specs = []
            for spec in self.applicable_specifications:
                specs.append(spec.qualname)
        else:
            specs = []
        return {
            "name": self.name,
            "description": self.description,
            "applicable_specifications": specs,
            "context_schema": self.context_schema.to_dict() if self.context_schema else None,
        }


class InterceptorContentTypeRegistry:
    """Registry for managing available InterceptorContentTypes.

    Args:
        - `interceptor_content_types`: List of InterceptorContentTypes to register.
    """

    def __init__(self, interceptor_content_types: list[InterceptorContentType]):
        self._interceptor_content_types: dict[str, InterceptorContentType] = {
            interceptor_content_type.name: interceptor_content_type
            for interceptor_content_type in interceptor_content_types
        }

    def get_by_name(self, name: str) -> InterceptorContentType:
        """Get an InterceptorContentType by name."""
        if name not in self._interceptor_content_types:
            raise ValueError(
                f"Invalid InterceptorContentType: {name}. Must be one of {list(self._interceptor_content_types.keys())}"
            )
        return self._interceptor_content_types[name]

    def get_all(self) -> list[InterceptorContentType]:
        """Get all available interceptor content types."""
        return list(self._interceptor_content_types.values())

    def __getattr__(self, name: str) -> InterceptorContentType:
        """Get an InterceptorContentType by name."""
        if name not in self._interceptor_content_types:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'. "
                f"Available interceptor content types: {', '.join(sorted(self._interceptor_content_types.keys()))}"
            )
        return self._interceptor_content_types[name]

    def __dir__(self) -> list[str]:
        """Return list of available attributes including all interceptor content type names."""
        return sorted(set(super().__dir__()) | set(self._interceptor_content_types.keys()))
