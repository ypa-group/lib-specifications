import asyncio
import sys
from pathlib import Path

# Add project root to Python path so examples can import from lib_specifications
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import lib_specifications.catalog.callback_registry as callback_registry  # noqa: E402
import lib_specifications.core as specs  # noqa: E402

should_user_be_arrested = {
    "type": "and",
    "left": {
        "type": "or",
        "left": {
            "type": "leaf",
            "subtype": "field",
            "name": "greater_than_or_equal",
            "field": "user.age",
            "compare_to": {
                "parameter_type": "path",
                "data_type": "int",
                "value": "country.age_of_majority",
            },
        },
        "right": {
            "type": "leaf",
            "subtype": "field",
            "name": "equal",
            "field": "user.country",
            "compare_to": {
                "parameter_type": "value",
                "data_type": "str",
                "value": "YOU*SHOULD*HAVE*THOUGHT*ABOUT*CONSEQUENCES*KID_COUNTRY",
            },
        },
    },
    "right": {
        "type": "leaf",
        "subtype": "field",
        "name": "equal",
        "field": "user.is_criminal",
        "compare_to": {
            "parameter_type": "value",
            "data_type": "bool",
            "value": True,
        },
    },
}


async def main():
    data = {
        "user": {
            "age": 15,
            "country": "UK",
            "is_criminal": True,
        },
        "country": {
            "age_of_majority": 18,
        },
    }
    builder = specs.SpecificationBuilder(callback_registry.CALLBACK_REGISTRY)
    spec = builder.build(should_user_be_arrested)
    print(spec.describe())
    evaluator = specs.SpecificationEvaluator(callback_registry.CALLBACK_REGISTRY)
    result = await evaluator.evaluate(spec, data)
    print("Should user be arrested?", result)


if __name__ == "__main__":
    asyncio.run(main())
