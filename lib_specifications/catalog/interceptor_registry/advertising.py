from ...core import (
    BaseCallback,
    ContextSchema,
    InterceptorContentType,
    InterceptorContentTypeEnum,
    ParameterSchema,
    ParameterTypeEnum,
)
from ..callback_registry import CALLBACK_REGISTRY

context_schema = ContextSchema(
    parameters={
        "session.last_interaction_at": ParameterSchema(
            name="session.last_interaction_at",
            data_type=ParameterTypeEnum.DATETIME,
        )
    }
)

available_specifications: list[BaseCallback] = [
    CALLBACK_REGISTRY.isTimeAfter,
    CALLBACK_REGISTRY.hasOnboarded,
]

ADVERTISING_INTERCEPTOR_CT: InterceptorContentType = InterceptorContentType(
    name=InterceptorContentTypeEnum.ADVERTISING,
    description="Promotional content or advertisements",
    applicable_specifications=set(available_specifications),
    context_schema=context_schema,
)
