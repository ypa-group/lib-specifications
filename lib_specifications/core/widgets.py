from dataclasses import dataclass
from typing import Literal
from uuid import UUID

WidgetType = Literal["language_selector",]


@dataclass(kw_only=True)
class BaseWidget:
    id: UUID
    widget_type: WidgetType


# Widget types
@dataclass
class LanguageSelectorWidget:
    """Language selector widget."""

    id: UUID
    widget_type: Literal["language_selector"] = "language_selector"
