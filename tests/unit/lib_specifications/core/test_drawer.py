"""Tests for drawer core classes."""

import pytest

from lib_specifications.core import (
    DrawerApp,
    DrawerRegistry,
    DrawerScreen,
    DrawerScreenOption,
)


@pytest.mark.unit
class TestDrawerScreenOption:
    """Tests for DrawerScreenOption dataclass."""

    def test_create_drawer_screen_option(self):
        """Test creating a DrawerScreenOption."""
        option = DrawerScreenOption(value="option1", label="Option 1")
        assert option.value == "option1"
        assert option.label == "Option 1"

    def test_drawer_screen_option_equality(self):
        """Test DrawerScreenOption equality."""
        option1 = DrawerScreenOption(value="option1", label="Option 1")
        option2 = DrawerScreenOption(value="option1", label="Option 1")
        option3 = DrawerScreenOption(value="option2", label="Option 2")
        assert option1 == option2
        assert option1 != option3


@pytest.mark.unit
class TestDrawerScreen:
    """Tests for DrawerScreen dataclass."""

    def test_create_drawer_screen_minimal(self):
        """Test creating a DrawerScreen with minimal fields."""
        screen = DrawerScreen(
            value="screen1",
            screen_type="external",
            label="Screen 1",
        )
        assert screen.value == "screen1"
        assert screen.screen_type == "external"
        assert screen.label == "Screen 1"
        assert screen.is_active is True  # Default value
        assert screen.options is None  # Default value

    def test_create_drawer_screen_with_all_fields(self):
        """Test creating a DrawerScreen with all fields."""
        options = [
            DrawerScreenOption(value="opt1", label="Option 1"),
            DrawerScreenOption(value="opt2", label="Option 2"),
        ]
        screen = DrawerScreen(
            value="screen1",
            screen_type="internal",
            label="Screen 1",
            is_active=False,
            options=options,
        )
        assert screen.value == "screen1"
        assert screen.screen_type == "internal"
        assert screen.label == "Screen 1"
        assert screen.is_active is False
        assert screen.options == options
        assert len(screen.options) == 2

    def test_drawer_screen_types(self):
        """Test DrawerScreen with different screen types."""
        external_screen = DrawerScreen(
            value="external_screen",
            screen_type="external",
            label="External Screen",
        )
        internal_screen = DrawerScreen(
            value="internal_screen",
            screen_type="internal",
            label="Internal Screen",
        )
        assert external_screen.screen_type == "external"
        assert internal_screen.screen_type == "internal"

    def test_drawer_screen_equality(self):
        """Test DrawerScreen equality."""
        screen1 = DrawerScreen(
            value="screen1",
            screen_type="external",
            label="Screen 1",
        )
        screen2 = DrawerScreen(
            value="screen1",
            screen_type="external",
            label="Screen 1",
        )
        screen3 = DrawerScreen(
            value="screen2",
            screen_type="external",
            label="Screen 2",
        )
        assert screen1 == screen2
        assert screen1 != screen3


@pytest.mark.unit
class TestDrawerApp:
    """Tests for DrawerApp dataclass."""

    def test_create_drawer_app(self):
        """Test creating a DrawerApp."""
        screens = {
            "screen1": DrawerScreen(
                value="screen1",
                screen_type="external",
                label="Screen 1",
            ),
            "screen2": DrawerScreen(
                value="screen2",
                screen_type="internal",
                label="Screen 2",
            ),
        }
        app = DrawerApp(
            value="app",
            label="App",
            screens=screens,
        )
        assert app.value == "app"
        assert app.label == "App"
        assert len(app.screens) == 2
        assert "screen1" in app.screens
        assert "screen2" in app.screens
        assert app.screens["screen1"].value == "screen1"
        assert app.screens["screen2"].value == "screen2"

    def test_drawer_app_empty_screens(self):
        """Test creating a DrawerApp with empty screens."""
        app = DrawerApp(
            value="app",
            label="App",
            screens={},
        )
        assert app.value == "app"
        assert len(app.screens) == 0

    def test_drawer_app_equality(self):
        """Test DrawerApp equality."""
        screens1 = {
            "screen1": DrawerScreen(
                value="screen1",
                screen_type="external",
                label="Screen 1",
            ),
        }
        screens2 = {
            "screen1": DrawerScreen(
                value="screen1",
                screen_type="external",
                label="Screen 1",
            ),
        }
        app1 = DrawerApp(value="app", label="App", screens=screens1)
        app2 = DrawerApp(value="app", label="App", screens=screens2)
        app3 = DrawerApp(value="other_app", label="Other App", screens=screens1)
        assert app1 == app2
        assert app1 != app3


@pytest.mark.unit
class TestDrawerRegistry:
    """Tests for DrawerRegistry class."""

    def test_create_registry(self):
        """Test creating a DrawerRegistry."""
        app1 = DrawerApp(
            value="app1",
            label="App 1",
            screens={
                "screen1": DrawerScreen(
                    value="screen1",
                    screen_type="external",
                    label="Screen 1",
                ),
            },
        )
        app2 = DrawerApp(
            value="app2",
            label="App 2",
            screens={
                "screen2": DrawerScreen(
                    value="screen2",
                    screen_type="internal",
                    label="Screen 2",
                ),
            },
        )
        registry = DrawerRegistry([app1, app2])
        assert len(registry.apps) == 2
        assert "app1" in registry.apps
        assert "app2" in registry.apps

    def test_get_app_success(self):
        """Test getting an app from registry."""
        app = DrawerApp(
            value="app",
            label="App",
            screens={
                "screen1": DrawerScreen(
                    value="screen1",
                    screen_type="external",
                    label="Screen 1",
                ),
            },
        )
        registry = DrawerRegistry([app])
        retrieved_app = registry.get_app("app")
        assert retrieved_app == app
        assert retrieved_app.value == "app"
        assert retrieved_app.label == "App"

    def test_get_app_not_found(self):
        """Test getting a non-existent app raises ValueError."""
        app = DrawerApp(
            value="app",
            label="App",
            screens={},
        )
        registry = DrawerRegistry([app])
        with pytest.raises(ValueError, match="Invalid DrawerAppType: invalid_app"):
            registry.get_app("invalid_app")

    def test_get_screen_success(self):
        """Test getting a screen from registry."""
        screen = DrawerScreen(
            value="screen1",
            screen_type="external",
            label="Screen 1",
        )
        app = DrawerApp(
            value="app",
            label="App",
            screens={"screen1": screen},
        )
        registry = DrawerRegistry([app])
        retrieved_screen = registry.get_screen("app", "screen1")
        assert retrieved_screen == screen
        assert retrieved_screen.value == "screen1"
        assert retrieved_screen.label == "Screen 1"

    def test_get_screen_app_not_found(self):
        """Test getting a screen from non-existent app raises ValueError."""
        app = DrawerApp(
            value="app",
            label="App",
            screens={},
        )
        registry = DrawerRegistry([app])
        with pytest.raises(ValueError, match="Invalid DrawerAppType: invalid_app"):
            registry.get_screen("invalid_app", "screen1")

    def test_get_screen_not_found(self):
        """Test getting a non-existent screen raises ValueError."""
        app = DrawerApp(
            value="app",
            label="App",
            screens={
                "screen1": DrawerScreen(
                    value="screen1",
                    screen_type="external",
                    label="Screen 1",
                ),
            },
        )
        registry = DrawerRegistry([app])
        with pytest.raises(ValueError, match="Invalid DrawerScreen: invalid_screen"):
            registry.get_screen("app", "invalid_screen")

    def test_registry_with_duplicate_apps(self):
        """Test that registry overwrites duplicate apps (last one wins)."""
        app1 = DrawerApp(
            value="app",
            label="App 1",
            screens={},
        )
        app2 = DrawerApp(
            value="app",
            label="App 2",
            screens={},
        )
        registry = DrawerRegistry([app1, app2])
        # Last app should win
        retrieved_app = registry.get_app("app")
        assert retrieved_app.label == "App 2"

    def test_registry_multiple_screens(self):
        """Test registry with app containing multiple screens."""
        screens = {
            "screen1": DrawerScreen(
                value="screen1",
                screen_type="external",
                label="Screen 1",
            ),
            "screen2": DrawerScreen(
                value="screen2",
                screen_type="internal",
                label="Screen 2",
            ),
            "screen3": DrawerScreen(
                value="screen3",
                screen_type="external",
                label="Screen 3",
                is_active=False,
            ),
        }
        app = DrawerApp(
            value="app",
            label="App",
            screens=screens,
        )
        registry = DrawerRegistry([app])
        assert registry.get_screen("app", "screen1").value == "screen1"
        assert registry.get_screen("app", "screen2").value == "screen2"
        assert registry.get_screen("app", "screen3").value == "screen3"
        assert registry.get_screen("app", "screen3").is_active is False

