"""Tests for operators module."""

from datetime import date, datetime

import pytest

from lib_specifications.core.operators import (
    ContainsOperator,
    EndsWithOperator,
    EqualOperator,
    GreaterThanOperator,
    GreaterThanOrEqualOperator,
    LessThanOperator,
    LessThanOrEqualOperator,
    NotEqualOperator,
    Operator,
    OperatorRegistry,
    StartsWithOperator,
)
from lib_specifications.core.parameters import ParameterTypeEnum


class TestOperator(Operator):
    """Test operator implementation."""

    @property
    def name(self) -> str:
        return "test"

    @property
    def symbol(self) -> str:
        return "="

    @property
    def compatible_types(self) -> list[ParameterTypeEnum]:
        return [ParameterTypeEnum.STR, ParameterTypeEnum.INT]

    def compare(self, left, right) -> bool:
        return left == right


@pytest.mark.unit
class TestOperatorBase:
    """Tests for Operator base class."""

    def test_operator_is_abstract(self):
        """Test that Operator is abstract."""
        with pytest.raises(TypeError):
            Operator()

    def test_operator_properties(self):
        """Test operator properties."""
        op = TestOperator()
        assert op.name == "test"
        assert op.symbol == "="
        assert len(op.compatible_types) == 2
        assert ParameterTypeEnum.STR in op.compatible_types
        assert ParameterTypeEnum.INT in op.compatible_types

    def test_is_compatible_with(self):
        """Test is_compatible_with method."""
        op = TestOperator()
        assert op.is_compatible_with(ParameterTypeEnum.STR) is True
        assert op.is_compatible_with(ParameterTypeEnum.INT) is True
        assert op.is_compatible_with(ParameterTypeEnum.FLOAT) is False

    def test_compare(self):
        """Test compare method."""
        op = TestOperator()
        assert op.compare(1, 1) is True
        assert op.compare(1, 2) is False
        assert op.compare("test", "test") is True
        assert op.compare("test", "other") is False


@pytest.mark.unit
class TestEqualOperator:
    """Tests for EqualOperator."""

    def test_name(self):
        """Test operator name."""
        op = EqualOperator()
        assert op.name == "equal"

    def test_symbol(self):
        """Test operator symbol."""
        op = EqualOperator()
        assert op.symbol == "=="

    def test_compatible_types(self):
        """Test compatible types."""
        op = EqualOperator()
        compatible = op.compatible_types
        assert ParameterTypeEnum.STR in compatible
        assert ParameterTypeEnum.INT in compatible
        assert ParameterTypeEnum.FLOAT in compatible
        assert ParameterTypeEnum.BOOL in compatible
        assert ParameterTypeEnum.DATE in compatible
        assert ParameterTypeEnum.DATETIME in compatible
        assert ParameterTypeEnum.LIST not in compatible
        assert ParameterTypeEnum.DICT not in compatible

    def test_compare_integers(self):
        """Test comparing integers."""
        op = EqualOperator()
        assert op.compare(1, 1) is True
        assert op.compare(1, 2) is False
        assert op.compare(0, 0) is True

    def test_compare_strings(self):
        """Test comparing strings."""
        op = EqualOperator()
        assert op.compare("test", "test") is True
        assert op.compare("test", "other") is False
        assert op.compare("", "") is True

    def test_compare_floats(self):
        """Test comparing floats."""
        op = EqualOperator()
        assert op.compare(1.5, 1.5) is True
        assert op.compare(1.5, 2.5) is False

    def test_compare_booleans(self):
        """Test comparing booleans."""
        op = EqualOperator()
        assert op.compare(True, True) is True
        assert op.compare(False, False) is True
        assert op.compare(True, False) is False

    def test_compare_dates(self):
        """Test comparing dates."""
        op = EqualOperator()
        date1 = date(2023, 1, 1)
        date2 = date(2023, 1, 1)
        date3 = date(2023, 1, 2)
        assert op.compare(date1, date2) is True
        assert op.compare(date1, date3) is False

    def test_compare_datetimes(self):
        """Test comparing datetimes."""
        op = EqualOperator()
        dt1 = datetime(2023, 1, 1, 12, 0, 0)
        dt2 = datetime(2023, 1, 1, 12, 0, 0)
        dt3 = datetime(2023, 1, 1, 12, 0, 1)
        assert op.compare(dt1, dt2) is True
        assert op.compare(dt1, dt3) is False

    def test_is_compatible_with(self):
        """Test is_compatible_with method."""
        op = EqualOperator()
        assert op.is_compatible_with(ParameterTypeEnum.STR) is True
        assert op.is_compatible_with(ParameterTypeEnum.INT) is True
        assert op.is_compatible_with(ParameterTypeEnum.LIST) is False


@pytest.mark.unit
class TestNotEqualOperator:
    """Tests for NotEqualOperator."""

    def test_name(self):
        """Test operator name."""
        op = NotEqualOperator()
        assert op.name == "not_equal"

    def test_symbol(self):
        """Test operator symbol."""
        op = NotEqualOperator()
        assert op.symbol == "!="

    def test_compatible_types(self):
        """Test compatible types."""
        op = NotEqualOperator()
        compatible = op.compatible_types
        assert ParameterTypeEnum.STR in compatible
        assert ParameterTypeEnum.INT in compatible
        assert ParameterTypeEnum.FLOAT in compatible
        assert ParameterTypeEnum.BOOL in compatible
        assert ParameterTypeEnum.DATE in compatible
        assert ParameterTypeEnum.DATETIME in compatible

    def test_compare_integers(self):
        """Test comparing integers."""
        op = NotEqualOperator()
        assert op.compare(1, 2) is True
        assert op.compare(1, 1) is False

    def test_compare_strings(self):
        """Test comparing strings."""
        op = NotEqualOperator()
        assert op.compare("test", "other") is True
        assert op.compare("test", "test") is False

    def test_compare_floats(self):
        """Test comparing floats."""
        op = NotEqualOperator()
        assert op.compare(1.5, 2.5) is True
        assert op.compare(1.5, 1.5) is False

    def test_compare_booleans(self):
        """Test comparing booleans."""
        op = NotEqualOperator()
        assert op.compare(True, False) is True
        assert op.compare(True, True) is False
        assert op.compare(False, False) is False

    def test_compare_dates(self):
        """Test comparing dates."""
        op = NotEqualOperator()
        date1 = date(2023, 1, 1)
        date2 = date(2023, 1, 2)
        assert op.compare(date1, date2) is True
        assert op.compare(date1, date1) is False

    def test_compare_datetimes(self):
        """Test comparing datetimes."""
        op = NotEqualOperator()
        dt1 = datetime(2023, 1, 1, 12, 0, 0)
        dt2 = datetime(2023, 1, 1, 12, 0, 1)
        dt3 = datetime(2023, 1, 1, 12, 0, 0)
        assert op.compare(dt1, dt2) is True
        assert op.compare(dt1, dt3) is False


@pytest.mark.unit
class TestGreaterThanOperator:
    """Tests for GreaterThanOperator."""

    def test_name(self):
        """Test operator name."""
        op = GreaterThanOperator()
        assert op.name == "greater_than"

    def test_symbol(self):
        """Test operator symbol."""
        op = GreaterThanOperator()
        assert op.symbol == ">"

    def test_compatible_types(self):
        """Test compatible types."""
        op = GreaterThanOperator()
        compatible = op.compatible_types
        assert ParameterTypeEnum.INT in compatible
        assert ParameterTypeEnum.FLOAT in compatible
        assert ParameterTypeEnum.DATE in compatible
        assert ParameterTypeEnum.DATETIME in compatible
        assert ParameterTypeEnum.STR not in compatible

    def test_compare_integers(self):
        """Test comparing integers."""
        op = GreaterThanOperator()
        assert op.compare(5, 3) is True
        assert op.compare(3, 5) is False
        assert op.compare(3, 3) is False

    def test_compare_floats(self):
        """Test comparing floats."""
        op = GreaterThanOperator()
        assert op.compare(5.5, 3.2) is True
        assert op.compare(3.2, 5.5) is False

    def test_compare_dates(self):
        """Test comparing dates."""
        op = GreaterThanOperator()
        date1 = date(2023, 1, 2)
        date2 = date(2023, 1, 1)
        assert op.compare(date1, date2) is True
        assert op.compare(date2, date1) is False

    def test_compare_datetimes(self):
        """Test comparing datetimes."""
        op = GreaterThanOperator()
        dt1 = datetime(2023, 1, 1, 12, 0, 1)
        dt2 = datetime(2023, 1, 1, 12, 0, 0)
        assert op.compare(dt1, dt2) is True
        assert op.compare(dt2, dt1) is False


@pytest.mark.unit
class TestGreaterThanOrEqualOperator:
    """Tests for GreaterThanOrEqualOperator."""

    def test_name(self):
        """Test operator name."""
        op = GreaterThanOrEqualOperator()
        assert op.name == "greater_than_or_equal"

    def test_symbol(self):
        """Test operator symbol."""
        op = GreaterThanOrEqualOperator()
        assert op.symbol == ">="

    def test_compatible_types(self):
        """Test compatible types."""
        op = GreaterThanOrEqualOperator()
        compatible = op.compatible_types
        assert ParameterTypeEnum.INT in compatible
        assert ParameterTypeEnum.FLOAT in compatible
        assert ParameterTypeEnum.DATE in compatible
        assert ParameterTypeEnum.DATETIME in compatible
        assert ParameterTypeEnum.STR not in compatible

    def test_compare_integers(self):
        """Test comparing integers."""
        op = GreaterThanOrEqualOperator()
        assert op.compare(5, 3) is True
        assert op.compare(3, 3) is True
        assert op.compare(3, 5) is False

    def test_compare_floats(self):
        """Test comparing floats."""
        op = GreaterThanOrEqualOperator()
        assert op.compare(5.5, 3.2) is True
        assert op.compare(3.2, 3.2) is True
        assert op.compare(3.2, 5.5) is False

    def test_compare_dates(self):
        """Test comparing dates."""
        op = GreaterThanOrEqualOperator()
        date1 = date(2023, 1, 2)
        date2 = date(2023, 1, 1)
        date3 = date(2023, 1, 2)
        assert op.compare(date1, date2) is True
        assert op.compare(date1, date3) is True
        assert op.compare(date2, date1) is False

    def test_compare_datetimes(self):
        """Test comparing datetimes."""
        op = GreaterThanOrEqualOperator()
        dt1 = datetime(2023, 1, 1, 12, 0, 1)
        dt2 = datetime(2023, 1, 1, 12, 0, 0)
        dt3 = datetime(2023, 1, 1, 12, 0, 1)
        assert op.compare(dt1, dt2) is True
        assert op.compare(dt1, dt3) is True
        assert op.compare(dt2, dt1) is False


@pytest.mark.unit
class TestLessThanOperator:
    """Tests for LessThanOperator."""

    def test_name(self):
        """Test operator name."""
        op = LessThanOperator()
        assert op.name == "less_than"

    def test_symbol(self):
        """Test operator symbol."""
        op = LessThanOperator()
        assert op.symbol == "<"

    def test_compatible_types(self):
        """Test compatible types."""
        op = LessThanOperator()
        compatible = op.compatible_types
        assert ParameterTypeEnum.INT in compatible
        assert ParameterTypeEnum.FLOAT in compatible
        assert ParameterTypeEnum.DATE in compatible
        assert ParameterTypeEnum.DATETIME in compatible
        assert ParameterTypeEnum.STR not in compatible

    def test_compare_integers(self):
        """Test comparing integers."""
        op = LessThanOperator()
        assert op.compare(3, 5) is True
        assert op.compare(5, 3) is False
        assert op.compare(3, 3) is False

    def test_compare_floats(self):
        """Test comparing floats."""
        op = LessThanOperator()
        assert op.compare(3.2, 5.5) is True
        assert op.compare(5.5, 3.2) is False

    def test_compare_dates(self):
        """Test comparing dates."""
        op = LessThanOperator()
        date1 = date(2023, 1, 1)
        date2 = date(2023, 1, 2)
        assert op.compare(date1, date2) is True
        assert op.compare(date2, date1) is False

    def test_compare_datetimes(self):
        """Test comparing datetimes."""
        op = LessThanOperator()
        dt1 = datetime(2023, 1, 1, 12, 0, 0)
        dt2 = datetime(2023, 1, 1, 12, 0, 1)
        assert op.compare(dt1, dt2) is True
        assert op.compare(dt2, dt1) is False


@pytest.mark.unit
class TestLessThanOrEqualOperator:
    """Tests for LessThanOrEqualOperator."""

    def test_name(self):
        """Test operator name."""
        op = LessThanOrEqualOperator()
        assert op.name == "less_than_or_equal"

    def test_symbol(self):
        """Test operator symbol."""
        op = LessThanOrEqualOperator()
        assert op.symbol == "<="

    def test_compatible_types(self):
        """Test compatible types."""
        op = LessThanOrEqualOperator()
        compatible = op.compatible_types
        assert ParameterTypeEnum.INT in compatible
        assert ParameterTypeEnum.FLOAT in compatible
        assert ParameterTypeEnum.DATE in compatible
        assert ParameterTypeEnum.DATETIME in compatible
        assert ParameterTypeEnum.STR not in compatible

    def test_compare_integers(self):
        """Test comparing integers."""
        op = LessThanOrEqualOperator()
        assert op.compare(3, 5) is True
        assert op.compare(3, 3) is True
        assert op.compare(5, 3) is False

    def test_compare_floats(self):
        """Test comparing floats."""
        op = LessThanOrEqualOperator()
        assert op.compare(3.2, 5.5) is True
        assert op.compare(3.2, 3.2) is True
        assert op.compare(5.5, 3.2) is False

    def test_compare_dates(self):
        """Test comparing dates."""
        op = LessThanOrEqualOperator()
        date1 = date(2023, 1, 1)
        date2 = date(2023, 1, 2)
        date3 = date(2023, 1, 1)
        assert op.compare(date1, date2) is True
        assert op.compare(date1, date3) is True
        assert op.compare(date2, date1) is False

    def test_compare_datetimes(self):
        """Test comparing datetimes."""
        op = LessThanOrEqualOperator()
        dt1 = datetime(2023, 1, 1, 12, 0, 0)
        dt2 = datetime(2023, 1, 1, 12, 0, 1)
        dt3 = datetime(2023, 1, 1, 12, 0, 0)
        assert op.compare(dt1, dt2) is True
        assert op.compare(dt1, dt3) is True
        assert op.compare(dt2, dt1) is False


@pytest.mark.unit
class TestContainsOperator:
    """Tests for ContainsOperator."""

    def test_name(self):
        """Test operator name."""
        op = ContainsOperator()
        assert op.name == "contains"

    def test_symbol(self):
        """Test operator symbol."""
        op = ContainsOperator()
        assert op.symbol == "IN"

    def test_compatible_types(self):
        """Test compatible types."""
        op = ContainsOperator()
        compatible = op.compatible_types
        assert ParameterTypeEnum.STR in compatible
        assert ParameterTypeEnum.LIST in compatible

    def test_compare_strings(self):
        """Test comparing strings."""
        op = ContainsOperator()
        assert op.compare("hello world", "world") is True
        assert op.compare("hello world", "hello") is True
        assert op.compare("hello world", "xyz") is False

    def test_compare_lists(self):
        """Test comparing lists."""
        op = ContainsOperator()
        assert op.compare([1, 2, 3], 2) is True
        assert op.compare([1, 2, 3], 4) is False
        assert op.compare(["a", "b", "c"], "b") is True

    def test_compare_none(self):
        """Test comparing with None."""
        op = ContainsOperator()
        assert op.compare(None, "test") is False
        assert op.compare(None, 1) is False

    def test_compare_empty_string(self):
        """Test comparing with empty string."""
        op = ContainsOperator()
        assert op.compare("", "test") is False
        assert op.compare("test", "") is True

    def test_compare_empty_list(self):
        """Test comparing with empty list."""
        op = ContainsOperator()
        assert op.compare([], 1) is False
        assert op.compare([], "test") is False


@pytest.mark.unit
class TestStartsWithOperator:
    """Tests for StartsWithOperator."""

    def test_name(self):
        """Test operator name."""
        op = StartsWithOperator()
        assert op.name == "starts_with"

    def test_symbol(self):
        """Test operator symbol."""
        op = StartsWithOperator()
        assert op.symbol == "STARTS WITH"

    def test_compatible_types(self):
        """Test compatible types."""
        op = StartsWithOperator()
        compatible = op.compatible_types
        assert ParameterTypeEnum.STR in compatible

    def test_compare_strings(self):
        """Test comparing strings."""
        op = StartsWithOperator()
        assert op.compare("hello world", "hello") is True
        assert op.compare("hello world", "world") is False
        assert op.compare("test", "test") is True
        assert op.compare("test", "xyz") is False

    def test_compare_empty_string(self):
        """Test comparing with empty string."""
        op = StartsWithOperator()
        assert op.compare("test", "") is True
        assert op.compare("", "test") is False
        assert op.compare("", "") is True

    def test_compare_non_string(self):
        """Test comparing with non-string (should return False)."""
        op = StartsWithOperator()
        assert op.compare(123, "12") is False
        assert op.compare(None, "test") is False


@pytest.mark.unit
class TestEndsWithOperator:
    """Tests for EndsWithOperator."""

    def test_name(self):
        """Test operator name."""
        op = EndsWithOperator()
        assert op.name == "ends_with"

    def test_symbol(self):
        """Test operator symbol."""
        op = EndsWithOperator()
        assert op.symbol == "ENDS WITH"

    def test_compatible_types(self):
        """Test compatible types."""
        op = EndsWithOperator()
        compatible = op.compatible_types
        assert ParameterTypeEnum.STR in compatible

    def test_compare_strings(self):
        """Test comparing strings."""
        op = EndsWithOperator()
        assert op.compare("hello world", "world") is True
        assert op.compare("hello world", "hello") is False
        assert op.compare("test", "test") is True
        assert op.compare("test", "xyz") is False

    def test_compare_empty_string(self):
        """Test comparing with empty string."""
        op = EndsWithOperator()
        assert op.compare("test", "") is True
        assert op.compare("", "test") is False
        assert op.compare("", "") is True

    def test_compare_non_string(self):
        """Test comparing with non-string (should return False)."""
        op = EndsWithOperator()
        assert op.compare(123, "23") is False
        assert op.compare(None, "test") is False


@pytest.mark.unit
class TestOperatorRegistry:
    """Tests for OperatorRegistry."""

    def test_create_registry(self):
        """Test creating an empty registry."""
        registry = OperatorRegistry()
        assert registry.list_names() == []

    def test_register_operator(self):
        """Test registering an operator."""
        registry = OperatorRegistry()
        operator = EqualOperator()
        registry.register(operator)
        assert "equal" in registry.list_names()

    def test_get_operator(self):
        """Test getting an operator by name."""
        registry = OperatorRegistry()
        operator = EqualOperator()
        registry.register(operator)
        retrieved = registry.get("equal")
        assert retrieved is not None
        assert retrieved.name == "equal"

    def test_get_nonexistent_operator(self):
        """Test getting a nonexistent operator."""
        registry = OperatorRegistry()
        result = registry.get("nonexistent")
        assert result is None

    def test_list_names(self):
        """Test listing operator names."""
        registry = OperatorRegistry()
        registry.register(EqualOperator())
        registry.register(GreaterThanOperator())
        names = registry.list_names()
        assert "equal" in names
        assert "greater_than" in names
        assert len(names) == 2

    def test_get_compatible_operators(self):
        """Test getting compatible operators for a type."""
        registry = OperatorRegistry()
        registry.register(EqualOperator())
        registry.register(GreaterThanOperator())

        # EqualOperator is compatible with INT
        compatible = registry.get_compatible_operators(ParameterTypeEnum.INT)
        assert "equal" in compatible
        assert "greater_than" in compatible

        # EqualOperator is compatible with STR, but GreaterThanOperator is not
        compatible = registry.get_compatible_operators(ParameterTypeEnum.STR)
        assert "equal" in compatible
        assert "greater_than" not in compatible

    def test_register_multiple_operators(self):
        """Test registering multiple operators."""
        registry = OperatorRegistry()
        registry.register(EqualOperator())
        registry.register(GreaterThanOperator())
        assert len(registry.list_names()) == 2

    def test_register_duplicate_operator(self):
        """Test registering duplicate operator (should overwrite)."""
        registry = OperatorRegistry()
        operator1 = EqualOperator()
        operator2 = EqualOperator()
        registry.register(operator1)
        registry.register(operator2)
        # Should only have one entry
        assert registry.list_names() == ["equal"]

