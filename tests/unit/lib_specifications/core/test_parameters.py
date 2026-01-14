"""Tests for types module."""

from datetime import date, datetime

import pytest

from lib_specifications.core.parameters import (
    ParameterSchema,
    ParameterTypeEnum,
    SignatureSchema,
    generate_signature_from_callable,
)


@pytest.mark.unit
class TestParameterTypeEnum:
    """Tests for ParameterTypeEnum."""

    def test_string_value(self):
        """Test string value property."""
        assert ParameterTypeEnum.STR.label == "str"
        assert ParameterTypeEnum.INT.label == "int"
        assert ParameterTypeEnum.FLOAT.label == "float"
        assert ParameterTypeEnum.BOOL.label == "bool"
        assert ParameterTypeEnum.DATE.label == "date"
        assert ParameterTypeEnum.DATETIME.label == "datetime"
        assert ParameterTypeEnum.LIST.label == "list"

    def test_python_type(self):
        """Test python_type property."""
        assert ParameterTypeEnum.STR.python_type is str
        assert ParameterTypeEnum.INT.python_type is int
        assert ParameterTypeEnum.FLOAT.python_type is float
        assert ParameterTypeEnum.BOOL.python_type is bool
        assert ParameterTypeEnum.DATE.python_type is date
        assert ParameterTypeEnum.DATETIME.python_type is datetime
        assert ParameterTypeEnum.LIST.python_type is list
        assert ParameterTypeEnum.DICT.python_type is dict

    def test_str_method(self):
        """Test __str__ method."""
        assert str(ParameterTypeEnum.STR) == "str"
        assert str(ParameterTypeEnum.INT) == "int"

    def test_from_string(self):
        """Test from_string class method."""
        assert ParameterTypeEnum.from_string("str") == ParameterTypeEnum.STR
        assert ParameterTypeEnum.from_string("int") == ParameterTypeEnum.INT
        assert ParameterTypeEnum.from_string("float") == ParameterTypeEnum.FLOAT
        assert ParameterTypeEnum.from_string("bool") == ParameterTypeEnum.BOOL
        assert ParameterTypeEnum.from_string("date") == ParameterTypeEnum.DATE
        assert ParameterTypeEnum.from_string("datetime") == ParameterTypeEnum.DATETIME
        assert ParameterTypeEnum.from_string("list") == ParameterTypeEnum.LIST
        assert ParameterTypeEnum.from_string("dict") == ParameterTypeEnum.DICT

    def test_from_string_invalid(self):
        """Test from_string with invalid value."""
        with pytest.raises(ValueError, match="No ParameterTypeEnum member"):
            ParameterTypeEnum.from_string("invalid")

    def test_from_type(self):
        """Test from_type class method."""
        assert ParameterTypeEnum.from_type(str) == ParameterTypeEnum.STR
        assert ParameterTypeEnum.from_type(int) == ParameterTypeEnum.INT
        assert ParameterTypeEnum.from_type(float) == ParameterTypeEnum.FLOAT
        assert ParameterTypeEnum.from_type(bool) == ParameterTypeEnum.BOOL
        assert ParameterTypeEnum.from_type(date) == ParameterTypeEnum.DATE
        assert ParameterTypeEnum.from_type(datetime) == ParameterTypeEnum.DATETIME
        assert ParameterTypeEnum.from_type(list) == ParameterTypeEnum.LIST
        assert ParameterTypeEnum.from_type(dict) == ParameterTypeEnum.DICT

    def test_from_type_invalid(self):
        """Test from_type with invalid type."""
        with pytest.raises(ValueError, match="No ParameterTypeEnum member"):
            ParameterTypeEnum.from_type(tuple)

    def test_get_dummy_value(self):
        """Test get_dummy_value method for all types."""
        from datetime import date, datetime

        assert ParameterTypeEnum.INT.get_dummy_value() == 1
        assert ParameterTypeEnum.STR.get_dummy_value() == ""
        assert ParameterTypeEnum.FLOAT.get_dummy_value() == 0.0
        assert ParameterTypeEnum.BOOL.get_dummy_value() is False
        assert ParameterTypeEnum.DICT.get_dummy_value() == {}
        assert ParameterTypeEnum.LIST.get_dummy_value() == []
        assert ParameterTypeEnum.DATE.get_dummy_value() == date(2025, 1, 1)
        assert ParameterTypeEnum.DATETIME.get_dummy_value() == datetime(2025, 1, 1)


@pytest.mark.unit
class TestParameterSchema:
    """Tests for ParameterSchema."""

    def test_create_parameter_schema(self):
        """Test creating a ParameterSchema."""
        param = ParameterSchema(
            name="age",
            data_type=ParameterTypeEnum.INT,
            required=False,
            default=18,
        )
        assert param.name == "age"
        assert param.data_type == ParameterTypeEnum.INT
        assert param.default == 18
        assert param.required is False

    def test_parameter_schema_required(self):
        """Test ParameterSchema with required parameter."""
        param = ParameterSchema(
            name="age",
            data_type=ParameterTypeEnum.INT,
            required=True,
        )
        assert param.name == "age"
        assert param.data_type == ParameterTypeEnum.INT
        assert param.required is True
        assert param.default is None

    def test_parameter_schema_to_dict(self):
        """Test ParameterSchema.to_dict method."""
        param = ParameterSchema(
            name="age",
            data_type=ParameterTypeEnum.INT,
            required=False,
            default=18,
        )
        result = param.to_dict()
        assert result == {
            "name": "age",
            "data_type": "int",
            "required": False,
            "default": 18,
        }

    def test_parameter_schema_from_dict(self):
        """Test ParameterSchema.from_dict method."""
        data = {
            "name": "age",
            "data_type": "int",
            "required": False,
            "default": 18,
        }
        param = ParameterSchema.from_dict(data)
        assert param.name == "age"
        assert param.data_type == ParameterTypeEnum.INT
        assert param.required is False
        assert param.default == 18

    def test_parameter_schema_from_dict_missing_data_type(self):
        """Test ParameterSchema.from_dict with missing data_type."""
        data = {
            "name": "age",
            "required": False,
            "default": 18,
        }
        with pytest.raises(ValueError, match="data_type is required"):
            ParameterSchema.from_dict(data)

    def test_parameter_schema_from_dict_invalid_data_type(self):
        """Test ParameterSchema.from_dict with invalid data_type."""
        data = {
            "name": "age",
            "data_type": "invalid",
            "required": False,
            "default": 18,
        }
        with pytest.raises(ValueError, match="Invalid data_type"):
            ParameterSchema.from_dict(data)

    def test_parameter_schema_required_with_default_raises_error(self):
        """Test ParameterSchema with required=True and default value raises ValueError."""
        with pytest.raises(ValueError, match="Default value is not allowed for required parameters"):
            ParameterSchema(
                name="age",
                data_type=ParameterTypeEnum.INT,
                required=True,
                default=18,
            )


@pytest.mark.unit
class TestSignatureSchema:
    """Tests for SignatureSchema."""

    def test_create_signature_schema(self):
        """Test creating a SignatureSchema."""
        signature = SignatureSchema(
            parameters={
                "age": ParameterSchema(
                    name="age",
                    data_type=ParameterTypeEnum.INT,
                    required=False,
                    default=18,
                ),
                "name": ParameterSchema(
                    name="name",
                    data_type=ParameterTypeEnum.STR,
                    required=False,
                    default="John Doe",
                ),
            }
        )
        assert len(signature.parameters) == 2
        assert "age" in signature.parameters
        assert "name" in signature.parameters

    def test_signature_schema_get_parameter(self):
        """Test SignatureSchema.get_parameter method."""
        signature = SignatureSchema(
            parameters={
                "age": ParameterSchema(
                    name="age",
                    data_type=ParameterTypeEnum.INT,
                    required=False,
                    default=18,
                ),
            }
        )
        param = signature.get_parameter("age")
        assert param is not None
        assert param.name == "age"
        assert param.required is False
        assert param.default == 18

        param = signature.get_parameter("nonexistent")
        assert param is None

    def test_signature_schema_has_parameter(self):
        """Test SignatureSchema.has_parameter method."""
        signature = SignatureSchema(
            parameters={
                "age": ParameterSchema(
                    name="age",
                    data_type=ParameterTypeEnum.INT,
                    required=False,
                    default=18,
                ),
            }
        )
        assert signature.has_parameter("age") is True
        assert signature.has_parameter("nonexistent") is False

    def test_signature_schema_to_dict(self):
        """Test SignatureSchema.to_dict method."""
        signature = SignatureSchema(
            parameters={
                "age": ParameterSchema(
                    name="age",
                    data_type=ParameterTypeEnum.INT,
                    required=False,
                    default=18,
                ),
            }
        )
        result = signature.to_dict()
        assert "parameters" in result
        assert "age" in result["parameters"]
        assert result["parameters"]["age"]["name"] == "age"
        assert result["parameters"]["age"]["data_type"] == "int"
        assert result["parameters"]["age"]["required"] is False
        assert result["parameters"]["age"]["default"] == 18

    def test_signature_schema_from_dict(self):
        """Test SignatureSchema.from_dict method."""
        data = {
            "parameters": {
                "age": {
                    "name": "age",
                    "data_type": "int",
                    "required": False,
                    "default": 18,
                },
            }
        }
        signature = SignatureSchema.from_dict(data)
        assert len(signature.parameters) == 1
        assert signature.parameters["age"].name == "age"
        assert signature.parameters["age"].data_type == ParameterTypeEnum.INT
        assert signature.parameters["age"].required is False
        assert signature.parameters["age"].default == 18

    def test_signature_schema_from_dict_invalid_parameters(self):
        """Test SignatureSchema.from_dict with invalid parameters."""
        data = {
            "parameters": "not a dict",
        }
        with pytest.raises(ValueError, match="parameters must be a dictionary"):
            SignatureSchema.from_dict(data)

    def test_signature_schema_from_dict_invalid_parameter(self):
        """Test SignatureSchema.from_dict with invalid parameter."""
        data = {
            "parameters": {
                "age": "not a dict",
            }
        }
        with pytest.raises(ValueError, match="parameter age must be a dictionary"):
            SignatureSchema.from_dict(data)


@pytest.mark.unit
class TestGenerateSignatureFromCallable:
    """Tests for generate_signature_from_callable function."""

    def test_generate_signature_single_required_parameter(self):
        """Test generating signature from function with single required parameter."""

        def is_adult(age: int) -> bool:
            return age >= 18

        schema = generate_signature_from_callable(is_adult)
        assert len(schema.parameters) == 1
        assert "age" in schema.parameters
        assert schema.parameters["age"].name == "age"
        assert schema.parameters["age"].data_type == ParameterTypeEnum.INT
        assert schema.parameters["age"].required is True
        assert schema.parameters["age"].default is None

    def test_generate_signature_with_default_value(self):
        """Test generating signature from function with default parameter."""

        def is_adult(age: int, min_age: int = 18) -> bool:
            return age >= min_age

        schema = generate_signature_from_callable(is_adult)
        assert len(schema.parameters) == 2
        assert schema.parameters["age"].required is True
        assert schema.parameters["min_age"].required is False
        assert schema.parameters["min_age"].default == 18

    def test_generate_signature_multiple_parameters(self):
        """Test generating signature from function with multiple parameters."""

        def check_user(name: str, age: int, active: bool) -> bool:
            return len(name) > 0 and age >= 18 and active

        schema = generate_signature_from_callable(check_user)
        assert len(schema.parameters) == 3
        assert schema.parameters["name"].data_type == ParameterTypeEnum.STR
        assert schema.parameters["age"].data_type == ParameterTypeEnum.INT
        assert schema.parameters["active"].data_type == ParameterTypeEnum.BOOL

    def test_generate_signature_all_types(self):
        """Test generating signature with all supported types."""

        def all_types(
            name: str,
            age: int,
            height: float,
            active: bool,
            birth_date: date,
            created_at: datetime,
            tags: list,
            metadata: dict,
        ) -> bool:
            return True

        schema = generate_signature_from_callable(all_types)
        assert len(schema.parameters) == 8
        assert schema.parameters["name"].data_type == ParameterTypeEnum.STR
        assert schema.parameters["age"].data_type == ParameterTypeEnum.INT
        assert schema.parameters["height"].data_type == ParameterTypeEnum.FLOAT
        assert schema.parameters["active"].data_type == ParameterTypeEnum.BOOL
        assert schema.parameters["birth_date"].data_type == ParameterTypeEnum.DATE
        assert schema.parameters["created_at"].data_type == ParameterTypeEnum.DATETIME
        assert schema.parameters["tags"].data_type == ParameterTypeEnum.LIST
        assert schema.parameters["metadata"].data_type == ParameterTypeEnum.DICT

    def test_generate_signature_skips_self_parameter(self):
        """Test that self parameter is skipped for methods."""

        class TestClass:
            def method(self, age: int) -> bool:
                return age >= 18

        schema = generate_signature_from_callable(TestClass.method)
        assert len(schema.parameters) == 1
        assert "age" in schema.parameters
        assert "self" not in schema.parameters

    def test_generate_signature_no_parameters(self):
        """Test generating signature from function with no parameters."""

        def no_params() -> bool:
            return True

        schema = generate_signature_from_callable(no_params)
        assert len(schema.parameters) == 0

    def test_generate_signature_with_none_default(self):
        """Test generating signature with None as default value."""

        def with_none(name: str, value: int = None) -> bool:
            return value is not None

        schema = generate_signature_from_callable(with_none)
        assert len(schema.parameters) == 2
        assert schema.parameters["name"].required is True
        assert schema.parameters["value"].required is False
        assert schema.parameters["value"].default is None

    def test_generate_signature_raises_error_for_args(self):
        """Test that *args parameter raises ValueError."""

        def with_args(*args: int) -> bool:
            return True

        with pytest.raises(ValueError, match="contains \\*args parameter"):
            generate_signature_from_callable(with_args)

    def test_generate_signature_raises_error_for_kwargs(self):
        """Test that **kwargs parameter raises ValueError."""

        def with_kwargs(**kwargs: dict) -> bool:
            return True

        with pytest.raises(ValueError, match="contains \\*\\*kwargs parameter"):
            generate_signature_from_callable(with_kwargs)

    def test_generate_signature_raises_error_missing_annotation(self):
        """Test that missing type annotation raises ValueError."""

        def no_annotation(age):  # noqa: ANN001
            return age >= 18

        with pytest.raises(ValueError, match="No annotation for parameter"):
            generate_signature_from_callable(no_annotation)

    def test_generate_signature_raises_error_invalid_type(self):
        """Test that invalid type (not in ParameterTypeEnum) raises ValueError."""

        def invalid_type(value: tuple) -> bool:  # tuple is not supported
            return True

        with pytest.raises(ValueError, match="Invalid type for parameter"):
            generate_signature_from_callable(invalid_type)

    def test_generate_signature_mixed_required_optional(self):
        """Test generating signature with mix of required and optional parameters."""

        def mixed(name: str, age: int, city: str = "Unknown", active: bool = True) -> bool:
            return len(name) > 0 and age >= 18

        schema = generate_signature_from_callable(mixed)
        assert len(schema.parameters) == 4
        assert schema.parameters["name"].required is True
        assert schema.parameters["age"].required is True
        assert schema.parameters["city"].required is False
        assert schema.parameters["city"].default == "Unknown"
        assert schema.parameters["active"].required is False
        assert schema.parameters["active"].default is True

    def test_generate_signature_with_async_function(self):
        """Test generating signature from async function."""

        async def async_func(age: int) -> bool:
            return age >= 18

        schema = generate_signature_from_callable(async_func)
        assert len(schema.parameters) == 1
        assert schema.parameters["age"].data_type == ParameterTypeEnum.INT
