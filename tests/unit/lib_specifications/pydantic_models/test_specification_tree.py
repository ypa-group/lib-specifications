"""Tests for specification tree pydantic models."""

import pytest

from lib_specifications.core.parameters import ParameterTypeEnum
from lib_specifications.pydantic_models.parameter import (
    PydanticParameterLiteralValue,
    PydanticParameterPathValue,
)
from lib_specifications.pydantic_models.specification_tree import (
    PydanticSpecificationAndNode,
    PydanticSpecificationCallbackLeafNode,
    PydanticSpecificationFieldLeafNode,
    PydanticSpecificationNotNode,
    PydanticSpecificationOrNode,
)


@pytest.mark.unit
class TestPydanticSpecificationFieldLeafNode:
    """Tests for PydanticSpecificationFieldLeafNode."""

    def test_create_from_dict(self):
        """Test creating PydanticSpecificationFieldLeafNode from dict."""
        data = {
            "type": "leaf",
            "subtype": "field",
            "name": "equal",
            "field": "user.age",
            "compare_to": {
                "parameter_type": "value",
                "data_type": ParameterTypeEnum.INT,
                "value": 18,
            },
        }
        node = PydanticSpecificationFieldLeafNode.model_validate(data)
        assert node.type == "leaf"
        assert node.subtype == "field"
        assert node.name == "equal"
        assert node.field == "user.age"
        assert isinstance(node.compare_to, PydanticParameterLiteralValue)
        assert node.compare_to.value == 18

    def test_create_from_dict_with_path(self):
        """Test creating PydanticSpecificationFieldLeafNode with path comparison."""
        data = {
            "type": "leaf",
            "subtype": "field",
            "name": "equal",
            "field": "user.age",
            "compare_to": {
                "parameter_type": "path",
                "data_type": ParameterTypeEnum.INT,
                "value": "other.age",
            },
        }
        node = PydanticSpecificationFieldLeafNode.model_validate(data)
        assert isinstance(node.compare_to, PydanticParameterPathValue)
        assert node.compare_to.value == "other.age"

    def test_create_from_attributes(self):
        """Test creating PydanticSpecificationFieldLeafNode from attributes."""
        from dataclasses import dataclass

        @dataclass
        class MockNode:
            type: str = "leaf"
            subtype: str = "field"
            name: str = "equal"
            field: str = "user.age"
            compare_to: dict = None

            def __post_init__(self):
                if self.compare_to is None:
                    self.compare_to = {
                        "parameter_type": "value",
                        "data_type": ParameterTypeEnum.INT,
                        "value": 18,
                    }

        mock_node = MockNode()
        # Create a proper compare_to object
        compare_to = PydanticParameterLiteralValue(
            parameter_type="value",
            data_type=ParameterTypeEnum.INT,
            value=18,
        )
        mock_node.compare_to = compare_to

        node = PydanticSpecificationFieldLeafNode.model_validate(mock_node, from_attributes=True)
        assert node.type == "leaf"
        assert node.subtype == "field"
        assert node.name == "equal"
        assert node.field == "user.age"

    def test_serialization_to_dict(self):
        """Test serializing PydanticSpecificationFieldLeafNode to dict."""
        compare_to = PydanticParameterLiteralValue(
            parameter_type="value",
            data_type=ParameterTypeEnum.INT,
            value=18,
        )
        node = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.age",
            compare_to=compare_to,
        )
        result = node.model_dump()
        assert result["type"] == "leaf"
        assert result["subtype"] == "field"
        assert result["name"] == "equal"
        assert result["field"] == "user.age"
        assert result["compare_to"]["parameter_type"] == "value"
        assert result["compare_to"]["value"] == 18

    def test_serialization_to_json(self):
        """Test serializing PydanticSpecificationFieldLeafNode to JSON."""
        compare_to = PydanticParameterLiteralValue(
            parameter_type="value",
            data_type=ParameterTypeEnum.STR,
            value="active",
        )
        node = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.status",
            compare_to=compare_to,
        )
        # Use model_dump with json-compatible mode to avoid enum serialization issues
        result = node.model_dump(mode="json")
        assert result["type"] == "leaf"
        assert result["subtype"] == "field"
        assert result["name"] == "equal"
        assert result["field"] == "user.status"
        # data_type is serialized as enum label
        assert result["compare_to"]["data_type"] == "str"


@pytest.mark.unit
class TestPydanticSpecificationCallbackLeafNode:
    """Tests for PydanticSpecificationCallbackLeafNode."""

    def test_create_from_dict(self):
        """Test creating PydanticSpecificationCallbackLeafNode from dict."""
        data = {
            "type": "leaf",
            "subtype": "callback",
            "name": "is_weekend",
            "params": {
                "date": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.DATE,
                    "value": "event.date",
                },
            },
        }
        node = PydanticSpecificationCallbackLeafNode.model_validate(data)
        assert node.type == "leaf"
        assert node.subtype == "callback"
        assert node.name == "is_weekend"
        assert len(node.params) == 1
        assert "date" in node.params
        assert isinstance(node.params["date"], PydanticParameterPathValue)
        assert node.params["date"].value == "event.date"

    def test_create_from_dict_multiple_params(self):
        """Test creating PydanticSpecificationCallbackLeafNode with multiple params."""
        data = {
            "type": "leaf",
            "subtype": "callback",
            "name": "check_range",
            "params": {
                "min": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT,
                    "value": 0,
                },
                "max": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT,
                    "value": 100,
                },
            },
        }
        node = PydanticSpecificationCallbackLeafNode.model_validate(data)
        assert len(node.params) == 2
        assert "min" in node.params
        assert "max" in node.params
        assert node.params["min"].value == 0
        assert node.params["max"].value == 100

    def test_create_from_attributes(self):
        """Test creating PydanticSpecificationCallbackLeafNode from attributes."""
        from dataclasses import dataclass

        @dataclass
        class MockNode:
            type: str = "leaf"
            subtype: str = "callback"
            name: str = "is_weekend"
            params: dict = None

            def __post_init__(self):
                if self.params is None:
                    self.params = {
                        "date": PydanticParameterPathValue(
                            parameter_type="path",
                            data_type=ParameterTypeEnum.DATE,
                            value="event.date",
                        ),
                    }

        mock_node = MockNode()
        node = PydanticSpecificationCallbackLeafNode.model_validate(mock_node, from_attributes=True)
        assert node.type == "leaf"
        assert node.subtype == "callback"
        assert node.name == "is_weekend"
        assert len(node.params) == 1

    def test_serialization_to_dict(self):
        """Test serializing PydanticSpecificationCallbackLeafNode to dict."""
        params = {
            "date": PydanticParameterPathValue(
                parameter_type="path",
                data_type=ParameterTypeEnum.DATE,
                value="event.date",
            ),
        }
        node = PydanticSpecificationCallbackLeafNode(
            type="leaf",
            subtype="callback",
            name="is_weekend",
            params=params,
        )
        result = node.model_dump()
        assert result["type"] == "leaf"
        assert result["subtype"] == "callback"
        assert result["name"] == "is_weekend"
        assert "params" in result
        assert "date" in result["params"]
        assert result["params"]["date"]["parameter_type"] == "path"

    def test_serialization_to_json(self):
        """Test serializing PydanticSpecificationCallbackLeafNode to JSON."""
        params = {
            "date": PydanticParameterPathValue(
                parameter_type="path",
                data_type=ParameterTypeEnum.DATE,
                value="event.date",
            ),
        }
        node = PydanticSpecificationCallbackLeafNode(
            type="leaf",
            subtype="callback",
            name="is_weekend",
            params=params,
        )
        # Use model_dump with json-compatible mode to avoid enum serialization issues
        result = node.model_dump(mode="json")
        assert result["type"] == "leaf"
        assert result["subtype"] == "callback"
        assert result["name"] == "is_weekend"
        # data_type is serialized as enum label
        assert result["params"]["date"]["data_type"] == "date"


@pytest.mark.unit
class TestPydanticSpecificationAndNode:
    """Tests for PydanticSpecificationAndNode."""

    def test_create_from_dict(self):
        """Test creating PydanticSpecificationAndNode from dict."""
        data = {
            "type": "and",
            "left": {
                "type": "leaf",
                "subtype": "field",
                "name": "greater_than_or_equal",
                "field": "user.age",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT,
                    "value": 18,
                },
            },
            "right": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.status",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR,
                    "value": "active",
                },
            },
        }
        node = PydanticSpecificationAndNode.model_validate(data)
        assert node.type == "and"
        assert isinstance(node.left, PydanticSpecificationFieldLeafNode)
        assert isinstance(node.right, PydanticSpecificationFieldLeafNode)
        assert node.left.name == "greater_than_or_equal"
        assert node.right.name == "equal"

    def test_create_from_attributes(self):
        """Test creating PydanticSpecificationAndNode from attributes."""
        from dataclasses import dataclass

        left = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.age",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.INT,
                value=18,
            ),
        )
        right = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.status",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.STR,
                value="active",
            ),
        )

        @dataclass
        class MockNode:
            type: str
            left: object
            right: object

        mock_node = MockNode(type="and", left=left, right=right)
        node = PydanticSpecificationAndNode.model_validate(mock_node, from_attributes=True)
        assert node.type == "and"
        assert isinstance(node.left, PydanticSpecificationFieldLeafNode)
        assert isinstance(node.right, PydanticSpecificationFieldLeafNode)

    def test_serialization_to_dict(self):
        """Test serializing PydanticSpecificationAndNode to dict."""
        left = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.age",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.INT,
                value=18,
            ),
        )
        right = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.status",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.STR,
                value="active",
            ),
        )
        node = PydanticSpecificationAndNode(type="and", left=left, right=right)
        result = node.model_dump()
        assert result["type"] == "and"
        assert "left" in result
        assert "right" in result
        assert result["left"]["type"] == "leaf"
        assert result["right"]["type"] == "leaf"

    def test_serialization_to_json(self):
        """Test serializing PydanticSpecificationAndNode to JSON."""
        left = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.age",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.INT,
                value=18,
            ),
        )
        right = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.status",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.STR,
                value="active",
            ),
        )
        node = PydanticSpecificationAndNode(type="and", left=left, right=right)
        # Use model_dump with json-compatible mode to avoid enum serialization issues
        result = node.model_dump(mode="json")
        assert result["type"] == "and"
        assert "left" in result
        assert "right" in result


@pytest.mark.unit
class TestPydanticSpecificationOrNode:
    """Tests for PydanticSpecificationOrNode."""

    def test_create_from_dict(self):
        """Test creating PydanticSpecificationOrNode from dict."""
        data = {
            "type": "or",
            "left": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.status",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR,
                    "value": "active",
                },
            },
            "right": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.status",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR,
                    "value": "premium",
                },
            },
        }
        node = PydanticSpecificationOrNode.model_validate(data)
        assert node.type == "or"
        assert isinstance(node.left, PydanticSpecificationFieldLeafNode)
        assert isinstance(node.right, PydanticSpecificationFieldLeafNode)

    def test_create_from_attributes(self):
        """Test creating PydanticSpecificationOrNode from attributes."""
        from dataclasses import dataclass

        left = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.status",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.STR,
                value="active",
            ),
        )
        right = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.status",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.STR,
                value="premium",
            ),
        )

        @dataclass
        class MockNode:
            type: str
            left: object
            right: object

        mock_node = MockNode(type="or", left=left, right=right)
        node = PydanticSpecificationOrNode.model_validate(mock_node, from_attributes=True)
        assert node.type == "or"
        assert isinstance(node.left, PydanticSpecificationFieldLeafNode)
        assert isinstance(node.right, PydanticSpecificationFieldLeafNode)

    def test_serialization_to_dict(self):
        """Test serializing PydanticSpecificationOrNode to dict."""
        left = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.status",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.STR,
                value="active",
            ),
        )
        right = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.status",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.STR,
                value="premium",
            ),
        )
        node = PydanticSpecificationOrNode(type="or", left=left, right=right)
        result = node.model_dump()
        assert result["type"] == "or"
        assert "left" in result
        assert "right" in result

    def test_serialization_to_json(self):
        """Test serializing PydanticSpecificationOrNode to JSON."""
        left = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.status",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.STR,
                value="active",
            ),
        )
        right = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.status",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.STR,
                value="premium",
            ),
        )
        node = PydanticSpecificationOrNode(type="or", left=left, right=right)
        # Use model_dump with json-compatible mode to avoid enum serialization issues
        result = node.model_dump(mode="json")
        assert result["type"] == "or"


@pytest.mark.unit
class TestPydanticSpecificationNotNode:
    """Tests for PydanticSpecificationNotNode."""

    def test_create_from_dict(self):
        """Test creating PydanticSpecificationNotNode from dict."""
        data = {
            "type": "not",
            "child": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.banned",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.BOOL,
                    "value": True,
                },
            },
        }
        node = PydanticSpecificationNotNode.model_validate(data)
        assert node.type == "not"
        assert isinstance(node.child, PydanticSpecificationFieldLeafNode)
        assert node.child.name == "equal"

    def test_create_from_attributes(self):
        """Test creating PydanticSpecificationNotNode from attributes."""
        from dataclasses import dataclass

        child = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.banned",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.BOOL,
                value=True,
            ),
        )

        @dataclass
        class MockNode:
            type: str
            child: object

        mock_node = MockNode(type="not", child=child)
        node = PydanticSpecificationNotNode.model_validate(mock_node, from_attributes=True)
        assert node.type == "not"
        assert isinstance(node.child, PydanticSpecificationFieldLeafNode)

    def test_serialization_to_dict(self):
        """Test serializing PydanticSpecificationNotNode to dict."""
        child = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.banned",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.BOOL,
                value=True,
            ),
        )
        node = PydanticSpecificationNotNode(type="not", child=child)
        result = node.model_dump()
        assert result["type"] == "not"
        assert "child" in result
        assert result["child"]["type"] == "leaf"

    def test_serialization_to_json(self):
        """Test serializing PydanticSpecificationNotNode to JSON."""
        child = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.banned",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.BOOL,
                value=True,
            ),
        )
        node = PydanticSpecificationNotNode(type="not", child=child)
        # Use model_dump with json-compatible mode to avoid enum serialization issues
        result = node.model_dump(mode="json")
        assert result["type"] == "not"
        assert "child" in result


@pytest.mark.unit
class TestPydanticSpecificationTree:
    """Tests for PydanticSpecificationTree discriminated union."""

    def test_discriminated_union_field_leaf(self):
        """Test that PydanticSpecificationTree correctly discriminates field leaf."""
        data = {
            "type": "leaf",
            "subtype": "field",
            "name": "equal",
            "field": "user.age",
            "compare_to": {
                "parameter_type": "value",
                "data_type": ParameterTypeEnum.INT,
                "value": 18,
            },
        }
        # PydanticSpecificationTree is a type alias, test via concrete type
        node = PydanticSpecificationFieldLeafNode.model_validate(data)
        assert isinstance(node, PydanticSpecificationFieldLeafNode)
        assert node.type == "leaf"
        assert node.subtype == "field"

    def test_discriminated_union_callback_leaf(self):
        """Test that PydanticSpecificationTree correctly discriminates callback leaf."""
        data = {
            "type": "leaf",
            "subtype": "callback",
            "name": "is_weekend",
            "params": {
                "date": {
                    "parameter_type": "path",
                    "data_type": ParameterTypeEnum.DATE,
                    "value": "event.date",
                },
            },
        }
        # PydanticSpecificationTree is a type alias, test via concrete type
        node = PydanticSpecificationCallbackLeafNode.model_validate(data)
        assert isinstance(node, PydanticSpecificationCallbackLeafNode)
        assert node.type == "leaf"
        assert node.subtype == "callback"

    def test_discriminated_union_and_node(self):
        """Test that PydanticSpecificationTree correctly discriminates and node."""
        data = {
            "type": "and",
            "left": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.age",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT,
                    "value": 18,
                },
            },
            "right": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.status",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR,
                    "value": "active",
                },
            },
        }
        # PydanticSpecificationTree is a type alias, test via concrete type
        node = PydanticSpecificationAndNode.model_validate(data)
        assert isinstance(node, PydanticSpecificationAndNode)
        assert node.type == "and"

    def test_discriminated_union_or_node(self):
        """Test that PydanticSpecificationTree correctly discriminates or node."""
        data = {
            "type": "or",
            "left": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.status",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR,
                    "value": "active",
                },
            },
            "right": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.status",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR,
                    "value": "premium",
                },
            },
        }
        # PydanticSpecificationTree is a type alias, test via concrete type
        node = PydanticSpecificationOrNode.model_validate(data)
        assert isinstance(node, PydanticSpecificationOrNode)
        assert node.type == "or"

    def test_discriminated_union_not_node(self):
        """Test that PydanticSpecificationTree correctly discriminates not node."""
        data = {
            "type": "not",
            "child": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.banned",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.BOOL,
                    "value": True,
                },
            },
        }
        # PydanticSpecificationTree is a type alias, test via concrete type
        node = PydanticSpecificationNotNode.model_validate(data)
        assert isinstance(node, PydanticSpecificationNotNode)
        assert node.type == "not"

    def test_nested_structure(self):
        """Test nested specification tree structure."""
        data = {
            "type": "and",
            "left": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.age",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT,
                    "value": 18,
                },
            },
            "right": {
                "type": "or",
                "left": {
                    "type": "leaf",
                    "subtype": "field",
                    "name": "equal",
                    "field": "user.status",
                    "compare_to": {
                        "parameter_type": "value",
                        "data_type": ParameterTypeEnum.STR,
                        "value": "active",
                    },
                },
                "right": {
                    "type": "leaf",
                    "subtype": "field",
                    "name": "equal",
                    "field": "user.status",
                    "compare_to": {
                        "parameter_type": "value",
                        "data_type": ParameterTypeEnum.STR,
                        "value": "premium",
                    },
                },
            },
        }
        # PydanticSpecificationTree is a type alias, test via concrete type
        node = PydanticSpecificationAndNode.model_validate(data)
        assert isinstance(node, PydanticSpecificationAndNode)
        assert isinstance(node.right, PydanticSpecificationOrNode)
        assert isinstance(node.right.left, PydanticSpecificationFieldLeafNode)

    def test_serialization_nested(self):
        """Test serialization of nested structure."""
        left = PydanticSpecificationFieldLeafNode(
            type="leaf",
            subtype="field",
            name="equal",
            field="user.age",
            compare_to=PydanticParameterLiteralValue(
                parameter_type="value",
                data_type=ParameterTypeEnum.INT,
                value=18,
            ),
        )
        right = PydanticSpecificationOrNode(
            type="or",
            left=PydanticSpecificationFieldLeafNode(
                type="leaf",
                subtype="field",
                name="equal",
                field="user.status",
                compare_to=PydanticParameterLiteralValue(
                    parameter_type="value",
                    data_type=ParameterTypeEnum.STR,
                    value="active",
                ),
            ),
            right=PydanticSpecificationFieldLeafNode(
                type="leaf",
                subtype="field",
                name="equal",
                field="user.status",
                compare_to=PydanticParameterLiteralValue(
                    parameter_type="value",
                    data_type=ParameterTypeEnum.STR,
                    value="premium",
                ),
            ),
        )
        node = PydanticSpecificationAndNode(type="and", left=left, right=right)
        result = node.model_dump()
        assert result["type"] == "and"
        assert result["right"]["type"] == "or"
        assert result["right"]["left"]["type"] == "leaf"
