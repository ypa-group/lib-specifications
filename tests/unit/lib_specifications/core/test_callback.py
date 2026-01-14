"""Tests for CallbackSpecification."""

import pytest

from lib_specifications.core.evaluator import SpecificationEvaluator
from lib_specifications.core.parameters import ParameterPathValue
from lib_specifications.core.callback import BaseCallback, CallbackRegistry
from lib_specifications.core import CallbackSpecification


# Concrete implementation
class IsAdultCallbackImpl(BaseCallback):
    """Concrete implementation of IsAdultCallback."""
    qualname = "is_adult"

    def __init__(self, age: int):
        self.age = age

    def __call__(self) -> bool:
        return self.age >= 18


# Concrete implementation
class WeekendAdultCallbackImpl(BaseCallback):
    """Concrete implementation of WeekendAdultCallback."""
    qualname = "weekend_adult"

    def __init__(self, age: int, day: str):
        self.age = age
        self.day = day

    def __call__(self) -> bool:
        return self.age >= 18 and self.day.lower() in ["saturday", "sunday"]


# Concrete implementation
class IsAdultWithMinCallbackImpl(BaseCallback):
    """Concrete implementation of IsAdultWithMinCallback."""
    qualname = "is_adult_min"

    def __init__(self, age: int, min_age: int = 18):
        self.age = age
        self.min_age = min_age

    def __call__(self) -> bool:
        return self.age >= self.min_age


@pytest.mark.unit
class TestCallbackSpecification:
    """Tests for CallbackSpecification."""

    @pytest.fixture
    def registry(self) -> CallbackRegistry:
        """Create a callback registry with test callbacks."""
        registry = CallbackRegistry()
        IsAdultCallbackImpl.qualname = "is_adult"
        WeekendAdultCallbackImpl.qualname = "weekend_adult"
        IsAdultWithMinCallbackImpl.qualname = "is_adult_min"
        registry.register(IsAdultCallbackImpl)
        registry.register(WeekendAdultCallbackImpl)
        registry.register(IsAdultWithMinCallbackImpl)
        return registry

    @pytest.fixture
    def evaluator(self, registry: CallbackRegistry) -> SpecificationEvaluator:
        """Create a specification evaluator."""
        return SpecificationEvaluator(registry)

    @pytest.mark.asynchronous
    async def test_evaluate_callback_simple(self, evaluator):
        """Test evaluating a simple callback specification."""
        from lib_specifications.core.parameters import generate_signature_from_callable

        signature = generate_signature_from_callable(IsAdultCallbackImpl.__init__)
        params: dict[str, ParameterPathValue] = {
            "age": {
                "parameter_type": "path",
                "data_type": "int",
                "value": "user.age",
            }
        }
        spec = CallbackSpecification(
            callback_name="is_adult",
            signature=signature,
            params=params,
        )

        data = {"user": {"age": 20}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        data = {"user": {"age": 15}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_evaluate_callback_multiple_params(self, evaluator):
        """Test evaluating callback with multiple parameters."""
        from lib_specifications.core.parameters import generate_signature_from_callable

        signature = generate_signature_from_callable(WeekendAdultCallbackImpl.__init__)
        params = {
            "age": {
                "parameter_type": "path",
                "data_type": "int",
                "value": "user.age",
            },
            "day": {
                "parameter_type": "path",
                "data_type": "str",
                "value": "date.day",
            },
        }
        spec = CallbackSpecification(
            callback_name="weekend_adult",
            signature=signature,
            params=params,
        )

        data = {"user": {"age": 20}, "date": {"day": "Saturday"}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        data = {"user": {"age": 15}, "date": {"day": "Saturday"}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

        data = {"user": {"age": 20}, "date": {"day": "Monday"}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_evaluate_callback_with_literal_value(self, evaluator):
        """Test evaluating callback with literal value parameter."""
        from lib_specifications.core.parameters import generate_signature_from_callable

        signature = generate_signature_from_callable(IsAdultWithMinCallbackImpl.__init__)
        params = {
            "age": {
                "parameter_type": "path",
                "data_type": "int",
                "value": "user.age",
            },
            "min_age": {
                "parameter_type": "value",
                "data_type": "int",
                "value": 21,  # Literal value
            },
        }
        spec = CallbackSpecification(
            callback_name="is_adult_min",
            signature=signature,
            params=params,
        )

        data = {"user": {"age": 25}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        data = {"user": {"age": 18}}
        result = await evaluator.evaluate(spec, data)
        assert result is False  # 18 < 21

    @pytest.mark.asynchronous
    async def test_evaluate_callback_not_found_raises_error(self, evaluator):
        """Test that evaluating callback not in registry raises error."""
        from lib_specifications.core.parameters import SignatureSchema

        signature = SignatureSchema(parameters={})  # noqa: F401
        spec = CallbackSpecification(
            callback_name="nonexistent",
            signature=signature,
            params={},
        )

        with pytest.raises(ValueError, match="not found in registry"):
            await evaluator.evaluate(spec, {})

    def test_callback_specification_describe(self):
        """Test callback specification description."""
        from lib_specifications.core.parameters import generate_signature_from_callable

        signature = generate_signature_from_callable(IsAdultCallbackImpl.__init__)
        spec = CallbackSpecification(
            callback_name="is_adult",
            signature=signature,
            params={},
        )
        description = spec.describe()
        assert "is_adult" in description
        assert "age" in description
