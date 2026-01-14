from typing import Protocol, runtime_checkable

from ...core import MiniApp, Trigger


@runtime_checkable
class CalculatorMiniAppProtocol(Protocol):
    CUSTOMIZE: Trigger
    GENERIC: Trigger


class CalculatorMiniApp(MiniApp, CalculatorMiniAppProtocol):
    pass


CALCULATOR: CalculatorMiniApp = MiniApp(
    name="CALCULATOR",
    description="Calculator MiniApp",
)


# Register "CUSTOMIZE" trigger
CALCULATOR.register_trigger(
    qualname="CUSTOMIZE",
    description="Calculator customize",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "GENERIC" trigger
CALCULATOR.register_trigger(
    qualname="GENERIC",
    description="Calculator generic",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)
