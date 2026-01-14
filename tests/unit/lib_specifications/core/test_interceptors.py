"""Tests for interceptors module."""

import pytest

from lib_specifications.core.interceptors import (
    InterceptorContentType,
    InterceptorContentTypeEnum,
    InterceptorContentTypeRegistry,
)
from lib_specifications.core.parameters import ContextSchema, ParameterSchema, ParameterTypeEnum


@pytest.mark.unit
class TestInterceptorContentTypeEnum:
    """Tests for InterceptorContentTypeEnum."""

    def test_enum_values(self):
        """Test that enum has expected values."""
        assert InterceptorContentTypeEnum.GREETINGS == "GREETINGS"
        assert InterceptorContentTypeEnum.ADVERTISING == "ADVERTISING"

    def test_enum_is_string_enum(self):
        """Test that enum values are strings."""
        assert isinstance(InterceptorContentTypeEnum.GREETINGS.value, str)
        assert isinstance(InterceptorContentTypeEnum.ADVERTISING.value, str)


@pytest.mark.unit
class TestInterceptorContentType:
    """Tests for InterceptorContentType dataclass."""

    def test_interceptor_content_type_creation_minimal(self):
        """Test creating InterceptorContentType with minimal fields."""
        interceptor = InterceptorContentType(name=InterceptorContentTypeEnum.GREETINGS)
        assert interceptor.name == InterceptorContentTypeEnum.GREETINGS
        assert interceptor.description is None
        assert interceptor.applicable_specifications is None
        assert interceptor.context_schema is None

    def test_interceptor_content_type_creation_full(self):
        """Test creating InterceptorContentType with all fields."""
        context_schema = ContextSchema(
            parameters={
                "user.id": ParameterSchema(
                    name="user.id",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                )
            }
        )
        interceptor = InterceptorContentType(
            name=InterceptorContentTypeEnum.GREETINGS,
            description="Welcome messages",
            applicable_specifications={"spec1", "spec2"},
            context_schema=context_schema,
        )
        assert interceptor.name == InterceptorContentTypeEnum.GREETINGS
        assert interceptor.description == "Welcome messages"
        assert interceptor.applicable_specifications == {"spec1", "spec2"}
        assert interceptor.context_schema == context_schema

    def test_interceptor_content_type_str(self):
        """Test string representation."""
        interceptor = InterceptorContentType(name=InterceptorContentTypeEnum.ADVERTISING)
        assert str(interceptor) == "ADVERTISING"

    def test_interceptor_content_type_to_dict_minimal(self):
        """Test to_dict with minimal fields."""
        interceptor = InterceptorContentType(name=InterceptorContentTypeEnum.GREETINGS)
        result = interceptor.to_dict()
        assert result["name"] == InterceptorContentTypeEnum.GREETINGS
        assert result["description"] is None
        assert result["applicable_specifications"] == []
        assert result["context_schema"] is None

    def test_interceptor_content_type_to_dict_full(self):
        """Test to_dict with all fields."""
        from lib_specifications.core.callback import BaseCallback

        # Create mock callback classes for testing
        class MockCallback1(BaseCallback):
            qualname = "spec1"

            def __init__(self):
                pass

            def __call__(self) -> bool:
                return True

        class MockCallback2(BaseCallback):
            qualname = "spec2"

            def __init__(self):
                pass

            def __call__(self) -> bool:
                return True

        context_schema = ContextSchema(
            parameters={
                "user.id": ParameterSchema(
                    name="user.id",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                )
            }
        )
        interceptor = InterceptorContentType(
            name=InterceptorContentTypeEnum.GREETINGS,
            description="Welcome messages",
            applicable_specifications={MockCallback1, MockCallback2},
            context_schema=context_schema,
        )
        result = interceptor.to_dict()
        assert result["name"] == InterceptorContentTypeEnum.GREETINGS
        assert result["description"] == "Welcome messages"
        assert set(result["applicable_specifications"]) == {"spec1", "spec2"}
        assert result["context_schema"] is not None
        assert "parameters" in result["context_schema"]


@pytest.mark.unit
class TestInterceptorContentTypeRegistry:
    """Tests for InterceptorContentTypeRegistry."""

    def test_registry_creation(self):
        """Test creating a registry."""
        interceptor1 = InterceptorContentType(name=InterceptorContentTypeEnum.GREETINGS)
        interceptor2 = InterceptorContentType(name=InterceptorContentTypeEnum.ADVERTISING)
        registry = InterceptorContentTypeRegistry([interceptor1, interceptor2])
        assert len(registry.get_all()) == 2

    def test_registry_get_by_name(self):
        """Test getting interceptor by name."""
        interceptor = InterceptorContentType(name=InterceptorContentTypeEnum.GREETINGS)
        registry = InterceptorContentTypeRegistry([interceptor])
        result = registry.get_by_name("GREETINGS")
        assert result == interceptor
        assert result.name == InterceptorContentTypeEnum.GREETINGS

    def test_registry_get_by_name_invalid(self):
        """Test getting interceptor by invalid name raises error."""
        interceptor = InterceptorContentType(name=InterceptorContentTypeEnum.GREETINGS)
        registry = InterceptorContentTypeRegistry([interceptor])
        with pytest.raises(ValueError, match="Invalid InterceptorContentType"):
            registry.get_by_name("invalid")

    def test_registry_get_by_name_case_sensitive(self):
        """Test that get_by_name is case sensitive."""
        interceptor = InterceptorContentType(name=InterceptorContentTypeEnum.GREETINGS)
        registry = InterceptorContentTypeRegistry([interceptor])
        with pytest.raises(ValueError):
            registry.get_by_name("greetings")  # Different case

    def test_registry_get_all(self):
        """Test getting all interceptors."""
        interceptor1 = InterceptorContentType(name=InterceptorContentTypeEnum.GREETINGS)
        interceptor2 = InterceptorContentType(name=InterceptorContentTypeEnum.ADVERTISING)
        registry = InterceptorContentTypeRegistry([interceptor1, interceptor2])
        all_interceptors = registry.get_all()
        assert len(all_interceptors) == 2
        assert interceptor1 in all_interceptors
        assert interceptor2 in all_interceptors

    def test_registry_get_all_empty(self):
        """Test getting all interceptors from empty registry."""
        registry = InterceptorContentTypeRegistry([])
        assert len(registry.get_all()) == 0

    def test_registry_duplicate_names(self):
        """Test that duplicate names overwrite previous entries."""
        interceptor1 = InterceptorContentType(
            name=InterceptorContentTypeEnum.GREETINGS,
            description="First",
        )
        interceptor2 = InterceptorContentType(
            name=InterceptorContentTypeEnum.GREETINGS,
            description="Second",
        )
        registry = InterceptorContentTypeRegistry([interceptor1, interceptor2])
        result = registry.get_by_name("GREETINGS")
        # Last one wins
        assert result.description == "Second"

    def test_registry_with_context_schema(self):
        """Test registry with interceptors that have context schemas."""
        context_schema = ContextSchema(
            parameters={
                "user.id": ParameterSchema(
                    name="user.id",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                )
            }
        )
        interceptor = InterceptorContentType(
            name=InterceptorContentTypeEnum.GREETINGS,
            context_schema=context_schema,
        )
        registry = InterceptorContentTypeRegistry([interceptor])
        result = registry.get_by_name("GREETINGS")
        assert result.context_schema == context_schema

    def test_registry_with_applicable_specifications(self):
        """Test registry with interceptors that have applicable specifications."""
        interceptor = InterceptorContentType(
            name=InterceptorContentTypeEnum.GREETINGS,
            applicable_specifications={"spec1", "spec2", "spec3"},
        )
        registry = InterceptorContentTypeRegistry([interceptor])
        result = registry.get_by_name("GREETINGS")
        assert result.applicable_specifications == {"spec1", "spec2", "spec3"}
