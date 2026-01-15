from dataclasses import dataclass
from typing import Literal


@dataclass
class EmojiesBar:
    type: Literal["emojies"] = "emojies"


@dataclass
class ButtonsBar:
    type: Literal["buttons"] = "buttons"
    buttons: list[str | None] | None = None


@dataclass
class ButtonsGrid:
    row_1: EmojiesBar | ButtonsBar | None = None
    row_2: ButtonsBar | None = None


