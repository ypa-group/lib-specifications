"""Callback catalog for pre-defined callbacks."""

from typing import Protocol, get_args, get_origin, get_type_hints

from ...core import BaseCallback, CallbackRegistry
from .datetime_callbacks import (
    IsDateInRangeCallback,
    IsDayAfterTodayCallback,
    IsDayBeforeTodayCallback,
    IsDayNotLaterThanCallback,
    IsDayOfMonthCallback,
    IsFutureDateCallback,
    IsSameDayOfWeekCallback,
    IsSameMonthCallback,
    IsSameYearCallback,
    IsTimeAfterCallback,
    IsTodayCallback,
    IsWithinDaysCallback,
)
from .user_callbacks import (
    HasArrayInitializedCallback,
    HasConnectedCreditCardCallback,
    HasCreditScoreCallback,
    HasOnboardedCallback,
    HasPlaidInitializedCallback,
)


class TypedCallbackRegistryProtocol(Protocol):
    isToday: type[IsTodayCallback]
    isDayAfterToday: type[IsDayAfterTodayCallback]
    isDayBeforeToday: type[IsDayBeforeTodayCallback]
    isDateInRange: type[IsDateInRangeCallback]
    isDayNotLaterThan: type[IsDayNotLaterThanCallback]
    isFutureDate: type[IsFutureDateCallback]
    isWithinDays: type[IsWithinDaysCallback]
    isSameDayOfWeek: type[IsSameDayOfWeekCallback]
    isDayOfMonth: type[IsDayOfMonthCallback]
    isSameMonth: type[IsSameMonthCallback]
    isSameYear: type[IsSameYearCallback]
    isTimeAfter: type[IsTimeAfterCallback]
    hasOnboarded: type[HasOnboardedCallback]
    hasPlaidInitialized: type[HasPlaidInitializedCallback]
    hasConnectedCreditCard: type[HasConnectedCreditCardCallback]
    hasArrayInitialized: type[HasArrayInitializedCallback]
    hasCreditScore: type[HasCreditScoreCallback]


def _get_callback_classes() -> list[type[BaseCallback]]:
    hints = get_type_hints(TypedCallbackRegistryProtocol)
    classes = []
    for hint in hints.values():
        # Extract the actual class from type[Class] annotation
        origin = get_origin(hint)
        if origin is type:
            # For type[X], get_args returns (X,)
            args = get_args(hint)
            if args:
                classes.append(args[0])
            else:
                # Fallback: if no args, try using hint directly
                classes.append(hint)
        else:
            # If it's not a type annotation, use it directly
            classes.append(hint)
    return classes


class TypedCallbackRegistry(CallbackRegistry, TypedCallbackRegistryProtocol):
    pass


CALLBACK_REGISTRY: TypedCallbackRegistry = CallbackRegistry(list(_get_callback_classes()))

# Public API:We only export default callback registry
__all__ = [
    # Default callback registry
    "CALLBACK_REGISTRY",
]
