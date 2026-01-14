import asyncio
import sys
from datetime import date, timedelta
from pathlib import Path

# Add project root to Python path so examples can import from lib_specifications
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import lib_specifications.catalog.callback_registry as callback_registry  # noqa: E402
import lib_specifications.specifications as specs  # noqa: E402

# Complex 4-level nested specification for "should_user_buy_a_milk"
# Level 1: AND
#   Level 2 (left): NOT
#     Level 3: OR
#       Level 4 (left): Field spec (user.has_milk == True)
#       Level 4 (right): Callback spec (isToday(user.last_milk_purchase_date))
#   Level 2 (right): AND
#     Level 3 (left): OR
#       Level 4 (left): Field spec (user.age >= 18)
#       Level 4 (right): Field spec (user.has_parent_permission == True)
#     Level 3 (right): OR
#       Level 4 (left): Field spec (user.money >= milk.price)
#       Level 4 (right): Callback spec (isWithinDays(user.last_milk_purchase_date, 7))
should_user_buy_a_milk = {
    "type": "and",
    "left": {
        "type": "not",
        "child": {
            "type": "or",
            "left": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.has_milk",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": "bool",
                    "value": True,
                },
            },
            "right": {
                "type": "leaf",
                "subtype": "callback",
                "name": "isToday",
                "params": {
                    "dt": {
                        "parameter_type": "path",
                        "data_type": "date",
                        "value": "user.last_milk_purchase_date",
                    },
                },
            },
        },
    },
    "right": {
        "type": "and",
        "left": {
            "type": "or",
            "left": {
                "type": "leaf",
                "subtype": "field",
                "name": "greater_than_or_equal",
                "field": "user.age",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": "int",
                    "value": 18,
                },
            },
            "right": {
                "type": "leaf",
                "subtype": "field",
                "name": "equal",
                "field": "user.has_parent_permission",
                "compare_to": {
                    "parameter_type": "value",
                    "data_type": "bool",
                    "value": True,
                },
            },
        },
        "right": {
            "type": "or",
            "left": {
                "type": "leaf",
                "subtype": "field",
                "name": "greater_than_or_equal",
                "field": "user.money",
                "compare_to": {
                    "parameter_type": "path",
                    "data_type": "float",
                    "value": "milk.price",
                },
            },
            "right": {
                "type": "leaf",
                "subtype": "callback",
                "name": "isWithinDays",
                "params": {
                    "dt": {
                        "parameter_type": "path",
                        "data_type": "date",
                        "value": "user.last_milk_purchase_date",
                    },
                    "days": {
                        "parameter_type": "value",
                        "data_type": "int",
                        "value": 7,
                    },
                },
            },
        },
    },
}


async def main():
    # Test data for evaluation
    today = date.today()
    data = {
        "user": {
            "age": 20,
            "has_milk": False,
            "has_parent_permission": False,
            "money": 2.5,
            "last_milk_purchase_date": today - timedelta(days=10),
        },
        "milk": {
            "price": 3.0,
        },
    }

    await callback_registry.CALLBACK_REGISTRY.load()

    # Build the specification
    builder = specs.SpecificationBuilder(callback_registry.CALLBACK_REGISTRY)
    spec = builder.build(should_user_buy_a_milk)

    # Describe the specification
    print("=" * 80)
    print("SPECIFICATION DESCRIPTION:")
    print("=" * 80)
    print(spec.describe())
    print()

    # Evaluate the specification
    evaluator = specs.SpecificationEvaluator(callback_registry.CALLBACK_REGISTRY)
    result = await evaluator.evaluate(spec, data)

    print("=" * 80)
    print("EVALUATION RESULT:")
    print("=" * 80)
    print(f"Should user buy a milk? {result}")
    print()

    # Print test data for reference
    print("=" * 80)
    print("TEST DATA:")
    print("=" * 80)
    print(f"User age: {data['user']['age']}")
    print(f"User has milk: {data['user']['has_milk']}")
    print(f"User has parent permission: {data['user']['has_parent_permission']}")
    print(f"User money: ${data['user']['money']}")
    print(f"Milk price: ${data['milk']['price']}")
    print(f"Last milk purchase date: {data['user']['last_milk_purchase_date']}")
    print(f"Days since last purchase: {(today - data['user']['last_milk_purchase_date']).days}")


if __name__ == "__main__":
    asyncio.run(main())
