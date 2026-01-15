import uuid
from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from ..core.actions import ActionType


class PydanticBaseAction(BaseModel):
    """Base action (pydantic model)"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    type: ActionType = Field(alias=AliasChoices("type", "action_type"))
    is_default: bool | None = Field(default=False)
    is_final: bool | None = Field(default=False)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    context: dict | None = Field(default_factory=dict)
    tracking_metadata: dict | None = Field(default=None)


class PydanticDrawerAction(PydanticBaseAction):
    """Drawer action (pydantic model)"""

    model_config = ConfigDict(from_attributes=True)

    type: Literal["drawer"] = Field(default="drawer", alias=AliasChoices("type", "action_type"))
    code: str | None = Field(default=None, min_length=1)
    on_close: Literal["refetch_node", "finish_scenario"] | None = Field(default=None)


class PydanticToTriggerAction(PydanticBaseAction):
    """To trigger action (pydantic model)"""

    model_config = ConfigDict(from_attributes=True)

    type: Literal["to_trigger"] = Field(default="to_trigger", alias=AliasChoices("type", "action_type"))
    trigger_id: str | None = Field(
        None,
        description="Qualname of the trigger to move to",
    )


class PydanticChangeAssistantAction(PydanticBaseAction):
    """Change assistant action (pydantic model)"""

    model_config = ConfigDict(from_attributes=True)

    type: Literal["change_assistant"] = Field(default="change_assistant", alias=AliasChoices("type", "action_type"))
    assistant_id: uuid.UUID | None = Field(
        default=None,
        description="UUID of the assistant to change to",
    )


class PydanticRepeatTransitionAction(PydanticBaseAction):
    model_config = ConfigDict(from_attributes=True)

    type: Literal["repeat_transition"] = Field(default="repeat_transition", alias=AliasChoices("type", "action_type"))
    parent_transition: Literal["default", "not_default"] | uuid.UUID | None = Field(
        default=None,
        description="UUID of the transition to repeat",
    )


class PydanticFinishAction(PydanticBaseAction):
    """Finish action (pydantic model)"""

    model_config = ConfigDict(from_attributes=True)

    type: Literal["finish"] = Field(default="finish", alias=AliasChoices("type", "action_type"))


class PydanticZeroAction(PydanticBaseAction):
    """Zero action (pydantic model)"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(default_factory=lambda: uuid.UUID(int=0))
    type: Literal["zero"] = Field(default="zero", alias=AliasChoices("type", "action_type"))
