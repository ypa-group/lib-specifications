"""
Shared pytest configuration and fixtures for all tests.
"""

import asyncio
from collections.abc import Generator
from unittest.mock import AsyncMock, Mock

import pytest


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an instance of the default event loop for the test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_async_function() -> AsyncMock:
    """Create a mock async function."""
    return AsyncMock()


@pytest.fixture
def mock_sync_function() -> Mock:
    """Create a mock sync function."""
    return Mock()


# Pytest hooks for test collection and execution
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests that test individual components in isolation")
    config.addinivalue_line("markers", "integration: Integration tests that test component interactions")
    config.addinivalue_line("markers", "e2e: End-to-end tests that test the full application flow")


def pytest_collection_modifyitems(config, items):
    """
    Automatically mark tests based on their location.
    """
    for item in items:
        # Mark tests based on directory
        test_path = str(item.path)
        if "/unit/" in test_path or "\\unit\\" in test_path:
            item.add_marker(pytest.mark.unit)
        elif "/integration/" in test_path or "\\integration\\" in test_path:
            item.add_marker(pytest.mark.integration)
        elif "/e2e/" in test_path or "\\e2e\\" in test_path:
            item.add_marker(pytest.mark.e2e)

        # Mark async tests
        if hasattr(item, "function") and asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asynchronous)
