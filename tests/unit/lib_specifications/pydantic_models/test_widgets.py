"""Tests for widget Pydantic models."""

from datetime import date
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from lib_specifications.pydantic_models.widgets import (
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
    PydanticWidgetInputValidator,
    PydanticWidgetOutputValidator,
)


class TestPydanticLanguageSelectorWidget:
    """Test language selector widget Pydantic models."""

    def test_input_model(self):
        """Test language selector widget input model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "language_selector",
        }
        widget = PydanticLanguageSelectorWidgetInput.model_validate(data)
        assert widget.id == widget_id
        assert widget.widget_type == "language_selector"

    def test_output_model(self):
        """Test language selector widget output model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "language_selector",
            "is_active": True,
            "is_deprecated": False,
        }
        widget = PydanticLanguageSelectorWidgetOutput.model_validate(data)
        assert widget.id == widget_id
        assert widget.widget_type == "language_selector"
        assert widget.is_active is True
        assert widget.is_deprecated is False


class TestPydanticCreditScoreValueWidget:
    """Test credit score value widget Pydantic models."""

    def test_input_model(self):
        """Test credit score value widget input model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
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
        widget = PydanticCreditScoreValueWidgetInput.model_validate(data)
        assert widget.id == widget_id
        assert widget.widget_type == "credit_score_value"
        assert "current_score_value" in widget.params
        assert "previous_score_value" in widget.params

    def test_output_model(self):
        """Test credit score value widget output model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "credit_score_value",
            "is_active": True,
            "is_deprecated": False,
            "score_value": 720,
            "score_color_zone": "good",
            "trend": "up",
        }
        widget = PydanticCreditScoreValueWidgetOutput.model_validate(data)
        assert widget.id == widget_id
        assert widget.widget_type == "credit_score_value"
        assert widget.score_value == 720
        assert widget.score_color_zone == "good"
        assert widget.trend == "up"

    def test_output_model_with_none_trend(self):
        """Test credit score value widget output model with None trend."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "credit_score_value",
            "is_active": True,
            "is_deprecated": False,
            "score_value": 720,
            "score_color_zone": "good",
            "trend": None,
        }
        widget = PydanticCreditScoreValueWidgetOutput.model_validate(data)
        assert widget.trend is None


class TestPydanticBudgetCategoryAmountWidget:
    """Test budget category amount widget Pydantic models."""

    def test_input_model(self):
        """Test budget category amount widget input model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "budget_category_amount",
            "params": {
                "category_name": {
                    "parameter_type": "path",
                    "data_type": "str",
                    "value": "budget.category.name",
                },
                "amount": {
                    "parameter_type": "path",
                    "data_type": "int",
                    "value": "budget.amount",
                },
                "currency": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "USD",
                },
                "period_type": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "month",
                },
                "target_date": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "budget.target_date",
                },
            },
        }
        widget = PydanticBudgetCategoryAmountWidgetInput.model_validate(data)
        assert widget.id == widget_id
        assert widget.widget_type == "budget_category_amount"
        assert len(widget.params) == 5

    def test_output_model(self):
        """Test budget category amount widget output model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "budget_category_amount",
            "is_active": True,
            "is_deprecated": False,
            "category_name": "Restaurants",
            "amount": 500,
            "currency": "USD",
            "period_type": "month",
            "target_date": "2024-12-31",
        }
        widget = PydanticBudgetCategoryAmountWidgetOutput.model_validate(data)
        assert widget.category_name == "Restaurants"
        assert widget.amount == 500
        assert widget.currency == "USD"
        assert widget.period_type == "month"
        assert widget.target_date == date(2024, 12, 31)


class TestPydanticCreditCardSummaryWidget:
    """Test credit card summary widget Pydantic models."""

    def test_input_model(self):
        """Test credit card summary widget input model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "credit_card_summary",
            "params": {
                "bank_name": {
                    "parameter_type": "path",
                    "data_type": "str",
                    "value": "card.bank_name",
                },
                "bank_logo": {
                    "parameter_type": "path",
                    "data_type": "str",
                    "value": "card.bank_logo",
                },
                "card_id": {
                    "parameter_type": "path",
                    "data_type": "str",
                    "value": "card.id",
                },
                "card_last_digits": {
                    "parameter_type": "path",
                    "data_type": "str",
                    "value": "card.last_digits",
                },
                "amount": {
                    "parameter_type": "path",
                    "data_type": "int",
                    "value": "card.debt_amount",
                },
            },
        }
        widget = PydanticCreditCardSummaryWidgetInput.model_validate(data)
        assert widget.id == widget_id
        assert widget.widget_type == "credit_card_summary"

    def test_output_model(self):
        """Test credit card summary widget output model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "credit_card_summary",
            "is_active": True,
            "is_deprecated": False,
            "bank_name": "Chase",
            "bank_logo": "https://example.com/chase.png",
            "card_id": "card_123",
            "card_last_digits": "1234",
            "amount": 2500,
        }
        widget = PydanticCreditCardSummaryWidgetOutput.model_validate(data)
        assert widget.bank_name == "Chase"
        assert widget.bank_logo == "https://example.com/chase.png"
        assert widget.card_id == "card_123"
        assert widget.card_last_digits == "1234"
        assert widget.amount == 2500


class TestPydanticPaymentReminderWidget:
    """Test payment reminder widget Pydantic models."""

    def test_input_model(self):
        """Test payment reminder widget input model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "payment_reminder",
            "params": {
                "bank_name": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "Bank of America",
                },
                "bank_logo": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "https://example.com/bofa.png",
                },
                "card_id": {
                    "parameter_type": "path",
                    "data_type": "str",
                    "value": "payment.card_id",
                },
                "card_last_digits": {
                    "parameter_type": "path",
                    "data_type": "str",
                    "value": "payment.card_last_digits",
                },
                "payment_amount": {
                    "parameter_type": "path",
                    "data_type": "int",
                    "value": "payment.amount",
                },
                "due_date": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "payment.due_date",
                },
            },
        }
        widget = PydanticPaymentReminderWidgetInput.model_validate(data)
        assert widget.id == widget_id
        assert widget.widget_type == "payment_reminder"

    def test_output_model(self):
        """Test payment reminder widget output model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "payment_reminder",
            "is_active": True,
            "is_deprecated": False,
            "bank_name": "Bank of America",
            "bank_logo": "https://example.com/bofa.png",
            "card_id": "card_456",
            "card_last_digits": "5678",
            "payment_amount": 150,
            "due_date": "2024-02-15",
        }
        widget = PydanticPaymentReminderWidgetOutput.model_validate(data)
        assert widget.bank_name == "Bank of America"
        assert widget.card_id == "card_456"
        assert widget.payment_amount == 150
        assert widget.due_date == date(2024, 2, 15)


class TestPydanticBudgetAlertWidget:
    """Test budget alert widget Pydantic models."""

    def test_input_model(self):
        """Test budget alert widget input model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "budget_alert",
            "params": {
                "category_name": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "Groceries",
                },
                "category_icon": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "🛒",
                },
                "spent_amount": {
                    "parameter_type": "path",
                    "data_type": "int",
                    "value": "budget.spent",
                },
                "period_type": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "month",
                },
                "target_date": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "budget.target_date",
                },
            },
        }
        widget = PydanticBudgetAlertWidgetInput.model_validate(data)
        assert widget.id == widget_id
        assert widget.widget_type == "budget_alert"
        # alert_type is not in params - it's computed directly in populate_widget

    def test_output_model(self):
        """Test budget alert widget output model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "budget_alert",
            "is_active": True,
            "is_deprecated": False,
            "category_name": "Groceries",
            "category_icon": "🛒",
            "spent_amount": 850,
            "period_type": "month",
            "target_date": "2024-03-31",
            "alert_type": "exceeded",
        }
        widget = PydanticBudgetAlertWidgetOutput.model_validate(data)
        assert widget.category_name == "Groceries"
        assert widget.category_icon == "🛒"
        assert widget.spent_amount == 850
        assert widget.alert_type == "exceeded"
        assert widget.target_date == date(2024, 3, 31)


class TestPydanticDebtFreeTimeWidget:
    """Test debt free time widget Pydantic models."""

    def test_input_model(self):
        """Test debt free time widget input model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "debt_free_time",
            "params": {
                "years": {
                    "parameter_type": "path",
                    "data_type": "int",
                    "value": "debt.years",
                },
                "months": {
                    "parameter_type": "path",
                    "data_type": "int",
                    "value": "debt.months",
                },
                "card_id": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "card_789",
                },
                "payment_strategy": {
                    "parameter_type": "path",
                    "data_type": "str",
                    "value": "debt.strategy",
                },
            },
        }
        widget = PydanticDebtFreeTimeWidgetInput.model_validate(data)
        assert widget.id == widget_id
        assert widget.widget_type == "debt_free_time"

    def test_output_model(self):
        """Test debt free time widget output model."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "debt_free_time",
            "is_active": True,
            "is_deprecated": False,
            "years": 2,
            "months": 6,
            "card_id": "card_789",
            "payment_strategy": "with_extra_payment",
        }
        widget = PydanticDebtFreeTimeWidgetOutput.model_validate(data)
        assert widget.years == 2
        assert widget.months == 6
        assert widget.card_id == "card_789"
        assert widget.payment_strategy == "with_extra_payment"


class TestPydanticWidgetDiscriminatedUnion:
    """Test discriminated union behavior for widget Pydantic models."""

    def test_discriminated_union_input_language_selector(self):
        """Test that PydanticWidgetInput correctly discriminates language_selector."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "language_selector",
        }
        widget = PydanticWidgetInputValidator.model_validate(data)
        assert isinstance(widget, PydanticLanguageSelectorWidgetInput)
        assert widget.widget_type == "language_selector"
        assert widget.id == widget_id

    def test_discriminated_union_input_credit_score_value(self):
        """Test that PydanticWidgetInput correctly discriminates credit_score_value."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
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
        widget = PydanticWidgetInputValidator.model_validate(data)
        assert isinstance(widget, PydanticCreditScoreValueWidgetInput)
        assert widget.widget_type == "credit_score_value"
        assert "current_score_value" in widget.params

    def test_discriminated_union_input_budget_category_amount(self):
        """Test that PydanticWidgetInput correctly discriminates budget_category_amount."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "budget_category_amount",
            "params": {
                "category_name": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "Restaurants",
                },
                "amount": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 500,
                },
                "currency": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "USD",
                },
                "period_type": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "month",
                },
                "target_date": {
                    "parameter_type": "value",
                    "data_type": "date",
                    "value": "2024-12-31",
                },
            },
        }
        widget = PydanticWidgetInputValidator.model_validate(data)
        assert isinstance(widget, PydanticBudgetCategoryAmountWidgetInput)
        assert widget.widget_type == "budget_category_amount"

    def test_discriminated_union_input_credit_card_summary(self):
        """Test that PydanticWidgetInput correctly discriminates credit_card_summary."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "credit_card_summary",
            "params": {
                "bank_name": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "Chase",
                },
                "bank_logo": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "https://example.com/chase.png",
                },
                "card_id": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "card_123",
                },
                "card_last_digits": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "1234",
                },
                "amount": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 2500,
                },
            },
        }
        widget = PydanticWidgetInputValidator.model_validate(data)
        assert isinstance(widget, PydanticCreditCardSummaryWidgetInput)
        assert widget.widget_type == "credit_card_summary"

    def test_discriminated_union_input_payment_reminder(self):
        """Test that PydanticWidgetInput correctly discriminates payment_reminder."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "payment_reminder",
            "params": {
                "bank_name": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "Bank of America",
                },
                "bank_logo": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "https://example.com/bofa.png",
                },
                "card_id": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "card_456",
                },
                "card_last_digits": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "5678",
                },
                "payment_amount": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 150,
                },
                "due_date": {
                    "parameter_type": "value",
                    "data_type": "date",
                    "value": "2024-02-15",
                },
            },
        }
        widget = PydanticWidgetInputValidator.model_validate(data)
        assert isinstance(widget, PydanticPaymentReminderWidgetInput)
        assert widget.widget_type == "payment_reminder"

    def test_discriminated_union_input_budget_alert(self):
        """Test that PydanticWidgetInput correctly discriminates budget_alert."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "budget_alert",
            "params": {
                "category_name": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "Groceries",
                },
                "category_icon": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "🛒",
                },
                "spent_amount": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 850,
                },
                "period_type": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "month",
                },
                "target_date": {
                    "parameter_type": "value",
                    "data_type": "date",
                    "value": "2024-03-31",
                },
            },
        }
        widget = PydanticWidgetInputValidator.model_validate(data)
        assert isinstance(widget, PydanticBudgetAlertWidgetInput)
        assert widget.widget_type == "budget_alert"
        # alert_type is not in params - it's computed directly in populate_widget

    def test_discriminated_union_input_debt_free_time(self):
        """Test that PydanticWidgetInput correctly discriminates debt_free_time."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "debt_free_time",
            "params": {
                "years": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 2,
                },
                "months": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 6,
                },
                "card_id": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "card_789",
                },
                "payment_strategy": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "with_extra_payment",
                },
            },
        }
        widget = PydanticWidgetInputValidator.model_validate(data)
        assert isinstance(widget, PydanticDebtFreeTimeWidgetInput)
        assert widget.widget_type == "debt_free_time"

    def test_discriminated_union_input_invalid_widget_type(self):
        """Test that invalid widget_type raises validation error."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "invalid_widget_type",
        }
        with pytest.raises(ValidationError) as exc_info:
            PydanticWidgetInputValidator.model_validate(data)
        assert "widget_type" in str(exc_info.value).lower() or "discriminator" in str(exc_info.value).lower()

    def test_discriminated_union_input_missing_widget_type(self):
        """Test that missing widget_type raises validation error."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
        }
        with pytest.raises(ValidationError):
            PydanticWidgetInputValidator.model_validate(data)

    def test_discriminated_union_output_language_selector(self):
        """Test that PydanticWidgetOutput correctly discriminates language_selector."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "language_selector",
            "is_active": True,
            "is_deprecated": False,
        }
        widget = PydanticWidgetOutputValidator.model_validate(data)
        assert isinstance(widget, PydanticLanguageSelectorWidgetOutput)
        assert widget.widget_type == "language_selector"

    def test_discriminated_union_output_credit_score_value(self):
        """Test that PydanticWidgetOutput correctly discriminates credit_score_value."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "credit_score_value",
            "is_active": True,
            "is_deprecated": False,
            "score_value": 720,
            "score_color_zone": "good",
            "trend": "up",
        }
        widget = PydanticWidgetOutputValidator.model_validate(data)
        assert isinstance(widget, PydanticCreditScoreValueWidgetOutput)
        assert widget.widget_type == "credit_score_value"
        assert widget.score_value == 720
        assert widget.score_color_zone == "good"

    def test_discriminated_union_output_budget_category_amount(self):
        """Test that PydanticWidgetOutput correctly discriminates budget_category_amount."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "budget_category_amount",
            "is_active": True,
            "is_deprecated": False,
            "category_name": "Restaurants",
            "amount": 500,
            "currency": "USD",
            "period_type": "month",
            "target_date": "2024-12-31",
        }
        widget = PydanticWidgetOutputValidator.model_validate(data)
        assert isinstance(widget, PydanticBudgetCategoryAmountWidgetOutput)
        assert widget.widget_type == "budget_category_amount"
        assert widget.category_name == "Restaurants"

    def test_discriminated_union_output_credit_card_summary(self):
        """Test that PydanticWidgetOutput correctly discriminates credit_card_summary."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "credit_card_summary",
            "is_active": True,
            "is_deprecated": False,
            "bank_name": "Chase",
            "bank_logo": "https://example.com/chase.png",
            "card_id": "card_123",
            "card_last_digits": "1234",
            "amount": 2500,
        }
        widget = PydanticWidgetOutputValidator.model_validate(data)
        assert isinstance(widget, PydanticCreditCardSummaryWidgetOutput)
        assert widget.widget_type == "credit_card_summary"
        assert widget.bank_name == "Chase"

    def test_discriminated_union_output_payment_reminder(self):
        """Test that PydanticWidgetOutput correctly discriminates payment_reminder."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "payment_reminder",
            "is_active": True,
            "is_deprecated": False,
            "bank_name": "Bank of America",
            "bank_logo": "https://example.com/bofa.png",
            "card_id": "card_456",
            "card_last_digits": "5678",
            "payment_amount": 150,
            "due_date": "2024-02-15",
        }
        widget = PydanticWidgetOutputValidator.model_validate(data)
        assert isinstance(widget, PydanticPaymentReminderWidgetOutput)
        assert widget.widget_type == "payment_reminder"
        assert widget.payment_amount == 150

    def test_discriminated_union_output_budget_alert(self):
        """Test that PydanticWidgetOutput correctly discriminates budget_alert."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "budget_alert",
            "is_active": True,
            "is_deprecated": False,
            "category_name": "Groceries",
            "category_icon": "🛒",
            "spent_amount": 850,
            "period_type": "month",
            "target_date": "2024-03-31",
            "alert_type": "exceeded",
        }
        widget = PydanticWidgetOutputValidator.model_validate(data)
        assert isinstance(widget, PydanticBudgetAlertWidgetOutput)
        assert widget.widget_type == "budget_alert"
        assert widget.alert_type == "exceeded"

    def test_discriminated_union_output_debt_free_time(self):
        """Test that PydanticWidgetOutput correctly discriminates debt_free_time."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "debt_free_time",
            "is_active": True,
            "is_deprecated": False,
            "years": 2,
            "months": 6,
            "card_id": "card_789",
            "payment_strategy": "with_extra_payment",
        }
        widget = PydanticWidgetOutputValidator.model_validate(data)
        assert isinstance(widget, PydanticDebtFreeTimeWidgetOutput)
        assert widget.widget_type == "debt_free_time"
        assert widget.years == 2

    def test_discriminated_union_output_invalid_widget_type(self):
        """Test that invalid widget_type raises validation error."""
        widget_id = uuid4()
        data = {
            "id": str(widget_id),
            "widget_type": "invalid_widget_type",
            "is_active": True,
            "is_deprecated": False,
        }
        with pytest.raises(ValidationError) as exc_info:
            PydanticWidgetOutputValidator.model_validate(data)
        assert "widget_type" in str(exc_info.value).lower() or "discriminator" in str(exc_info.value).lower()

    def test_discriminated_union_serialization_input(self):
        """Test serialization of discriminated union input."""
        widget_id = uuid4()
        widget = PydanticLanguageSelectorWidgetInput(
            id=widget_id,
            widget_type="language_selector",
        )
        result = widget.model_dump()
        assert result["widget_type"] == "language_selector"
        assert result["id"] == widget_id  # UUID is preserved in model_dump()

        # Test JSON serialization
        json_result = widget.model_dump(mode="json")
        assert json_result["widget_type"] == "language_selector"
        assert json_result["id"] == str(widget_id)  # UUID is stringified in JSON mode

    def test_discriminated_union_serialization_output(self):
        """Test serialization of discriminated union output."""
        widget_id = uuid4()
        widget = PydanticCreditScoreValueWidgetOutput(
            id=widget_id,
            widget_type="credit_score_value",
            is_active=True,
            is_deprecated=False,
            score_value=720,
            score_color_zone="good",
            trend="up",
        )
        result = widget.model_dump()
        assert result["widget_type"] == "credit_score_value"
        assert result["score_value"] == 720
        assert result["score_color_zone"] == "good"
        assert result["trend"] == "up"

    def test_discriminated_union_from_attributes_input(self):
        """Test discriminated union from attributes for input."""
        from dataclasses import dataclass

        @dataclass
        class MockWidget:
            id: UUID
            widget_type: str

        mock_widget = MockWidget(id=uuid4(), widget_type="language_selector")
        widget = PydanticWidgetInputValidator.model_validate(mock_widget, from_attributes=True)
        assert isinstance(widget, PydanticLanguageSelectorWidgetInput)
        assert widget.widget_type == "language_selector"

    def test_discriminated_union_from_attributes_output(self):
        """Test discriminated union from attributes for output."""
        from dataclasses import dataclass

        @dataclass
        class MockWidget:
            id: UUID
            widget_type: str
            is_active: bool
            is_deprecated: bool
            score_value: int
            score_color_zone: str
            trend: str

        mock_widget = MockWidget(
            id=uuid4(),
            widget_type="credit_score_value",
            is_active=True,
            is_deprecated=False,
            score_value=720,
            score_color_zone="good",
            trend="up",
        )
        widget = PydanticWidgetOutputValidator.model_validate(mock_widget, from_attributes=True)
        assert isinstance(widget, PydanticCreditScoreValueWidgetOutput)
        assert widget.score_value == 720
