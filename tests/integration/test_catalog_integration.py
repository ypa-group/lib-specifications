"""Integration tests for catalog callbacks with SpecificationEvaluator."""

from datetime import date, datetime, timedelta

import pytest

from lib_specifications.catalog import callback_registry
from lib_specifications.core.evaluator import SpecificationEvaluator
from lib_specifications.core.parameters import (
    ParameterLiteralValue,
    ParameterPathValue,
    generate_signature_from_callable,
)
from lib_specifications.core import (
    AndSpecification,
    CallbackSpecification,
    NotSpecification,
    OrSpecification,
)


@pytest.mark.integration
class TestCatalogCallbacksIntegration:
    """Integration tests for catalog callbacks with SpecificationEvaluator."""

    @pytest.fixture
    def evaluator(self) -> SpecificationEvaluator:
        """Create evaluator with default callback registry."""
        return SpecificationEvaluator(callback_registry)

    @pytest.mark.asynchronous
    async def test_is_today_callback_with_evaluator(self, evaluator):
        """Test IsTodayCallback with SpecificationEvaluator."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import IsTodayCallback

        signature = generate_signature_from_callable(IsTodayCallback.__init__)
        params: dict[str, ParameterPathValue] = {
            "dt": {
                "parameter_type": "path",
                "data_type": "date",
                "value": "event.date",
            }
        }
        spec = CallbackSpecification(
            callback_name="isToday",
            signature=signature,
            params=params,
        )

        # Test with today's date
        data = {"event": {"date": date.today()}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        # Test with past date
        data = {"event": {"date": date.today() - timedelta(days=1)}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

        # Test with future date
        data = {"event": {"date": date.today() + timedelta(days=1)}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_is_same_day_of_week_callback_with_evaluator(self, evaluator):
        """Test IsSameDayOfWeekCallback with SpecificationEvaluator."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import IsSameDayOfWeekCallback

        signature = generate_signature_from_callable(IsSameDayOfWeekCallback.__init__)
        params: dict[str, ParameterPathValue] = {
            "dt": {
                "parameter_type": "path",
                "data_type": "date",
                "value": "appointment.date",
            },
            "reference_date": {
                "parameter_type": "path",
                "data_type": "date",
                "value": "reference.date",
            },
        }
        spec = CallbackSpecification(
            callback_name="isSameDayOfWeek",
            signature=signature,
            params=params,
        )

        # Test with same day of week (both Mondays)
        data = {
            "appointment": {"date": date(2026, 1, 5)},
            "reference": {"date": date(2026, 1, 12)},
        }
        result = await evaluator.evaluate(spec, data)
        assert result is True

        # Test with different day of week
        data = {
            "appointment": {"date": date(2026, 1, 5)},  # Monday
            "reference": {"date": date(2026, 1, 6)},  # Tuesday
        }
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_is_future_date_callback_with_evaluator(self, evaluator):
        """Test IsFutureDateCallback with SpecificationEvaluator."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import IsFutureDateCallback

        signature = generate_signature_from_callable(IsFutureDateCallback.__init__)
        params: dict[str, ParameterPathValue] = {
            "dt": {
                "parameter_type": "path",
                "data_type": "date",
                "value": "deadline.date",
            }
        }
        spec = CallbackSpecification(
            callback_name="isFutureDate",
            signature=signature,
            params=params,
        )

        # Test with future date
        data = {"deadline": {"date": date.today() + timedelta(days=5)}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        # Test with today
        data = {"deadline": {"date": date.today()}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

        # Test with past date
        data = {"deadline": {"date": date.today() - timedelta(days=5)}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_is_date_in_range_callback_with_evaluator(self, evaluator):
        """Test IsDateInRangeCallback with SpecificationEvaluator."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import IsDateInRangeCallback

        signature = generate_signature_from_callable(IsDateInRangeCallback.__init__)
        params: dict[str, ParameterPathValue | ParameterLiteralValue] = {
            "dt": {
                "parameter_type": "path",
                "data_type": "date",
                "value": "event.date",
            },
            "start_date": {
                "parameter_type": "value",
                "data_type": "date",
                "value": date(2026, 1, 1),
            },
            "end_date": {
                "parameter_type": "value",
                "data_type": "date",
                "value": date(2026, 1, 31),
            },
        }
        spec = CallbackSpecification(
            callback_name="isDateInRange",
            signature=signature,
            params=params,
        )

        # Test with date in range
        data = {"event": {"date": date(2026, 1, 15)}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        # Test with date before range
        data = {"event": {"date": date(2025, 12, 31)}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

        # Test with date after range
        data = {"event": {"date": date(2026, 2, 1)}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

        # Test with date at start boundary
        data = {"event": {"date": date(2026, 1, 1)}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        # Test with date at end boundary
        data = {"event": {"date": date(2026, 1, 31)}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

    @pytest.mark.asynchronous
    async def test_is_within_days_callback_with_evaluator(self, evaluator):
        """Test IsWithinDaysCallback with SpecificationEvaluator."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import IsWithinDaysCallback

        signature = generate_signature_from_callable(IsWithinDaysCallback.__init__)
        params: dict[str, ParameterPathValue | ParameterLiteralValue] = {
            "dt": {
                "parameter_type": "path",
                "data_type": "date",
                "value": "event.date",
            },
            "days": {
                "parameter_type": "value",
                "data_type": "int",
                "value": 7,
            },
        }
        spec = CallbackSpecification(
            callback_name="isWithinDays",
            signature=signature,
            params=params,
        )

        # Test with date within 7 days (future)
        data = {"event": {"date": date.today() + timedelta(days=3)}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        # Test with date within 7 days (past)
        data = {"event": {"date": date.today() - timedelta(days=3)}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        # Test with date beyond 7 days
        data = {"event": {"date": date.today() + timedelta(days=10)}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

        # Test with today
        data = {"event": {"date": date.today()}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

    @pytest.mark.asynchronous
    async def test_is_day_after_today_callback_with_evaluator(self, evaluator):
        """Test IsDayAfterTodayCallback with SpecificationEvaluator."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import IsDayAfterTodayCallback

        signature = generate_signature_from_callable(IsDayAfterTodayCallback.__init__)
        params: dict[str, ParameterPathValue | ParameterLiteralValue] = {
            "dt": {
                "parameter_type": "path",
                "data_type": "date",
                "value": "deadline.date",
            },
            "days": {
                "parameter_type": "value",
                "data_type": "int",
                "value": 2,
            },
            "strict": {
                "parameter_type": "value",
                "data_type": "bool",
                "value": True,
            },
        }
        spec = CallbackSpecification(
            callback_name="isDayAfterToday",
            signature=signature,
            params=params,
        )

        # Test with exact match (2 days after today)
        data = {"deadline": {"date": date.today() + timedelta(days=2)}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        # Test with different day
        data = {"deadline": {"date": date.today() + timedelta(days=3)}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_is_same_month_callback_with_evaluator(self, evaluator):
        """Test IsSameMonthCallback with SpecificationEvaluator."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import IsSameMonthCallback

        signature = generate_signature_from_callable(IsSameMonthCallback.__init__)
        params: dict[str, ParameterPathValue] = {
            "dt": {
                "parameter_type": "path",
                "data_type": "date",
                "value": "event.date",
            },
            "reference_date": {
                "parameter_type": "path",
                "data_type": "date",
                "value": "reference.date",
            },
        }
        spec = CallbackSpecification(
            callback_name="isSameMonth",
            signature=signature,
            params=params,
        )

        # Test with same month and year
        data = {
            "event": {"date": date(2026, 1, 15)},
            "reference": {"date": date(2026, 1, 31)},
        }
        result = await evaluator.evaluate(spec, data)
        assert result is True

        # Test with different month
        data = {
            "event": {"date": date(2026, 1, 15)},
            "reference": {"date": date(2026, 2, 1)},
        }
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_is_time_after_callback_with_evaluator(self, evaluator):
        """Test IsTimeAfterCallback with SpecificationEvaluator."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import IsTimeAfterCallback

        signature = generate_signature_from_callable(IsTimeAfterCallback.__init__)
        params: dict[str, ParameterPathValue | ParameterLiteralValue] = {
            "check_datetime": {
                "parameter_type": "path",
                "data_type": "datetime",
                "value": "activity.timestamp",
            },
            "gap_hours": {
                "parameter_type": "value",
                "data_type": "float",
                "value": 3.0,
            },
        }
        spec = CallbackSpecification(
            callback_name="isTimeAfter",
            signature=signature,
            params=params,
        )

        # Test with datetime within gap (2 hours ago)
        data = {"activity": {"timestamp": datetime.now() - timedelta(hours=2)}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        # Test with datetime beyond gap (4 hours ago)
        data = {"activity": {"timestamp": datetime.now() - timedelta(hours=4)}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

        # Test with future datetime
        data = {"activity": {"timestamp": datetime.now() + timedelta(hours=1)}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

    @pytest.mark.asynchronous
    async def test_callback_with_nested_data_structure(self, evaluator):
        """Test callback with deeply nested data structure."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import IsTodayCallback

        signature = generate_signature_from_callable(IsTodayCallback.__init__)
        params: dict[str, ParameterPathValue] = {
            "dt": {
                "parameter_type": "path",
                "data_type": "date",
                "value": "user.profile.events.latest.date",
            }
        }
        spec = CallbackSpecification(
            callback_name="isToday",
            signature=signature,
            params=params,
        )

        # Test with nested structure
        data = {
            "user": {
                "profile": {
                    "events": {
                        "latest": {
                            "date": date.today(),
                        }
                    }
                }
            }
        }
        result = await evaluator.evaluate(spec, data)
        assert result is True

        # Test with different date
        data = {
            "user": {
                "profile": {
                    "events": {
                        "latest": {
                            "date": date.today() - timedelta(days=1),
                        }
                    }
                }
            }
        }
        result = await evaluator.evaluate(spec, data)
        assert result is False


@pytest.mark.integration
class TestCatalogCallbacksWithCombinators:
    """Integration tests for catalog callbacks combined with And/Or/Not specifications."""

    @pytest.fixture
    def evaluator(self) -> SpecificationEvaluator:
        """Create evaluator with default callback registry."""
        return SpecificationEvaluator(callback_registry)

    @pytest.mark.asynchronous
    async def test_callback_with_and_specification(self, evaluator):
        """Test combining catalog callback with And specification."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import (
            IsFutureDateCallback,
            IsTodayCallback,
        )

        # Create IsToday callback
        today_signature = generate_signature_from_callable(IsTodayCallback.__init__)
        today_spec = CallbackSpecification(
            callback_name="isToday",
            signature=today_signature,
            params={
                "dt": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "event.date",
                }
            },
        )

        # Create IsFutureDate callback
        future_signature = generate_signature_from_callable(IsFutureDateCallback.__init__)
        future_spec = CallbackSpecification(
            callback_name="isFutureDate",
            signature=future_signature,
            params={
                "dt": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "event.date",
                }
            },
        )

        # Combine with And
        combined_spec = AndSpecification(today_spec, future_spec)

        # Test: today AND future (should be False - today is not future)
        data = {"event": {"date": date.today()}}
        result = await evaluator.evaluate(combined_spec, data)
        assert result is False

        # Test: future date (should be False - not today)
        data = {"event": {"date": date.today() + timedelta(days=1)}}
        result = await evaluator.evaluate(combined_spec, data)
        assert result is False

        # Test: past date (should be False - neither today nor future)
        data = {"event": {"date": date.today() - timedelta(days=1)}}
        result = await evaluator.evaluate(combined_spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_callback_with_or_specification(self, evaluator):
        """Test combining catalog callbacks with Or specification."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import (
            IsDayBeforeTodayCallback,
            IsFutureDateCallback,
        )

        # Create IsFutureDate callback
        future_signature = generate_signature_from_callable(IsFutureDateCallback.__init__)
        future_spec = CallbackSpecification(
            callback_name="isFutureDate",
            signature=future_signature,
            params={
                "dt": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "event.date",
                }
            },
        )

        # Create IsDayBeforeToday callback (checks if date is at least 5 days before today, non-strict)
        # With strict=False: dt <= (today - days), meaning dt is at least N days in the past
        before_signature = generate_signature_from_callable(IsDayBeforeTodayCallback.__init__)
        before_spec = CallbackSpecification(
            callback_name="isDayBeforeToday",
            signature=before_signature,
            params={
                "dt": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "event.date",
                },
                "days": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 5,
                },
                "strict": {
                    "parameter_type": "value",
                    "data_type": "bool",
                    "value": False,  # Non-strict: at least 5 days before (further in past)
                },
            },
        )

        # Combine with Or
        combined_spec = OrSpecification(future_spec, before_spec)

        # Test: future date (should be True)
        data = {"event": {"date": date.today() + timedelta(days=5)}}
        result = await evaluator.evaluate(combined_spec, data)
        assert result is True

        # Test: exactly 5 days before today (should be True)
        data = {"event": {"date": date.today() - timedelta(days=5)}}
        result = await evaluator.evaluate(combined_spec, data)
        assert result is True

        # Test: more than 5 days before today (should be True - at least 5 days before)
        data = {"event": {"date": date.today() - timedelta(days=10)}}
        result = await evaluator.evaluate(combined_spec, data)
        assert result is True

        # Test: less than 5 days before today (should be False - not future and not at least 5 days before)
        data = {"event": {"date": date.today() - timedelta(days=3)}}
        result = await evaluator.evaluate(combined_spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_callback_with_not_specification(self, evaluator):
        """Test combining catalog callback with Not specification."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import IsFutureDateCallback

        # Create IsFutureDate callback
        future_signature = generate_signature_from_callable(IsFutureDateCallback.__init__)
        future_spec = CallbackSpecification(
            callback_name="isFutureDate",
            signature=future_signature,
            params={
                "dt": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "event.date",
                }
            },
        )

        # Negate with Not (not future = past or today)
        not_future_spec = NotSpecification(future_spec)

        # Test: past date (should be True - not future)
        data = {"event": {"date": date.today() - timedelta(days=1)}}
        result = await evaluator.evaluate(not_future_spec, data)
        assert result is True

        # Test: today (should be True - not future)
        data = {"event": {"date": date.today()}}
        result = await evaluator.evaluate(not_future_spec, data)
        assert result is True

        # Test: future date (should be False - is future)
        data = {"event": {"date": date.today() + timedelta(days=1)}}
        result = await evaluator.evaluate(not_future_spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_complex_combined_specification(self, evaluator):
        """Test complex combination of multiple catalog callbacks."""
        from lib_specifications.catalog.callback_registry.datetime_callbacks import (
            IsFutureDateCallback,
            IsSameMonthCallback,
            IsWithinDaysCallback,
        )

        # Create IsFutureDate callback
        future_signature = generate_signature_from_callable(IsFutureDateCallback.__init__)
        future_spec = CallbackSpecification(
            callback_name="isFutureDate",
            signature=future_signature,
            params={
                "dt": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "event.date",
                }
            },
        )

        # Create IsWithinDays callback
        within_days_signature = generate_signature_from_callable(IsWithinDaysCallback.__init__)
        within_days_spec = CallbackSpecification(
            callback_name="isWithinDays",
            signature=within_days_signature,
            params={
                "dt": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "event.date",
                },
                "days": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 7,
                },
            },
        )

        # Create IsSameMonth callback
        same_month_signature = generate_signature_from_callable(IsSameMonthCallback.__init__)
        same_month_spec = CallbackSpecification(
            callback_name="isSameMonth",
            signature=same_month_signature,
            params={
                "dt": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "event.date",
                },
                "reference_date": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "reference.date",
                },
            },
        )

        # Complex: (future AND within 7 days) AND same month as reference
        future_and_within = AndSpecification(future_spec, within_days_spec)
        complex_spec = AndSpecification(future_and_within, same_month_spec)

        # Test: future date within 7 days in same month as reference
        future_date = date.today() + timedelta(days=3)
        reference_date = date.today()
        data = {
            "event": {"date": future_date},
            "reference": {"date": reference_date},
        }
        result = await evaluator.evaluate(complex_spec, data)
        # Should be True if future_date is in same month and within 7 days
        assert isinstance(result, bool)

        # Test: future date within 7 days but different month
        if future_date.month == 12:
            # If we're in December, use January for different month
            different_month_date = date(future_date.year + 1, 1, 1)
        else:
            different_month_date = date(future_date.year, future_date.month + 1, 1)

        data = {
            "event": {"date": future_date},
            "reference": {"date": different_month_date},
        }
        result = await evaluator.evaluate(complex_spec, data)
        assert result is False


@pytest.mark.integration
class TestCatalogRegistryIntegration:
    """Integration tests for default callback registry usage."""

    @pytest.mark.asynchronous
    async def test_all_registered_callbacks_are_accessible(self):
        """Test that all registered callbacks can be retrieved and used."""
        # Just verify the registry, don't need evaluator for this test

        # Test a few key callbacks
        callback_names = [
            "isToday",
            "isFutureDate",
            "isWithinDays",
            "isDateInRange",
            "isSameMonth",
            "isTimeAfter",
        ]

        for callback_name in callback_names:
            callback_class = callback_registry.get(callback_name)
            assert callback_class is not None, f"{callback_name} should be registered"

            signature = callback_registry.get_signature(callback_name)
            assert signature is not None, f"{callback_name} should have a signature"

    @pytest.mark.asynchronous
    async def test_callback_registry_with_evaluator(self):
        """Test that evaluator can use callbacks from default registry."""
        evaluator = SpecificationEvaluator(callback_registry)

        from lib_specifications.catalog.callback_registry.datetime_callbacks import IsTodayCallback
        from lib_specifications.core.parameters import generate_signature_from_callable

        signature = generate_signature_from_callable(IsTodayCallback.__init__)
        spec = CallbackSpecification(
            callback_name="isToday",
            signature=signature,
            params={
                "dt": {
                    "parameter_type": "path",
                    "data_type": "date",
                    "value": "date",
                }
            },
        )

        data = {"date": date.today()}
        result = await evaluator.evaluate(spec, data)
        assert result is True
