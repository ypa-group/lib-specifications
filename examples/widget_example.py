"""Example demonstrating widget usage with context data population.

This example shows:
1. How to create widgets of different types
2. How widgets are populated with context data
3. How to use both path-based and literal parameter values
"""

import sys
from pathlib import Path
from uuid import uuid4

# Add project root to Python path so examples can import from lib_specifications
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from lib_specifications.core.parameters import ParameterTypeEnum  # noqa: E402
from lib_specifications.core.widgets import (  # noqa: E402
    CreditScoreValueWidget,
    LanguageSelectorWidget,
)


def example_language_selector_widget():
    """Example: Simple language selector widget."""
    print("=" * 80)
    print("EXAMPLE 1: Language Selector Widget")
    print("=" * 80)

    widget = LanguageSelectorWidget(
        id=uuid4(),
    )

    # Language selector doesn't need context data
    context = {}
    result = widget.populate_widget(context)

    print(f"Widget ID: {result['id']}")
    print(f"Widget Type: {result['widget_type']}")
    print(f"Is Active: {result['is_active']}")
    print(f"Is Deprecated: {result['is_deprecated']}")
    print()


def example_credit_score_widget_with_context():
    """Example: Credit score widget populated from context data."""
    print("=" * 80)
    print("EXAMPLE 2: Credit Score Widget with Context Data (Path-based)")
    print("=" * 80)

    widget = CreditScoreValueWidget(
        id=uuid4(),
        score_value=0,  # Will be populated from context
        params={
            "current_score_value": {
                "parameter_type": "path",
                "data_type": ParameterTypeEnum.INT.label,
                "value": "user.credit_score.current",
            },
            "previous_score_value": {
                "parameter_type": "path",
                "data_type": ParameterTypeEnum.INT.label,
                "value": "user.credit_score.previous",
            },
        },
    )

    # Context data structure
    context = {
        "user": {
            "id": "user_123",
            "name": "John Doe",
            "credit_score": {
                "current": 720,
                "previous": 680,
                "updated_at": "2024-01-15",
            },
        },
        "metadata": {
            "source": "credit_bureau",
        },
    }

    result = widget.populate_widget(context)

    print(f"Widget ID: {result['id']}")
    print(f"Widget Type: {result['widget_type']}")
    print(f"Score Value: {result['score_value']} (from context: user.credit_score.current)")
    print(f"Score Color Zone: {result['score_color_zone']} (calculated from score)")
    print(f"Trend: {result['trend']} (720 > 680)")
    print()
    print("Context Data Used:")
    print(f"  - user.credit_score.current: {context['user']['credit_score']['current']}")
    print(f"  - user.credit_score.previous: {context['user']['credit_score']['previous']}")
    print()


def example_credit_score_widget_with_literals():
    """Example: Credit score widget with literal parameter values."""
    print("=" * 80)
    print("EXAMPLE 3: Credit Score Widget with Literal Values")
    print("=" * 80)

    widget = CreditScoreValueWidget(
        id=uuid4(),
        score_value=0,
        params={
            "current_score_value": {
                "parameter_type": "value",
                "data_type": ParameterTypeEnum.INT.label,
                "value": 650,  # Literal value
            },
            "previous_score_value": {
                "parameter_type": "value",
                "data_type": ParameterTypeEnum.INT.label,
                "value": 700,  # Literal value
            },
        },
    )

    # No context needed when using literal values
    context = {}
    result = widget.populate_widget(context)

    print(f"Score Value: {result['score_value']} (literal: 650)")
    print(f"Score Color Zone: {result['score_color_zone']} (fair: 580-669)")
    print(f"Trend: {result['trend']} (down: 650 < 700)")
    print()


def example_credit_score_widget_mixed():
    """Example: Credit score widget with mixed path and literal parameters."""
    print("=" * 80)
    print("EXAMPLE 4: Credit Score Widget with Mixed Parameters")
    print("=" * 80)

    widget = CreditScoreValueWidget(
        id=uuid4(),
        score_value=0,
        params={
            "current_score_value": {
                "parameter_type": "path",  # From context
                "data_type": ParameterTypeEnum.INT.label,
                "value": "credit.current",
            },
            "previous_score_value": {
                "parameter_type": "value",  # Literal
                "data_type": ParameterTypeEnum.INT.label,
                "value": 600,
            },
        },
    )

    context = {
        "credit": {
            "current": 800,
            "provider": "Experian",
        },
    }

    result = widget.populate_widget(context)

    print(f"Score Value: {result['score_value']} (from context: credit.current = 800)")
    print("Previous Score: 600 (literal value)")
    print(f"Score Color Zone: {result['score_color_zone']} (excellent: 800-850)")
    print(f"Trend: {result['trend']} (up: 800 > 600)")
    print()


def example_all_score_zones():
    """Example: Demonstrating all credit score color zones."""
    print("=" * 80)
    print("EXAMPLE 5: All Credit Score Color Zones")
    print("=" * 80)

    test_scores = [
        (400, "poor"),
        (600, "fair"),
        (700, "good"),
        (750, "very good"),
        (820, "excellent"),
    ]

    for score, expected_zone in test_scores:
        widget = CreditScoreValueWidget(
            id=uuid4(),
            score_value=score,
            params={
                "current_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": score,
                },
                "previous_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": score - 50,
                },
            },
        )

        result = widget.populate_widget({})
        print(f"Score {score:3d} -> Zone: {result['score_color_zone']:12s} (expected: {expected_zone})")
    print()


def main():
    """Run all widget examples."""
    print("\n" + "=" * 80)
    print("WIDGET EXAMPLES: Context Data Population")
    print("=" * 80 + "\n")

    example_language_selector_widget()
    example_credit_score_widget_with_context()
    example_credit_score_widget_with_literals()
    example_credit_score_widget_mixed()
    example_all_score_zones()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("""
Widgets can be configured via UI with:
1. Widget type selection (e.g., "credit_score_value", "language_selector")
2. Parameter configuration:
   - parameter_type: "path" (extract from context) or "value" (literal)
   - data_type: The data type (int, str, etc.)
   - value: Either a dot-notation path (e.g., "user.credit_score.current")
            or a literal value (e.g., 650)

When populate_widget(context) is called:
- Path parameters extract values from the context dictionary using dot notation
- Literal parameters use their fixed values
- Widget-specific logic calculates derived values (e.g., color zones, trends)
- Returns a dictionary ready for UI consumption
    """)


if __name__ == "__main__":
    main()
