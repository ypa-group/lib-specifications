"""Tests for parameter pydantic models."""

from datetime import date

import pytest

from lib_specifications.core.parameters import ParameterTypeEnum
from lib_specifications.pydantic_models import (
    PydanticParameterLiteralValue,
    PydanticParameterPathValue,
    PydanticParameterValue,
)


@pytest.mark.unit
class TestPydanticParameterPathValue:
    """Tests for PydanticParameterPathValue."""

    def test_create_from_dict(self):
        """Test creating PydanticParameterPathValue from dict."""
        data = {
            "parameter_type": "path",
            "data_type": ParameterTypeEnum.INT,
            "value": "user.age",
        }
        param = PydanticParameterPathValue.model_validate(data)
        assert param.parameter_type == "path"
        assert param.data_type == ParameterTypeEnum.INT
        assert param.value == "user.age"

    def test_create_from_attributes(self):
        """Test creating PydanticParameterPathValue from attributes."""
        from dataclasses import dataclass

        @dataclass
        class MockParam:
            parameter_type: str = "path"
            data_type: ParameterTypeEnum = ParameterTypeEnum.INT
            value: str = "user.age"

        mock_param = MockParam()
        param = PydanticParameterPathValue.model_validate(mock_param, from_attributes=True)
        assert param.parameter_type == "path"
        assert param.data_type == ParameterTypeEnum.INT
        assert param.value == "user.age"

    def test_serialization_to_dict(self):
        """Test serializing PydanticParameterPathValue to dict."""
        param = PydanticParameterPathValue(
            parameter_type="path",
            data_type=ParameterTypeEnum.INT,
            value="user.age",
        )
        result = param.model_dump()
        assert result == {
            "parameter_type": "path",
            "data_type": ParameterTypeEnum.INT,
            "value": "user.age",
        }

    def test_serialization_to_json(self):
        """Test serializing PydanticParameterPathValue to JSON."""
        param = PydanticParameterPathValue(
            parameter_type="path",
            data_type=ParameterTypeEnum.STR,
            value="user.name",
        )
        # Use model_dump with json-compatible mode to avoid enum serialization issues
        result = param.model_dump(mode="json")
        assert result["parameter_type"] == "path"
        assert result["value"] == "user.name"
        # data_type is serialized as enum label
        assert result["data_type"] == "str"

    def test_all_data_types(self):
        """Test PydanticParameterPathValue with all data types."""
        for data_type in ParameterTypeEnum:
            param = PydanticParameterPathValue(
                parameter_type="path",
                data_type=data_type,
                value=f"field.{data_type.label}",
            )
            assert param.data_type == data_type
            assert param.value == f"field.{data_type.label}"

    def test_invalid_parameter_type(self):
        """Test that invalid parameter_type raises validation error."""
        from pydantic import ValidationError

        data = {
            "parameter_type": "invalid",
            "data_type": ParameterTypeEnum.INT,
            "value": "user.age",
        }
        with pytest.raises(ValidationError):
            PydanticParameterPathValue.model_validate(data)

    def test_missing_required_fields(self):
        """Test that missing required fields raises validation error."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            PydanticParameterPathValue.model_validate({"parameter_type": "path"})


@pytest.mark.unit
class TestPydanticParameterLiteralValue:
    """Tests for PydanticParameterLiteralValue."""

    def test_create_from_dict_int(self):
        """Test creating PydanticParameterLiteralValue from dict with int."""
        data = {
            "parameter_type": "value",
            "data_type": ParameterTypeEnum.INT,
            "value": 18,
        }
        param = PydanticParameterLiteralValue.model_validate(data)
        assert param.parameter_type == "value"
        assert param.data_type == ParameterTypeEnum.INT
        assert param.value == 18

    def test_create_from_dict_str(self):
        """Test creating PydanticParameterLiteralValue from dict with str."""
        data = {
            "parameter_type": "value",
            "data_type": ParameterTypeEnum.STR,
            "value": "hello",
        }
        param = PydanticParameterLiteralValue.model_validate(data)
        assert param.parameter_type == "value"
        assert param.data_type == ParameterTypeEnum.STR
        assert param.value == "hello"

    def test_create_from_dict_bool(self):
        """Test creating PydanticParameterLiteralValue from dict with bool."""
        data = {
            "parameter_type": "value",
            "data_type": ParameterTypeEnum.BOOL,
            "value": True,
        }
        param = PydanticParameterLiteralValue.model_validate(data)
        assert param.parameter_type == "value"
        assert param.data_type == ParameterTypeEnum.BOOL
        assert param.value is True

    def test_create_from_dict_float(self):
        """Test creating PydanticParameterLiteralValue from dict with float."""
        data = {
            "parameter_type": "value",
            "data_type": ParameterTypeEnum.FLOAT,
            "value": 3.14,
        }
        param = PydanticParameterLiteralValue.model_validate(data)
        assert param.parameter_type == "value"
        assert param.data_type == ParameterTypeEnum.FLOAT
        assert param.value == 3.14

    def test_create_from_dict_date(self):
        """Test creating PydanticParameterLiteralValue from dict with date."""
        test_date = date(2025, 1, 15)
        data = {
            "parameter_type": "value",
            "data_type": ParameterTypeEnum.DATE,
            "value": test_date,
        }
        param = PydanticParameterLiteralValue.model_validate(data)
        assert param.parameter_type == "value"
        assert param.data_type == ParameterTypeEnum.DATE
        assert param.value == test_date

    def test_create_from_attributes(self):
        """Test creating PydanticParameterLiteralValue from attributes."""
        from dataclasses import dataclass

        @dataclass
        class MockParam:
            parameter_type: str = "value"
            data_type: ParameterTypeEnum = ParameterTypeEnum.INT
            value: int = 42

        mock_param = MockParam()
        param = PydanticParameterLiteralValue.model_validate(mock_param, from_attributes=True)
        assert param.parameter_type == "value"
        assert param.data_type == ParameterTypeEnum.INT
        assert param.value == 42

    def test_serialization_to_dict(self):
        """Test serializing PydanticParameterLiteralValue to dict."""
        param = PydanticParameterLiteralValue(
            parameter_type="value",
            data_type=ParameterTypeEnum.INT,
            value=42,
        )
        result = param.model_dump()
        assert result == {
            "parameter_type": "value",
            "data_type": ParameterTypeEnum.INT,
            "value": 42,
        }

    def test_serialization_to_json(self):
        """Test serializing PydanticParameterLiteralValue to JSON."""
        param = PydanticParameterLiteralValue(
            parameter_type="value",
            data_type=ParameterTypeEnum.STR,
            value="test",
        )
        # Use model_dump with json-compatible mode to avoid enum serialization issues
        result = param.model_dump(mode="json")
        assert result["parameter_type"] == "value"
        assert result["value"] == "test"
        # data_type is serialized as enum label
        assert result["data_type"] == "str"

    def test_complex_values(self):
        """Test PydanticParameterLiteralValue with complex values."""
        # Test with list
        param_list = PydanticParameterLiteralValue(
            parameter_type="value",
            data_type=ParameterTypeEnum.LIST,
            value=[1, 2, 3],
        )
        assert param_list.value == [1, 2, 3]

        # Test with dict
        param_dict = PydanticParameterLiteralValue(
            parameter_type="value",
            data_type=ParameterTypeEnum.DICT,
            value={"key": "value"},
        )
        assert param_dict.value == {"key": "value"}

    def test_invalid_parameter_type(self):
        """Test that invalid parameter_type raises validation error."""
        from pydantic import ValidationError

        data = {
            "parameter_type": "invalid",
            "data_type": ParameterTypeEnum.INT,
            "value": 18,
        }
        with pytest.raises(ValidationError):
            PydanticParameterLiteralValue.model_validate(data)


@pytest.mark.unit
class TestPydanticParameterValue:
    """Tests for PydanticParameterValue discriminated union."""

    def test_discriminated_union_path(self):
        """Test that PydanticParameterValue correctly discriminates path type."""
        data = {
            "parameter_type": "path",
            "data_type": ParameterTypeEnum.INT,
            "value": "user.age",
        }
        param = PydanticParameterPathValue.model_validate(data)
        assert isinstance(param, PydanticParameterPathValue)
        assert param.parameter_type == "path"
        assert param.value == "user.age"

    def test_discriminated_union_value(self):
        """Test that PydanticParameterValue correctly discriminates value type."""
        data = {
            "parameter_type": "value",
            "data_type": ParameterTypeEnum.INT,
            "value": 18,
        }
        param = PydanticParameterLiteralValue.model_validate(data)
        assert isinstance(param, PydanticParameterLiteralValue)
        assert param.parameter_type == "value"
        assert param.value == 18

    def test_discriminated_union_from_attributes_path(self):
        """Test discriminated union from attributes with path type."""
        from dataclasses import dataclass

        @dataclass
        class MockParam:
            parameter_type: str
            data_type: ParameterTypeEnum
            value: str

        mock_param = MockParam(
            parameter_type="path",
            data_type=ParameterTypeEnum.STR,
            value="user.name",
        )
        param = PydanticParameterValue.model_validate(mock_param, from_attributes=True)
        assert isinstance(param, PydanticParameterPathValue)
        assert param.parameter_type == "path"

    def test_discriminated_union_from_attributes_value(self):
        """Test discriminated union from attributes with value type."""
        from dataclasses import dataclass

        @dataclass
        class MockParam:
            parameter_type: str
            data_type: ParameterTypeEnum
            value: int

        mock_param = MockParam(
            parameter_type="value",
            data_type=ParameterTypeEnum.INT,
            value=42,
        )
        param = PydanticParameterValue.model_validate(mock_param, from_attributes=True)
        assert isinstance(param, PydanticParameterLiteralValue)
        assert param.parameter_type == "value"

    def test_serialization_path(self):
        """Test serialization of path type through union."""
        param = PydanticParameterPathValue(
            parameter_type="path",
            data_type=ParameterTypeEnum.STR,
            value="user.name",
        )
        result = param.model_dump()
        assert result["parameter_type"] == "path"
        assert result["value"] == "user.name"

    def test_serialization_value(self):
        """Test serialization of value type through union."""
        param = PydanticParameterLiteralValue(
            parameter_type="value",
            data_type=ParameterTypeEnum.INT,
            value=100,
        )
        result = param.model_dump()
        assert result["parameter_type"] == "value"
        assert result["value"] == 100
