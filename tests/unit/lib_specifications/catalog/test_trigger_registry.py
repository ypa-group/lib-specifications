"""Tests for default trigger registry."""

import pytest

from lib_specifications.catalog.trigger_registry import TRIGGER_REGISTRY
from lib_specifications.catalog.trigger_registry.budget import BUDGET
from lib_specifications.catalog.trigger_registry.calculator import CALCULATOR
from lib_specifications.catalog.trigger_registry.contact_us import CONTACT_US
from lib_specifications.catalog.trigger_registry.credit_score import CREDIT_SCORE
from lib_specifications.catalog.trigger_registry.general import GENERAL
from lib_specifications.catalog.trigger_registry.onboarding import ONBOARDING
from lib_specifications.catalog.trigger_registry.timely import TIMELY
from lib_specifications.catalog.trigger_registry.welcome import WELCOME


@pytest.mark.unit
class TestDefaultTriggerRegistry:
    """Tests for default trigger registry."""

    def test_registry_is_initialized(self):
        """Test that trigger_registry is initialized."""
        assert TRIGGER_REGISTRY is not None
        assert hasattr(TRIGGER_REGISTRY, "get_miniapp_by_name")
        assert hasattr(TRIGGER_REGISTRY, "get_all_miniapps")
        assert hasattr(TRIGGER_REGISTRY, "get_trigger_by_fullname")
        assert hasattr(TRIGGER_REGISTRY, "get_all_triggers")

    def test_general_miniapp_registered(self):
        """Test that GENERAL miniapp is registered."""
        assert TRIGGER_REGISTRY.get_miniapp_by_name("GENERAL") == GENERAL
        assert TRIGGER_REGISTRY.GENERAL == GENERAL

    def test_welcome_miniapp_registered(self):
        """Test that WELCOME miniapp is registered."""
        assert TRIGGER_REGISTRY.get_miniapp_by_name("WELCOME") == WELCOME
        assert TRIGGER_REGISTRY.WELCOME == WELCOME

    def test_timely_miniapp_registered(self):
        """Test that TIMELY miniapp is registered."""
        assert TRIGGER_REGISTRY.get_miniapp_by_name("TIMELY") == TIMELY
        assert TRIGGER_REGISTRY.TIMELY == TIMELY

    def test_budget_miniapp_registered(self):
        """Test that BUDGET miniapp is registered."""
        assert TRIGGER_REGISTRY.get_miniapp_by_name("BUDGET") == BUDGET
        assert TRIGGER_REGISTRY.BUDGET == BUDGET

    def test_calculator_miniapp_registered(self):
        """Test that CALCULATOR miniapp is registered."""
        assert TRIGGER_REGISTRY.get_miniapp_by_name("CALCULATOR") == CALCULATOR
        assert TRIGGER_REGISTRY.CALCULATOR == CALCULATOR

    def test_credit_score_miniapp_registered(self):
        """Test that CREDIT_SCORE miniapp is registered."""
        assert TRIGGER_REGISTRY.get_miniapp_by_name("CREDIT_SCORE") == CREDIT_SCORE
        assert TRIGGER_REGISTRY.CREDIT_SCORE == CREDIT_SCORE

    def test_contact_us_miniapp_registered(self):
        """Test that CONTACT_US miniapp is registered."""
        assert TRIGGER_REGISTRY.get_miniapp_by_name("CONTACT_US") == CONTACT_US
        assert TRIGGER_REGISTRY.CONTACT_US == CONTACT_US

    def test_onboarding_miniapp_registered(self):
        """Test that ONBOARDING miniapp is registered."""
        assert TRIGGER_REGISTRY.get_miniapp_by_name("ONBOARDING") == ONBOARDING
        assert TRIGGER_REGISTRY.ONBOARDING == ONBOARDING

    def test_all_miniapps_registered(self):
        """Test that all miniapps are registered."""
        expected_miniapps = {
            "GENERAL": GENERAL,
            "WELCOME": WELCOME,
            "TIMELY": TIMELY,
            "BUDGET": BUDGET,
            "CALCULATOR": CALCULATOR,
            "CREDIT_SCORE": CREDIT_SCORE,
            "CONTACT_US": CONTACT_US,
            "ONBOARDING": ONBOARDING,
        }

        for name, miniapp in expected_miniapps.items():
            assert TRIGGER_REGISTRY.get_miniapp_by_name(name) == miniapp, f"{name} should be registered"
            assert getattr(TRIGGER_REGISTRY, name) == miniapp, f"{name} should be accessible as attribute"

    def test_get_all_miniapps(self):
        """Test that get_all_miniapps returns all registered miniapps."""
        all_miniapps = TRIGGER_REGISTRY.get_all_miniapps()
        assert len(all_miniapps) == 8

        miniapp_names = {miniapp.name for miniapp in all_miniapps}
        expected_names = {
            "GENERAL",
            "WELCOME",
            "TIMELY",
            "BUDGET",
            "CALCULATOR",
            "CREDIT_SCORE",
            "CONTACT_US",
            "ONBOARDING",
        }
        assert miniapp_names == expected_names

    def test_get_all_triggers(self):
        """Test that get_all_triggers returns all triggers from all miniapps."""
        all_triggers = TRIGGER_REGISTRY.get_all_triggers()
        assert len(all_triggers) > 0

        # Check that triggers have fullname format
        for trigger in all_triggers:
            assert "__" in trigger.fullname
            assert trigger.mini_app.name in trigger.fullname
            assert trigger.qualname in trigger.fullname
