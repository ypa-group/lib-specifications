from dataclasses import dataclass
from typing import Literal

DrawerAppType = Literal[
    "app",
    "array",
    "assistant_corporation",
    "budget",
    "calculator",
    "credit_score",
    "contact_us",
    "freezing",
    "plaid",
]
DrawerScreenType = Literal["external", "internal"]


@dataclass
class DrawerScreenOption:
    value: str
    label: str

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "label": self.label,
        }


@dataclass
class DrawerScreen:
    value: str
    screen_type: DrawerScreenType
    label: str
    is_active: bool = True
    options: list[DrawerScreenOption] | None = None

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "screen_type": self.screen_type,
            "label": self.label,
            "is_active": self.is_active,
            "options": [option.to_dict() for option in self.options] if self.options else None,
        }


@dataclass
class DrawerApp:
    value: DrawerAppType
    label: str
    screens: dict[str, DrawerScreen]

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "label": self.label,
            "screens": {screen.value: screen.to_dict() for screen in self.screens.values()},
        }


class DrawerRegistry:
    def __init__(self, apps: list[DrawerApp]):
        self.apps = {app.value: app for app in apps}

    def get_app(self, value: DrawerAppType) -> DrawerApp:
        if value not in self.apps:
            raise ValueError(f"Invalid DrawerAppType: {value}. Must be one of {list(self.apps.keys())}")
        return self.apps[value]

    def get_screen(self, app_value: DrawerAppType, screen_value: str) -> DrawerScreen:
        app = self.get_app(app_value)
        if screen_value not in app.screens:
            raise ValueError(f"Invalid DrawerScreen: {screen_value}. Must be one of {list(app.screens.keys())}")
        return app.screens[screen_value]

    def get_all_apps(self) -> list[DrawerApp]:
        return list(self.apps.values())
