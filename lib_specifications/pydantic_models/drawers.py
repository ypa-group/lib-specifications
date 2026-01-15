from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator

from ..core import DrawerScreenType


class PydanticDrawerOption(BaseModel):
    """Information about a drawer option for serialization."""

    model_config = ConfigDict(from_attributes=True)

    value: str = Field(..., description="Drawer option value")
    label: str = Field(..., description="Drawer option label")


class PydanticDrawerScreen(BaseModel):
    """Information about a drawer screen for serialization."""

    model_config = ConfigDict(from_attributes=True)

    value: str = Field(..., description="Drawer screen value")
    type: DrawerScreenType = Field(
        ...,
        description="Drawer screen type",
        alias=AliasChoices("type", "screen_type"),
    )
    is_active: bool = Field(default=True, description="Whether the drawer screen is active")
    label: str = Field(..., description="Drawer screen label")
    options: list[PydanticDrawerOption] | None = Field(default=None, description="Drawer screen options")

    @field_validator("options", mode="before")
    @classmethod
    def validate_options(cls, v):
        """Convert list of strings or dicts to list of PydanticDrawerOption if needed."""
        if v is None:
            return v
        if isinstance(v, list):
            if len(v) == 0:
                return v
            # If already PydanticDrawerOption objects, return as-is
            if isinstance(v[0], PydanticDrawerOption):
                return v
            # If list contains strings, convert them to PydanticDrawerOption
            if isinstance(v[0], str):
                return [PydanticDrawerOption(value=item, label=item) for item in v]
            # If list contains dicts, convert them to PydanticDrawerOption
            if isinstance(v[0], dict):
                return [PydanticDrawerOption.model_validate(item) for item in v]
            # If list contains DrawerScreenOption objects, convert them
            from ..core import DrawerScreenOption

            if isinstance(v[0], DrawerScreenOption):
                return [PydanticDrawerOption.model_validate(item, from_attributes=True) for item in v]
            # Otherwise, let Pydantic handle it
            return v
        return v


class PydanticDrawerApp(BaseModel):
    """Information about a drawer app for serialization."""

    model_config = ConfigDict(from_attributes=True)

    value: str = Field(..., description="Drawer app value")
    label: str = Field(..., description="Drawer app label")
    screens: list[PydanticDrawerScreen] = Field(..., description="Drawer app screens")

    @field_validator("screens", mode="before")
    @classmethod
    def validate_screens(cls, v):
        """Convert dict or list of strings/dicts to list of PydanticDrawerScreen if needed."""
        if v is None:
            return v
        # Handle dict (from DrawerApp.screens which is a dict)
        if isinstance(v, dict):
            return list(v.values())
        # Handle list
        if isinstance(v, list):
            if len(v) == 0:
                return v
            # If already PydanticDrawerScreen objects, return as-is
            if isinstance(v[0], PydanticDrawerScreen):
                return v
            # If list contains strings, convert them to PydanticDrawerScreen
            if isinstance(v[0], str):
                return [PydanticDrawerScreen(value=item, type="external", label=item) for item in v]
            # If list contains dicts, convert them to PydanticDrawerScreen
            if isinstance(v[0], dict):
                return [PydanticDrawerScreen.model_validate(item) for item in v]
            # If list contains DrawerScreen objects, convert them
            from ..core import DrawerScreen

            if isinstance(v[0], DrawerScreen):
                return [PydanticDrawerScreen.model_validate(item, from_attributes=True) for item in v]
            # Otherwise, let Pydantic handle it
            return v
        return v
