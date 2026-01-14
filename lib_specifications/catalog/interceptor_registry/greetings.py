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


GREETINGS_INTERCEPTOR_CT = InterceptorContentType(
    name=InterceptorContentTypeEnum.GREETINGS,
    description="Welcome messages like 'Good day' or 'Hi again'",
    applicable_specifications=set(available_specifications),
    context_schema=context_schema,
)
