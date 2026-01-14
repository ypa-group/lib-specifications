"""Tests for operator pydantic models."""

import pytest

from lib_specifications.core.parameters import ParameterTypeEnum
from lib_specifications.pydantic_models.operator import PydanticOperatorInfo


@pytest.mark.unit
class TestPydanticOperatorInfo:
    """Tests for PydanticOperatorInfo."""

    def test_create_from_dict(self):
        """Test creating PydanticOperatorInfo from dict."""
        data = {
            "name": "equal",
            "symbol": "==",
            "compatible_types": ["str", "int", "float", "bool", "date", "datetime"],
        }
        operator = PydanticOperatorInfo.model_validate(data)
        assert operator.name == "equal"
        assert operator.symbol == "=="
        assert len(operator.compatible_types) == 6
        assert ParameterTypeEnum.STR in operator.compatible_types
        assert ParameterTypeEnum.INT in operator.compatible_types

    def test_create_from_dict_single_type(self):
        """Test creating PydanticOperatorInfo with single compatible type."""
        data = {
            "name": "greater_than",
            "symbol": ">",
            "compatible_types": ["int"],
        }
        operator = PydanticOperatorInfo.model_validate(data)
        assert operator.name == "greater_than"
        assert operator.symbol == ">"
        assert len(operator.compatible_types) == 1
        assert ParameterTypeEnum.INT in operator.compatible_types

    def test_create_from_attributes(self):
        """Test creating PydanticOperatorInfo from attributes."""
        from dataclasses import dataclass

        @dataclass
        class MockOperator:
            name: str = "equal"
            symbol: str = "=="
            compatible_types: list = None

            def __post_init__(self):
                if self.compatible_types is None:
                    self.compatible_types = [ParameterTypeEnum.STR, ParameterTypeEnum.INT]

        mock_operator = MockOperator()
        operator = PydanticOperatorInfo.model_validate(mock_operator, from_attributes=True)
        assert operator.name == "equal"
        assert operator.symbol == "=="
        assert len(operator.compatible_types) == 2

    def test_create_from_attributes_with_enum_list(self):
        """Test creating PydanticOperatorInfo from attributes with enum list."""
        from dataclasses import dataclass

        @dataclass
        class MockOperator:
            name: str = "equal"
            symbol: str = "=="
            compatible_types: list[ParameterTypeEnum] = None

            def __post_init__(self):
                if self.compatible_types is None:
                    self.compatible_types = [
                        ParameterTypeEnum.STR,
                        ParameterTypeEnum.INT,
                        ParameterTypeEnum.FLOAT,
                    ]

        mock_operator = MockOperator()
        operator = PydanticOperatorInfo.model_validate(mock_operator, from_attributes=True)
        assert operator.name == "equal"
        assert operator.symbol == "=="
        assert len(operator.compatible_types) == 3
        assert all(isinstance(t, ParameterTypeEnum) for t in operator.compatible_types)

    def test_serialization_to_dict(self):
        """Test serializing PydanticOperatorInfo to dict."""
        operator = PydanticOperatorInfo(
            name="equal",
            symbol="==",
            compatible_types=[ParameterTypeEnum.STR, ParameterTypeEnum.INT, ParameterTypeEnum.BOOL],
        )
        result = operator.model_dump()
        assert result == {
            "name": "equal",
            "symbol": "==",
            "compatible_types": [
                ParameterTypeEnum.STR,
                ParameterTypeEnum.INT,
                ParameterTypeEnum.BOOL,
            ],
        }

    def test_serialization_to_json(self):
        """Test serializing PydanticOperatorInfo to JSON."""
        operator = PydanticOperatorInfo(
            name="greater_than",
            symbol=">",
            compatible_types=[ParameterTypeEnum.INT, ParameterTypeEnum.FLOAT],
        )
        # Use model_dump with json-compatible mode to avoid enum serialization issues
        result = operator.model_dump(mode="json")
        assert result["name"] == "greater_than"
        assert result["symbol"] == ">"
        assert "compatible_types" in result
        # compatible_types are serialized as enum labels
        assert "int" in result["compatible_types"]
        assert "float" in result["compatible_types"]

    def test_all_compatible_types(self):
        """Test PydanticOperatorInfo with all compatible types."""
        all_types = list(ParameterTypeEnum)
        operator = PydanticOperatorInfo(
            name="universal",
            symbol="?",
            compatible_types=all_types,
        )
        assert len(operator.compatible_types) == len(ParameterTypeEnum)
        assert all(t in operator.compatible_types for t in ParameterTypeEnum)

    def test_empty_compatible_types(self):
        """Test PydanticOperatorInfo with empty compatible types list."""
        operator = PydanticOperatorInfo(
            name="no_types",
            symbol="?",
            compatible_types=[],
        )
        assert len(operator.compatible_types) == 0

    def test_missing_required_fields(self):
        """Test that missing required fields raises validation error."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            PydanticOperatorInfo.model_validate({"name": "equal"})

    def test_string_compatible_types(self):
        """Test that string compatible types are converted to enums."""
        data = {
            "name": "equal",
            "symbol": "==",
            "compatible_types": ["str", "int", "bool"],
        }
        operator = PydanticOperatorInfo.model_validate(data)
        assert all(isinstance(t, ParameterTypeEnum) for t in operator.compatible_types)
        assert ParameterTypeEnum.STR in operator.compatible_types
        assert ParameterTypeEnum.INT in operator.compatible_types
        assert ParameterTypeEnum.BOOL in operator.compatible_types

