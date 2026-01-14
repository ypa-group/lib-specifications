"""Tests for SpecificationEvaluator."""

import pytest

from lib_specifications.core import (
    AndSpecification,
    CallbackSpecification,
    FieldSpecification,
    NotSpecification,
    OrSpecification,
)
from lib_specifications.core.callback import BaseCallback, CallbackRegistry
from lib_specifications.core.evaluator import SpecificationEvaluator
from lib_specifications.core.parameters import (
    ParameterLiteralValue,
    ParameterPathValue,
    generate_signature_from_callable,
)


# Test callback implementations
class IsAdultCallback(BaseCallback):
    """Test callback for checking if person is adult."""

    qualname = "is_adult"

    def __init__(self, age: int):
        self.age = age

    def __call__(self) -> bool:
        return self.age >= 18


class IsWeekendCallback(BaseCallback):
    """Test callback for checking if day is weekend."""

    qualname = "is_weekend"

    def __init__(self, day: str):
        self.day = day

    def __call__(self) -> bool:
        return self.day.lower() in ["saturday", "sunday"]


class ComplexCallback(BaseCallback):
    """Test callback with multiple parameters."""

    qualname = "complex"

    def __init__(self, age: int, day: str, min_age: int = 18):
        self.age = age
        self.day = day
        self.min_age = min_age

    def __call__(self) -> bool:
        return self.age >= self.min_age and self.day.lower() in ["saturday", "sunday"]


@pytest.mark.unit
class TestSpecificationEvaluator:
    """Tests for SpecificationEvaluator."""

    @pytest.fixture
    def callback_registry(self) -> CallbackRegistry:
        """Create a callback registry with test callbacks."""
        registry = CallbackRegistry()
        IsAdultCallback.qualname = "is_adult"
        IsWeekendCallback.qualname = "is_weekend"
        ComplexCallback.qualname = "complex"
        registry.register(IsAdultCallback)
        registry.register(IsWeekendCallback)
        registry.register(ComplexCallback)
        return registry

    @pytest.fixture
    def evaluator(self, callback_registry: CallbackRegistry) -> SpecificationEvaluator:
        """Create a specification evaluator."""
        return SpecificationEvaluator(callback_registry)

    # Field specification tests
    @pytest.mark.asynchronous
    async def test_evaluate_field_spec_equal(self, evaluator):
        """Test evaluating field specification with equal operator."""
        field: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.age",
        }
        compare_to: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 18,
        }
        spec = FieldSpecification(field=field, operator="equal", compare_to=compare_to)

        data = {"user": {"age": 18}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        data = {"user": {"age": 20}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_evaluate_field_spec_greater_than(self, evaluator):
        """Test evaluating field specification with greater_than operator."""
        field: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.age",
        }
        compare_to: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 18,
        }
        spec = FieldSpecification(field=field, operator="greater_than", compare_to=compare_to)

        data = {"user": {"age": 20}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        data = {"user": {"age": 15}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_evaluate_field_spec_path_to_path(self, evaluator):
        """Test evaluating field specification comparing path to path."""
        field: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.age",
        }
        compare_to: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "min_age",
        }
        spec = FieldSpecification(field=field, operator="greater_than_or_equal", compare_to=compare_to)

        data = {"user": {"age": 20}, "min_age": 18}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        data = {"user": {"age": 15}, "min_age": 18}
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_evaluate_field_spec_string_contains(self, evaluator):
        """Test evaluating field specification with string contains operator."""
        field: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "str",
            "value": "user.name",
        }
        compare_to: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "str",
            "value": "John",
        }
        spec = FieldSpecification(field=field, operator="contains", compare_to=compare_to)

        data = {"user": {"name": "John Doe"}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        data = {"user": {"name": "Jane Smith"}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_evaluate_field_spec_missing_key_raises_error(self, evaluator):
        """Test that missing key in data raises KeyError."""
        field: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.age",
        }
        compare_to: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 18,
        }
        spec = FieldSpecification(field=field, operator="equal", compare_to=compare_to)

        data = {"user": {}}  # Missing age
        with pytest.raises(KeyError, match="key 'age' doesn't exist"):
            await evaluator.evaluate(spec, data)

    @pytest.mark.asynchronous
    async def test_evaluate_field_spec_invalid_path_raises_error(self, evaluator):
        """Test that invalid path raises KeyError."""
        field: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.profile.age",
        }
        compare_to: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 18,
        }
        spec = FieldSpecification(field=field, operator="equal", compare_to=compare_to)

        data = {"user": {"profile": "not_a_dict"}}  # profile is not a dict
        with pytest.raises(KeyError, match="is not a dictionary"):
            await evaluator.evaluate(spec, data)

    # Callback specification tests
    @pytest.mark.asynchronous
    async def test_evaluate_callback_spec_simple(self, evaluator):
        """Test evaluating simple callback specification."""
        signature = generate_signature_from_callable(IsAdultCallback.__init__)
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
    async def test_evaluate_callback_spec_multiple_params(self, evaluator):
        """Test evaluating callback with multiple parameters."""
        signature = generate_signature_from_callable(IsWeekendCallback.__init__)
        params: dict[str, ParameterPathValue] = {
            "day": {
                "parameter_type": "path",
                "data_type": "str",
                "value": "date.day",
            }
        }
        spec = CallbackSpecification(
            callback_name="is_weekend",
            signature=signature,
            params=params,
        )

        data = {"date": {"day": "Saturday"}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        data = {"date": {"day": "Monday"}}
        result = await evaluator.evaluate(spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_evaluate_callback_spec_with_literal(self, evaluator):
        """Test evaluating callback with literal value parameter."""
        signature = generate_signature_from_callable(ComplexCallback.__init__)
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
            "min_age": {
                "parameter_type": "value",
                "data_type": "int",
                "value": 21,  # Literal value
            },
        }
        spec = CallbackSpecification(
            callback_name="complex",
            signature=signature,
            params=params,
        )

        data = {"user": {"age": 25}, "date": {"day": "Saturday"}}
        result = await evaluator.evaluate(spec, data)
        assert result is True

        data = {"user": {"age": 18}, "date": {"day": "Saturday"}}
        result = await evaluator.evaluate(spec, data)
        assert result is False  # 18 < 21

    @pytest.mark.asynchronous
    async def test_evaluate_callback_not_found_raises_error(self, evaluator):
        """Test that callback not in registry raises ValueError."""
        from lib_specifications.core.parameters import SignatureSchema

        signature = SignatureSchema(parameters={})
        spec = CallbackSpecification(
            callback_name="nonexistent",
            signature=signature,
            params={},
        )

        with pytest.raises(ValueError, match="not found in registry"):
            await evaluator.evaluate(spec, {})

    # Logical combinator tests
    @pytest.mark.asynchronous
    async def test_evaluate_and_spec(self, evaluator):
        """Test evaluating AND specification."""
        field1: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.age",
        }
        compare_to1: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 18,
        }
        spec1 = FieldSpecification(field=field1, operator="greater_than_or_equal", compare_to=compare_to1)

        field2: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "str",
            "value": "user.name",
        }
        compare_to2: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "str",
            "value": "John",
        }
        spec2 = FieldSpecification(field=field2, operator="contains", compare_to=compare_to2)

        and_spec = AndSpecification(spec1, spec2)

        data = {"user": {"age": 20, "name": "John Doe"}}
        result = await evaluator.evaluate(and_spec, data)
        assert result is True

        data = {"user": {"age": 15, "name": "John Doe"}}  # age fails
        result = await evaluator.evaluate(and_spec, data)
        assert result is False

        data = {"user": {"age": 20, "name": "Jane"}}  # name fails
        result = await evaluator.evaluate(and_spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_evaluate_and_spec_lazy_evaluation(self, evaluator):
        """Test that AND specification uses lazy evaluation."""
        # Create a spec that will fail and check it's not evaluated if left fails
        field1: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.age",
        }
        compare_to1: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 18,
        }
        spec1 = FieldSpecification(field=field1, operator="less_than", compare_to=compare_to1)  # Will be False

        field2: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "nonexistent.field",  # This would raise KeyError if evaluated
        }
        compare_to2: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 10,
        }
        spec2 = FieldSpecification(field=field2, operator="equal", compare_to=compare_to2)

        and_spec = AndSpecification(spec1, spec2)

        data = {"user": {"age": 20}}  # spec1 is False, so spec2 shouldn't be evaluated
        result = await evaluator.evaluate(and_spec, data)
        assert result is False
        # If lazy evaluation works, we shouldn't get a KeyError

    @pytest.mark.asynchronous
    async def test_evaluate_or_spec(self, evaluator):
        """Test evaluating OR specification."""
        field1: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.age",
        }
        compare_to1: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 18,
        }
        spec1 = FieldSpecification(field=field1, operator="less_than", compare_to=compare_to1)

        field2: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "str",
            "value": "user.name",
        }
        compare_to2: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "str",
            "value": "John",
        }
        spec2 = FieldSpecification(field=field2, operator="contains", compare_to=compare_to2)

        or_spec = OrSpecification(spec1, spec2)

        data = {"user": {"age": 15, "name": "Jane"}}  # spec1 True
        result = await evaluator.evaluate(or_spec, data)
        assert result is True

        data = {"user": {"age": 20, "name": "John Doe"}}  # spec2 True
        result = await evaluator.evaluate(or_spec, data)
        assert result is True

        data = {"user": {"age": 20, "name": "Jane"}}  # Both False
        result = await evaluator.evaluate(or_spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_evaluate_or_spec_lazy_evaluation(self, evaluator):
        """Test that OR specification uses lazy evaluation."""
        field1: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.age",
        }
        compare_to1: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 18,
        }
        spec1 = FieldSpecification(
            field=field1, operator="greater_than_or_equal", compare_to=compare_to1
        )  # Will be True

        field2: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "nonexistent.field",  # This would raise KeyError if evaluated
        }
        compare_to2: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 10,
        }
        spec2 = FieldSpecification(field=field2, operator="equal", compare_to=compare_to2)

        or_spec = OrSpecification(spec1, spec2)

        data = {"user": {"age": 20}}  # spec1 is True, so spec2 shouldn't be evaluated
        result = await evaluator.evaluate(or_spec, data)
        assert result is True
        # If lazy evaluation works, we shouldn't get a KeyError

    @pytest.mark.asynchronous
    async def test_evaluate_not_spec(self, evaluator):
        """Test evaluating NOT specification."""
        field: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.age",
        }
        compare_to: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 18,
        }
        spec = FieldSpecification(field=field, operator="less_than", compare_to=compare_to)
        not_spec = NotSpecification(spec)

        data = {"user": {"age": 20}}  # spec is False, so not_spec is True
        result = await evaluator.evaluate(not_spec, data)
        assert result is True

        data = {"user": {"age": 15}}  # spec is True, so not_spec is False
        result = await evaluator.evaluate(not_spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_evaluate_complex_nested_spec(self, evaluator):
        """Test evaluating complex nested specification."""
        # (age >= 18 AND name contains "John") OR (day is weekend)
        field1: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.age",
        }
        compare_to1: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 18,
        }
        spec1 = FieldSpecification(field=field1, operator="greater_than_or_equal", compare_to=compare_to1)

        field2: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "str",
            "value": "user.name",
        }
        compare_to2: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "str",
            "value": "John",
        }
        spec2 = FieldSpecification(field=field2, operator="contains", compare_to=compare_to2)

        and_spec = AndSpecification(spec1, spec2)

        signature = generate_signature_from_callable(IsWeekendCallback.__init__)
        params: dict[str, ParameterPathValue] = {
            "day": {
                "parameter_type": "path",
                "data_type": "str",
                "value": "date.day",
            }
        }
        callback_spec = CallbackSpecification(
            callback_name="is_weekend",
            signature=signature,
            params=params,
        )

        or_spec = OrSpecification(and_spec, callback_spec)

        # Test case 1: AND is True
        data = {"user": {"age": 20, "name": "John Doe"}, "date": {"day": "Monday"}}
        result = await evaluator.evaluate(or_spec, data)
        assert result is True

        # Test case 2: AND is False, but callback is True
        data = {"user": {"age": 15, "name": "Jane"}, "date": {"day": "Saturday"}}
        result = await evaluator.evaluate(or_spec, data)
        assert result is True

        # Test case 3: Both False
        data = {"user": {"age": 15, "name": "Jane"}, "date": {"day": "Monday"}}
        result = await evaluator.evaluate(or_spec, data)
        assert result is False

    # Helper method tests
    def test_get_nested_value(self, evaluator):
        """Test get_nested_value helper method."""
        data = {"user": {"profile": {"age": 25}}}
        value = evaluator.get_nested_value(data, "user.profile.age")
        assert value == 25

        data = {"user": {"age": 20}}
        value = evaluator.get_nested_value(data, "user.age")
        assert value == 20

        data = {"top_level": 10}
        value = evaluator.get_nested_value(data, "top_level")
        assert value == 10

    def test_get_nested_value_missing_key(self, evaluator):
        """Test get_nested_value with missing key raises KeyError."""
        data = {"user": {}}
        with pytest.raises(KeyError, match="key 'age' doesn't exist"):
            evaluator.get_nested_value(data, "user.age")

    def test_get_nested_value_invalid_path(self, evaluator):
        """Test get_nested_value with invalid path raises KeyError."""
        data = {"user": {"profile": "not_a_dict"}}
        with pytest.raises(KeyError, match="is not a dictionary"):
            evaluator.get_nested_value(data, "user.profile.age")

    def test_get_parameter_value_path(self, evaluator):
        """Test _get_parameter_value with path parameter."""
        param: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.age",
        }
        data = {"user": {"age": 20}}
        value = evaluator._get_parameter_value(param, data)
        assert value == 20

    def test_get_parameter_value_literal(self, evaluator):
        """Test _get_parameter_value with literal parameter."""
        param: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 18,
        }
        data = {}
        value = evaluator._get_parameter_value(param, data)
        assert value == 18

    def test_get_parameter_value_invalid_type(self, evaluator):
        """Test _get_parameter_value with invalid parameter_type raises ValueError."""
        param = {
            "parameter_type": "invalid",
            "data_type": "int",
            "value": 18,
        }
        with pytest.raises(ValueError, match="Invalid parameter_type"):
            evaluator._get_parameter_value(param, {})

    def test_extract_parameter_values(self, evaluator):
        """Test _extract_parameter_values helper method."""
        params = {
            "age": {
                "parameter_type": "path",
                "data_type": "int",
                "value": "user.age",
            },
            "min_age": {
                "parameter_type": "value",
                "data_type": "int",
                "value": 18,
            },
        }
        data = {"user": {"age": 20}}
        extracted = evaluator._extract_parameter_values(params, data)
        assert extracted == {"age": 20, "min_age": 18}

    def test_apply_operator(self, evaluator):
        """Test _apply_operator helper method."""
        result = evaluator._apply_operator("equal", 5, 5)
        assert result is True

        result = evaluator._apply_operator("equal", 5, 3)
        assert result is False

        result = evaluator._apply_operator("greater_than", 10, 5)
        assert result is True

    def test_apply_operator_not_found(self, evaluator):
        """Test _apply_operator with non-existent operator raises ValueError."""
        with pytest.raises(ValueError, match="not found in registry"):
            evaluator._apply_operator("nonexistent", 5, 3)

    def test_apply_operator_incompatible_type(self, evaluator):
        """Test _apply_operator with incompatible type raises ValueError."""
        # Try to use string operator on int
        with pytest.raises(ValueError, match="not compatible with type"):
            evaluator._apply_operator("starts_with", 123, "12")

    @pytest.mark.asynchronous
    async def test_evaluate_unknown_spec_type_raises_error(self, evaluator):
        """Test that unknown specification type raises ValueError."""

        # Create a mock specification that doesn't match any known type
        class UnknownSpec:
            pass

        unknown_spec = UnknownSpec()
        with pytest.raises(ValueError, match="Unknown specification type"):
            await evaluator.evaluate(unknown_spec, {})  # type: ignore
