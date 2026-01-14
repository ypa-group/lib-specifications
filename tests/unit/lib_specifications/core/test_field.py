"""Tests for FieldSpecification."""

import pytest

from lib_specifications.core.parameters import ParameterLiteralValue, ParameterPathValue
from lib_specifications.core.field import FieldSpecification


@pytest.mark.unit
class TestFieldSpecification:
    """Tests for FieldSpecification class."""

    def test_field_specification_creation(self):
        """Test creating a FieldSpecification instance."""
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
        spec = FieldSpecification(field=field, operator="equal", compare_to=compare_to)
        assert spec.field == field
        assert spec.operator == "equal"
        assert spec.compare_to == compare_to

    def test_field_specification_describe_with_literal_value(self):
        """Test describe method with literal value."""
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
        spec = FieldSpecification(field=field, operator="equal", compare_to=compare_to)
        description = spec.describe()
        assert "user.name" in description
        assert "John" in description
        assert "==" in description or "equal" in description.lower()

    def test_field_specification_describe_with_path_value(self):
        """Test describe method with path value."""
        field: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "str",
            "value": "user.name",
        }
        compare_to: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "str",
            "value": "profile.name",
        }
        spec = FieldSpecification(field=field, operator="equal", compare_to=compare_to)
        description = spec.describe()
        assert "user.name" in description
        assert "profile.name" in description

    def test_field_specification_describe_with_different_operators(self):
        """Test describe method with different operators."""
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

        operators = ["equal", "not_equal", "greater_than", "less_than", "greater_than_or_equal", "less_than_or_equal"]
        for operator in operators:
            spec = FieldSpecification(field=field, operator=operator, compare_to=compare_to)
            description = spec.describe()
            assert "user.age" in description
            assert isinstance(description, str)
            assert len(description) > 0

    def test_field_specification_describe_with_string_operators(self):
        """Test describe method with string operators."""
        field: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "str",
            "value": "user.email",
        }
        compare_to: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "str",
            "value": "@example.com",
        }

        string_operators = ["contains", "starts_with", "ends_with"]
        for operator in string_operators:
            spec = FieldSpecification(field=field, operator=operator, compare_to=compare_to)
            description = spec.describe()
            assert "user.email" in description
            assert isinstance(description, str)

    def test_field_specification_with_nested_path(self):
        """Test FieldSpecification with nested path."""
        field: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "user.profile.age",
        }
        compare_to: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "int",
            "value": 25,
        }
        spec = FieldSpecification(field=field, operator="greater_than", compare_to=compare_to)
        description = spec.describe()
        assert "user.profile.age" in description

    def test_field_specification_with_different_data_types(self):
        """Test FieldSpecification with different data types."""
        test_cases = [
            ("int", 42),
            ("float", 3.14),
            ("bool", True),
            ("str", "test"),
        ]

        for data_type, value in test_cases:
            field: ParameterPathValue = {
                "parameter_type": "path",
                "data_type": data_type,
                "value": "test.field",
            }
            compare_to: ParameterLiteralValue = {
                "parameter_type": "value",
                "data_type": data_type,
                "value": value,
            }
            spec = FieldSpecification(field=field, operator="equal", compare_to=compare_to)
            description = spec.describe()
            assert "test.field" in description
            assert isinstance(description, str)

    def test_field_specification_inherits_from_base(self):
        """Test that FieldSpecification inherits from BaseSpecification."""
        field: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "str",
            "value": "test",
        }
        compare_to: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "str",
            "value": "test",
        }
        spec = FieldSpecification(field=field, operator="equal", compare_to=compare_to)
        # Should be able to use BaseSpecification methods
        assert hasattr(spec, "describe")
        assert hasattr(spec, "__and__")
        assert hasattr(spec, "__or__")
        assert hasattr(spec, "__invert__")

    def test_field_specification_can_be_combined(self):
        """Test that FieldSpecification can be combined with logical operators."""
        field1: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "int",
            "value": "age",
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
            "value": "status",
        }
        compare_to2: ParameterLiteralValue = {
            "parameter_type": "value",
            "data_type": "str",
            "value": "active",
        }
        spec2 = FieldSpecification(field=field2, operator="equal", compare_to=compare_to2)

        # Test AND combination
        combined_and = spec1 & spec2
        assert hasattr(combined_and, "left")
        assert hasattr(combined_and, "right")

        # Test OR combination
        combined_or = spec1 | spec2
        assert hasattr(combined_or, "left")
        assert hasattr(combined_or, "right")

        # Test NOT
        not_spec = ~spec1
        assert hasattr(not_spec, "spec")

