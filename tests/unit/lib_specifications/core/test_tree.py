"""Tests for SpecificationTree type definitions."""

import pytest

from lib_specifications.core.tree import (
    SpecificationAndNode,
    SpecificationCallbackLeafNode,
    SpecificationFieldLeafNode,
    SpecificationNotNode,
    SpecificationOrNode,
    SpecificationTree,
)


@pytest.mark.unit
class TestSpecificationTree:
    """Tests for SpecificationTree type definitions."""

    def test_field_leaf_node_structure(self):
        """Test that SpecificationFieldLeafNode has correct structure."""
        node: SpecificationFieldLeafNode = {
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

        assert node["type"] == "leaf"
        assert node["subtype"] == "field"
        assert node["name"] == "equal"
        assert node["field"] == "user.age"
        assert node["compare_to"]["parameter_type"] == "value"

    def test_callback_leaf_node_structure(self):
        """Test that SpecificationCallbackLeafNode has correct structure."""
        node: SpecificationCallbackLeafNode = {
            "type": "leaf",
            "subtype": "callback",
            "name": "test_callback",
            "params": {
                "age": {
                    "parameter_type": "path",
                    "data_type": "int",
                    "value": "user.age",
                },
            },
        }

        assert node["type"] == "leaf"
        assert node["subtype"] == "callback"
        assert node["name"] == "test_callback"
        assert "age" in node["params"]
        assert node["params"]["age"]["value"] == "user.age"

    def test_and_node_structure(self):
        """Test that SpecificationAndNode has correct structure."""
        left: SpecificationFieldLeafNode = {
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

        right: SpecificationFieldLeafNode = {
            "type": "leaf",
            "subtype": "field",
            "name": "equal",
            "field": "user.name",
            "compare_to": {
                "parameter_type": "value",
                "data_type": "str",
                "value": "John",
            },
        }

        node: SpecificationAndNode = {
            "type": "and",
            "left": left,
            "right": right,
        }

        assert node["type"] == "and"
        assert node["left"]["type"] == "leaf"
        assert node["right"]["type"] == "leaf"

    def test_or_node_structure(self):
        """Test that SpecificationOrNode has correct structure."""
        left: SpecificationFieldLeafNode = {
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

        right: SpecificationFieldLeafNode = {
            "type": "leaf",
            "subtype": "field",
            "name": "equal",
            "field": "user.name",
            "compare_to": {
                "parameter_type": "value",
                "data_type": "str",
                "value": "John",
            },
        }

        node: SpecificationOrNode = {
            "type": "or",
            "left": left,
            "right": right,
        }

        assert node["type"] == "or"
        assert node["left"]["type"] == "leaf"
        assert node["right"]["type"] == "leaf"

    def test_not_node_structure(self):
        """Test that SpecificationNotNode has correct structure."""
        child: SpecificationFieldLeafNode = {
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

        node: SpecificationNotNode = {
            "type": "not",
            "child": child,
        }

        assert node["type"] == "not"
        assert node["child"]["type"] == "leaf"

    def test_nested_tree_structure(self):
        """Test that nested SpecificationTree structures work correctly."""
        # Create a complex nested tree: (age >= 18) AND ((name contains "John") OR callback)
        field1: SpecificationFieldLeafNode = {
            "type": "leaf",
            "subtype": "field",
            "name": "greater_than_or_equal",
            "field": "user.age",
            "compare_to": {
                "parameter_type": "value",
                "data_type": "int",
                "value": 18,
            },
        }

        field2: SpecificationFieldLeafNode = {
            "type": "leaf",
            "subtype": "field",
            "name": "contains",
            "field": "user.name",
            "compare_to": {
                "parameter_type": "value",
                "data_type": "str",
                "value": "John",
            },
        }

        callback: SpecificationCallbackLeafNode = {
            "type": "leaf",
            "subtype": "callback",
            "name": "test_callback",
            "params": {
                "age": {
                    "parameter_type": "path",
                    "data_type": "int",
                    "value": "user.age",
                },
            },
        }

        or_node: SpecificationOrNode = {
            "type": "or",
            "left": field2,
            "right": callback,
        }

        and_node: SpecificationAndNode = {
            "type": "and",
            "left": field1,
            "right": or_node,
        }

        tree: SpecificationTree = and_node

        assert tree["type"] == "and"
        assert tree["left"]["type"] == "leaf"
        assert tree["right"]["type"] == "or"
        assert tree["right"]["left"]["type"] == "leaf"
        assert tree["right"]["right"]["type"] == "leaf"
        assert tree["right"]["right"]["subtype"] == "callback"

    def test_tree_with_path_compare_to(self):
        """Test tree with path compare_to parameter."""
        node: SpecificationFieldLeafNode = {
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

        assert node["compare_to"]["parameter_type"] == "path"
        assert node["compare_to"]["value"] == "min_age"

    def test_tree_with_mixed_callback_params(self):
        """Test callback node with mixed path and literal parameters."""
        node: SpecificationCallbackLeafNode = {
            "type": "leaf",
            "subtype": "callback",
            "name": "test_callback",
            "params": {
                "age": {
                    "parameter_type": "path",
                    "data_type": "int",
                    "value": "user.age",
                },
                "min_age": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 21,
                },
            },
        }

        assert node["params"]["age"]["parameter_type"] == "path"
        assert node["params"]["min_age"]["parameter_type"] == "value"
        assert node["params"]["min_age"]["value"] == 21

    def test_tree_type_union(self):
        """Test that SpecificationTree accepts all node types."""
        # Test that we can assign different node types to SpecificationTree
        field_node: SpecificationTree = {
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

        callback_node: SpecificationTree = {
            "type": "leaf",
            "subtype": "callback",
            "name": "test",
            "params": {},
        }

        and_node: SpecificationTree = {
            "type": "and",
            "left": field_node,
            "right": callback_node,
        }

        or_node: SpecificationTree = {
            "type": "or",
            "left": field_node,
            "right": callback_node,
        }

        not_node: SpecificationTree = {
            "type": "not",
            "child": field_node,
        }

        # All should be valid SpecificationTree types
        assert field_node["type"] in ["leaf", "and", "or", "not"]
        assert callback_node["type"] == "leaf"
        assert and_node["type"] == "and"
        assert or_node["type"] == "or"
        assert not_node["type"] == "not"
