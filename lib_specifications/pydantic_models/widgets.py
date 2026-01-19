"""Pydantic models for widgets - both for editing and fetching populated widgets."""

from datetime import date
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

from ..core.widgets import (
    BaseWidget,
    BudgetAlertWidget,
    BudgetCategoryAmountWidget,
    CreditCardSummaryWidget,
    CreditScoreValueWidget,
    DebtFreeTimeWidget,
    LanguageSelectorWidget,
    PaymentReminderWidget,
)
from .parameter import PydanticParameterValue


# Base widget models
class PydanticBaseWidgetInput(BaseModel):
    """Base widget input model for editing/creating widgets."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Widget unique identifier")
    widget_type: Literal[
        "language_selector",
        "credit_score_value",
        "budget_category_amount",
        "credit_card_summary",
        "payment_reminder",
        "budget_alert",
        "debt_free_time",
    ] = Field(..., description="Widget type")


class PydanticBaseWidgetOutput(BaseModel):
    """Base widget output model for fetching populated widgets."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Widget unique identifier")
    widget_type: Literal[
        "language_selector",
        "credit_score_value",
        "budget_category_amount",
        "credit_card_summary",
        "payment_reminder",
        "budget_alert",
        "debt_free_time",
    ] = Field(..., description="Widget type")
    is_active: bool = Field(default=True, description="Whether the widget is active")
    is_deprecated: bool = Field(default=False, description="Whether the widget is deprecated")


# Language Selector Widget
class PydanticLanguageSelectorWidgetInput(PydanticBaseWidgetInput):
    """Language selector widget input model for editing."""

    widget_type: Literal["language_selector"] = "language_selector"


class PydanticLanguageSelectorWidgetOutput(PydanticBaseWidgetOutput):
    """Language selector widget output model for fetching populated widget."""

    widget_type: Literal["language_selector"] = "language_selector"


# Credit Score Value Widget
class PydanticCreditScoreValueWidgetInput(PydanticBaseWidgetInput):
    """Credit score value widget input model for editing."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "widget_type": "credit_score_value",
                "params": {
                    "current_score_value": {
                        "parameter_type": "path",
                        "data_type": "int",
                        "value": "user.credit_score.current",
                    },
                    "previous_score_value": {
                        "parameter_type": "path",
                        "data_type": "int",
                        "value": "user.credit_score.previous",
                    },
                },
            }
        },
    )

    widget_type: Literal["credit_score_value"] = "credit_score_value"
    params: dict[
        Literal["current_score_value", "previous_score_value"],
        PydanticParameterValue,
    ] = Field(..., description="Widget parameters")


class PydanticCreditScoreValueWidgetOutput(PydanticBaseWidgetOutput):
    """Credit score value widget output model for fetching populated widget."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "widget_type": "credit_score_value",
                "is_active": True,
                "is_deprecated": False,
                "score_value": 720,
                "score_color_zone": "good",
                "trend": "up",
            }
        },
    )

    widget_type: Literal["credit_score_value"] = "credit_score_value"
    score_value: int = Field(..., description="Current credit score value")
    score_color_zone: Literal["poor", "fair", "good", "very good", "excellent"] = Field(
        ..., description="Credit score color zone"
    )
    trend: Literal["up", "down"] | None = Field(default=None, description="Score trend (up/down) compared to previous")


# Budget Category Amount Widget
class PydanticBudgetCategoryAmountWidgetInput(PydanticBaseWidgetInput):
    """Budget category amount widget input model for editing."""

    widget_type: Literal["budget_category_amount"] = "budget_category_amount"
    params: dict[
        Literal["category_name", "amount", "currency", "period_type", "target_date"],
        PydanticParameterValue,
    ] = Field(..., description="Widget parameters")


class PydanticBudgetCategoryAmountWidgetOutput(PydanticBaseWidgetOutput):
    """Budget category amount widget output model for fetching populated widget."""

    widget_type: Literal["budget_category_amount"] = "budget_category_amount"
    category_name: str = Field(..., description="Category name")
    amount: int = Field(..., description="Budget amount")
    currency: str = Field(..., description="Currency code")
    period_type: str | None = Field(default=None, description="Period type (month, quarter, week)")
    target_date: date | None = Field(default=None, description="Target date")


# Credit Card Summary Widget
class PydanticCreditCardSummaryWidgetInput(PydanticBaseWidgetInput):
    """Credit card summary widget input model for editing."""

    widget_type: Literal["credit_card_summary"] = "credit_card_summary"
    params: dict[
        Literal["bank_name", "bank_logo", "card_id", "card_last_digits", "amount"],
        PydanticParameterValue,
    ] = Field(..., description="Widget parameters")


class PydanticCreditCardSummaryWidgetOutput(PydanticBaseWidgetOutput):
    """Credit card summary widget output model for fetching populated widget."""

    widget_type: Literal["credit_card_summary"] = "credit_card_summary"
    bank_name: str = Field(..., description="Bank name")
    bank_logo: str = Field(..., description="Bank logo URL")
    card_id: str = Field(..., description="Card identifier")
    card_last_digits: str = Field(..., description="Last 4 digits of the card")
    amount: int = Field(..., description="Debt amount")


# Payment Reminder Widget
class PydanticPaymentReminderWidgetInput(PydanticBaseWidgetInput):
    """Payment reminder widget input model for editing."""

    widget_type: Literal["payment_reminder"] = "payment_reminder"
    params: dict[
        Literal["bank_name", "bank_logo", "card_id", "card_last_digits", "payment_amount", "due_date"],
        PydanticParameterValue,
    ] = Field(..., description="Widget parameters")


class PydanticPaymentReminderWidgetOutput(PydanticBaseWidgetOutput):
    """Payment reminder widget output model for fetching populated widget."""

    widget_type: Literal["payment_reminder"] = "payment_reminder"
    bank_name: str = Field(..., description="Bank name")
    bank_logo: str = Field(..., description="Bank logo URL")
    card_id: str = Field(..., description="Card identifier")
    card_last_digits: str = Field(..., description="Last 4 digits of the card")
    payment_amount: int = Field(..., description="Payment amount")
    due_date: date = Field(..., description="Payment due date")


# Budget Alert Widget
class PydanticBudgetAlertWidgetInput(PydanticBaseWidgetInput):
    """Budget alert widget input model for editing."""

    widget_type: Literal["budget_alert"] = "budget_alert"
    params: dict[
        Literal["category_name", "category_icon", "spent_amount", "period_type", "target_date"],
        PydanticParameterValue,
    ] = Field(..., description="Widget parameters")


class PydanticBudgetAlertWidgetOutput(PydanticBaseWidgetOutput):
    """Budget alert widget output model for fetching populated widget."""

    widget_type: Literal["budget_alert"] = "budget_alert"
    category_name: str = Field(..., description="Category name")
    category_icon: str = Field(..., description="Category icon")
    spent_amount: int = Field(..., description="Spent amount")
    period_type: str | None = Field(default=None, description="Period type (month, quarter, week)")
    target_date: date | None = Field(default=None, description="Target date")
    alert_type: Literal["warning", "exceeded"] = Field(..., description="Alert type (warning, exceeded)")


# Debt Free Time Widget
class PydanticDebtFreeTimeWidgetInput(PydanticBaseWidgetInput):
    """Debt free time widget input model for editing."""

    widget_type: Literal["debt_free_time"] = "debt_free_time"
    params: dict[
        Literal["years", "months", "card_id", "payment_strategy"],
        PydanticParameterValue,
    ] = Field(..., description="Widget parameters")


class PydanticDebtFreeTimeWidgetOutput(PydanticBaseWidgetOutput):
    """Debt free time widget output model for fetching populated widget."""

    widget_type: Literal["debt_free_time"] = "debt_free_time"
    years: int = Field(..., description="Number of years until debt free")
    months: int = Field(..., description="Number of months until debt free")
    card_id: str = Field(..., description="Card identifier")
    payment_strategy: Literal["minimum_only", "with_extra_payment"] = Field(
        ..., description="Payment strategy (minimum_only, with_extra_payment)"
    )


# Union types for input and output
_PydanticWidgetInputUnion = (
    PydanticLanguageSelectorWidgetInput
    | PydanticCreditScoreValueWidgetInput
    | PydanticBudgetCategoryAmountWidgetInput
    | PydanticCreditCardSummaryWidgetInput
    | PydanticPaymentReminderWidgetInput
    | PydanticBudgetAlertWidgetInput
    | PydanticDebtFreeTimeWidgetInput
)

_PydanticWidgetOutputUnion = (
    PydanticLanguageSelectorWidgetOutput
    | PydanticCreditScoreValueWidgetOutput
    | PydanticBudgetCategoryAmountWidgetOutput
    | PydanticCreditCardSummaryWidgetOutput
    | PydanticPaymentReminderWidgetOutput
    | PydanticBudgetAlertWidgetOutput
    | PydanticDebtFreeTimeWidgetOutput
)

# TypeAdapters for validation with discriminator
_PydanticWidgetInputAdapter = TypeAdapter(
    Annotated[
        _PydanticWidgetInputUnion,
        Field(discriminator="widget_type"),
    ]
)

_PydanticWidgetOutputAdapter = TypeAdapter(
    Annotated[
        _PydanticWidgetOutputUnion,
        Field(discriminator="widget_type"),
    ]
)

PydanticWidgetInput = Annotated[
    _PydanticWidgetInputUnion,
    Field(discriminator="widget_type"),
]

PydanticWidgetOutput = Annotated[
    _PydanticWidgetOutputUnion,
    Field(discriminator="widget_type"),
]


# Helper classes for model_validate (similar to PydanticParameterValue)
class PydanticWidgetInputValidator:
    """Helper class for validating widget input discriminated unions."""

    @staticmethod
    def model_validate(obj, *, from_attributes=False):
        """Validate and return the appropriate widget input model."""
        return _PydanticWidgetInputAdapter.validate_python(obj, from_attributes=from_attributes)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """Tell Pydantic how to handle this type when used in annotations."""
        return handler(PydanticWidgetInput)


class PydanticWidgetOutputValidator:
    """Helper class for validating widget output discriminated unions."""

    @staticmethod
    def model_validate(obj, *, from_attributes=False):
        """Validate and return the appropriate widget output model."""
        return _PydanticWidgetOutputAdapter.validate_python(obj, from_attributes=from_attributes)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """Tell Pydantic how to handle this type when used in annotations."""
        return handler(PydanticWidgetOutput)


# Mapping from widget classes to their Pydantic input/output model classes
_WIDGET_TO_PYDANTIC_INPUT: dict[type[BaseWidget], type[BaseModel]] = {
    LanguageSelectorWidget: PydanticLanguageSelectorWidgetInput,
    CreditScoreValueWidget: PydanticCreditScoreValueWidgetInput,
    BudgetCategoryAmountWidget: PydanticBudgetCategoryAmountWidgetInput,
    CreditCardSummaryWidget: PydanticCreditCardSummaryWidgetInput,
    PaymentReminderWidget: PydanticPaymentReminderWidgetInput,
    BudgetAlertWidget: PydanticBudgetAlertWidgetInput,
    DebtFreeTimeWidget: PydanticDebtFreeTimeWidgetInput,
}

_WIDGET_TO_PYDANTIC_OUTPUT: dict[type[BaseWidget], type[BaseModel]] = {
    LanguageSelectorWidget: PydanticLanguageSelectorWidgetOutput,
    CreditScoreValueWidget: PydanticCreditScoreValueWidgetOutput,
    BudgetCategoryAmountWidget: PydanticBudgetCategoryAmountWidgetOutput,
    CreditCardSummaryWidget: PydanticCreditCardSummaryWidgetOutput,
    PaymentReminderWidget: PydanticPaymentReminderWidgetOutput,
    BudgetAlertWidget: PydanticBudgetAlertWidgetOutput,
    DebtFreeTimeWidget: PydanticDebtFreeTimeWidgetOutput,
}


def get_pydantic_widget_input_class(widget_class: type[BaseWidget]) -> type[BaseModel]:
    """Get Pydantic input model class for a widget class.

    Args:
        widget_class: The widget class to get the Pydantic input model for

    Returns:
        The corresponding Pydantic input model class

    Raises:
        ValueError: If the widget class is not mapped to a Pydantic model
    """
    if widget_class not in _WIDGET_TO_PYDANTIC_INPUT:
        raise ValueError(
            f"Widget class {widget_class.__name__} is not mapped to a Pydantic input model. "
            f"Available widget classes: {list(_WIDGET_TO_PYDANTIC_INPUT.keys())}"
        )
    return _WIDGET_TO_PYDANTIC_INPUT[widget_class]


def get_pydantic_widget_output_class(widget_class: type[BaseWidget]) -> type[BaseModel]:
    """Get Pydantic output model class for a widget class.

    Args:
        widget_class: The widget class to get the Pydantic output model for

    Returns:
        The corresponding Pydantic output model class

    Raises:
        ValueError: If the widget class is not mapped to a Pydantic model
    """
    if widget_class not in _WIDGET_TO_PYDANTIC_OUTPUT:
        raise ValueError(
            f"Widget class {widget_class.__name__} is not mapped to a Pydantic output model. "
            f"Available widget classes: {list(_WIDGET_TO_PYDANTIC_OUTPUT.keys())}"
        )
    return _WIDGET_TO_PYDANTIC_OUTPUT[widget_class]
