"""Tests for callback pydantic models."""

import pytest

from lib_specifications.core.parameters import ParameterSchema, ParameterTypeEnum, SignatureSchema
from lib_specifications.pydantic_models.callback import PydanticCallbackInfo
from lib_specifications.pydantic_models.parameter_schema import (
    PydanticParameterSchema,
    PydanticSignatureSchema,
)


@pytest.mark.unit
class TestPydanticCallbackInfo:
    """Tests for PydanticCallbackInfo."""

    def test_create_from_dict(self):
        """Test creating PydanticCallbackInfo from dict."""
        data = {
            "name": "is_weekend",
            "signature": {
                "parameters": {
                    "date": {
                        "name": "date",
                        "data_type": "date",
                        "required": True,
                        "default": None,
                    },
                },
            },
        }
        callback = PydanticCallbackInfo.model_validate(data)
        assert callback.name == "is_weekend"
        assert isinstance(callback.signature, PydanticSignatureSchema)
        assert len(callback.signature.parameters) == 1
        assert "date" in callback.signature.parameters

    def test_create_from_dict_multiple_params(self):
        """Test creating PydanticCallbackInfo with multiple parameters."""
        data = {
            "name": "check_range",
            "signature": {
                "parameters": {
                    "min": {
                        "name": "min",
                        "data_type": "int",
                        "required": True,
                        "default": None,
                    },
                    "max": {
                        "name": "max",
                        "data_type": "int",
                        "required": False,
                        "default": 100,
                    },
                },
            },
        }
        callback = PydanticCallbackInfo.model_validate(data)
        assert callback.name == "check_range"
        assert len(callback.signature.parameters) == 2
        assert "min" in callback.signature.parameters
        assert "max" in callback.signature.parameters
        assert callback.signature.parameters["min"].required is True
        assert callback.signature.parameters["max"].required is False
        assert callback.signature.parameters["max"].default == 100

    def test_create_from_dict_empty_params(self):
        """Test creating PydanticCallbackInfo with empty parameters."""
        data = {
            "name": "no_params",
            "signature": {
                "parameters": {},
            },
        }
        callback = PydanticCallbackInfo.model_validate(data)
        assert callback.name == "no_params"
        assert len(callback.signature.parameters) == 0

    def test_create_from_attributes(self):
        """Test creating PydanticCallbackInfo from attributes."""
        internal_signature = SignatureSchema(
            parameters={
                "date": ParameterSchema(
                    name="date",
                    data_type=ParameterTypeEnum.DATE,
                    required=True,
                    default=None,
                ),
            }
        )
        from dataclasses import dataclass, field

        @dataclass
        class MockCallback:
            name: str = "is_weekend"
            signature: SignatureSchema = field(default_factory=lambda: internal_signature)

        mock_callback = MockCallback()
        callback = PydanticCallbackInfo.model_validate(mock_callback, from_attributes=True)
        assert callback.name == "is_weekend"
        assert isinstance(callback.signature, PydanticSignatureSchema)
        assert len(callback.signature.parameters) == 1

    def test_create_from_attributes_with_pydantic_signature(self):
        """Test creating PydanticCallbackInfo from attributes with PydanticSignatureSchema."""
        pydantic_signature = PydanticSignatureSchema(
            parameters={
                "date": PydanticParameterSchema(
                    name="date",
                    data_type=ParameterTypeEnum.DATE,
                    required=True,
                    default=None,
                ),
            }
        )
        from dataclasses import dataclass, field

        @dataclass
        class MockCallback:
            name: str = "is_weekend"
            signature: PydanticSignatureSchema = field(default_factory=lambda: pydantic_signature)

        mock_callback = MockCallback()
        callback = PydanticCallbackInfo.model_validate(mock_callback, from_attributes=True)
        assert callback.name == "is_weekend"
        assert isinstance(callback.signature, PydanticSignatureSchema)

    def test_serialization_to_dict(self):
        """Test serializing PydanticCallbackInfo to dict."""
        signature = PydanticSignatureSchema(
            parameters={
                "date": PydanticParameterSchema(
                    name="date",
                    data_type=ParameterTypeEnum.DATE,
                    required=True,
                    default=None,
                ),
            }
        )
        callback = PydanticCallbackInfo(
            name="is_weekend",
            signature=signature,
        )
        result = callback.model_dump()
        assert result == {
            "name": "is_weekend",
            "signature": {
                "parameters": {
                    "date": {
                        "name": "date",
                        "data_type": ParameterTypeEnum.DATE,
                        "required": True,
                        "default": None,
                    },
                },
            },
        }

    def test_serialization_to_json(self):
        """Test serializing PydanticCallbackInfo to JSON."""
        signature = PydanticSignatureSchema(
            parameters={
                "date": PydanticParameterSchema(
                    name="date",
                    data_type=ParameterTypeEnum.DATE,
                    required=True,
                    default=None,
                ),
            }
        )
        callback = PydanticCallbackInfo(
            name="is_weekend",
            signature=signature,
        )
        # Use model_dump with json-compatible mode to avoid enum serialization issues
        result = callback.model_dump(mode="json")
        assert result["name"] == "is_weekend"
        assert "signature" in result
        assert "parameters" in result["signature"]

    def test_complex_signature(self):
        """Test PydanticCallbackInfo with complex signature."""
        signature = PydanticSignatureSchema(
            parameters={
                "name": PydanticParameterSchema(
                    name="name",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                    default=None,
                ),
                "age": PydanticParameterSchema(
                    name="age",
                    data_type=ParameterTypeEnum.INT,
                    required=False,
                    default=18,
                ),
                "active": PydanticParameterSchema(
                    name="active",
                    data_type=ParameterTypeEnum.BOOL,
                    required=False,
                    default=True,
                ),
            }
        )
        callback = PydanticCallbackInfo(
            name="check_user",
            signature=signature,
        )
        assert len(callback.signature.parameters) == 3
        assert "name" in callback.signature.parameters
        assert "age" in callback.signature.parameters
        assert "active" in callback.signature.parameters

    def test_missing_required_fields(self):
        """Test that missing required fields raises validation error."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            PydanticCallbackInfo.model_validate({"name": "is_weekend"})

    def test_nested_parameter_serialization(self):
        """Test that nested parameters are properly serialized."""
        signature = PydanticSignatureSchema(
            parameters={
                "param1": PydanticParameterSchema(
                    name="param1",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                    default=None,
                ),
                "param2": PydanticParameterSchema(
                    name="param2",
                    data_type=ParameterTypeEnum.STR,
                    required=False,
                    default="default",
                ),
            }
        )
        callback = PydanticCallbackInfo(
            name="test_callback",
            signature=signature,
        )
        result = callback.model_dump()
        assert result["signature"]["parameters"]["param1"]["data_type"] == ParameterTypeEnum.INT
        assert result["signature"]["parameters"]["param2"]["data_type"] == ParameterTypeEnum.STR
        assert result["signature"]["parameters"]["param2"]["default"] == "default"
