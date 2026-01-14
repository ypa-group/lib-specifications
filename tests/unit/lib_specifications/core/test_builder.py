"""Tests for SpecificationBuilder."""

import pytest

from lib_specifications.core.builder import SpecificationBuilder
from lib_specifications.core.callback import BaseCallback, CallbackRegistry
from lib_specifications.core.tree import (
    SpecificationAndNode,
    SpecificationCallbackLeafNode,
    SpecificationFieldLeafNode,
    SpecificationNotNode,
    SpecificationOrNode,
)
from lib_specifications.core import (
    AndSpecification,
    CallbackSpecification,
    FieldSpecification,
    NotSpecification,
    OrSpecification,
)


# Test callback implementations
class MockCallback(BaseCallback):
    """Test callback for builder tests."""
    qualname = "mock_callback"

    def __init__(self, age: int):
        self.age = age

    def __call__(self) -> bool:
        return self.age >= 18


class MultiParamCallback(BaseCallback):
    """Test callback with multiple parameters."""
    qualname = "multi_param"

    def __init__(self, age: int, name: str, min_age: int = 18):
        self.age = age
        self.name = name
        self.min_age = min_age

    def __call__(self) -> bool:
        return self.age >= self.min_age and len(self.name) > 0


@pytest.mark.unit
class TestSpecificationBuilder:
    """Tests for SpecificationBuilder."""

    @pytest.fixture
    def callback_registry(self) -> CallbackRegistry:
        """Create a callback registry with test callbacks."""
        registry = CallbackRegistry()
        MockCallback.qualname = "mock_callback"
        MultiParamCallback.qualname = "multi_param"
        registry.register(MockCallback)
        registry.register(MultiParamCallback)
        return registry

    @pytest.fixture
    def builder(self, callback_registry: CallbackRegistry) -> SpecificationBuilder:
        """Create a specification builder."""
        return SpecificationBuilder(callback_registry)

    # Field specification building tests
    def test_build_field_spec(self, builder):
        """Test building field specification from tree."""
        tree: SpecificationFieldLeafNode = {
            "type": "leaf",
            "subtype": "field",
            "name": "equal",
            "field": "user.age",
            "compare_to": {
                "parameter_type": "value",
                "data_type": "int",
                "value": 18,
            },
        }

        spec = builder.build(tree)
        assert isinstance(spec, FieldSpecification)
        assert spec.operator == "equal"
        assert spec.field["value"] == "user.age"
        assert spec.compare_to["value"] == 18

    def test_build_field_spec_path_compare_to(self, builder):
        """Test building field specification with path compare_to."""
        tree: SpecificationFieldLeafNode = {
            "type": "leaf",
            "subtype": "field",
            "name": "greater_than",
            "field": "user.age",
            "compare_to": {
                "parameter_type": "path",
                "data_type": "int",
                "value": "min_age",
            },
        }

        spec = builder.build(tree)
        assert isinstance(spec, FieldSpecification)
        assert spec.operator == "greater_than"
        assert spec.field["value"] == "user.age"
        assert spec.compare_to["parameter_type"] == "path"
        assert spec.compare_to["value"] == "min_age"

    def test_build_field_spec_missing_field_raises_error(self, builder):
        """Test that missing field in tree raises ValueError."""
        tree = {
            "type": "leaf",
            "subtype": "field",
            "name": "equal",
            "compare_to": {
                "parameter_type": "value",
                "data_type": "int",
                "value": 18,
            },
        }

        with pytest.raises(ValueError, match="requires 'field'"):
            builder.build(tree)  # type: ignore

    def test_build_field_spec_missing_name_raises_error(self, builder):
        """Test that missing name in tree raises ValueError."""
        tree = {
            "type": "leaf",
            "subtype": "field",
            "field": "user.age",
            "compare_to": {
                "parameter_type": "value",
                "data_type": "int",
                "value": 18,
            },
        }

        with pytest.raises(ValueError, match="requires 'name'"):
            builder.build(tree)  # type: ignore

    def test_build_field_spec_missing_compare_to_raises_error(self, builder):
        """Test that missing compare_to in tree raises ValueError."""
        tree = {
            "type": "leaf",
            "subtype": "field",
            "name": "equal",
            "field": "user.age",
        }

        with pytest.raises(ValueError, match="requires 'compare_to'"):
            builder.build(tree)  # type: ignore

    # Callback specification building tests
    def test_build_callback_spec(self, builder):
        """Test building callback specification from tree."""
        tree: SpecificationCallbackLeafNode = {
            "type": "leaf",
            "subtype": "callback",
            "name": "mock_callback",
            "params": {
                "age": {
                    "parameter_type": "path",
                    "data_type": "int",
                    "value": "user.age",
                },
            },
        }

        spec = builder.build(tree)
        assert isinstance(spec, CallbackSpecification)
        assert spec.callback_name == "mock_callback"
        assert "age" in spec.params
        assert spec.params["age"]["value"] == "user.age"

    def test_build_callback_spec_multiple_params(self, builder):
        """Test building callback specification with multiple parameters."""
        tree: SpecificationCallbackLeafNode = {
            "type": "leaf",
            "subtype": "callback",
            "name": "multi_param",
            "params": {
                "age": {
                    "parameter_type": "path",
                    "data_type": "int",
                    "value": "user.age",
                },
                "name": {
                    "parameter_type": "path",
                    "data_type": "str",
                    "value": "user.name",
                },
                "min_age": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 21,
                },
            },
        }

        spec = builder.build(tree)
        assert isinstance(spec, CallbackSpecification)
        assert spec.callback_name == "multi_param"
        assert len(spec.params) == 3
        assert spec.params["age"]["value"] == "user.age"
        assert spec.params["name"]["value"] == "user.name"
        assert spec.params["min_age"]["value"] == 21

    def test_build_callback_spec_empty_params(self, builder):
        """Test building callback specification with empty params."""
        tree: SpecificationCallbackLeafNode = {
            "type": "leaf",
            "subtype": "callback",
            "name": "mock_callback",
            "params": {},
        }

        spec = builder.build(tree)
        assert isinstance(spec, CallbackSpecification)
        assert spec.callback_name == "mock_callback"
        assert spec.params == {}

    def test_build_callback_spec_missing_name_raises_error(self, builder):
        """Test that missing name in callback tree raises ValueError."""
        tree = {
            "type": "leaf",
            "subtype": "callback",
            "params": {},
        }

        with pytest.raises(ValueError, match="requires 'name'"):
            builder.build(tree)  # type: ignore

    def test_build_callback_spec_not_found_raises_error(self, builder):
        """Test that callback not in registry raises KeyError."""
        tree: SpecificationCallbackLeafNode = {
            "type": "leaf",
            "subtype": "callback",
            "name": "nonexistent",
            "params": {},
        }

        with pytest.raises(ValueError, match="not found in registry"):
            builder.build(tree)

    # Logical combinator building tests
    def test_build_and_spec(self, builder):
        """Test building AND specification from tree."""
        tree: SpecificationAndNode = {
            "type": "and",
            "left": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.age",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 18,
                },
            },
            "right": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.name",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "John",
                },
            },
        }

        spec = builder.build(tree)
        assert isinstance(spec, AndSpecification)
        assert isinstance(spec.left, FieldSpecification)
        assert isinstance(spec.right, FieldSpecification)
        assert spec.left.field["value"] == "user.age"
        assert spec.right.field["value"] == "user.name"

    def test_build_or_spec(self, builder):
        """Test building OR specification from tree."""
        tree: SpecificationOrNode = {
            "type": "or",
            "left": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.age",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 18,
                },
            },
            "right": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.name",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": "str",
                    "value": "John",
                },
            },
        }

        spec = builder.build(tree)
        assert isinstance(spec, OrSpecification)
        assert isinstance(spec.left, FieldSpecification)
        assert isinstance(spec.right, FieldSpecification)

    def test_build_not_spec(self, builder):
        """Test building NOT specification from tree."""
        tree: SpecificationNotNode = {
            "type": "not",
            "child": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.age",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 18,
                },
            },
        }

        spec = builder.build(tree)
        assert isinstance(spec, NotSpecification)
        assert isinstance(spec.spec, FieldSpecification)
        assert spec.spec.field["value"] == "user.age"

    def test_build_nested_complex_spec(self, builder):
        """Test building complex nested specification."""
        tree: SpecificationAndNode = {
            "type": "and",
            "left": {
                "type": "leaf",
                "subtype": "field",
                "name": "greater_than_or_equal",
                "field": "user.age",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 18,
                },
            },
            "right": {
                "type": "or",
                "left": {
                    "type": "leaf",
                    "subtype": "field",
                    "name": "contains",
                    "field": "user.name",
                    "compare_to": {
                        "parameter_type": "value",
                        "data_type": "str",
                        "value": "John",
                    },
                },
                "right": {
                    "type": "leaf",
                    "subtype": "callback",
                    "name": "mock_callback",
                    "params": {
                        "age": {
                            "parameter_type": "path",
                            "data_type": "int",
                            "value": "user.age",
                        },
                    },
                },
            },
        }

        spec = builder.build(tree)
        assert isinstance(spec, AndSpecification)
        assert isinstance(spec.left, FieldSpecification)
        assert isinstance(spec.right, OrSpecification)
        assert isinstance(spec.right.left, FieldSpecification)
        assert isinstance(spec.right.right, CallbackSpecification)

    def test_build_unknown_type_raises_error(self, builder):
        """Test that unknown node type raises ValueError."""
        tree = {
            "type": "unknown",
        }

        with pytest.raises(ValueError, match="Unknown specification type"):
            builder.build(tree)  # type: ignore

    def test_build_unknown_leaf_subtype_raises_error(self, builder):
        """Test that unknown leaf subtype raises ValueError."""
        tree = {
            "type": "leaf",
            "subtype": "unknown",
        }

        with pytest.raises(ValueError, match="Unknown leaf subtype"):
            builder.build(tree)  # type: ignore

    def test_build_missing_type_raises_error(self, builder):
        """Test that missing type in tree raises error."""
        tree = {
            "subtype": "field",
        }

        with pytest.raises((ValueError, KeyError)):
            builder.build(tree)  # type: ignore
