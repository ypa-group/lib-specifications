"""Tests for default callback registry."""

import pytest

from lib_specifications.catalog.callback_registry import (
    CALLBACK_REGISTRY,
    HasArrayInitializedCallback,
    HasConnectedCreditCardCallback,
    HasCreditScoreCallback,
    HasOnboardedCallback,
    HasPlaidInitializedCallback,
)
from lib_specifications.catalog.callback_registry.datetime_callbacks import (
    IsDateInRangeCallback,
    IsDayAfterTodayCallback,
    IsDayBeforeTodayCallback,
    IsDayNotLaterThanCallback,
    IsDayOfMonthCallback,
    IsFutureDateCallback,
    IsSameDayOfWeekCallback,
    IsSameMonthCallback,
    IsSameYearCallback,
    IsTimeAfterCallback,
    IsTodayCallback,
    IsWithinDaysCallback,
)


@pytest.mark.unit
class TestDefaultCallbackRegistry:
    """Tests for default callback registry."""

    def test_registry_is_initialized(self):
        """Test that callback_registry is initialized."""
        assert CALLBACK_REGISTRY is not None
        assert hasattr(CALLBACK_REGISTRY, "register")
        assert hasattr(CALLBACK_REGISTRY, "get")
        assert hasattr(CALLBACK_REGISTRY, "has")

    def test_is_today_registered(self):
        """Test that isToday callback is registered."""
        assert CALLBACK_REGISTRY.has("isToday")
        assert CALLBACK_REGISTRY.get("isToday") == IsTodayCallback

    def test_is_day_after_today_registered(self):
        """Test that isDayAfterToday callback is registered."""
        assert CALLBACK_REGISTRY.has("isDayAfterToday")
        assert CALLBACK_REGISTRY.get("isDayAfterToday") == IsDayAfterTodayCallback

    def test_is_day_before_today_registered(self):
        """Test that isDayBeforeToday callback is registered."""
        assert CALLBACK_REGISTRY.has("isDayBeforeToday")
        assert CALLBACK_REGISTRY.get("isDayBeforeToday") == IsDayBeforeTodayCallback

    def test_is_date_in_range_registered(self):
        """Test that isDateInRange callback is registered."""
        assert CALLBACK_REGISTRY.has("isDateInRange")
        assert CALLBACK_REGISTRY.get("isDateInRange") == IsDateInRangeCallback

    def test_is_day_not_later_than_registered(self):
        """Test that isDayNotLaterThan callback is registered."""
        assert CALLBACK_REGISTRY.has("isDayNotLaterThan")
        assert CALLBACK_REGISTRY.get("isDayNotLaterThan") == IsDayNotLaterThanCallback

    def test_is_future_date_registered(self):
        """Test that isFutureDate callback is registered."""
        assert CALLBACK_REGISTRY.has("isFutureDate")
        assert CALLBACK_REGISTRY.get("isFutureDate") == IsFutureDateCallback

    def test_is_within_days_registered(self):
        """Test that isWithinDays callback is registered."""
        assert CALLBACK_REGISTRY.has("isWithinDays")
        assert CALLBACK_REGISTRY.get("isWithinDays") == IsWithinDaysCallback

    def test_is_same_day_of_week_registered(self):
        """Test that isSameDayOfWeek callback is registered."""
        assert CALLBACK_REGISTRY.has("isSameDayOfWeek")
        assert CALLBACK_REGISTRY.get("isSameDayOfWeek") == IsSameDayOfWeekCallback

    def test_is_day_of_month_registered(self):
        """Test that isDayOfMonth callback is registered."""
        assert CALLBACK_REGISTRY.has("isDayOfMonth")
        assert CALLBACK_REGISTRY.get("isDayOfMonth") == IsDayOfMonthCallback

    def test_is_same_month_registered(self):
        """Test that isSameMonth callback is registered."""
        assert CALLBACK_REGISTRY.has("isSameMonth")
        assert CALLBACK_REGISTRY.get("isSameMonth") == IsSameMonthCallback

    def test_is_same_year_registered(self):
        """Test that isSameYear callback is registered."""
        assert CALLBACK_REGISTRY.has("isSameYear")
        assert CALLBACK_REGISTRY.get("isSameYear") == IsSameYearCallback

    def test_is_time_after_registered(self):
        """Test that isTimeAfter callback is registered."""
        assert CALLBACK_REGISTRY.has("isTimeAfter")
        assert CALLBACK_REGISTRY.get("isTimeAfter") == IsTimeAfterCallback

    def test_has_user_onboarded_registered(self):
        """Test that hasOnboarded callback is registered."""
        assert CALLBACK_REGISTRY.has("hasOnboarded")
        assert CALLBACK_REGISTRY.get("hasOnboarded") == HasOnboardedCallback

    def test_all_datetime_callbacks_registered(self):
        """Test that all datetime callbacks are registered."""
        expected_callbacks = {
            "isToday": IsTodayCallback,
            "isDayAfterToday": IsDayAfterTodayCallback,
            "isDayBeforeToday": IsDayBeforeTodayCallback,
            "isDateInRange": IsDateInRangeCallback,
            "isDayNotLaterThan": IsDayNotLaterThanCallback,
            "isFutureDate": IsFutureDateCallback,
            "isWithinDays": IsWithinDaysCallback,
            "isSameDayOfWeek": IsSameDayOfWeekCallback,
            "isDayOfMonth": IsDayOfMonthCallback,
            "isSameMonth": IsSameMonthCallback,
            "isSameYear": IsSameYearCallback,
            "isTimeAfter": IsTimeAfterCallback,
        }

        for name, callback_class in expected_callbacks.items():
            assert CALLBACK_REGISTRY.has(name), f"{name} should be registered"
            assert CALLBACK_REGISTRY.get(name) == callback_class, f"{name} should map to {callback_class.__name__}"

    def test_user_callbacks_registered(self):
        """Test that user callbacks are registered."""
        expected_callbacks = {
            "hasOnboarded": HasOnboardedCallback,
            "hasPlaidInitialized": HasPlaidInitializedCallback,
            "hasConnectedCreditCard": HasConnectedCreditCardCallback,
            "hasArrayInitialized": HasArrayInitializedCallback,
            "hasCreditScore": HasCreditScoreCallback,
        }

        for name, callback_class in expected_callbacks.items():
            assert CALLBACK_REGISTRY.has(name), f"{name} should be registered"
            assert CALLBACK_REGISTRY.get(name) == callback_class, f"{name} should map to {callback_class.__name__}"

    def test_registry_has_signatures(self):
        """Test that all registered callbacks have signatures."""
        callback_names = [
            "isToday",
            "isDayAfterToday",
            "isDayBeforeToday",
            "isDateInRange",
            "isDayNotLaterThan",
            "isFutureDate",
            "isWithinDays",
            "isSameDayOfWeek",
            "isDayOfMonth",
            "isSameMonth",
            "isSameYear",
            "isTimeAfter",
            "hasOnboarded",
            "hasPlaidInitialized",
            "hasConnectedCreditCard",
            "hasArrayInitialized",
            "hasCreditScore",
        ]

        for name in callback_names:
            signature = CALLBACK_REGISTRY.get_signature(name)
            assert signature is not None, f"{name} should have a signature"

    def test_is_today_signature(self):
        """Test that isToday has correct signature."""
        signature = CALLBACK_REGISTRY.get_signature("isToday")
        assert signature is not None
        assert "dt" in signature.parameters
        assert signature.parameters["dt"].data_type.label == "date"

    def test_is_day_after_today_signature(self):
        """Test that isDayAfterToday has correct signature."""
        signature = CALLBACK_REGISTRY.get_signature("isDayAfterToday")
        assert signature is not None
        assert "dt" in signature.parameters
        assert "days" in signature.parameters
        assert "strict" in signature.parameters

    def test_has_user_onboarded_signature(self):
        """Test that hasOnboarded has correct signature."""
        signature = CALLBACK_REGISTRY.get_signature("hasOnboarded")
        assert signature is not None
        assert "auth_provider" in signature.parameters
        assert "auth_provider_user_id" in signature.parameters

    def test_list_names_includes_all_callbacks(self):
        """Test that list_names includes all registered callbacks."""
        names = CALLBACK_REGISTRY.list_names()

        expected_names = {
            "isToday",
            "isDayAfterToday",
            "isDayBeforeToday",
            "isDateInRange",
            "isDayNotLaterThan",
            "isFutureDate",
            "isWithinDays",
            "isSameDayOfWeek",
            "isDayOfMonth",
            "isSameMonth",
            "isSameYear",
            "isTimeAfter",
            "hasOnboarded",
            "hasPlaidInitialized",
            "hasConnectedCreditCard",
            "hasArrayInitialized",
            "hasCreditScore",
        }

        for name in expected_names:
            assert name in names, f"{name} should be in list_names()"
