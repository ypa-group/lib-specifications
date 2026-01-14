"""Tests for BaseSpecification and logical combinators."""

import pytest

from lib_specifications.core import (
    AndSpecification,
    BaseSpecification,
    FieldSpecification,
    NotSpecification,
    OrSpecification,
)
from lib_specifications.core.callback import CallbackRegistry
from lib_specifications.core.evaluator import SpecificationEvaluator
from lib_specifications.core.parameters import ParameterLiteralValue, ParameterPathValue


# Helper function to create a field specification that always evaluates to True
def create_always_true_spec() -> FieldSpecification:
    """Create a field specification that always evaluates to True when data has always_true=True."""
    field: ParameterPathValue = {
        "parameter_type": "path",
        "data_type": "bool",
        "value": "always_true",
    }
    compare_to: ParameterLiteralValue = {
        "parameter_type": "value",
        "data_type": "bool",
        "value": True,
    }
    return FieldSpecification(field=field, operator="equal", compare_to=compare_to)


# Helper function to create a field specification that always evaluates to False
def create_always_false_spec() -> FieldSpecification:
    """Create a field specification that always evaluates to False when data has always_false=False."""
    field: ParameterPathValue = {
        "parameter_type": "path",
        "data_type": "bool",
        "value": "always_false",
    }
    compare_to: ParameterLiteralValue = {
        "parameter_type": "value",
        "data_type": "bool",
        "value": True,  # Compare to True, but field will be False, so result is False
    }
    return FieldSpecification(field=field, operator="equal", compare_to=compare_to)


# Helper function to create a field specification that checks a value
def create_value_check_spec(field_path: str, expected_value: int) -> FieldSpecification:
    """Create a field specification that checks if a field equals a value."""
    field: ParameterPathValue = {
        "parameter_type": "path",
        "data_type": "int",
        "value": field_path,
    }
    compare_to: ParameterLiteralValue = {
        "parameter_type": "value",
        "data_type": "int",
        "value": expected_value,
    }
    return FieldSpecification(field=field, operator="equal", compare_to=compare_to)


@pytest.mark.unit
class TestBaseSpecification:
    """Tests for BaseSpecification base class."""

    def test_describe_abstract(self):
        """Test that BaseSpecification is abstract."""
        with pytest.raises(TypeError):
            BaseSpecification()

    def test_describe_method(self):
        """Test that specifications have describe method."""
        spec = create_always_true_spec()
        description = spec.describe()
        assert isinstance(description, str)
        assert len(description) > 0


@pytest.mark.unit
class TestAndSpecification:
    """Tests for AndSpecification."""

    @pytest.fixture
    def evaluator(self):
        """Create a specification evaluator."""
        return SpecificationEvaluator(CallbackRegistry())

    @pytest.mark.asynchronous
    async def test_and_both_true(self, evaluator):
        """Test AND with both specifications returning True."""
        left = create_always_true_spec()
        right = create_always_true_spec()
        and_spec = AndSpecification(left, right)
        data = {"always_true": True}
        result = await evaluator.evaluate(and_spec, data)
        assert result is True

    @pytest.mark.asynchronous
    async def test_and_left_false(self, evaluator):
        """Test AND with left specification returning False."""
        left = create_always_false_spec()
        right = create_always_true_spec()
        and_spec = AndSpecification(left, right)
        data = {"always_false": False, "always_true": True}
        result = await evaluator.evaluate(and_spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_and_right_false(self, evaluator):
        """Test AND with right specification returning False."""
        left = create_always_true_spec()
        right = create_always_false_spec()
        and_spec = AndSpecification(left, right)
        data = {"always_true": True, "always_false": False}
        result = await evaluator.evaluate(and_spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_and_both_false(self, evaluator):
        """Test AND with both specifications returning False."""
        left = create_always_false_spec()
        right = create_always_false_spec()
        and_spec = AndSpecification(left, right)
        data = {"always_false": False}
        result = await evaluator.evaluate(and_spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_and_short_circuit(self, evaluator):
        """Test that AND short-circuits when left is False."""
        left = create_always_false_spec()
        right = create_always_true_spec()
        and_spec = AndSpecification(left, right)
        data = {"always_false": False, "always_true": True}
        result = await evaluator.evaluate(and_spec, data)
        assert result is False

    def test_and_describe(self):
        """Test AND description."""
        left = create_always_true_spec()
        right = create_always_false_spec()
        and_spec = AndSpecification(left, right)
        description = and_spec.describe()
        assert "AND" in description

    def test_and_operator(self):
        """Test using & operator for AND."""
        left = create_always_true_spec()
        right = create_always_true_spec()
        and_spec = left & right
        assert isinstance(and_spec, AndSpecification)


@pytest.mark.unit
class TestOrSpecification:
    """Tests for OrSpecification."""

    @pytest.fixture
    def evaluator(self):
        """Create a specification evaluator."""
        return SpecificationEvaluator(CallbackRegistry())

    @pytest.mark.asynchronous
    async def test_or_both_true(self, evaluator):
        """Test OR with both specifications returning True."""
        left = create_always_true_spec()
        right = create_always_true_spec()
        or_spec = OrSpecification(left, right)
        data = {"always_true": True}
        result = await evaluator.evaluate(or_spec, data)
        assert result is True

    @pytest.mark.asynchronous
    async def test_or_left_true(self, evaluator):
        """Test OR with left specification returning True."""
        left = create_always_true_spec()
        right = create_always_false_spec()
        or_spec = OrSpecification(left, right)
        data = {"always_true": True, "always_false": False}
        result = await evaluator.evaluate(or_spec, data)
        assert result is True

    @pytest.mark.asynchronous
    async def test_or_right_true(self, evaluator):
        """Test OR with right specification returning True."""
        left = create_always_false_spec()
        right = create_always_true_spec()
        or_spec = OrSpecification(left, right)
        data = {"always_false": False, "always_true": True}
        result = await evaluator.evaluate(or_spec, data)
        assert result is True

    @pytest.mark.asynchronous
    async def test_or_both_false(self, evaluator):
        """Test OR with both specifications returning False."""
        left = create_always_false_spec()
        right = create_always_false_spec()
        or_spec = OrSpecification(left, right)
        data = {"always_false": False}
        result = await evaluator.evaluate(or_spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_or_short_circuit(self, evaluator):
        """Test that OR short-circuits when left is True."""
        left = create_always_true_spec()
        right = create_always_false_spec()
        or_spec = OrSpecification(left, right)
        data = {"always_true": True, "always_false": False}
        result = await evaluator.evaluate(or_spec, data)
        assert result is True

    def test_or_describe(self):
        """Test OR description."""
        left = create_always_true_spec()
        right = create_always_false_spec()
        or_spec = OrSpecification(left, right)
        description = or_spec.describe()
        assert "OR" in description

    def test_or_operator(self):
        """Test using | operator for OR."""
        left = create_always_true_spec()
        right = create_always_false_spec()
        or_spec = left | right
        assert isinstance(or_spec, OrSpecification)


@pytest.mark.unit
class TestNotSpecification:
    """Tests for NotSpecification."""

    @pytest.fixture
    def evaluator(self):
        """Create a specification evaluator."""
        return SpecificationEvaluator(CallbackRegistry())

    @pytest.mark.asynchronous
    async def test_not_true(self, evaluator):
        """Test NOT with specification returning True."""
        spec = create_always_true_spec()
        not_spec = NotSpecification(spec)
        data = {"always_true": True}
        result = await evaluator.evaluate(not_spec, data)
        assert result is False

    @pytest.mark.asynchronous
    async def test_not_false(self, evaluator):
        """Test NOT with specification returning False."""
        spec = create_always_false_spec()
        not_spec = NotSpecification(spec)
        data = {"always_false": False}
        result = await evaluator.evaluate(not_spec, data)
        assert result is True

    def test_not_describe(self):
        """Test NOT description."""
        spec = create_always_true_spec()
        not_spec = NotSpecification(spec)
        description = not_spec.describe()
        assert "NOT" in description

    def test_not_operator(self):
        """Test using ~ operator for NOT."""
        spec = create_always_true_spec()
        not_spec = ~spec
        assert isinstance(not_spec, NotSpecification)


@pytest.mark.unit
class TestComplexCombinations:
    """Tests for complex specification combinations."""

    @pytest.fixture
    def evaluator(self):
        """Create a specification evaluator."""
        return SpecificationEvaluator(CallbackRegistry())

    @pytest.mark.asynchronous
    async def test_and_or_combination(self, evaluator):
        """Test combining AND and OR."""
        spec1 = create_value_check_spec("value", 1)
        spec2 = create_value_check_spec("value", 2)
        spec3 = create_value_check_spec("value", 3)

        # (spec1 AND spec2) OR spec3
        combined = (spec1 & spec2) | spec3

        # Should be True for 3 (OR branch)
        data = {"value": 3}
        assert await evaluator.evaluate(combined, data) is True

        # Should be False for 1 (AND fails)
        data = {"value": 1}
        assert await evaluator.evaluate(combined, data) is False

        # Should be False for 2 (AND fails)
        data = {"value": 2}
        assert await evaluator.evaluate(combined, data) is False

    @pytest.mark.asynchronous
    async def test_not_and_combination(self, evaluator):
        """Test combining NOT and AND."""
        spec1 = create_value_check_spec("value", 1)
        spec2 = create_value_check_spec("value", 2)

        # NOT (spec1 AND spec2)
        combined = ~(spec1 & spec2)

        # Should be True for 1 (AND fails, NOT makes it True)
        data = {"value": 1}
        assert await evaluator.evaluate(combined, data) is True

        # Should be True for 2 (AND fails, NOT makes it True)
        data = {"value": 2}
        assert await evaluator.evaluate(combined, data) is True

        # Should be True for anything else (AND would be False, NOT makes it True)
        data = {"value": 999}
        assert await evaluator.evaluate(combined, data) is True
