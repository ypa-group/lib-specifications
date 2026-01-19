"""Tests for widget functionality and context data population."""

from datetime import date
from uuid import uuid4

import pytest

from lib_specifications.catalog.trigger_registry.budget import BUDGET
from lib_specifications.catalog.widget_registry import WIDGETS_REGISTRY
from lib_specifications.core.parameters import ParameterTypeEnum
from lib_specifications.core.widgets import (
    BaseWidget,
    BudgetAlertWidget,
    BudgetCategoryAmountWidget,
    CreditCardSummaryWidget,
    CreditScoreValueWidget,
    DebtFreeTimeWidget,
    LanguageSelectorWidget,
    PaymentReminderWidget,
    WidgetRegistry,
)


class TestBaseWidget:
    """Test base widget functionality."""

    def test_get_nested_value_simple(self):
        """Test getting a simple nested value."""
        widget = BaseWidget(
            id=uuid4(),
            widget_type="language_selector",
        )
        data = {"user": {"id": 123}}
        result = widget._get_nested_value(data, "user.id")
        assert result == 123

    def test_get_nested_value_deep(self):
        """Test getting a deeply nested value."""
        widget = BaseWidget(
            id=uuid4(),
            widget_type="language_selector",
        )
        data = {"user": {"profile": {"settings": {"theme": "dark"}}}}
        result = widget._get_nested_value(data, "user.profile.settings.theme")
        assert result == "dark"

    def test_get_nested_value_missing_key(self):
        """Test error when key is missing."""
        widget = BaseWidget(
            id=uuid4(),
            widget_type="language_selector",
        )
        data = {"user": {"id": 123}}
        with pytest.raises(KeyError, match="Path 'user.name' not found"):
            widget._get_nested_value(data, "user.name")

    def test_extract_parameter_value_literal(self):
        """Test extracting a literal parameter value."""
        widget = BaseWidget(
            id=uuid4(),
            widget_type="language_selector",
        )
        parameter = {
            "parameter_type": "value",
            "data_type": ParameterTypeEnum.INT.label,
            "value": 42,
        }
        context = {}
        result = widget._extract_parameter_value(parameter, context, "test_param")
        assert result == 42

    def test_extract_parameter_value_path(self):
        """Test extracting a parameter value from context path."""
        widget = BaseWidget(
            id=uuid4(),
            widget_type="language_selector",
        )
        parameter = {
            "parameter_type": "path",
            "data_type": ParameterTypeEnum.INT.label,
            "value": "user.score",
        }
        context = {"user": {"score": 750}}
        result = widget._extract_parameter_value(parameter, context, "test_param")
        assert result == 750

    def test_populate_widget_base(self):
        """Test base widget population."""
        widget_id = uuid4()
        widget = BaseWidget(
            id=widget_id,
            widget_type="language_selector",
        )
        context = {}
        result = widget.populate_widget(context)
        assert result == {
            "id": widget_id,
            "widget_type": "language_selector",
            "is_active": True,
            "is_deprecated": False,
        }


class TestLanguageSelectorWidget:
    """Test language selector widget."""

    def test_populate_widget(self):
        """Test language selector widget population."""
        widget_id = uuid4()
        widget = LanguageSelectorWidget(
            id=widget_id,
        )
        context = {}
        result = widget.populate_widget(context)
        assert result == {
            "id": widget_id,
            "widget_type": "language_selector",
            "is_active": True,
            "is_deprecated": False,
        }


class TestCreditScoreValueWidget:
    """Test credit score value widget with context data population."""

    def test_populate_widget_with_context_data(self):
        """Test credit score widget populated from context data."""
        widget_id = uuid4()
        widget = CreditScoreValueWidget(
            id=widget_id,
            params={
                "current_score_value": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "user.credit_score.current",
                },
                "previous_score_value": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "user.credit_score.previous",
                },
            },
        )

        # Context data that will be used to populate the widget
        context = {
            "user": {
                "credit_score": {
                    "current": 720,
                    "previous": 680,
                }
            }
        }

        result = widget.populate_widget(context)

        assert result["id"] == widget_id
        assert result["widget_type"] == "credit_score_value"
        assert result["score_value"] == 720  # From context
        assert result["score_color_zone"] == "good"  # Calculated (670-739)
        assert result["trend"] == "up"  # 720 > 680

    def test_populate_widget_with_literal_values(self):
        """Test credit score widget with literal parameter values."""
        widget_id = uuid4()
        widget = CreditScoreValueWidget(
            id=widget_id,
            params={
                "current_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 650,
                },
                "previous_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 700,
                },
            },
        )

        context = {}

        result = widget.populate_widget(context)

        assert result["score_value"] == 650
        assert result["score_color_zone"] == "fair"  # 580-669
        assert result["trend"] == "down"  # 650 < 700

    def test_populate_widget_mixed_parameters(self):
        """Test credit score widget with mixed path and literal parameters."""
        widget_id = uuid4()
        widget = CreditScoreValueWidget(
            id=widget_id,
            params={
                "current_score_value": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "credit.current",
                },
                "previous_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 600,
                },
            },
        )

        context = {
            "credit": {
                "current": 800,
            }
        }

        result = widget.populate_widget(context)

        assert result["score_value"] == 800
        assert result["score_color_zone"] == "excellent"  # 800-850
        assert result["trend"] == "up"  # 800 > 600

    def test_score_color_zones(self):
        """Test all credit score color zones."""
        widget_id = uuid4()

        test_cases = [
            (300, "poor"),
            (579, "poor"),
            (580, "fair"),
            (669, "fair"),
            (670, "good"),
            (739, "good"),
            (740, "very good"),
            (799, "very good"),
            (800, "excellent"),
            (850, "excellent"),
        ]

        for score, expected_zone in test_cases:
            widget = CreditScoreValueWidget(
                id=widget_id,
                params={
                    "current_score_value": {
                        "parameter_type": "value",
                        "data_type": ParameterTypeEnum.INT.label,
                        "value": score,
                    },
                    "previous_score_value": {
                        "parameter_type": "value",
                        "data_type": ParameterTypeEnum.INT.label,
                        "value": score - 10,
                    },
                },
            )

            context = {}
            result = widget.populate_widget(context)
            assert result["score_color_zone"] == expected_zone, f"Score {score} should be {expected_zone}"

    def test_trend_calculation(self):
        """Test trend calculation (up vs down)."""
        widget_id = uuid4()

        # Test upward trend
        widget_up = CreditScoreValueWidget(
            id=widget_id,
            params={
                "current_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 750,
                },
                "previous_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 700,
                },
            },
        )
        result_up = widget_up.populate_widget({})
        assert result_up["trend"] == "up"

        # Test downward trend
        widget_down = CreditScoreValueWidget(
            id=widget_id,
            params={
                "current_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 650,
                },
                "previous_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 700,
                },
            },
        )
        result_down = widget_down.populate_widget({})
        assert result_down["trend"] == "down"

        # Test equal (should be "up" based on implementation)
        widget_equal = CreditScoreValueWidget(
            id=widget_id,
            params={
                "current_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 700,
                },
                "previous_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 700,
                },
            },
        )
        result_equal = widget_equal.populate_widget({})
        assert result_equal["trend"] == "up"  # Equal is treated as "up"


class TestWidgetContextDataPopulation:
    """Test widget population with various context data structures."""

    def test_complex_context_structure(self):
        """Test widget with complex nested context data."""
        widget_id = uuid4()
        widget = CreditScoreValueWidget(
            id=widget_id,
            params={
                "current_score_value": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "financial.credit.score.current",
                },
                "previous_score_value": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "financial.credit.score.previous",
                },
            },
        )

        # Complex nested context structure
        context = {
            "financial": {
                "credit": {
                    "score": {
                        "current": 780,
                        "previous": 750,
                        "history": [750, 760, 770, 780],
                    }
                }
            },
            "user": {
                "id": "123",
                "name": "John Doe",
            },
        }

        result = widget.populate_widget(context)

        assert result["score_value"] == 780
        assert result["score_color_zone"] == "very good"
        assert result["trend"] == "up"

    def test_widget_with_missing_context_path(self):
        """Test widget error handling when context path is missing."""
        widget_id = uuid4()
        widget = CreditScoreValueWidget(
            id=widget_id,
            params={
                "current_score_value": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "user.credit_score.current",
                },
                "previous_score_value": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "user.credit_score.previous",
                },
            },
        )

        # Context missing the required path
        context = {
            "user": {
                "id": "123",
            }
        }

        with pytest.raises(KeyError, match="Path 'user.credit_score.current' not found"):
            widget.populate_widget(context)

    def test_credit_score_widget_with_none_previous(self):
        """Test credit score widget when previous_score_value is None."""
        widget_id = uuid4()
        widget = CreditScoreValueWidget(
            id=widget_id,
            params={
                "current_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 720,
                },
                "previous_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": None,
                },
            },
        )
        result = widget.populate_widget({})
        assert result["score_value"] == 720
        assert result["trend"] is None


class TestBudgetCategoryAmountWidget:
    """Test budget category amount widget."""

    def test_populate_widget(self):
        """Test budget category amount widget population."""
        widget_id = uuid4()
        widget = BudgetCategoryAmountWidget(
            id=widget_id,
            params={
                "category_name": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "budget.category.name",
                },
                "amount": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "budget.category.amount",
                },
                "currency": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "USD",
                },
                "period_type": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "month",
                },
                "target_date": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.DATE.label,
                    "value": "budget.target_date",
                },
            },
        )

        context = {
            "budget": {
                "category": {
                    "name": "Restaurants",
                    "amount": 500,
                },
                "target_date": "2024-12-31",
            }
        }

        result = widget.populate_widget(context)
        assert result["category_name"] == "Restaurants"
        assert result["amount"] == 500
        assert result["currency"] == "USD"
        assert result["period_type"] == "month"
        assert result["target_date"] == date(2024, 12, 31)

    def test_budget_customize_trigger_with_widget(self):
        """Test budget__customize trigger with BudgetCategoryAmountWidget.

        This test emulates how UI would bind trigger context fields to widget params.
        The trigger context fields are at the root level of the context dict.
        """
        # Get the budget__customize trigger
        trigger = BUDGET.CUSTOMIZE
        assert trigger.fullname == "BUDGET__CUSTOMIZE"
        assert trigger.context_schema is not None

        # Verify trigger context schema matches widget signature
        trigger_params = trigger.context_schema.parameters
        assert "category_name" in trigger_params
        assert "amount" in trigger_params
        assert "currency" in trigger_params
        assert "period_type" in trigger_params
        assert "target_date" in trigger_params

        # Create context matching trigger's context schema
        # In real UI, trigger context fields are at root level
        context = {
            "category_name": "Groceries",
            "amount": 750,
            "currency": "USD",
            "period_type": "month",
            "target_date": "2024-06-15",
        }

        # Create widget with params bound to trigger context fields
        # This emulates how UI would bind: widget params reference trigger context fields directly
        widget_id = uuid4()
        widget = BudgetCategoryAmountWidget(
            id=widget_id,
            params={
                "category_name": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "category_name",  # Direct reference to trigger context field
                },
                "amount": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "amount",  # Direct reference to trigger context field
                },
                "currency": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "currency",  # Direct reference to trigger context field
                },
                "period_type": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "period_type",  # Direct reference to trigger context field
                },
                "target_date": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.DATE.label,
                    "value": "target_date",  # Direct reference to trigger context field
                },
            },
        )

        # Test widget creation - verify it has correct signature schema
        signature = widget.signature_schema
        assert signature.has_parameter("category_name")
        assert signature.has_parameter("amount")
        assert signature.has_parameter("currency")
        assert signature.has_parameter("period_type")
        assert signature.has_parameter("target_date")

        # Test widget evaluation/population
        result = widget.populate_widget(context)

        # Verify populated widget values match trigger context
        assert result["id"] == widget_id
        assert result["widget_type"] == "budget_category_amount"
        assert result["category_name"] == "Groceries"
        assert result["amount"] == 750
        assert result["currency"] == "USD"
        assert result["period_type"] == "month"
        assert result["target_date"] == date(2024, 6, 15)

        # Test with optional fields as None
        context_optional_none = {
            "category_name": "Entertainment",
            "amount": 200,
            "currency": "EUR",
            "period_type": None,
            "target_date": None,
        }

        result_optional = widget.populate_widget(context_optional_none)
        assert result_optional["category_name"] == "Entertainment"
        assert result_optional["amount"] == 200
        assert result_optional["currency"] == "EUR"
        assert result_optional["period_type"] is None
        assert result_optional["target_date"] is None


class TestCreditCardSummaryWidget:
    """Test credit card summary widget."""

    def test_populate_widget(self):
        """Test credit card summary widget population."""
        widget_id = uuid4()
        widget = CreditCardSummaryWidget(
            id=widget_id,
            params={
                "bank_name": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "card.bank_name",
                },
                "bank_logo": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "card.bank_logo",
                },
                "card_id": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "card.id",
                },
                "card_last_digits": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "card.last_digits",
                },
                "amount": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "card.debt_amount",
                },
            },
        )

        context = {
            "card": {
                "bank_name": "Chase",
                "bank_logo": "https://example.com/chase.png",
                "id": "card_123",
                "last_digits": "1234",
                "debt_amount": 2500,
            }
        }

        result = widget.populate_widget(context)
        assert result["bank_name"] == "Chase"
        assert result["bank_logo"] == "https://example.com/chase.png"
        assert result["card_id"] == "card_123"
        assert result["card_last_digits"] == "1234"
        assert result["amount"] == 2500


class TestPaymentReminderWidget:
    """Test payment reminder widget."""

    def test_populate_widget(self):
        """Test payment reminder widget population."""
        widget_id = uuid4()
        widget = PaymentReminderWidget(
            id=widget_id,
            params={
                "bank_name": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "Bank of America",
                },
                "bank_logo": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "https://example.com/bofa.png",
                },
                "card_id": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "payment.card_id",
                },
                "card_last_digits": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "payment.card_last_digits",
                },
                "payment_amount": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "payment.amount",
                },
                "due_date": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.DATE.label,
                    "value": "payment.due_date",
                },
            },
        )

        context = {
            "payment": {
                "card_id": "card_456",
                "card_last_digits": "5678",
                "amount": 150,
                "due_date": "2024-02-15",
            }
        }

        result = widget.populate_widget(context)
        assert result["bank_name"] == "Bank of America"
        assert result["bank_logo"] == "https://example.com/bofa.png"
        assert result["card_id"] == "card_456"
        assert result["card_last_digits"] == "5678"
        assert result["payment_amount"] == 150
        assert result["due_date"] == date(2024, 2, 15)


class TestBudgetAlertWidget:
    """Test budget alert widget."""

    def test_populate_widget(self):
        """Test budget alert widget population."""
        widget_id = uuid4()
        widget = BudgetAlertWidget(
            id=widget_id,
            params={
                "category_name": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "Groceries",
                },
                "category_icon": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "🛒",
                },
                "spent_amount": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "budget.spent",
                },
                "period_type": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "month",
                },
                "target_date": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.DATE.label,
                    "value": "budget.target_date",
                },
                "alert_type": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "exceeded",
                },
            },
        )

        context = {
            "budget": {
                "spent": 850,
                "target_date": "2024-03-31",
            }
        }

        result = widget.populate_widget(context)
        assert result["category_name"] == "Groceries"
        assert result["category_icon"] == "🛒"
        assert result["spent_amount"] == 850
        assert result["period_type"] == "month"
        assert result["target_date"] == date(2024, 3, 31)
        assert result["alert_type"] == "exceeded"


class TestDebtFreeTimeWidget:
    """Test debt free time widget."""

    def test_populate_widget(self):
        """Test debt free time widget population."""
        widget_id = uuid4()
        widget = DebtFreeTimeWidget(
            id=widget_id,
            params={
                "years": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "debt.years",
                },
                "months": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": "debt.months",
                },
                "card_id": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "card_789",
                },
                "payment_strategy": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "debt.strategy",
                },
            },
        )

        context = {
            "debt": {
                "years": 2,
                "months": 6,
                "strategy": "with_extra_payment",
            }
        }

        result = widget.populate_widget(context)
        assert result["years"] == 2
        assert result["months"] == 6
        assert result["card_id"] == "card_789"
        assert result["payment_strategy"] == "with_extra_payment"


class TestWidgetsRegistry:
    """Test widgets registry."""

    def test_registry_is_initialized(self):
        """Test that WIDGETS_REGISTRY is initialized."""
        assert WIDGETS_REGISTRY is not None
        assert isinstance(WIDGETS_REGISTRY, WidgetRegistry)
        assert len(WIDGETS_REGISTRY.widgets) > 0

    def test_all_widget_types_registered(self):
        """Test that all widget types from WidgetType are in the registry."""
        # Get all widget types from the registry
        registered_types = set(WIDGETS_REGISTRY.widgets.keys())

        # Expected widget types (from WidgetType literal)
        expected_types = {
            "language_selector",
            "credit_score_value",
            "budget_category_amount",
            "credit_card_summary",
            "payment_reminder",
            "budget_alert",
            "debt_free_time",
        }

        assert registered_types == expected_types, (
            f"Registry types {registered_types} don't match expected types {expected_types}"
        )

    def test_registry_maps_to_correct_widget_instances(self):
        """Test that each widget type maps to the correct widget instance."""
        assert isinstance(WIDGETS_REGISTRY.get_widget("language_selector"), LanguageSelectorWidget)
        assert isinstance(WIDGETS_REGISTRY.get_widget("credit_score_value"), CreditScoreValueWidget)
        assert isinstance(WIDGETS_REGISTRY.get_widget("budget_category_amount"), BudgetCategoryAmountWidget)
        assert isinstance(WIDGETS_REGISTRY.get_widget("credit_card_summary"), CreditCardSummaryWidget)
        assert isinstance(WIDGETS_REGISTRY.get_widget("payment_reminder"), PaymentReminderWidget)
        assert isinstance(WIDGETS_REGISTRY.get_widget("budget_alert"), BudgetAlertWidget)
        assert isinstance(WIDGETS_REGISTRY.get_widget("debt_free_time"), DebtFreeTimeWidget)

    def test_registry_widgets_are_base_widget_instances(self):
        """Test that all registry widgets are instances of BaseWidget."""
        for widget_type, widget_instance in WIDGETS_REGISTRY.widgets.items():
            assert isinstance(widget_instance, BaseWidget), (
                f"Widget instance for type '{widget_type}' is not an instance of BaseWidget"
            )
            assert widget_instance.widget_type == widget_type, (
                f"Widget instance type '{widget_instance.widget_type}' doesn't match registry key '{widget_type}'"
            )

    def test_get_widget_method(self):
        """Test that get_widget method returns correct widget instances."""
        # Test getting each widget type
        language_widget = WIDGETS_REGISTRY.get_widget("language_selector")
        assert isinstance(language_widget, LanguageSelectorWidget)
        assert language_widget.widget_type == "language_selector"

        credit_score_widget = WIDGETS_REGISTRY.get_widget("credit_score_value")
        assert isinstance(credit_score_widget, CreditScoreValueWidget)
        assert credit_score_widget.widget_type == "credit_score_value"

        budget_widget = WIDGETS_REGISTRY.get_widget("budget_category_amount")
        assert isinstance(budget_widget, BudgetCategoryAmountWidget)
        assert budget_widget.widget_type == "budget_category_amount"

        card_widget = WIDGETS_REGISTRY.get_widget("credit_card_summary")
        assert isinstance(card_widget, CreditCardSummaryWidget)
        assert card_widget.widget_type == "credit_card_summary"

        payment_widget = WIDGETS_REGISTRY.get_widget("payment_reminder")
        assert isinstance(payment_widget, PaymentReminderWidget)
        assert payment_widget.widget_type == "payment_reminder"

        alert_widget = WIDGETS_REGISTRY.get_widget("budget_alert")
        assert isinstance(alert_widget, BudgetAlertWidget)
        assert alert_widget.widget_type == "budget_alert"

        debt_widget = WIDGETS_REGISTRY.get_widget("debt_free_time")
        assert isinstance(debt_widget, DebtFreeTimeWidget)
        assert debt_widget.widget_type == "debt_free_time"

    def test_get_widget_invalid_type(self):
        """Test that get_widget raises ValueError for invalid widget type."""
        with pytest.raises(ValueError, match="Invalid widget type"):
            WIDGETS_REGISTRY.get_widget("invalid_widget_type")

    def test_get_all_widgets(self):
        """Test that get_all_widgets returns all registered widgets."""
        all_widgets = WIDGETS_REGISTRY.get_all_widgets()
        assert len(all_widgets) == 7
        assert all(isinstance(widget, BaseWidget) for widget in all_widgets)

        # Verify all widget types are present
        widget_types = {widget.widget_type for widget in all_widgets}
        expected_types = {
            "language_selector",
            "credit_score_value",
            "budget_category_amount",
            "credit_card_summary",
            "payment_reminder",
            "budget_alert",
            "debt_free_time",
        }
        assert widget_types == expected_types

    def test_widget_type_matches_registry_key(self):
        """Test that each widget's widget_type matches its registry key."""
        for widget_type in WIDGETS_REGISTRY.widgets.keys():
            widget = WIDGETS_REGISTRY.get_widget(widget_type)
            assert widget.widget_type == widget_type, (
                f"Widget type '{widget.widget_type}' doesn't match registry key '{widget_type}'"
            )
