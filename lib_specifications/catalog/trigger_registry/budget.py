from typing import Protocol, runtime_checkable

from ...core import MiniApp, Trigger


@runtime_checkable
class BudgetMiniAppProtocol(Protocol):
    GENERIC: Trigger
    CUSTOMIZE: Trigger


class BudgetMiniApp(MiniApp, BudgetMiniAppProtocol):
    pass


BUDGET: BudgetMiniApp = MiniApp(
    name="BUDGET",
    description="Budget MiniApp",
)


# Register "CUSTOMIZE" trigger
BUDGET.register_trigger(
    qualname="CUSTOMIZE",
    description="Budget customize",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "GENERIC" trigger
BUDGET.register_trigger(
    qualname="GENERIC",
    description="Budget generic",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)
