from __future__ import annotations

from .callback import BaseCallback
from .parameters import ContextSchema


class Trigger:
    """Trigger definition.

    Args:
        - `mini_app`: MiniApp that the trigger belongs to.
        - `qualname`: Qualname of the trigger.
        - `description`: Description of the trigger.
        - `context_schema`: Context schema of the trigger.
        - `applicable_callbacks`: Callbacks that the trigger applies to.
        - `is_deprecated`: Whether the trigger is deprecated.
    """

    def __init__(
        self,
        mini_app: MiniApp,
        qualname: str,
        description: str | None = None,
        context_schema: ContextSchema | None = None,
        applicable_callbacks: set[BaseCallback] | None = None,
        is_deprecated: bool = False,
    ):
        self.mini_app = mini_app
        self.qualname = qualname
        self.description = description
        self.context_schema = context_schema
        self.applicable_callbacks = applicable_callbacks
        self.is_deprecated = is_deprecated

    @property
    def qualname(self) -> str:
        return self._qualname

    @qualname.setter
    def qualname(self, value: str) -> None:
        if not value:
            raise ValueError("Qualname must not be empty")
        if "__" in value:
            raise ValueError("Qualname must not contain double underscores")
        self._qualname = value

    @property
    def fullname(self) -> str:
        """Get the full Trigger qualname including MiniApp."""
        return f"{self.mini_app.name}__{self.qualname}"

    def __str__(self) -> str:
        return self.fullname

    def to_dict(self) -> dict:
        if self.applicable_callbacks:
            callbacks = [callback.qualname for callback in self.applicable_callbacks]
        else:
            callbacks = []
        return {
            "fullname": self.fullname,
            "mini_app": self.mini_app.to_dict(),
            "qualname": self.qualname,
            "description": self.description,
            "context_schema": self.context_schema.to_dict() if self.context_schema else None,
            "applicable_callbacks": callbacks,
            "is_deprecated": self.is_deprecated,
        }


class MiniApp:
    """MiniApp definition.

    Args:
        - `name`: Name of the MiniApp.
        - `triggers`: Triggers belonging to the MiniApp.
    """

    def __init__(
        self,
        name: str,
        description: str | None = None,
    ):
        # Validate name during initialization
        if not name:
            raise ValueError("MiniApp name must not be empty")
        if "__" in name:
            raise ValueError("MiniApp name must not contain double underscores")
        self._name = name
        self.description = description
        self._triggers: dict[str, Trigger] = {}

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value:
            raise ValueError("MiniApp name must not be empty")
        if "__" in value:
            raise ValueError("MiniApp name must not contain double underscores")

        self._name = value

    def __str__(self) -> str:
        return self.name

    def __getattr__(self, name: str) -> Trigger:
        """Allow accessing triggers by their qualname as attributes.

        Example:
            MINI_APP.GENERIC  # Returns the generic trigger
        """
        if name not in self._triggers:
            raise AttributeError(f"Trigger '{name}' not found in the '{self.name}' miniapp")
        return self._triggers[name]

    def __dir__(self) -> list[str]:
        """Return list of available attributes including all trigger qualnames."""
        return sorted(set(super().__dir__()) | set(self._triggers.keys()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MiniApp):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
        }

    def register_trigger(
        self,
        *,
        qualname: str,
        description: str | None = None,
        context_schema: ContextSchema | None = None,
        applicable_callbacks: set[BaseCallback] | None = None,
        is_deprecated: bool = False,
    ) -> None:
        trigger = Trigger(
            mini_app=self,
            qualname=qualname,
            description=description,
            context_schema=context_schema,
            applicable_callbacks=applicable_callbacks,
            is_deprecated=is_deprecated,
        )
        self._triggers[trigger.qualname] = trigger

    def get_triggers(self) -> list[Trigger]:
        """Get all triggers."""
        return list(self._triggers.values())


class TriggerRegistry:
    """Registry for managing available MiniApps and Triggers.
    Triggers are batch registered via MiniApp.

    Args:
        - `miniapps`: List of MiniApps to register.
    """

    def __init__(self, miniapps: list[MiniApp]):
        self._miniapps: dict[str, MiniApp] = {miniapp.name: miniapp for miniapp in miniapps}
        self._triggers: dict[str, Trigger] = {
            trigger.fullname: trigger for miniapp in miniapps for trigger in miniapp.get_triggers()
        }

    def get_miniapp_by_name(self, name: str) -> MiniApp:
        """Get a MiniApp by name."""
        if name not in self._miniapps:
            raise ValueError(f"Invalid MiniApp: {name}. Must be one of {list(self._miniapps.keys())}")
        return self._miniapps[name]

    def get_all_miniapps(self) -> list[MiniApp]:
        """Get all available miniapps."""
        return list(self._miniapps.values())

    def get_trigger_by_fullname(self, fullname: str) -> Trigger:
        """Get a trigger by full qualname."""
        if fullname not in self._triggers:
            raise ValueError(f"Invalid trigger: fullname={fullname}. Must be one of {list(self._triggers.keys())}")
        return self._triggers[fullname]

    def get_all_triggers(self) -> list[Trigger]:
        """Get all available triggers."""
        return list(self._triggers.values())

    def __getattr__(self, name: str) -> MiniApp | None:
        """Allow accessing miniapps by their name as attributes.

        Example:
            MINI_APP_REGISTRY.BUDGET  # Returns the budget miniapp
        """
        if name in self._miniapps:
            return self._miniapps[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'. "
            f"Available miniapps: {', '.join(sorted(self._miniapps.keys()))}"
        )

    def __dir__(self) -> list[str]:
        """Return list of available attributes including all miniapp names."""
        return sorted(set(super().__dir__()) | set(self._miniapps.keys()))
