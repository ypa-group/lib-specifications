# lib-specifications

A specification pattern implementation for Python with full type hint support, tree-based serialization, and async evaluation.

## Features

- **Specification Pattern**: Clean implementation of the Specification pattern for business rules
- **Type Safety**: Full type hints and IDE autocompletion support
- **Tree-Based**: Specifications can be represented as TypedDict trees for serialization
- **Flexible**: Support for field comparisons and callback-based specifications
- **Composable**: Logical operators (AND, OR, NOT) for building complex specifications
- **Async Evaluation**: Async evaluation with lazy evaluation for performance
- **Extensible**: Easy registration of custom operators and callbacks

## Installation

```bash
pip install lib-specifications
```

## Quick Start

### Basic Usage

```python
import asyncio
from lib_specifications.core import (
    FieldSpecification,
    AndSpecification,
    ParameterPathValue,
    SpecificationEvaluator,
    CallbackRegistry,
)
from lib_specifications.core.parameters import ParameterLiteralValue

# Create field specifications
field: ParameterPathValue = {
    "parameter_type": "path",
    "data_type": "int",
    "value": "user.age",
}

compare_to: ParameterLiteralValue = {
    "parameter_type": "value",
    "data_type": "int",
    "value": 18,
}

age_spec = FieldSpecification(field=field, operator="greater_than_or_equal", compare_to=compare_to)

status_field: ParameterPathValue = {
    "parameter_type": "path",
    "data_type": "str",
    "value": "user.status",
}

status_compare: ParameterLiteralValue = {
    "parameter_type": "value",
    "data_type": "str",
    "value": "active",
}

status_spec = FieldSpecification(field=status_field, operator="equal", compare_to=status_compare)

# Combine specifications using logical operators
user_spec = age_spec & status_spec

# Or use operators directly
user_spec = (
    FieldSpecification(field=field, operator="greater_than_or_equal", compare_to=compare_to) &
    FieldSpecification(field=status_field, operator="equal", compare_to=status_compare)
)

# Evaluate against data
data = {
    "user": {
        "age": 25,
        "status": "active",
    }
}

callback_registry = CallbackRegistry()
evaluator = SpecificationEvaluator(callback_registry)

result = asyncio.run(evaluator.evaluate(user_spec, data))
print(result)  # True

# Get human-readable description
print(user_spec.describe())  # (user.age >= 18 AND user.status == active)
```

### Building from Specification Trees

Specifications can be built from tree structures (TypedDict/JSON) for serialization:

```python
from lib_specifications.core import (
    SpecificationBuilder,
    SpecificationFieldLeafNode,
    SpecificationAndNode,
    CallbackRegistry,
)

# Create a callback registry
callback_registry = CallbackRegistry()

# Create a builder
builder = SpecificationBuilder(callback_registry)

# Define specification tree
tree: SpecificationAndNode = {
    "type": "and",
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
        "field": "user.status",
        "compare_to": {
            "parameter_type": "value",
            "data_type": "str",
            "value": "active",
        },
    },
}

# Build specification from tree
spec = builder.build(tree)

# Evaluate
evaluator = SpecificationEvaluator(callback_registry)
data = {"user": {"age": 25, "status": "active"}}
result = asyncio.run(evaluator.evaluate(spec, data))
print(result)  # True
```

### Field Comparisons

Field specifications can compare a field against a literal value or another field:

```python
from datetime import date
from lib_specifications.core import (
    FieldSpecification,
    ParameterPathValue,
)
from lib_specifications.core.parameters import ParameterLiteralValue

# Compare field to literal value
field: ParameterPathValue = {
    "parameter_type": "path",
    "data_type": "int",
    "value": "user.age",
}

compare_to: ParameterLiteralValue = {
    "parameter_type": "value",
    "data_type": "int",
    "value": 18,
}

spec = FieldSpecification(field=field, operator="greater_than", compare_to=compare_to)

# Compare field to another field
start_field: ParameterPathValue = {
    "parameter_type": "path",
    "data_type": "date",
    "value": "event.start_date",
}

end_field: ParameterPathValue = {
    "parameter_type": "path",
    "data_type": "date",
    "value": "event.end_date",
}

# Compare start_date <= end_date
date_spec = FieldSpecification(field=start_field, operator="less_than_or_equal", compare_to=end_field)

data = {
    "event": {
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 1, 31),
    }
}

callback_registry = CallbackRegistry()
evaluator = SpecificationEvaluator(callback_registry)
result = asyncio.run(evaluator.evaluate(date_spec, data))
print(result)  # True
```

### Callback Specifications

Register and use callbacks for custom logic:

```python
from datetime import date
from lib_specifications.core import (
    CallbackSpecification,
    CallbackRegistry,
    SpecificationEvaluator,
    ParameterPathValue,
    BaseCallback,
)

# Define a callback class with qualname attribute
class IsWeekendCallback(BaseCallback):
    """Check if a date falls on a weekend."""
    qualname = "is_weekend"
    
    def __init__(self, dt: date):
        self.dt = dt
    
    def __call__(self) -> bool:
        return self.dt.weekday() >= 5

# Register callback (uses qualname from the class)
callback_registry = CallbackRegistry()
callback_registry.register(IsWeekendCallback)

# Create callback specification
date_param: ParameterPathValue = {
    "parameter_type": "path",
    "data_type": "date",
    "value": "event.date",
}

signature = callback_registry.get_signature("is_weekend")
callback_spec = CallbackSpecification(
    callback_name="is_weekend",
    signature=signature,
    params={"dt": date_param},
)

# Evaluate
data = {"event": {"date": date(2024, 1, 6)}}  # Saturday
evaluator = SpecificationEvaluator(callback_registry)
result = asyncio.run(evaluator.evaluate(callback_spec, data))
print(result)  # True
```

### Available Operators

The library includes the following operators:

- `equal` - Equality comparison (==)
- `not_equal` - Inequality comparison (!=)
- `greater_than` - Greater than (>)
- `less_than` - Less than (<)
- `greater_than_or_equal` - Greater than or equal (>=)
- `less_than_or_equal` - Less than or equal (<=)
- `contains` - String contains (for strings)
- `starts_with` - String starts with (for strings)
- `ends_with` - String ends with (for strings)

```python
from lib_specifications.core.operators import get_operator, list_operators
from lib_specifications import ParameterTypeEnum

# List all available operators
print(list_operators())
# ['equal', 'not_equal', 'greater_than', 'less_than', ...]

# Get a specific operator
operator = get_operator("equal")
print(operator.symbol)  # "=="
print(operator.compatible_types)  # [ParameterTypeEnum.STR, ParameterTypeEnum.INT, ...]
```

### Complex Specifications

Build complex specifications with AND, OR, and NOT:

```python
from lib_specifications.core import (
    FieldSpecification,
    NotSpecification,
    OrSpecification,
    ParameterPathValue,
)
from lib_specifications.core.parameters import ParameterLiteralValue

# Create field specifications
age_field: ParameterPathValue = {
    "parameter_type": "path",
    "data_type": "int",
    "value": "user.age",
}

age_compare: ParameterLiteralValue = {
    "parameter_type": "value",
    "data_type": "int",
    "value": 18,
}

status_field: ParameterPathValue = {
    "parameter_type": "path",
    "data_type": "str",
    "value": "user.status",
}

active_compare: ParameterLiteralValue = {
    "parameter_type": "value",
    "data_type": "str",
    "value": "active",
}

banned_compare: ParameterLiteralValue = {
    "parameter_type": "value",
    "data_type": "str",
    "value": "banned",
}

# Build: (age >= 18) AND (status == "active" OR status != "banned")
age_spec = FieldSpecification(field=age_field, operator="greater_than_or_equal", compare_to=age_compare)
active_spec = FieldSpecification(field=status_field, operator="equal", compare_to=active_compare)
banned_spec = FieldSpecification(field=status_field, operator="not_equal", compare_to=banned_compare)

complex_spec = age_spec & (active_spec | banned_spec)

# Or using NOT
not_banned_spec = ~banned_spec
final_spec = age_spec & not_banned_spec
```

### Using Pre-defined Catalog

The library includes a catalog of pre-defined callbacks, triggers, and interceptors:

```python
from lib_specifications.catalog.callback_registry import CALLBACK_REGISTRY
from lib_specifications.catalog.trigger_registry import TRIGGER_REGISTRY
from lib_specifications.catalog.interceptor_registry import INTERCEPTOR_REGISTRY

# Use pre-defined callbacks
is_today_callback = CALLBACK_REGISTRY.isToday
has_onboarded_callback = CALLBACK_REGISTRY.hasOnboarded

# Access miniapps and triggers
welcome_miniapp = TRIGGER_REGISTRY.WELCOME
intro_trigger = welcome_miniapp.INTRO

# Access interceptors
greetings_interceptor = INTERCEPTOR_REGISTRY.GREETINGS
```

### Using Catalog Callbacks in Specifications

```python
import asyncio
from datetime import date
from lib_specifications import (
    SpecificationBuilder,
    SpecificationEvaluator,
    CallbackSpecification,
    ParameterPathValue,
)
from lib_specifications.catalog.callback_registry import CALLBACK_REGISTRY

# Use pre-defined callback from catalog
signature = CALLBACK_REGISTRY.get_signature("isToday")

# Create callback specification using catalog callback
date_param: ParameterPathValue = {
    "parameter_type": "path",
    "data_type": "date",
    "value": "event.date",
}

callback_spec = CallbackSpecification(
    callback_name="isToday",
    signature=signature,
    params={"dt": date_param},
)

# Evaluate
evaluator = SpecificationEvaluator(CALLBACK_REGISTRY)
data = {"event": {"date": date.today()}}
result = asyncio.run(evaluator.evaluate(callback_spec, data))
print(result)  # True
```

## Architecture

The package is organized into:

### Core Module (`lib_specifications.core`)

- **base.py**: Base specification classes (BaseSpecification, AndSpecification, OrSpecification, NotSpecification)
- **field.py**: FieldSpecification for field comparisons
- **callback.py**: CallbackSpecification, BaseCallback, and CallbackRegistry
- **operators.py**: Comparison operators (equal, greater_than, etc.) and OperatorRegistry
- **parameters.py**: Parameter value types, schemas, and type enums
- **builder.py**: SpecificationBuilder for building from trees
- **evaluator.py**: SpecificationEvaluator for async evaluation
- **tree.py**: Type definitions for specification trees (TypedDict)
- **trigger.py**: MiniApp, Trigger, and TriggerRegistry
- **interceptors.py**: InterceptorContentType and InterceptorContentTypeRegistry
- **languages.py**: Language and LanguageEnum

### Catalog Module (`lib_specifications.catalog`)

Pre-defined callbacks, triggers, and interceptors:

- **callback_registry/**: Pre-defined callback implementations
  - `datetime_callbacks.py`: Date/time related callbacks (isToday, isDayAfterToday, etc.)
  - `user_callbacks.py`: User-related callbacks (hasOnboarded, hasCreditScore, etc.)
- **trigger_registry/**: Pre-defined MiniApps and Triggers
  - Various miniapp modules (budget, calculator, credit_score, etc.)
- **interceptor_registry/**: Pre-defined interceptor content types
  - `greetings.py`: Greeting interceptors
  - `advertising.py`: Advertising interceptors

### Pydantic Models (`lib_specifications.pydantic_models`)

Pydantic models for serialization and validation of specification trees and parameters.

## API Reference

### Core Classes

- `BaseSpecification`: Abstract base class for all specifications
- `FieldSpecification`: Specification for comparing field values
- `CallbackSpecification`: Specification for callback evaluation
- `AndSpecification`: Logical AND combinator
- `OrSpecification`: Logical OR combinator
- `NotSpecification`: Logical NOT combinator

### Builders

- `SpecificationBuilder`: Builds specifications from tree structures

### Evaluators

- `SpecificationEvaluator`: Evaluates specifications against data dictionaries (async)

### Registries

- `CallbackRegistry`: Registry for managing callback classes
- `OperatorRegistry`: Registry for managing operators (global instance)
- `TriggerRegistry`: Registry for managing MiniApps and Triggers
- `InterceptorContentTypeRegistry`: Registry for managing interceptor content types

### Parameters

- `ParameterPathValue`: Parameter that extracts value from data using a path
- `ParameterLiteralValue`: Parameter that uses a literal value
- `ParameterSchema`: Schema for a single parameter
- `SignatureSchema`: Schema for callback parameters
- `ParameterTypeEnum`: Enum for parameter types (str, int, float, bool, date, datetime, list, dict)

### Operators

- `Operator`: Base class for comparison operators
- `EqualOperator`, `NotEqualOperator`: Equality operators
- `GreaterThanOperator`, `LessThanOperator`: Comparison operators
- `GreaterThanOrEqualOperator`, `LessThanOrEqualOperator`: Comparison operators
- `ContainsOperator`, `StartsWithOperator`, `EndsWithOperator`: String operators

### Specification Trees

- `SpecificationTree`: Type union for all specification tree nodes
- `SpecificationFieldLeafNode`: Field comparison leaf node
- `SpecificationCallbackLeafNode`: Callback leaf node
- `SpecificationAndNode`, `SpecificationOrNode`, `SpecificationNotNode`: Logical combinator nodes

### Triggers and MiniApps

- `MiniApp`: Represents a mini application with associated triggers
- `Trigger`: Represents a trigger point in a mini app flow
- `TriggerRegistry`: Registry for managing MiniApps and their triggers

### Interceptors

- `InterceptorContentType`: Defines types of content that can interrupt scenario flow
- `InterceptorContentTypeEnum`: Enum for interceptor content types (GREETINGS, ADVERTISING)
- `InterceptorContentTypeRegistry`: Registry for managing interceptor content types

### Languages

- `Language`: Represents a language with ID and display name
- `LanguageEnum`: Enum for supported languages (ENGLISH, RUSSIAN, FRENCH, etc.)

### Catalog

- `CALLBACK_REGISTRY`: Pre-configured registry with datetime and user callbacks
- `TRIGGER_REGISTRY`: Pre-configured registry with MiniApps and Triggers
- `INTERCEPTOR_REGISTRY`: Pre-configured registry with interceptor content types

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
