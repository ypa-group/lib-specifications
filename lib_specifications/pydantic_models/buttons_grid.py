from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PydanticEmojiesBar(BaseModel):
    """Emojies bar (pydantic model)"""

    model_config = ConfigDict(from_attributes=True)

    type: Literal["emojies"] = Field(default="emojies")


class PydanticButtonsBar(BaseModel):
    """Buttons bar (pydantic model)"""

    model_config = ConfigDict(from_attributes=True)

    type: Literal["buttons"] = Field(default="buttons")
    buttons: list[str | None] | None = Field(default=None)


class PydanticButtonsGrid(BaseModel):
    """Buttons grid (pydantic model)"""

    model_config = ConfigDict(from_attributes=True)

    row_1: PydanticEmojiesBar | PydanticButtonsBar | None = Field(default=None)
    row_2: PydanticButtonsBar | None = Field(default=None)
