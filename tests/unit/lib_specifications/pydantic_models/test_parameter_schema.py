"""Tests for parameter schema pydantic models."""

import pytest

from lib_specifications.core.parameters import ParameterSchema, ParameterTypeEnum, SignatureSchema
from lib_specifications.pydantic_models.parameter_schema import (
    PydanticParameterSchema,
    PydanticSignatureSchema,
)


@pytest.mark.unit
class TestPydanticParameterSchema:
    """Tests for PydanticParameterSchema."""

    def test_create_from_dict_required(self):
        """Test creating PydanticParameterSchema from dict with required parameter."""
        data = {
            "name": "age",
            "data_type": ParameterTypeEnum.INT,
            "required": True,
            "default": None,
        }
        param = PydanticParameterSchema.model_validate(data)
        assert param.name == "age"
        assert param.data_type == ParameterTypeEnum.INT
        assert param.required is True
        assert param.default is None

    def test_create_from_dict_optional(self):
        """Test creating PydanticParameterSchema from dict with optional parameter."""
        data = {
            "name": "name",
            "data_type": ParameterTypeEnum.STR,
            "required": False,
            "default": "John Doe",
        }
        param = PydanticParameterSchema.model_validate(data)
        assert param.name == "name"
        assert param.data_type == ParameterTypeEnum.STR
        assert param.required is False
        assert param.default == "John Doe"

    def test_create_from_dict_defaults(self):
        """Test creating PydanticParameterSchema with default values."""
        data = {
            "name": "age",
            "data_type": ParameterTypeEnum.INT,
        }
        param = PydanticParameterSchema.model_validate(data)
        assert param.name == "age"
        assert param.data_type == ParameterTypeEnum.INT
        assert param.required is True  # default
        assert param.default is None  # default

    def test_create_from_attributes(self):
        """Test creating PydanticParameterSchema from attributes."""
        internal_param = ParameterSchema(
            name="age",
            data_type=ParameterTypeEnum.INT,
            required=False,
            default=18,
        )
        param = PydanticParameterSchema.model_validate(internal_param, from_attributes=True)
        assert param.name == "age"
        assert param.data_type == ParameterTypeEnum.INT
        assert param.required is False
        assert param.default == 18

    def test_serialization_to_dict(self):
        """Test serializing PydanticParameterSchema to dict."""
        param = PydanticParameterSchema(
            name="age",
            data_type=ParameterTypeEnum.INT,
            required=False,
            default=18,
        )
        result = param.model_dump()
        assert result == {
            "name": "age",
            "data_type": ParameterTypeEnum.INT,
            "required": False,
            "default": 18,
        }

    def test_serialization_to_json(self):
        """Test serializing PydanticParameterSchema to JSON."""
        param = PydanticParameterSchema(
            name="name",
            data_type=ParameterTypeEnum.STR,
            required=True,
            default=None,
        )
        # Use model_dump with json-compatible mode to avoid enum serialization issues
        result = param.model_dump(mode="json")
        assert result["name"] == "name"
        # data_type is serialized as enum label
        assert result["data_type"] == "str"

    def test_all_data_types(self):
        """Test PydanticParameterSchema with all data types."""
        for data_type in ParameterTypeEnum:
            param = PydanticParameterSchema(
                name=f"field_{data_type.label}",
                data_type=data_type,
                required=True,
                default=None,
            )
            assert param.data_type == data_type

    def test_to_internal(self):
        """Test converting PydanticParameterSchema to internal ParameterSchema."""
        pydantic_param = PydanticParameterSchema(
            name="age",
            data_type=ParameterTypeEnum.INT,
            required=False,
            default=18,
        )
        internal_param = pydantic_param.to_internal()
        assert isinstance(internal_param, ParameterSchema)
        assert internal_param.name == "age"
        assert internal_param.data_type == ParameterTypeEnum.INT
        assert internal_param.required is False
        assert internal_param.default == 18

    def test_missing_required_fields(self):
        """Test that missing required fields raises validation error."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            PydanticParameterSchema.model_validate({"name": "age"})


@pytest.mark.unit
class TestPydanticSignatureSchema:
    """Tests for PydanticSignatureSchema."""

    def test_create_from_dict(self):
        """Test creating PydanticSignatureSchema from dict."""
        data = {
            "parameters": {
                "age": {
                    "name": "age",
                    "data_type": ParameterTypeEnum.INT,
                    "required": True,
                    "default": None,
                },
                "name": {
                    "name": "name",
                    "data_type": ParameterTypeEnum.STR,
                    "required": False,
                    "default": "John Doe",
                },
            }
        }
        signature = PydanticSignatureSchema.model_validate(data)
        assert len(signature.parameters) == 2
        assert "age" in signature.parameters
        assert "name" in signature.parameters
        assert signature.parameters["age"].name == "age"
        assert signature.parameters["name"].name == "name"

    def test_create_from_dict_empty(self):
        """Test creating PydanticSignatureSchema from dict with empty parameters."""
        data = {"parameters": {}}
        signature = PydanticSignatureSchema.model_validate(data)
        assert len(signature.parameters) == 0

    def test_create_from_attributes(self):
        """Test creating PydanticSignatureSchema from attributes."""
        internal_signature = SignatureSchema(
            parameters={
                "age": ParameterSchema(
                    name="age",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                    default=None,
                ),
                "name": ParameterSchema(
                    name="name",
                    data_type=ParameterTypeEnum.STR,
                    required=False,
                    default="John Doe",
                ),
            }
        )
        signature = PydanticSignatureSchema.model_validate(internal_signature, from_attributes=True)
        assert len(signature.parameters) == 2
        assert "age" in signature.parameters
        assert "name" in signature.parameters

    def test_serialization_to_dict(self):
        """Test serializing PydanticSignatureSchema to dict."""
        signature = PydanticSignatureSchema(
            parameters={
                "age": PydanticParameterSchema(
                    name="age",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                    default=None,
                ),
                "name": PydanticParameterSchema(
                    name="name",
                    data_type=ParameterTypeEnum.STR,
                    required=False,
                    default="John Doe",
                ),
            }
        )
        result = signature.model_dump()
        assert "parameters" in result
        assert len(result["parameters"]) == 2
        assert result["parameters"]["age"]["name"] == "age"
        assert result["parameters"]["name"]["name"] == "name"

    def test_serialization_to_json(self):
        """Test serializing PydanticSignatureSchema to JSON."""
        signature = PydanticSignatureSchema(
            parameters={
                "age": PydanticParameterSchema(
                    name="age",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                    default=None,
                ),
            }
        )
        # Use model_dump with json-compatible mode to avoid enum serialization issues
        result = signature.model_dump(mode="json")
        assert "parameters" in result
        assert "age" in result["parameters"]
        # data_type is serialized as enum label
        assert result["parameters"]["age"]["data_type"] == "int"

    def test_to_internal(self):
        """Test converting PydanticSignatureSchema to internal SignatureSchema."""
        pydantic_signature = PydanticSignatureSchema(
            parameters={
                "age": PydanticParameterSchema(
                    name="age",
                    data_type=ParameterTypeEnum.INT,
                    required=False,
                    default=18,
                ),
                "name": PydanticParameterSchema(
                    name="name",
                    data_type=ParameterTypeEnum.STR,
                    required=True,
                    default=None,
                ),
            }
        )
        internal_signature = pydantic_signature.to_internal()
        assert isinstance(internal_signature, SignatureSchema)
        assert len(internal_signature.parameters) == 2
        assert "age" in internal_signature.parameters
        assert "name" in internal_signature.parameters
        assert internal_signature.parameters["age"].name == "age"
        assert internal_signature.parameters["name"].name == "name"

    def test_missing_required_fields(self):
        """Test that missing required fields raises validation error."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            PydanticSignatureSchema.model_validate({})

    def test_nested_parameter_serialization(self):
        """Test that nested parameters are properly serialized."""
        signature = PydanticSignatureSchema(
            parameters={
                "param1": PydanticParameterSchema(
                    name="param1",
                    data_type=ParameterTypeEnum.BOOL,
                    required=True,
                    default=None,
                ),
                "param2": PydanticParameterSchema(
                    name="param2",
                    data_type=ParameterTypeEnum.FLOAT,
                    required=False,
                    default=3.14,
                ),
            }
        )
        result = signature.model_dump()
        assert result["parameters"]["param1"]["data_type"] == ParameterTypeEnum.BOOL
        assert result["parameters"]["param2"]["data_type"] == ParameterTypeEnum.FLOAT
        assert result["parameters"]["param2"]["default"] == 3.14

