"""Tests for drawer pydantic models."""

import pytest
from pydantic import ValidationError

from lib_specifications.core import DrawerApp, DrawerScreen, DrawerScreenOption
from lib_specifications.pydantic_models import (
    PydanticDrawerApp,
    PydanticDrawerOption,
    PydanticDrawerScreen,
)


@pytest.mark.unit
class TestPydanticDrawerOption:
    """Tests for PydanticDrawerOption."""

    def test_create_from_dict(self):
        """Test creating PydanticDrawerOption from dict."""
        data = {
            "value": "option1",
            "label": "Option 1",
        }
        option = PydanticDrawerOption.model_validate(data)
        assert option.value == "option1"
        assert option.label == "Option 1"

    def test_create_from_attributes(self):
        """Test creating PydanticDrawerOption from attributes."""
        drawer_option = DrawerScreenOption(value="option1", label="Option 1")
        option = PydanticDrawerOption.model_validate(drawer_option, from_attributes=True)
        assert option.value == "option1"
        assert option.label == "Option 1"

    def test_serialization_to_dict(self):
        """Test serializing PydanticDrawerOption to dict."""
        option = PydanticDrawerOption(value="option1", label="Option 1")
        result = option.model_dump()
        assert result == {
            "value": "option1",
            "label": "Option 1",
        }

    def test_serialization_to_json(self):
        """Test serializing PydanticDrawerOption to JSON."""
        option = PydanticDrawerOption(value="option1", label="Option 1")
        result = option.model_dump(mode="json")
        assert result["value"] == "option1"
        assert result["label"] == "Option 1"

    def test_missing_required_fields(self):
        """Test that missing required fields raises ValidationError."""
        with pytest.raises(ValidationError):
            PydanticDrawerOption.model_validate({"value": "option1"})
        with pytest.raises(ValidationError):
            PydanticDrawerOption.model_validate({"label": "Option 1"})


@pytest.mark.unit
class TestPydanticDrawerScreen:
    """Tests for PydanticDrawerScreen."""

    def test_create_from_dict_minimal(self):
        """Test creating PydanticDrawerScreen from dict with minimal fields."""
        data = {
            "value": "screen1",
            "type": "external",
            "label": "Screen 1",
        }
        screen = PydanticDrawerScreen.model_validate(data)
        assert screen.value == "screen1"
        assert screen.type == "external"
        assert screen.label == "Screen 1"
        assert screen.is_active is True  # Default value
        assert screen.options is None  # Default value

    def test_create_from_dict_with_all_fields(self):
        """Test creating PydanticDrawerScreen from dict with all fields."""
        data = {
            "value": "screen1",
            "type": "internal",
            "label": "Screen 1",
            "is_active": False,
            "options": [
                {"value": "opt1", "label": "Option 1"},
                {"value": "opt2", "label": "Option 2"},
            ],
        }
        screen = PydanticDrawerScreen.model_validate(data)
        assert screen.value == "screen1"
        assert screen.type == "internal"
        assert screen.label == "Screen 1"
        assert screen.is_active is False
        assert screen.options is not None
        assert len(screen.options) == 2
        assert screen.options[0].value == "opt1"
        assert screen.options[1].value == "opt2"

    def test_create_from_dict_with_screen_type_alias(self):
        """Test creating PydanticDrawerScreen with screen_type alias."""
        data = {
            "value": "screen1",
            "screen_type": "external",  # Using alias
            "label": "Screen 1",
        }
        screen = PydanticDrawerScreen.model_validate(data)
        assert screen.type == "external"

    def test_create_from_attributes(self):
        """Test creating PydanticDrawerScreen from attributes."""
        drawer_screen = DrawerScreen(
            value="screen1",
            screen_type="external",
            label="Screen 1",
            is_active=False,
        )
        screen = PydanticDrawerScreen.model_validate(drawer_screen, from_attributes=True)
        assert screen.value == "screen1"
        assert screen.type == "external"
        assert screen.label == "Screen 1"
        assert screen.is_active is False

    def test_create_from_attributes_with_options(self):
        """Test creating PydanticDrawerScreen from attributes with options."""
        options = [
            DrawerScreenOption(value="opt1", label="Option 1"),
            DrawerScreenOption(value="opt2", label="Option 2"),
        ]
        drawer_screen = DrawerScreen(
            value="screen1",
            screen_type="internal",
            label="Screen 1",
            options=options,
        )
        screen = PydanticDrawerScreen.model_validate(drawer_screen, from_attributes=True)
        assert screen.options is not None
        assert len(screen.options) == 2
        assert screen.options[0].value == "opt1"
        assert screen.options[1].value == "opt2"

    def test_validate_options_from_strings(self):
        """Test that options validator converts strings to PydanticDrawerOption."""
        data = {
            "value": "screen1",
            "type": "external",
            "label": "Screen 1",
            "options": ["option1", "option2"],  # List of strings
        }
        screen = PydanticDrawerScreen.model_validate(data)
        assert screen.options is not None
        assert len(screen.options) == 2
        assert screen.options[0].value == "option1"
        assert screen.options[0].label == "option1"
        assert screen.options[1].value == "option2"
        assert screen.options[1].label == "option2"

    def test_validate_options_from_dicts(self):
        """Test that options validator handles list of dicts."""
        data = {
            "value": "screen1",
            "type": "external",
            "label": "Screen 1",
            "options": [
                {"value": "opt1", "label": "Option 1"},
                {"value": "opt2", "label": "Option 2"},
            ],
        }
        screen = PydanticDrawerScreen.model_validate(data)
        assert screen.options is not None
        assert len(screen.options) == 2

    def test_serialization_to_dict(self):
        """Test serializing PydanticDrawerScreen to dict."""
        screen = PydanticDrawerScreen(
            value="screen1",
            type="external",
            label="Screen 1",
            is_active=False,
        )
        result = screen.model_dump()
        assert result["value"] == "screen1"
        assert result["type"] == "external"
        assert result["label"] == "Screen 1"
        assert result["is_active"] is False
        assert result["options"] is None

    def test_serialization_with_options(self):
        """Test serializing PydanticDrawerScreen with options."""
        options = [
            PydanticDrawerOption(value="opt1", label="Option 1"),
            PydanticDrawerOption(value="opt2", label="Option 2"),
        ]
        screen = PydanticDrawerScreen(
            value="screen1",
            type="external",
            label="Screen 1",
            options=options,
        )
        result = screen.model_dump()
        assert result["options"] is not None
        assert len(result["options"]) == 2
        assert result["options"][0]["value"] == "opt1"

    def test_invalid_screen_type(self):
        """Test that invalid screen_type raises ValidationError."""
        data = {
            "value": "screen1",
            "type": "invalid_type",
            "label": "Screen 1",
        }
        with pytest.raises(ValidationError):
            PydanticDrawerScreen.model_validate(data)

    def test_missing_required_fields(self):
        """Test that missing required fields raises ValidationError."""
        with pytest.raises(ValidationError):
            PydanticDrawerScreen.model_validate({"value": "screen1"})
        with pytest.raises(ValidationError):
            PydanticDrawerScreen.model_validate({"type": "external"})


@pytest.mark.unit
class TestPydanticDrawerApp:
    """Tests for PydanticDrawerApp."""

    def test_create_from_dict(self):
        """Test creating PydanticDrawerApp from dict."""
        data = {
            "value": "app",
            "label": "App",
            "screens": [
                {
                    "value": "screen1",
                    "type": "external",
                    "label": "Screen 1",
                },
                {
                    "value": "screen2",
                    "type": "internal",
                    "label": "Screen 2",
                },
            ],
        }
        app = PydanticDrawerApp.model_validate(data)
        assert app.value == "app"
        assert app.label == "App"
        assert len(app.screens) == 2
        assert app.screens[0].value == "screen1"
        assert app.screens[1].value == "screen2"

    def test_create_from_attributes(self):
        """Test creating PydanticDrawerApp from attributes."""
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
        drawer_app = DrawerApp(
            value="app",
            label="App",
            screens=screens,
        )
        app = PydanticDrawerApp.model_validate(drawer_app, from_attributes=True)
        assert app.value == "app"
        assert app.label == "App"
        assert len(app.screens) == 2
        # Screens are converted from dict to list
        screen_values = {screen.value for screen in app.screens}
        assert "screen1" in screen_values
        assert "screen2" in screen_values

    def test_validate_screens_from_strings(self):
        """Test that screens validator converts strings to PydanticDrawerScreen."""
        data = {
            "value": "app",
            "label": "App",
            "screens": ["screen1", "screen2"],  # List of strings
        }
        app = PydanticDrawerApp.model_validate(data)
        assert len(app.screens) == 2
        assert app.screens[0].value == "screen1"
        assert app.screens[0].type == "external"  # Validator uses "external" as default type
        assert app.screens[0].label == "screen1"
        assert app.screens[1].value == "screen2"
        assert app.screens[1].type == "external"

    def test_validate_screens_from_dicts(self):
        """Test that screens validator handles list of dicts."""
        data = {
            "value": "app",
            "label": "App",
            "screens": [
                {
                    "value": "screen1",
                    "type": "external",
                    "label": "Screen 1",
                },
            ],
        }
        app = PydanticDrawerApp.model_validate(data)
        assert len(app.screens) == 1
        assert app.screens[0].value == "screen1"

    def test_serialization_to_dict(self):
        """Test serializing PydanticDrawerApp to dict."""
        screens = [
            PydanticDrawerScreen(
                value="screen1",
                type="external",
                label="Screen 1",
            ),
            PydanticDrawerScreen(
                value="screen2",
                type="internal",
                label="Screen 2",
            ),
        ]
        app = PydanticDrawerApp(
            value="app",
            label="App",
            screens=screens,
        )
        result = app.model_dump()
        assert result["value"] == "app"
        assert result["label"] == "App"
        assert len(result["screens"]) == 2
        assert result["screens"][0]["value"] == "screen1"
        assert result["screens"][1]["value"] == "screen2"

    def test_serialization_to_json(self):
        """Test serializing PydanticDrawerApp to JSON."""
        screens = [
            PydanticDrawerScreen(
                value="screen1",
                type="external",
                label="Screen 1",
            ),
        ]
        app = PydanticDrawerApp(
            value="app",
            label="App",
            screens=screens,
        )
        result = app.model_dump(mode="json")
        assert result["value"] == "app"
        assert result["label"] == "App"
        assert isinstance(result["screens"], list)

    def test_missing_required_fields(self):
        """Test that missing required fields raises ValidationError."""
        with pytest.raises(ValidationError):
            PydanticDrawerApp.model_validate({"value": "app"})
        with pytest.raises(ValidationError):
            PydanticDrawerApp.model_validate({"label": "App"})
        with pytest.raises(ValidationError):
            PydanticDrawerApp.model_validate({"value": "app", "label": "App"})

    def test_empty_screens(self):
        """Test PydanticDrawerApp with empty screens list."""
        app = PydanticDrawerApp(
            value="app",
            label="App",
            screens=[],
        )
        assert len(app.screens) == 0

    def test_complex_app_with_options(self):
        """Test PydanticDrawerApp with screens containing options."""
        screens = [
            PydanticDrawerScreen(
                value="screen1",
                type="external",
                label="Screen 1",
                options=[
                    PydanticDrawerOption(value="opt1", label="Option 1"),
                    PydanticDrawerOption(value="opt2", label="Option 2"),
                ],
            ),
        ]
        app = PydanticDrawerApp(
            value="app",
            label="App",
            screens=screens,
        )
        assert len(app.screens) == 1
        assert app.screens[0].options is not None
        assert len(app.screens[0].options) == 2
