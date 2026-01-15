from typing import Protocol, runtime_checkable

from ...core import MiniApp, Trigger


@runtime_checkable
class GeneralMiniAppProtocol(Protocol):
    GENERAL_NEWS: Trigger


class GeneralMiniApp(MiniApp, GeneralMiniAppProtocol):
    pass


GENERAL: GeneralMiniApp = MiniApp(
    name="GENERAL",
    description="General MiniApp",
)


# Register "GENERAL_NEWS" trigger
GENERAL.register_trigger(
    qualname="GENERAL_NEWS",
    description="Home General news",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)
