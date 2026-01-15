from dataclasses import dataclass, field
from typing import Literal
from uuid import UUID

ActionType = Literal[
    "drawer",
    "to_trigger",
    "change_assistant",
    "repeat_transition",
    "finish",
    "zero",
]


@dataclass(kw_only=True)
class BaseAction:
    id: UUID
    action_type: ActionType
    is_default: bool = False
    is_final: bool = False
    title: str | None = None
    context: dict | None = None
    tracking_metadata: dict | None = None


@dataclass(kw_only=True)
class DrawerAction(BaseAction):
    action_type: Literal["drawer"] = "drawer"
    code: str | None = None
    on_close: Literal["refetch_node", "finish_scenario"] | None = None


@dataclass(kw_only=True)
class ToTriggerAction(BaseAction):
    action_type: Literal["to_trigger"] = "to_trigger"
    trigger_id: str | None = None


@dataclass(kw_only=True)
class ChangeAssistantAction(BaseAction):
    action_type: Literal["change_assistant"] = "change_assistant"
    assistant_id: UUID | None = None


@dataclass(kw_only=True)
class RepeatTransitionAction(BaseAction):
    action_type: Literal["repeat_transition"] = "repeat_transition"
    parent_transition: Literal["default", "not_default"] | UUID | None = None


@dataclass(kw_only=True)
class FinishAction(BaseAction):
    action_type: Literal["finish"] = "finish"


@dataclass(kw_only=True)
class ZeroAction(BaseAction):
    id: UUID = field(default_factory=lambda: UUID(int=0))
    action_type: Literal["zero"] = "zero"

    def __post_init__(self):
        self.id = UUID(int=0)  # Allways set the id to 0
