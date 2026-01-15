from typing import Protocol, runtime_checkable

from ...core import MiniApp, Trigger


@runtime_checkable
class WelcomeMiniAppProtocol(Protocol):
    INTRO: Trigger
    MORNING: Trigger
    DAY: Trigger
    EVENING: Trigger
    NIGHT: Trigger
    REPEATEDLY: Trigger
    RARELY: Trigger


class WelcomeMiniApp(MiniApp, WelcomeMiniAppProtocol):
    pass


WELCOME: WelcomeMiniApp = MiniApp(
    name="WELCOME",
    description="Welcome MiniApp",
)


# Register "INTRO" trigger
WELCOME.register_trigger(
    qualname="INTRO",
    description="Initial onboarding introduction screen",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "MORNING" trigger
WELCOME.register_trigger(
    qualname="MORNING",
    description="Welcome morning",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "DAY" trigger
WELCOME.register_trigger(
    qualname="DAY",
    description="Welcome day",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "EVENING" trigger
WELCOME.register_trigger(
    qualname="EVENING",
    description="Welcome evening",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "NIGHT" trigger
WELCOME.register_trigger(
    qualname="NIGHT",
    description="Welcome night",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "REPEATEDLY" trigger
WELCOME.register_trigger(
    qualname="REPEATEDLY",
    description="Welcome repeatedly",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "RARELY" trigger
WELCOME.register_trigger(
    qualname="RARELY",
    description="Welcome rarely",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)
