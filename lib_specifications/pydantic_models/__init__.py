"""Pydantic models for data transfer and serialization."""

from .actions import (
    PydanticBaseAction,
    PydanticChangeAssistantAction,
    PydanticDrawerAction,
    PydanticFinishAction,
    PydanticRepeatTransitionAction,
    PydanticToTriggerAction,
    PydanticZeroAction,
)
from .buttons_grid import PydanticButtonsBar, PydanticButtonsGrid, PydanticEmojiesBar
from .callback import PydanticCallbackInfo
from .drawers import PydanticDrawerApp, PydanticDrawerOption, PydanticDrawerScreen
from .operator import PydanticOperatorInfo
from .parameter import (
    PydanticParameterLiteralValue,
    PydanticParameterPathValue,
    _PydanticParameterValueAdapter,
)
from .parameter import (
    PydanticParameterValue as _PydanticParameterValueType,
)
from .parameter_schema import PydanticContextSchema, PydanticParameterSchema, PydanticSignatureSchema
from .specification_tree import (
    PydanticSpecificationAndNode,
    PydanticSpecificationCallbackLeafNode,
    PydanticSpecificationFieldLeafNode,
    PydanticSpecificationLeafNode,
    PydanticSpecificationNode,
    PydanticSpecificationNotNode,
    PydanticSpecificationOrNode,
    PydanticSpecificationTree,
)
from .widgets import (
    PydanticBaseWidgetInput,
    PydanticBaseWidgetOutput,
    PydanticBudgetAlertWidgetInput,
    PydanticBudgetAlertWidgetOutput,
    PydanticBudgetCategoryAmountWidgetInput,
    PydanticBudgetCategoryAmountWidgetOutput,
    PydanticCreditCardSummaryWidgetInput,
    PydanticCreditCardSummaryWidgetOutput,
    PydanticCreditScoreValueWidgetInput,
    PydanticCreditScoreValueWidgetOutput,
    PydanticDebtFreeTimeWidgetInput,
    PydanticDebtFreeTimeWidgetOutput,
    PydanticLanguageSelectorWidgetInput,
    PydanticLanguageSelectorWidgetOutput,
    PydanticPaymentReminderWidgetInput,
    PydanticPaymentReminderWidgetOutput,
    PydanticWidgetInput,
    PydanticWidgetInputValidator,
    PydanticWidgetOutput,
    PydanticWidgetOutputValidator,
    get_pydantic_widget_input_class,
    get_pydantic_widget_output_class,
)


# Create a class that works both as a type annotation and has model_validate
# When used as a type annotation, Pydantic will use __get_pydantic_core_schema__
# When used as a class, it has model_validate for tests
class PydanticParameterValue:
    """Discriminated union type for parameter values.

    Can be used as a type annotation in Pydantic models.
    Has model_validate method for standalone validation (for tests).
    """

    @staticmethod
    def model_validate(obj, *, from_attributes=False):
        """Validate and return a PydanticParameterPathValue or PydanticParameterLiteralValue."""
        return _PydanticParameterValueAdapter.validate_python(obj, from_attributes=from_attributes)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """Tell Pydantic how to handle this type when used in annotations."""
        # Return the schema for the Annotated union type
        return handler(_PydanticParameterValueType)


__all__ = [
    # Parameters
    "PydanticParameterValue",
    "PydanticParameterPathValue",
    "PydanticParameterLiteralValue",
    # Parameter Schemas
    "PydanticParameterSchema",
    "PydanticSignatureSchema",
    "PydanticContextSchema",
    # Specification Tree
    "PydanticSpecificationTree",
    "PydanticSpecificationNode",
    "PydanticSpecificationLeafNode",
    "PydanticSpecificationFieldLeafNode",
    "PydanticSpecificationCallbackLeafNode",
    "PydanticSpecificationAndNode",
    "PydanticSpecificationOrNode",
    "PydanticSpecificationNotNode",
    # Operator
    "PydanticOperatorInfo",
    # Callback
    "PydanticCallbackInfo",
    # Buttons grid
    "PydanticButtonsBar",
    "PydanticButtonsGrid",
    "PydanticEmojiesBar",
    # Actions
    "PydanticBaseAction",
    "PydanticDrawerAction",
    "PydanticToTriggerAction",
    "PydanticChangeAssistantAction",
    "PydanticRepeatTransitionAction",
    "PydanticFinishAction",
    "PydanticZeroAction",
    # Drawers
    "PydanticDrawerApp",
    "PydanticDrawerOption",
    "PydanticDrawerScreen",
    # Widgets
    "PydanticBaseWidgetInput",
    "PydanticBaseWidgetOutput",
    "PydanticLanguageSelectorWidgetInput",
    "PydanticLanguageSelectorWidgetOutput",
    "PydanticCreditScoreValueWidgetInput",
    "PydanticCreditScoreValueWidgetOutput",
    "PydanticBudgetCategoryAmountWidgetInput",
    "PydanticBudgetCategoryAmountWidgetOutput",
    "PydanticCreditCardSummaryWidgetInput",
    "PydanticCreditCardSummaryWidgetOutput",
    "PydanticPaymentReminderWidgetInput",
    "PydanticPaymentReminderWidgetOutput",
    "PydanticBudgetAlertWidgetInput",
    "PydanticBudgetAlertWidgetOutput",
    "PydanticDebtFreeTimeWidgetInput",
    "PydanticDebtFreeTimeWidgetOutput",
    "PydanticWidgetInput",
    "PydanticWidgetInputValidator",
    "PydanticWidgetOutput",
    "PydanticWidgetOutputValidator",
    "get_pydantic_widget_input_class",
    "get_pydantic_widget_output_class",
]
