"""Tests for user callbacks."""

import pytest

from lib_specifications.catalog.callback_registry.user_callbacks import HasOnboardedCallback


# Concrete implementation for testing
class HasOnboardedCallbackImpl(HasOnboardedCallback):
    """Concrete implementation for testing."""

    def __call__(self) -> bool:
        """Mock implementation for testing."""
        return True


@pytest.mark.unit
class TestHasOnboardedCallback:
    """Tests for HasOnboardedCallback."""

    def test_initialization(self):
        """Test that callback can be initialized with required parameters."""
        callback = HasOnboardedCallbackImpl(auth_provider="google", auth_provider_user_id="user123")
        assert callback.auth_provider == "google"
        assert callback.auth_provider_user_id == "user123"

    def test_initialization_different_provider(self):
        """Test initialization with different auth provider."""
        callback = HasOnboardedCallbackImpl(auth_provider="github", auth_provider_user_id="gh_user456")
        assert callback.auth_provider == "github"
        assert callback.auth_provider_user_id == "gh_user456"

    def test_is_base_callback(self):
        """Test that HasOnboardedCallback inherits from BaseCallback."""
        from lib_specifications.core.callback import BaseCallback

        assert issubclass(HasOnboardedCallback, BaseCallback)

    def test_concrete_implementation_can_be_called(self):
        """Test that concrete implementation can be called."""
        callback = HasOnboardedCallbackImpl(auth_provider="google", auth_provider_user_id="user123")
        result = callback()
        assert result is True

    def test_abstract_callback_raises_not_implemented(self):
        """Test that abstract callback raises NotImplementedError when called."""
        # HasOnboardedCallback is not an ABC, but raises NotImplementedError when __call__ is invoked
        callback = HasOnboardedCallback(auth_provider="google", auth_provider_user_id="user123")
        assert callback.auth_provider == "google"
        assert callback.auth_provider_user_id == "user123"

        # Verify it raises NotImplementedError when called
        with pytest.raises(NotImplementedError, match="This callback should be implemented"):
            callback()
