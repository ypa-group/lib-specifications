"""Tests for trigger module."""

import pytest

from lib_specifications.core.parameters import ContextSchema, ParameterSchema, ParameterTypeEnum
from lib_specifications.core.trigger import (
    MiniApp,
    Trigger,
    TriggerRegistry,
)


@pytest.mark.unit
class TestMiniApp:
    """Tests for MiniApp dataclass."""

    def test_miniapp_creation_minimal(self):
        """Test creating MiniApp with minimal fields."""
        miniapp = MiniApp(name="test_app")
        assert miniapp.name == "test_app"
        assert miniapp.description is None

    def test_miniapp_creation_full(self):
        """Test creating MiniApp with all fields."""
        miniapp = MiniApp(name="test_app", description="Test application")
        assert miniapp.name == "test_app"
        assert miniapp.description == "Test application"

    def test_miniapp_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="MiniApp name must not be empty"):
            MiniApp(name="")

    def test_miniapp_none_name_raises_error(self):
        """Test that None name raises ValueError."""
        with pytest.raises(ValueError, match="MiniApp name must not be empty"):
            MiniApp(name=None)  # type: ignore

    def test_miniapp_double_underscore_raises_error(self):
        """Test that double underscore in name raises ValueError."""
        with pytest.raises(ValueError, match="MiniApp name must not contain double underscores"):
            MiniApp(name="test__app")

    def test_miniapp_str(self):
        """Test string representation."""
        miniapp = MiniApp(name="test_app")
        assert str(miniapp) == "test_app"

    def test_miniapp_to_dict(self):
        """Test to_dict method."""
        miniapp = MiniApp(name="test_app", description="Test application")
        result = miniapp.to_dict()
        assert result["name"] == "test_app"
        assert result["description"] == "Test application"

    def test_miniapp_to_dict_no_description(self):
        """Test to_dict method without description."""
        miniapp = MiniApp(name="test_app")
        result = miniapp.to_dict()
        assert result["name"] == "test_app"
        assert result["description"] is None


@pytest.mark.unit
class TestTriggerRegistry:
    """Tests for TriggerRegistry (which includes MiniApp management)."""

    def test_registry_creation(self):
        """Test creating a registry."""
        miniapp1 = MiniApp(name="app1")
        miniapp1.register_trigger(qualname="trigger1")
        miniapp2 = MiniApp(name="app2")
        miniapp2.register_trigger(qualname="trigger2")
        registry = TriggerRegistry([miniapp1, miniapp2])
        assert len(registry.get_all_miniapps()) == 2
        assert len(registry.get_all_triggers()) == 2

    def test_registry_get_miniapp_by_name(self):
        """Test getting miniapp by name."""
        miniapp = MiniApp(name="test_app")
        registry = TriggerRegistry([miniapp])
        result = registry.get_miniapp_by_name("test_app")
        assert result == miniapp
        assert result.name == "test_app"

    def test_registry_get_miniapp_by_name_invalid(self):
        """Test getting miniapp by invalid name raises error."""
        miniapp = MiniApp(name="test_app")
        registry = TriggerRegistry([miniapp])
        with pytest.raises(ValueError, match="Invalid MiniApp"):
            registry.get_miniapp_by_name("invalid")

    def test_registry_get_all_miniapps(self):
        """Test getting all miniapps."""
        miniapp1 = MiniApp(name="app1")
        miniapp2 = MiniApp(name="app2")
        registry = TriggerRegistry([miniapp1, miniapp2])
        all_miniapps = registry.get_all_miniapps()
        assert len(all_miniapps) == 2
        assert miniapp1 in all_miniapps
        assert miniapp2 in all_miniapps

    def test_registry_get_all_miniapps_empty(self):
        """Test getting all miniapps from empty registry."""
        registry = TriggerRegistry([])
        assert len(registry.get_all_miniapps()) == 0


@pytest.mark.unit
class TestTrigger:
    """Tests for Trigger dataclass."""

    @pytest.fixture
    def miniapp(self):
        """Create a test MiniApp."""
        return MiniApp(name="test_app")

    def test_trigger_creation_minimal(self, miniapp):
        """Test creating Trigger with minimal fields."""
        trigger = Trigger(mini_app=miniapp, qualname="test_trigger")
        assert trigger.mini_app == miniapp
        assert trigger.qualname == "test_trigger"
        assert trigger.description is None
        assert trigger.context_schema is None
        assert trigger.applicable_specifications is None
        assert trigger.is_deprecated is False

    def test_trigger_creation_full(self, miniapp):
        """Test creating Trigger with all fields."""
        context_schema = ContextSchema(
            parameters={
                "user.id": ParameterSchema(
                    name="user.id",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                )
            }
        )
        trigger = Trigger(
            mini_app=miniapp,
            qualname="test_trigger",
            description="Test trigger",
            context_schema=context_schema,
            applicable_specifications={"spec1", "spec2"},
            is_deprecated=True,
        )
        assert trigger.mini_app == miniapp
        assert trigger.qualname == "test_trigger"
        assert trigger.description == "Test trigger"
        assert trigger.context_schema == context_schema
        assert trigger.applicable_specifications == {"spec1", "spec2"}
        assert trigger.is_deprecated is True

    def test_trigger_empty_qualname_raises_error(self, miniapp):
        """Test that empty qualname raises ValueError."""
        with pytest.raises(ValueError, match="Qualname must not be empty"):
            Trigger(mini_app=miniapp, qualname="")

    def test_trigger_double_underscore_in_qualname_raises_error(self, miniapp):
        """Test that double underscore in qualname raises ValueError."""
        with pytest.raises(ValueError, match="Qualname must not contain double underscores"):
            Trigger(mini_app=miniapp, qualname="test__trigger")

    def test_trigger_fullname(self, miniapp):
        """Test fullname property."""
        trigger = Trigger(mini_app=miniapp, qualname="test_trigger")
        assert trigger.fullname == "test_app__test_trigger"

    def test_trigger_str(self, miniapp):
        """Test string representation."""
        trigger = Trigger(mini_app=miniapp, qualname="test_trigger")
        assert str(trigger) == "test_app__test_trigger"

    def test_trigger_to_dict(self, miniapp):
        """Test to_dict method."""
        context_schema = ContextSchema(
            parameters={
                "user.id": ParameterSchema(
                    name="user.id",
                    data_type=ParameterTypeEnum.INT,
                    required=True,
                )
            }
        )
        trigger = Trigger(
            mini_app=miniapp,
            qualname="test_trigger",
            description="Test trigger",
            context_schema=context_schema,
            applicable_specifications={"spec1", "spec2"},
            is_deprecated=True,
        )
        result = trigger.to_dict()
        assert result["fullname"] == "test_app__test_trigger"
        assert result["qualname"] == "test_trigger"
        assert result["description"] == "Test trigger"
        assert result["is_deprecated"] is True
        assert set(result["applicable_specifications"]) == {"spec1", "spec2"}
        assert result["context_schema"] is not None
        assert "mini_app" in result


@pytest.mark.unit
class TestTriggerRegistryFull:
    """Tests for TriggerRegistry with triggers."""

    @pytest.fixture
    def miniapp1(self):
        """Create first test MiniApp."""
        miniapp = MiniApp(name="app1")
        miniapp.register_trigger(qualname="trigger1")
        miniapp.register_trigger(qualname="trigger2")
        return miniapp

    @pytest.fixture
    def miniapp2(self):
        """Create second test MiniApp."""
        miniapp = MiniApp(name="app2")
        miniapp.register_trigger(qualname="trigger3")
        return miniapp

    def test_registry_creation(self, miniapp1, miniapp2):
        """Test creating a registry."""
        registry = TriggerRegistry([miniapp1, miniapp2])
        assert len(registry.get_all_triggers()) == 3
        assert len(registry.get_all_miniapps()) == 2

    def test_registry_get_trigger_by_fullname(self, miniapp1, miniapp2):
        """Test getting trigger by fullname."""
        registry = TriggerRegistry([miniapp1, miniapp2])
        result = registry.get_trigger_by_fullname("app1__trigger1")
        assert result is not None
        assert result.qualname == "trigger1"
        assert result.mini_app.name == "app1"

    def test_registry_get_trigger_by_fullname_invalid(self, miniapp1):
        """Test getting trigger by invalid fullname raises error."""
        registry = TriggerRegistry([miniapp1])
        with pytest.raises(ValueError, match="Invalid trigger"):
            registry.get_trigger_by_fullname("invalid__trigger")

    def test_registry_get_all_triggers(self, miniapp1, miniapp2):
        """Test getting all triggers."""
        registry = TriggerRegistry([miniapp1, miniapp2])
        all_triggers = registry.get_all_triggers()
        assert len(all_triggers) == 3
        trigger_names = {t.fullname for t in all_triggers}
        assert "app1__trigger1" in trigger_names
        assert "app1__trigger2" in trigger_names
        assert "app2__trigger3" in trigger_names

    def test_registry_get_all_triggers_empty(self):
        """Test getting all triggers from empty registry."""
        registry = TriggerRegistry([])
        assert len(registry.get_all_triggers()) == 0

    def test_registry_get_miniapp_attribute_access(self, miniapp1, miniapp2):
        """Test accessing miniapps as attributes."""
        registry = TriggerRegistry([miniapp1, miniapp2])
        assert registry.app1 == miniapp1
        assert registry.app2 == miniapp2
        with pytest.raises(AttributeError):
            _ = registry.invalid

    def test_registry_get_miniapp_dir(self, miniapp1, miniapp2):
        """Test __dir__ includes miniapp names."""
        registry = TriggerRegistry([miniapp1, miniapp2])
        dir_list = dir(registry)
        assert "app1" in dir_list
        assert "app2" in dir_list


