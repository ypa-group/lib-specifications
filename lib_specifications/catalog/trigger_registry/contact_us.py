from typing import Protocol, runtime_checkable

from ...core import MiniApp, Trigger


@runtime_checkable
class ContactUsMiniAppProtocol(Protocol):
    CUSTOMIZE: Trigger


class ContactUsMiniApp(MiniApp, ContactUsMiniAppProtocol):
    pass


CONTACT_US: ContactUsMiniApp = MiniApp(
    name="CONTACT_US",
    description="Contact Us MiniApp",
)


# Register "CUSTOMIZE" trigger
CONTACT_US.register_trigger(
    qualname="CUSTOMIZE",
    description="Contact us customize",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)
