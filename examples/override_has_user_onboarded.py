"""Example: Override HasOnboarded callback to call an API service.

This example demonstrates how to override the abstract HasOnboarded callback
with a concrete implementation
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path so examples can import from lib_specifications
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


import lib_specifications.core as specs  # noqa: E402
from lib_specifications.catalog.callback_registry import CALLBACK_REGISTRY, HasOnboardedCallback  # noqa: E402


class RealHasOnboardedCallback(HasOnboardedCallback):
    """Concrete implementation of HasOnboardedCallback."""

    async def __call__(self) -> bool:
        await asyncio.sleep(1)
        print(f"We still await for user {self.auth_provider_user_id}...")
        await asyncio.sleep(1)
        print(f"We still await for user {self.auth_provider_user_id}...")
        await asyncio.sleep(1)
        print(f"We still await for user {self.auth_provider_user_id}...")
        return True


# Specification that uses the hasUserOnboarded callback
should_user_access_feature = {
    "type": "and",
    "left": {
        "type": "leaf",
        "subtype": "field",
        "name": "equal",
        "field": "user.is_premium",
        "compare_to": {
            "parameter_type": "value",
            "data_type": "bool",
            "value": True,
        },
    },
    "right": {
        "type": "leaf",
        "subtype": "callback",
        "name": "hasOnboarded",
        "params": {
            "auth_provider": {
                "parameter_type": "path",
                "data_type": "str",
                "value": "user.auth_provider",
            },
            "auth_provider_user_id": {
                "parameter_type": "path",
                "data_type": "str",
                "value": "user.auth_provider_user_id",
            },
        },
    },
}


async def main():
    """Main function to demonstrate the overridden callback."""

    # Override the hasOnboarded callback with real implementation
    # Note: The registry allows overriding abstract callbacks with concrete implementations
    CALLBACK_REGISTRY.override(RealHasOnboardedCallback)

    # Test data for evaluation
    data = {
        "user": {
            "is_premium": True,
            "auth_provider": "google",
            "auth_provider_user_id": "user123",
        },
    }

    # Build the specification
    builder = specs.SpecificationBuilder(CALLBACK_REGISTRY)
    spec = builder.build(should_user_access_feature)

    # Describe the specification
    print("=" * 80)
    print("SPECIFICATION DESCRIPTION:")
    print("=" * 80)
    print(spec.describe())
    print()

    # Evaluate the specification
    # Note: The evaluator needs to handle async callbacks
    evaluator = specs.SpecificationEvaluator(CALLBACK_REGISTRY)
    result = await evaluator.evaluate(spec, data)

    print("=" * 80)
    print("EVALUATION RESULT:")
    print("=" * 80)
    print(f"Should user access feature? {result}")
    print()

    # Print test data for reference
    print("=" * 80)
    print("TEST DATA:")
    print("=" * 80)
    print(f"User is premium: {data['user']['is_premium']}")
    print(f"Auth provider: {data['user']['auth_provider']}")
    print(f"Auth provider user ID: {data['user']['auth_provider_user_id']}")
    print()

    # Test with different user IDs to show the API callback in action
    print("=" * 80)
    print("TESTING WITH DIFFERENT USER IDs:")
    print("=" * 80)
    for user_id in ["user123", "user456", "user789"]:
        data["user"]["auth_provider_user_id"] = user_id
        result = await evaluator.evaluate(spec, data)
        print(f"User ID: {user_id} -> Access granted: {result}")


if __name__ == "__main__":
    asyncio.run(main())
