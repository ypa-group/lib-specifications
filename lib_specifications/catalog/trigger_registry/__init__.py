from typing import Protocol

from ...core import MiniApp, TriggerRegistry
from .budget import BUDGET, BudgetMiniApp
from .calculator import CALCULATOR, CalculatorMiniApp
from .contact_us import CONTACT_US, ContactUsMiniApp
from .credit_score import CREDIT_SCORE, CreditScoreMiniApp
from .general import GENERAL, GeneralMiniApp
from .onboarding import ONBOARDING, OnboardingMiniApp
from .timely import TIMELY, TimelyMiniApp
from .welcome import WELCOME, WelcomeMiniApp


class TypedTriggerRegistryProtocol(Protocol):
    BUDGET: BudgetMiniApp
    CALCULATOR: CalculatorMiniApp
    GENERAL: GeneralMiniApp
    CONTACT_US: ContactUsMiniApp
    CREDIT_SCORE: CreditScoreMiniApp
    TIMELY: TimelyMiniApp
    WELCOME: WelcomeMiniApp
    ONBOARDING: OnboardingMiniApp


def _get_mini_app_classes() -> list[MiniApp]:
    return [
        GENERAL,
        WELCOME,
        TIMELY,
        BUDGET,
        CALCULATOR,
        CREDIT_SCORE,
        CONTACT_US,
        ONBOARDING,
    ]


class TypedTriggerRegistry(TriggerRegistry, TypedTriggerRegistryProtocol):
    pass


TRIGGER_REGISTRY: TypedTriggerRegistry = TriggerRegistry(list(_get_mini_app_classes()))


# Public API:We only export default trigger registry
__all__ = [
    # Default trigger registry
    "TRIGGER_REGISTRY",
]
