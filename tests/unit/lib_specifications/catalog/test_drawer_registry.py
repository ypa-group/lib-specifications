"""Tests for drawer registry catalog."""

import pytest

from lib_specifications.catalog.drawer_registry import DRAWER_REGISTRY
from lib_specifications.core import DrawerScreen


@pytest.mark.unit
class TestDrawerRegistryCatalog:
    """Tests for the default drawer registry catalog."""

    def test_registry_is_initialized(self):
        """Test that DRAWER_REGISTRY is initialized."""
        assert DRAWER_REGISTRY is not None
        assert hasattr(DRAWER_REGISTRY, "apps")
        assert hasattr(DRAWER_REGISTRY, "get_app")
        assert hasattr(DRAWER_REGISTRY, "get_screen")

    def test_registry_has_apps(self):
        """Test that registry contains apps."""
        assert len(DRAWER_REGISTRY.apps) > 0

    def test_app_drawer_registered(self):
        """Test that app drawer is registered."""
        assert "app" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("app")
        assert app.value == "app"
        assert app.label == "App"

    def test_faq_drawer_registered(self):
        """Test that FAQ drawer is registered."""
        assert "faq" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("faq")
        assert app.value == "faq"
        assert app.label == "FAQ"

    def test_contact_us_drawer_registered(self):
        """Test that contact_us drawer is registered."""
        assert "contact_us" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("contact_us")
        assert app.value == "contact_us"
        assert app.label == "Contact Us"

    def test_modals_drawer_registered(self):
        """Test that modals drawer is registered."""
        assert "modals" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("modals")
        assert app.value == "modals"
        assert app.label == "Modals"

    def test_onboarding_drawer_registered(self):
        """Test that onboarding drawer is registered."""
        assert "onboarding" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("onboarding")
        assert app.value == "onboarding"
        assert app.label == "Onboarding"

    def test_pro_features_drawer_registered(self):
        """Test that pro_features drawer is registered."""
        assert "pro_features" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("pro_features")
        assert app.value == "pro_features"
        assert app.label == "Pro Features"

    def test_ypiqs_drawer_registered(self):
        """Test that ypiqs drawer is registered."""
        assert "ypiqs" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("ypiqs")
        assert app.value == "ypiqs"
        assert app.label == "YPIQS"

    def test_array_drawer_registered(self):
        """Test that array drawer is registered."""
        assert "array" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("array")
        assert app.value == "array"
        assert app.label == "Array"

    def test_assistant_corporation_drawer_registered(self):
        """Test that assistant_corporation drawer is registered."""
        assert "assistant_corporation" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("assistant_corporation")
        assert app.value == "assistant_corporation"
        assert app.label == "Assistant Corporation"

    def test_budget_drawer_registered(self):
        """Test that budget drawer is registered."""
        assert "budget" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("budget")
        assert app.value == "budget"
        assert app.label == "Budget"

    def test_calculator_drawer_registered(self):
        """Test that calculator drawer is registered."""
        assert "calculator" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("calculator")
        assert app.value == "calculator"
        assert app.label == "Calculator"

    def test_credit_score_drawer_registered(self):
        """Test that credit_score drawer is registered."""
        assert "credit_score" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("credit_score")
        assert app.value == "credit_score"
        assert app.label == "Credit Score"

    def test_plaid_drawer_registered(self):
        """Test that plaid drawer is registered."""
        assert "plaid" in DRAWER_REGISTRY.apps
        app = DRAWER_REGISTRY.get_app("plaid")
        assert app.value == "plaid"
        assert app.label == "Plaid"

    def test_app_drawer_screens(self):
        """Test app drawer screens."""
        app = DRAWER_REGISTRY.get_app("app")
        assert "app_registration_login" in app.screens
        assert "app_forced_update_required" in app.screens
        screen = DRAWER_REGISTRY.get_screen("app", "app_registration_login")
        assert screen.value == "app_registration_login"
        assert screen.screen_type == "external"
        assert screen.label == "App Registration Login"

    def test_faq_drawer_screens(self):
        """Test FAQ drawer screens."""
        app = DRAWER_REGISTRY.get_app("faq")
        assert "faq" in app.screens
        screen = DRAWER_REGISTRY.get_screen("faq", "faq")
        assert screen.value == "faq"
        assert screen.screen_type == "external"
        assert screen.label == "FAQ"

    def test_contact_us_drawer_screens(self):
        """Test contact_us drawer screens."""
        app = DRAWER_REGISTRY.get_app("contact_us")
        expected_screens = {"idea", "review", "help", "live_chat"}
        assert set(app.screens.keys()) == expected_screens
        screen = DRAWER_REGISTRY.get_screen("contact_us", "idea")
        assert screen.value == "idea"
        assert screen.screen_type == "external"
        assert screen.label == "Idea"

    def test_modals_drawer_screens(self):
        """Test modals drawer screens."""
        app = DRAWER_REGISTRY.get_app("modals")
        assert "error" in app.screens
        screen = DRAWER_REGISTRY.get_screen("modals", "error")
        assert screen.value == "error"
        assert screen.screen_type == "internal"
        assert screen.label == "Error"

    def test_onboarding_drawer_screens(self):
        """Test onboarding drawer screens."""
        app = DRAWER_REGISTRY.get_app("onboarding")
        assert "age_check" in app.screens
        screen = DRAWER_REGISTRY.get_screen("onboarding", "age_check")
        assert screen.value == "age_check"
        assert screen.screen_type == "internal"
        assert screen.label == "Age Check"

    def test_pro_features_drawer_screens(self):
        """Test pro_features drawer screens."""
        app = DRAWER_REGISTRY.get_app("pro_features")
        expected_screens = {
            "freezing_question_mark",
            "data_frozen_question_mark",
            "pro_freezing_in_5_days",
            "cancel_pro_reasons",
            "short_description",
            "subscription_free_period_ends",
        }
        assert set(app.screens.keys()) == expected_screens
        # Test active screen
        screen = DRAWER_REGISTRY.get_screen("pro_features", "short_description")
        assert screen.is_active is True
        # Test inactive screen
        screen = DRAWER_REGISTRY.get_screen("pro_features", "freezing_question_mark")
        assert screen.is_active is False

    def test_ypiqs_drawer_screens(self):
        """Test ypiqs drawer screens."""
        app = DRAWER_REGISTRY.get_app("ypiqs")
        expected_screens = {"main", "question_mark"}
        assert set(app.screens.keys()) == expected_screens
        screen = DRAWER_REGISTRY.get_screen("ypiqs", "main")
        assert screen.value == "main"
        assert screen.screen_type == "external"
        assert screen.label == "Main"

    def test_array_drawer_screens(self):
        """Test array drawer screens."""
        app = DRAWER_REGISTRY.get_app("array")
        expected_screens = {
            "ssn_info",
            "preverification_info",
            "security_info",
            "registration",
            "component_auth_start",
            "create_credit_history",
            "failed_data",
        }
        assert set(app.screens.keys()) == expected_screens
        screen = DRAWER_REGISTRY.get_screen("array", "registration")
        assert screen.value == "registration"
        assert screen.screen_type == "external"
        assert screen.label == "Registration"

    def test_assistant_corporation_drawer_screens(self):
        """Test assistant_corporation drawer screens."""
        app = DRAWER_REGISTRY.get_app("assistant_corporation")
        expected_screens = {"question_mark", "main", "demo", "decore"}
        assert set(app.screens.keys()) == expected_screens
        screen = DRAWER_REGISTRY.get_screen("assistant_corporation", "main")
        assert screen.value == "main"
        assert screen.screen_type == "external"
        assert screen.label == "Main"

    def test_budget_drawer_screens(self):
        """Test budget drawer screens."""
        app = DRAWER_REGISTRY.get_app("budget")
        expected_screens = {"question_mark", "main", "categories", "disable_btn", "demo"}
        assert set(app.screens.keys()) == expected_screens
        screen = DRAWER_REGISTRY.get_screen("budget", "main")
        assert screen.value == "main"
        assert screen.screen_type == "external"
        assert screen.label == "Main"

    def test_calculator_drawer_screens(self):
        """Test calculator drawer screens."""
        app = DRAWER_REGISTRY.get_app("calculator")
        expected_screens = {"question_mark", "main", "constructor", "disable_btn", "demo"}
        assert set(app.screens.keys()) == expected_screens
        screen = DRAWER_REGISTRY.get_screen("calculator", "constructor")
        assert screen.value == "constructor"
        assert screen.screen_type == "external"
        assert screen.label == "Constructor"

    def test_credit_score_drawer_screens(self):
        """Test credit_score drawer screens."""
        app = DRAWER_REGISTRY.get_app("credit_score")
        expected_screens = {"info", "question_mark", "main", "disable_btn", "demo", "factors"}
        assert set(app.screens.keys()) == expected_screens
        screen = DRAWER_REGISTRY.get_screen("credit_score", "main")
        assert screen.value == "main"
        assert screen.screen_type == "external"
        assert screen.label == "Main"
        # Test screen with options
        factors_screen = DRAWER_REGISTRY.get_screen("credit_score", "factors")
        assert factors_screen.value == "factors"
        assert factors_screen.options is not None
        assert len(factors_screen.options) == 6
        option_values = {opt.value for opt in factors_screen.options}
        assert "payment_history" in option_values
        assert "credit_card_utilization" in option_values

    def test_plaid_drawer_screens(self):
        """Test plaid drawer screens."""
        app = DRAWER_REGISTRY.get_app("plaid")
        expected_screens = {
            "security_info",
            "why_connect_plaid",
            "connection_guide",
            "question_mark",
            "linking_cards",
            "phone_verification",
        }
        assert set(app.screens.keys()) == expected_screens
        screen = DRAWER_REGISTRY.get_screen("plaid", "linking_cards")
        assert screen.value == "linking_cards"
        assert screen.screen_type == "external"
        assert screen.label == "Linking Cards"
        # Test inactive screen
        inactive_screen = DRAWER_REGISTRY.get_screen("plaid", "question_mark")
        assert inactive_screen.is_active is False

    def test_all_apps_have_screens(self):
        """Test that all registered apps have at least one screen."""
        for app_value, app in DRAWER_REGISTRY.apps.items():
            assert len(app.screens) > 0, f"App {app_value} should have at least one screen"
            assert isinstance(app.screens, dict)
            for screen_value, screen in app.screens.items():
                assert isinstance(screen, DrawerScreen)
                assert screen.value == screen_value

    def test_all_screens_have_required_fields(self):
        """Test that all screens have required fields."""
        for app_value, app in DRAWER_REGISTRY.apps.items():
            assert app.value == app_value
            for screen_value, screen in app.screens.items():
                assert screen.value == screen_value
                assert screen.screen_type in ("external", "internal")
                assert isinstance(screen.label, str)
                assert len(screen.label) > 0
                assert isinstance(screen.is_active, bool)

    def test_get_invalid_app_raises_error(self):
        """Test that getting an invalid app raises ValueError."""
        with pytest.raises(ValueError, match="Invalid DrawerAppType"):
            DRAWER_REGISTRY.get_app("invalid_app")

    def test_get_invalid_screen_raises_error(self):
        """Test that getting an invalid screen raises ValueError."""
        with pytest.raises(ValueError, match="Invalid DrawerScreen"):
            DRAWER_REGISTRY.get_screen("app", "invalid_screen")
