from typing import Protocol, runtime_checkable

from ...core import MiniApp, Trigger


@runtime_checkable
class TimelyMiniAppProtocol(Protocol):
    ONBOARDING_APP_EXIT_LONG: Trigger
    ONBOARDING_APP_EXIT_SHORT: Trigger
    ONBOARDING_ARRAY_VERIFICATION_AFTER_24_HRS: Trigger
    ONBOARDING_COMPLETED_CARDS_NOT_LINKED: Trigger
    ONBOARDING_COMPLETED_CS_NOT_LINKED: Trigger
    ONBOARDING_COMPLETED_NOTHING_LINKED: Trigger
    ONBOARDING_EXIT_TO_GENERAL: Trigger


class TimelyMiniApp(MiniApp, TimelyMiniAppProtocol):
    pass


TIMELY: TimelyMiniApp = MiniApp(
    name="TIMELY",
    description="Timely MiniApp",
)


# Register "ONBOARDING_APP_EXIT_LONG" trigger
TIMELY.register_trigger(
    qualname="ONBOARDING_APP_EXIT_LONG",
    description="Onboarding app exit long",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "ONBOARDING_APP_EXIT_SHORT" trigger
TIMELY.register_trigger(
    qualname="ONBOARDING_APP_EXIT_SHORT",
    description="Onboarding app exit short",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "ONBOARDING_ARRAY_VERIFICATION_AFTER_24_HRS" trigger
TIMELY.register_trigger(
    qualname="ONBOARDING_ARRAY_VERIFICATION_AFTER_24_HRS",
    description="Onboarding array verification after 24 hrs",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "ONBOARDING_COMPLETED_CARDS_NOT_LINKED" trigger
TIMELY.register_trigger(
    qualname="ONBOARDING_COMPLETED_CARDS_NOT_LINKED",
    description="Onboarding completed cards not linked",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "ONBOARDING_COMPLETED_CS_NOT_LINKED" trigger
TIMELY.register_trigger(
    qualname="ONBOARDING_COMPLETED_CS_NOT_LINKED",
    description="Onboarding completed CS not linked",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "ONBOARDING_COMPLETED_NOTHING_LINKED" trigger
TIMELY.register_trigger(
    qualname="ONBOARDING_COMPLETED_NOTHING_LINKED",
    description="Onboarding completed nothing linked",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "ONBOARDING_EXIT_TO_GENERAL" trigger
TIMELY.register_trigger(
    qualname="ONBOARDING_EXIT_TO_GENERAL",
    description="Onboarding exit to general",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)
