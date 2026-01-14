from typing import Protocol

from ...core import InterceptorContentType, InterceptorContentTypeRegistry
from .advertising import ADVERTISING_INTERCEPTOR_CT
from .greetings import GREETINGS_INTERCEPTOR_CT


class TypedInterceptorRegistryProtocol(Protocol):
    GREETINGS: InterceptorContentType
    ADVERTISING: InterceptorContentType


def _get_interceptor_content_types() -> list[InterceptorContentType]:
    return [GREETINGS_INTERCEPTOR_CT, ADVERTISING_INTERCEPTOR_CT]


class TypedInterceptorRegistry(InterceptorContentTypeRegistry, TypedInterceptorRegistryProtocol):
    pass


INTERCEPTOR_REGISTRY: TypedInterceptorRegistry = InterceptorContentTypeRegistry(
    interceptor_content_types=_get_interceptor_content_types(),
)


# Public API:We only export default interceptor registry
__all__ = [
    # Default interceptor registry
    "INTERCEPTOR_REGISTRY",
]
