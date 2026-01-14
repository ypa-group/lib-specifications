from typing import Protocol, runtime_checkable

from ...core import MiniApp, Trigger


@runtime_checkable
class CreditScoreMiniAppProtocol(Protocol):
    CUSTOMIZE: Trigger
    GENERIC: Trigger


class CreditScoreMiniApp(MiniApp, CreditScoreMiniAppProtocol):
    pass


CREDIT_SCORE: CreditScoreMiniApp = MiniApp(
    name="CREDIT_SCORE",
    description="Credit Score MiniApp",
)


# Register "CUSTOMIZE" trigger
CREDIT_SCORE.register_trigger(
    qualname="CUSTOMIZE",
    description="Credit score customize",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)


# Register "GENERIC" trigger
CREDIT_SCORE.register_trigger(
    qualname="GENERIC",
    description="Credit score generic",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)
