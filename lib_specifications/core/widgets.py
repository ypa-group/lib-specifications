from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from ..logging_config import get_logger
from .parameters import ParameterSchema, ParameterTypeEnum, ParameterValue, SignatureSchema

logger = get_logger(__name__)


WidgetType = Literal[
    "language_selector",
    "credit_score_value",
    "budget_category_amount",
    "credit_card_summary",
    "payment_reminder",
    "budget_alert",
    "debt_free_time",
]


@dataclass(kw_only=True)
class BaseWidget:
    id: UUID
    widget_type: WidgetType

    @property
    def is_active(self) -> bool:
        return True

    @property
    def is_deprecated(self) -> bool:
        return False

    @property
    def signature_schema(self) -> SignatureSchema:
        return SignatureSchema(parameters={})

    def _get_nested_value(self, data: dict[str, Any], path: str) -> Any:
        """Get a value from nested dictionary using dot-notation path.

        Args:
            data: Nested dictionary structure
            path: Dot-notation path (e.g., "user.id", "meta.size")

        Returns:
            The value at the specified path

        Raises:
            KeyError: If the path doesn't exist in data
        """
        logger.debug(f"Getting nested value for path: '{path}'")
        keys = path.split(".")
        current = data

        for key in keys:
            if not isinstance(current, dict):
                logger.error(f"Path '{path}' is invalid: '{key}' is not a dictionary")
                raise KeyError(f"Path '{path}' is invalid: '{key}' is not a dictionary")
            if key not in current:
                logger.error(f"Path '{path}' not found: key '{key}' doesn't exist")
                raise KeyError(f"Path '{path}' not found: key '{key}' doesn't exist")
            current = current[key]

        logger.debug(f"Successfully extracted value from path '{path}': {current}")
        return current

    def _extract_parameter_value(self, parameter: ParameterValue, context: dict, parameter_name: str) -> Any:
        if parameter["parameter_type"] == "value":
            return parameter["value"]
        if parameter["parameter_type"] == "path":
            try:
                return self._get_nested_value(context, parameter["value"])
            except KeyError:
                parameter_schema = self.signature_schema.get_parameter(parameter_name)
                if parameter_schema and not parameter_schema.required:
                    return parameter_schema.default
                else:
                    raise
        else:
            raise ValueError(f"Invalid parameter type: {parameter['parameter_type']}")

    def populate_widget(self, context: dict) -> dict:
        return {
            "id": self.id,
            "widget_type": self.widget_type,
            "is_active": self.is_active,
            "is_deprecated": self.is_deprecated,
        }

    def validate_params(self, params: dict) -> None:
        for param_name, param_value in self.signature_schema.parameters.items():
            if param_name not in params and param_value.required:
                raise ValueError(
                    f"{self.__class__.__name__} requires signature schema parameter {param_name} but it is not provided"
                )


# Widget types
@dataclass(kw_only=True)
class LanguageSelectorWidget(BaseWidget):
    """Language selector widget."""

    widget_type: Literal["language_selector"] = "language_selector"

    def populate_widget(self, context: dict) -> dict:
        return super().populate_widget(context)


@dataclass(kw_only=True)
class CreditScoreValueWidget(BaseWidget):
    """Credit score value widget.

    Populated by:

    `score_value` : for example: 500, 650, 720

    `score_color_zone`
        - poor (red): 300-579
        - fair (pink): 580-669
        - good (dark_blue): 670-739
        - very good (light_blue): 740-799
        - excellent (light_green): 800-850

    `trend` (optional):
        - up
        - down"

    Should redirect to the factor by which the change occurred
    """

    widget_type: Literal["credit_score_value"] = "credit_score_value"
    params: dict[Literal["current_score_value", "previous_score_value"], ParameterValue]

    @property
    def signature_schema(self) -> SignatureSchema:
        return SignatureSchema(
            parameters={
                "current_score_value": ParameterSchema(
                    name="current_score_value",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                ),
                "previous_score_value": ParameterSchema(
                    name="previous_score_value",
                    data_type=ParameterTypeEnum.INT,
                    required=False,
                    default=None,
                ),
            }
        )

    def _calculate_score_color_zone(self, score: int) -> Literal["poor", "fair", "good", "very good", "excellent"]:
        if score < 580:
            return "poor"
        elif score < 670:
            return "fair"
        elif score < 740:
            return "good"
        elif score < 800:
            return "very good"
        else:
            return "excellent"

    def populate_widget(self, context: dict) -> dict:
        widget = super().populate_widget(context)

        current_score_value = int(
            self._extract_parameter_value(self.params["current_score_value"], context, "current_score_value")
        )
        previous_score_value = self._extract_parameter_value(
            self.params["previous_score_value"], context, "previous_score_value"
        )
        if previous_score_value is not None:
            try:
                previous_score_value = int(previous_score_value)
            except ValueError:
                logger.error(f"Previous score value is not a number: {previous_score_value}")
                previous_score_value = None

        if previous_score_value is None:
            trend = None
        else:
            if current_score_value < previous_score_value:
                trend = "down"
            else:
                trend = "up"

        widget["score_value"] = self._extract_parameter_value(
            self.params["current_score_value"], context, "current_score_value"
        )
        widget["score_color_zone"] = self._calculate_score_color_zone(current_score_value)
        widget["trend"] = trend
        return widget


@dataclass(kw_only=True)
class BudgetCategoryAmountWidget(BaseWidget):
    """Budget category amount widget.

    Populated by:

    `category_name`: Restaurants, Pets, Rent and etc.
    `amount`: number
    `currency`: currency
    `period_type`: month, quarter, week
    `target_date`: date
    """

    widget_type: Literal["budget_category_amount"] = "budget_category_amount"
    params: dict[Literal["category_name", "amount", "currency", "period_type", "target_date"], ParameterValue]

    @property
    def signature_schema(self) -> SignatureSchema:
        return SignatureSchema(
            parameters={
                "category_name": ParameterSchema(
                    name="category_name",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "amount": ParameterSchema(
                    name="amount",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                ),
                "currency": ParameterSchema(
                    name="currency",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "period_type": ParameterSchema(
                    name="period_type",
                    data_type=ParameterTypeEnum.STR,
                    required=False,
                    default=None,
                ),
                "target_date": ParameterSchema(
                    name="target_date",
                    data_type=ParameterTypeEnum.DATE,
                    required=False,
                    default=None,
                ),
            }
        )

    def populate_widget(self, context: dict) -> dict:
        widget = super().populate_widget(context)
        category_name = self._extract_parameter_value(self.params["category_name"], context, "category_name")
        amount = self._extract_parameter_value(self.params["amount"], context, "amount")
        currency = self._extract_parameter_value(self.params["currency"], context, "currency")
        period_type = self._extract_parameter_value(self.params["period_type"], context, "period_type")
        target_date = self._extract_parameter_value(self.params["target_date"], context, "target_date")

        widget["category_name"] = category_name
        widget["amount"] = int(amount)
        widget["currency"] = currency
        widget["period_type"] = period_type
        widget["target_date"] = (
            target_date if target_date is None else datetime.strptime(target_date, "%Y-%m-%d").date()
        )
        return widget


@dataclass(kw_only=True)
class CreditCardSummaryWidget(BaseWidget):
    """Credit card summary widget.

    Populated by:

    `bank_name`: name of the bank
    `bank_logo`: logo of the bank
    `card_id`: for redirect to this card
    `card_last_digits`: last 4 digits of the card
    `amount`: amount of the debt
    """

    widget_type: Literal["credit_card_summary"] = "credit_card_summary"
    params: dict[Literal["bank_name", "bank_logo", "card_id", "card_last_digits", "amount"], ParameterValue]

    @property
    def signature_schema(self) -> SignatureSchema:
        return SignatureSchema(
            parameters={
                "bank_name": ParameterSchema(
                    name="bank_name",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "bank_logo": ParameterSchema(
                    name="bank_logo",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "card_id": ParameterSchema(
                    name="card_id",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "card_last_digits": ParameterSchema(
                    name="card_last_digits",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "amount": ParameterSchema(
                    name="amount",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                ),
            }
        )

    def populate_widget(self, context: dict) -> dict:
        widget = super().populate_widget(context)
        bank_name = self._extract_parameter_value(self.params["bank_name"], context, "bank_name")
        bank_logo = self._extract_parameter_value(self.params["bank_logo"], context, "bank_logo")
        card_id = self._extract_parameter_value(self.params["card_id"], context, "card_id")
        card_last_digits = self._extract_parameter_value(self.params["card_last_digits"], context, "card_last_digits")
        amount = self._extract_parameter_value(self.params["amount"], context, "amount")

        widget["bank_name"] = bank_name
        widget["bank_logo"] = bank_logo
        widget["card_id"] = card_id
        widget["card_last_digits"] = card_last_digits
        widget["amount"] = int(amount)
        return widget


@dataclass(kw_only=True)
class PaymentReminderWidget(BaseWidget):
    """Payment reminder widget.

    Populated by:

    `bank_name`: name of the bank
    `bank_logo`: logo of the bank
    `card_id`: for redirect to this card
    `card_last_digits`: last 4 digits of the card
    `payment_amount`: amount of the payment
    `due_date`: date of the payment
    """

    widget_type: Literal["payment_reminder"] = "payment_reminder"
    params: dict[
        Literal["bank_name", "bank_logo", "card_id", "card_last_digits", "payment_amount", "due_date"], ParameterValue
    ]

    @property
    def signature_schema(self) -> SignatureSchema:
        return SignatureSchema(
            parameters={
                "bank_name": ParameterSchema(
                    name="bank_name",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "bank_logo": ParameterSchema(
                    name="bank_logo",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "card_id": ParameterSchema(
                    name="card_id",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "card_last_digits": ParameterSchema(
                    name="card_last_digits",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "payment_amount": ParameterSchema(
                    name="payment_amount",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                ),
                "due_date": ParameterSchema(
                    name="due_date",
                    data_type=ParameterTypeEnum.DATE,
                    required=True,
                ),
            }
        )

    def populate_widget(self, context: dict) -> dict:
        widget = super().populate_widget(context)
        bank_name = self._extract_parameter_value(self.params["bank_name"], context, "bank_name")
        bank_logo = self._extract_parameter_value(self.params["bank_logo"], context, "bank_logo")
        card_id = self._extract_parameter_value(self.params["card_id"], context, "card_id")
        card_last_digits = self._extract_parameter_value(self.params["card_last_digits"], context, "card_last_digits")
        payment_amount = self._extract_parameter_value(self.params["payment_amount"], context, "payment_amount")
        due_date = self._extract_parameter_value(self.params["due_date"], context, "due_date")

        widget["bank_name"] = bank_name
        widget["bank_logo"] = bank_logo
        widget["card_id"] = card_id
        widget["card_last_digits"] = card_last_digits
        widget["payment_amount"] = int(payment_amount)
        widget["due_date"] = due_date if due_date is None else datetime.strptime(due_date, "%Y-%m-%d").date()
        return widget


@dataclass(kw_only=True)
class BudgetAlertWidget(BaseWidget):
    """Budget alert widget.

    Populated by:

    `category_name`: name of the category
    `category_icon`: icon of the category
    `spent_amount`: amount of the spent
    `period_type`: month, quarter, week
    `target_date`: date
    TODO: `alert_type`: type of the alert

        - warning (approaching the limit)
        - exceeded (limit exceeded)
    """

    widget_type: Literal["budget_alert"] = "budget_alert"
    params: dict[
        Literal["category_name", "category_icon", "spent_amount", "period_type", "target_date", "alert_type"],
        ParameterValue,
    ]

    @property
    def signature_schema(self) -> SignatureSchema:
        return SignatureSchema(
            parameters={
                "category_name": ParameterSchema(
                    name="category_name",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "category_icon": ParameterSchema(
                    name="category_icon",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
                "spent_amount": ParameterSchema(
                    name="spent_amount",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                ),
                "period_type": ParameterSchema(
                    name="period_type",
                    data_type=ParameterTypeEnum.STR,
                    required=False,
                    default=None,
                ),
                "target_date": ParameterSchema(
                    name="target_date",
                    data_type=ParameterTypeEnum.DATE,
                    required=False,
                    default=None,
                ),
                "alert_type": ParameterSchema(
                    name="alert_type",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                ),
            }
        )

    def populate_widget(self, context: dict) -> dict:
        widget = super().populate_widget(context)
        category_name = self._extract_parameter_value(self.params["category_name"], context, "category_name")
        category_icon = self._extract_parameter_value(self.params["category_icon"], context, "category_icon")
        spent_amount = self._extract_parameter_value(self.params["spent_amount"], context, "spent_amount")
        period_type = self._extract_parameter_value(self.params["period_type"], context, "period_type")
        target_date = self._extract_parameter_value(self.params["target_date"], context, "target_date")
        alert_type = self._extract_parameter_value(self.params["alert_type"], context, "alert_type")
        widget["category_name"] = category_name
        widget["category_icon"] = category_icon
        widget["spent_amount"] = int(spent_amount)
        widget["period_type"] = period_type
        widget["target_date"] = (
            target_date if target_date is None else datetime.strptime(target_date, "%Y-%m-%d").date()
        )
        widget["alert_type"] = alert_type
        return widget


@dataclass(kw_only=True)
class DebtFreeTimeWidget(BaseWidget):
    """Debt free time widget.
    Populated by:

    `years`: number of years
    `months`: number of months
    `card_id`: for redirect to this card
    `payment_strategy`: 'minimum_only' or 'with_extra_payment'

    TODO: Visual contrast:
    - red → long
    - green → fast
    - (optional) icon ⚡ for extra payments
    """

    widget_type: Literal["debt_free_time"] = "debt_free_time"
    params: dict[Literal["years", "months", "card_id", "payment_strategy"], ParameterValue]

    @property
    def signature_schema(self) -> SignatureSchema:
        return SignatureSchema(
            parameters={
                "years": ParameterSchema(name="years", data_type=ParameterTypeEnum.INT, required=True),
                "months": ParameterSchema(name="months", data_type=ParameterTypeEnum.INT, required=True),
                "card_id": ParameterSchema(name="card_id", data_type=ParameterTypeEnum.STR, required=True),
                "payment_strategy": ParameterSchema(
                    name="payment_strategy", data_type=ParameterTypeEnum.STR, required=True
                ),
            }
        )

    def populate_widget(self, context: dict) -> dict:
        widget = super().populate_widget(context)
        years = self._extract_parameter_value(self.params["years"], context, "years")
        months = self._extract_parameter_value(self.params["months"], context, "months")
        card_id = self._extract_parameter_value(self.params["card_id"], context, "card_id")
        payment_strategy = self._extract_parameter_value(self.params["payment_strategy"], context, "payment_strategy")

        widget["years"] = years
        widget["months"] = months
        widget["card_id"] = card_id
        widget["payment_strategy"] = payment_strategy
        return widget
