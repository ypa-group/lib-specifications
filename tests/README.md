# Test Infrastructure

This directory contains the test suite for the lib-specifications project.

## Directory Structure

```
tests/
├── unit/                      # Unit tests - test individual components in isolation
│   └── lib_specifications/    # Mirrors lib_specifications package structure
│       ├── core/              # Tests for core module
│       │   ├── test_base.py   # Tests for BaseSpecification and combinators
│       │   ├── test_callback.py  # Tests for CallbackSpecification
│       │   └── test_types.py  # Tests for types (ParameterTypeEnum, etc.)
│       └── operators/         # Tests for operators module
│           ├── test_operator.py  # Tests for Operator base class
│           ├── test_operator_registry.py  # Tests for OperatorRegistry
│           ├── test_equal.py  # Tests for EqualOperator
│           ├── test_not_equal.py  # Tests for NotEqualOperator
│           ├── test_comparison_operators.py  # Tests for gt, gte, lt, lte
│           └── test_string_operators.py  # Tests for contains, startswith, endswith
├── integration/               # Integration tests - test component interactions
├── e2e/                       # End-to-end tests - test full application flow
├── conftest.py                # Shared pytest configuration and fixtures
└── README.md                  # This file
```

## Test Types

### Unit Tests (`tests/unit/`)

- Test individual functions, classes, and modules in isolation
- Use mocks and stubs for dependencies
- Should be fast and deterministic
- Example: Testing a single specification class or operator

### Integration Tests (`tests/integration/`)

- Test interactions between multiple components
- Test specification combinations and operator usage
- Example: Testing a complete specification evaluation flow

### End-to-End Tests (`tests/e2e/`)

- Test the full application flow
- Test real-world usage scenarios
- Example: Testing a complete specification pattern implementation

## Running Tests

### Using Make (Recommended)

```bash
# Run all unit tests (default)
make test

# Run only unit tests
make test-unit

# Run only integration tests
make test-integration

# Run only e2e tests
make test-e2e

# Run all tests
make test-all

# Run tests with coverage
make test-coverage

# Run tests in parallel
make test-parallel

# Run specific test file
make test-specific FILE=tests/unit/lib_specifications/core/test_base.py

# Run tests with specific marker
make test-marker MARKER=asynchronous

# Clean test artifacts
make clean-test
```

### Using pytest directly

```bash
# Run all tests
pytest

# Run specific test directory
pytest tests/unit

# Run specific test file
pytest tests/unit/lib_specifications/core/test_base.py

# Run specific test function
pytest tests/unit/lib_specifications/core/test_base.py::TestBaseSpecification::test_call_method

# Run tests with markers
pytest -m unit
pytest -m integration
pytest -m "not slow"

# Run with coverage
pytest --cov=lib_specifications --cov-report=html

# Run in parallel (requires pytest-xdist)
pytest -n auto

# Run with verbose output
pytest -vv

# Run with debugging
pytest --pdb
```

## Test Markers

Tests can be marked with pytest markers for categorization:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.slow` - Tests that take a long time
- `@pytest.mark.asynchronous` - Async tests

Example:

```python
@pytest.mark.unit
@pytest.mark.asynchronous
async def test_something():
    ...
```

## Writing Tests

### Unit Test Example

```python
import pytest
from lib_specifications.core.base import BaseSpecification

@pytest.mark.unit
class TestMySpecification:
    @pytest.mark.asynchronous
    async def test_something(self):
        # Arrange
        spec = MySpecification()
        
        # Act
        result = await spec.is_satisfied_by(candidate)
        
        # Assert
        assert result is True
```

### Async Test Example

```python
import pytest

@pytest.mark.unit
@pytest.mark.asynchronous
async def test_async_function():
    result = await my_async_function()
    assert result is not None
```

## Fixtures

Shared fixtures are defined in `conftest.py`. Common fixtures include:

- `event_loop` - Async event loop for async tests
- `mock_async_function` - Mock async function
- `mock_sync_function` - Mock sync function

## Configuration

Test configuration is in `pytest.ini` at the project root. Key settings:

- Test discovery patterns
- Markers
- Coverage settings
- Asyncio mode

## Coverage

To generate coverage reports:

```bash
# HTML report
make test-coverage

# XML report (for CI)
make test-coverage-xml
```

Coverage reports are generated in `htmlcov/` directory.

## Best Practices

1. **Test Naming**: Use descriptive names that explain what is being tested
2. **Arrange-Act-Assert**: Structure tests clearly
3. **Isolation**: Each test should be independent
4. **Fast Tests**: Unit tests should be fast (< 1 second)
5. **Clear Assertions**: Use descriptive assertion messages
6. **Mock External Dependencies**: Don't make real API calls in unit tests
7. **Use Markers**: Mark tests appropriately for easy filtering
8. **Test Edge Cases**: Don't just test happy paths

## CI/CD Integration

Tests can be run in CI/CD pipelines:

```bash
# Run all tests
pytest

# Run with coverage for CI
pytest --cov=lib_specifications --cov-report=xml

# Run only fast tests
pytest -m "not slow"
```

