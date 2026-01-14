"""Tests for default interceptor registry."""

import pytest

from lib_specifications.catalog.interceptor_registry import INTERCEPTOR_REGISTRY
from lib_specifications.catalog.interceptor_registry.advertising import ADVERTISING_INTERCEPTOR_CT
from lib_specifications.catalog.interceptor_registry.greetings import GREETINGS_INTERCEPTOR_CT
from lib_specifications.core import InterceptorContentTypeEnum


@pytest.mark.unit
class TestDefaultInterceptorRegistry:
    """Tests for default interceptor registry."""

    def test_registry_is_initialized(self):
        """Test that interceptor_registry is initialized."""
        assert INTERCEPTOR_REGISTRY is not None
        assert hasattr(INTERCEPTOR_REGISTRY, "get_by_name")
        assert hasattr(INTERCEPTOR_REGISTRY, "get_all")

    def test_greetings_interceptor_registered(self):
        """Test that GREETINGS interceptor is registered."""
        interceptor = INTERCEPTOR_REGISTRY.get_by_name("GREETINGS")
        assert interceptor == GREETINGS_INTERCEPTOR_CT
        assert interceptor.name == InterceptorContentTypeEnum.GREETINGS
        assert INTERCEPTOR_REGISTRY.GREETINGS == GREETINGS_INTERCEPTOR_CT

    def test_advertising_interceptor_registered(self):
        """Test that ADVERTISING interceptor is registered."""
        interceptor = INTERCEPTOR_REGISTRY.get_by_name("ADVERTISING")
        assert interceptor == ADVERTISING_INTERCEPTOR_CT
        assert interceptor.name == InterceptorContentTypeEnum.ADVERTISING
        assert INTERCEPTOR_REGISTRY.ADVERTISING == ADVERTISING_INTERCEPTOR_CT

    def test_all_interceptors_registered(self):
        """Test that all interceptors are registered."""
        expected_interceptors = {
            "GREETINGS": GREETINGS_INTERCEPTOR_CT,
            "ADVERTISING": ADVERTISING_INTERCEPTOR_CT,
        }

        for name, interceptor in expected_interceptors.items():
            assert INTERCEPTOR_REGISTRY.get_by_name(name) == interceptor, f"{name} should be registered"
            assert getattr(INTERCEPTOR_REGISTRY, name) == interceptor, f"{name} should be accessible as attribute"

    def test_get_all_interceptors(self):
        """Test that get_all returns all registered interceptors."""
        all_interceptors = INTERCEPTOR_REGISTRY.get_all()
        assert len(all_interceptors) == 2

        interceptor_names = {interceptor.name for interceptor in all_interceptors}
        expected_names = {
            InterceptorContentTypeEnum.GREETINGS,
            InterceptorContentTypeEnum.ADVERTISING,
        }
        assert interceptor_names == expected_names

    def test_greetings_interceptor_has_context_schema(self):
        """Test that GREETINGS interceptor has context schema."""
        interceptor = INTERCEPTOR_REGISTRY.get_by_name("GREETINGS")
        assert interceptor.context_schema is not None
        assert "session.last_interaction_at" in interceptor.context_schema.parameters

    def test_greetings_interceptor_has_applicable_specifications(self):
        """Test that GREETINGS interceptor has applicable specifications."""
        interceptor = INTERCEPTOR_REGISTRY.get_by_name("GREETINGS")
        assert interceptor.applicable_specifications is not None
        assert len(interceptor.applicable_specifications) > 0
        # Check that it contains expected callbacks
        specs = interceptor.applicable_specifications
        callback_qualnames = {cb.qualname for cb in specs}
        assert "isTimeAfter" in callback_qualnames
        assert "hasOnboarded" in callback_qualnames

    def test_advertising_interceptor_has_context_schema(self):
        """Test that ADVERTISING interceptor has context schema."""
        interceptor = INTERCEPTOR_REGISTRY.get_by_name("ADVERTISING")
        assert interceptor.context_schema is not None
        assert "session.last_interaction_at" in interceptor.context_schema.parameters

    def test_advertising_interceptor_has_applicable_specifications(self):
        """Test that ADVERTISING interceptor has applicable specifications."""
        interceptor = INTERCEPTOR_REGISTRY.get_by_name("ADVERTISING")
        assert interceptor.applicable_specifications is not None
        assert len(interceptor.applicable_specifications) > 0
        # Check that it contains expected callbacks
        specs = interceptor.applicable_specifications
        callback_qualnames = {cb.qualname for cb in specs}
        assert "isTimeAfter" in callback_qualnames
        assert "hasOnboarded" in callback_qualnames
