from typing import Any

from ..logging_config import get_logger
from .base import (
    AndSpecification,
    BaseSpecification,
    NotSpecification,
    OrSpecification,
)
from .callback import CallbackRegistry, CallbackSpecification
from .field import FieldSpecification
from .operators import get_operator
from .parameters import ParameterTypeEnum, ParameterValue

logger = get_logger(__name__)


class SpecificationEvaluator:
    """Evaluates Specification objects against data dictionaries.

    This evaluator recursively evaluates specification objects with lazy evaluation:
    - AND: stops if left is False
    - OR: stops if left is True

    Example:
        >>> from lib_specifications.specifications import FieldSpecification, AndSpecification
        >>> from lib_specifications.specification_tree import ParameterPathValue, ParameterLiteralValue
        >>> field = ParameterPathValue(parameter_type="path", data_type="str", value="user.age")
        >>> compare_to = ParameterLiteralValue(parameter_type="value", data_type="int", value=18)
        >>> field_spec = FieldSpecification(field=field, operator="equal", compare_to=compare_to)
        >>> data = {"user": {"age": 18}}
        >>> evaluator = SpecificationEvaluator()
        >>> import asyncio
        >>> asyncio.run(evaluator.evaluate(field_spec, data))
        True
    """

    def __init__(
        self,
        callback_registry: CallbackRegistry,
    ):
        """Initialize the specification evaluator.

        Args:
            callback_registry: Callback registry with concrete implementations.
        """
        self.callback_registry = callback_registry
        logger.debug("Initialized SpecificationEvaluator")

    async def evaluate(
        self,
        specification: BaseSpecification,
        data: dict[str, Any],
    ) -> bool:
        """Evaluate a specification against data.

        Args:
            specification: The Specification to evaluate
            data: Nested dictionary structure containing the data to evaluate against

        Returns:
            True if the specification is satisfied, False otherwise

        Raises:
            ValueError: If specification structure is invalid or callback not found
            KeyError: If required fields are missing in data
        """
        logger.debug(f"Starting evaluation of specification: {type(specification).__name__}")
        result = await self._evaluate_spec(specification, data)
        logger.info(f"Evaluation completed with result: {result}")
        return result

    async def _evaluate_spec(
        self,
        spec: BaseSpecification,
        data: dict[str, Any],
    ) -> bool:
        """Recursively evaluate a specification.

        Args:
            spec: The specification to evaluate
            data: Nested dictionary structure containing the data

        Returns:
            True if the specification is satisfied, False otherwise
        """
        spec_type = type(spec).__name__
        logger.debug(f"Evaluating {spec_type}")
        if isinstance(spec, AndSpecification):
            return await self._evaluate_and_spec(spec, data)
        elif isinstance(spec, OrSpecification):
            return await self._evaluate_or_spec(spec, data)
        elif isinstance(spec, NotSpecification):
            return await self._evaluate_not_spec(spec, data)
        elif isinstance(spec, FieldSpecification):
            return self._evaluate_field_spec(spec, data)
        elif isinstance(spec, CallbackSpecification):
            return await self._evaluate_callback_spec(spec, data)
        else:
            logger.error(f"Unknown specification type: {spec_type}")
            raise ValueError(f"Unknown specification type: {spec_type}")

    def _evaluate_field_spec(
        self,
        spec: FieldSpecification,
        data: dict[str, Any],
    ) -> bool:
        """Evaluate a field specification.

        Args:
            spec: The field specification to evaluate
            data: Nested dictionary structure containing the data

        Returns:
            True if the field comparison is satisfied, False otherwise
        """
        # Extract field value from data (always a path)
        field_path = spec.field["value"]
        logger.debug(f"Evaluating field specification: path='{field_path}', operator='{spec.operator}'")
        try:
            field_value = self.get_nested_value(data, field_path)
            logger.debug(f"Extracted field value: {field_value}")

            # Extract or get compare_to value (can be path or literal)
            compare_to_value = self._get_parameter_value(spec.compare_to, data)
            logger.debug(f"Compare-to value: {compare_to_value}")

            # Apply operator (sync)
            result = self._apply_operator(spec.operator, field_value, compare_to_value)
            logger.debug(f"Field specification result: {result}")
            return result
        except (KeyError, ValueError) as e:
            logger.error(f"Field specification evaluation failed: {e}")
            raise

    async def _evaluate_callback_spec(
        self,
        spec: CallbackSpecification,
        data: dict[str, Any],
    ) -> bool:
        """Evaluate a callback specification.

        Args:
            spec: The callback specification to evaluate
            data: Nested dictionary structure containing the data

        Returns:
            True if the callback returns True, False otherwise

        Raises:
            KeyError: If callback is not found in callback registry
            ValueError: If callback execution fails
        """
        logger.debug(f"Evaluating callback specification: '{spec.callback_name}'")
        # Get callback class from registry
        callback_class = self.callback_registry.get(spec.callback_name)
        if callback_class is None:
            logger.error(f"Callback '{spec.callback_name}' not found in callback registry")
            raise KeyError(f"Callback '{spec.callback_name}' not found in callback registry")

        # Extract values from parameters
        extracted_values = self._extract_parameter_values(spec.params, data)
        logger.debug(f"Extracted callback parameters: {list(extracted_values.keys())}")

        # Create callback instance with extracted values
        callback_instance = callback_class(**extracted_values)

        # Execute callback (handle both sync and async)
        try:
            logger.debug(f"Executing callback '{spec.callback_name}' of type {callback_class.run_type}")

            if callback_class.run_type == "sync":
                result = callback_instance()
            elif callback_class.run_type == "async":
                result = await callback_instance()
            else:
                raise ValueError(f"Invalid callback run type: {callback_class.run_type}")

            logger.debug(f"Callback '{spec.callback_name}' returned: {result}")
            return result
        except Exception as e:
            logger.error(f"Callback '{spec.callback_name}' execution failed: {e}", exc_info=True)
            raise ValueError(f"Callback '{spec.callback_name}' execution failed: {e}") from e

    async def _evaluate_and_spec(
        self,
        spec: AndSpecification,
        data: dict[str, Any],
    ) -> bool:
        """Evaluate an AND specification with lazy evaluation.

        Args:
            spec: The AND specification to evaluate
            data: Nested dictionary structure containing the data

        Returns:
            True if both left and right are satisfied, False otherwise
        """
        logger.debug("Evaluating AND specification")
        left_result = await self._evaluate_spec(spec.left, data)
        logger.debug(f"AND left result: {left_result}")
        if not left_result:
            logger.debug("AND short-circuit: left is False, skipping right evaluation")
            return False  # Short-circuit: don't evaluate right if left is False
        right_result = await self._evaluate_spec(spec.right, data)
        logger.debug(f"AND right result: {right_result}, final result: {right_result}")
        return right_result

    async def _evaluate_or_spec(
        self,
        spec: OrSpecification,
        data: dict[str, Any],
    ) -> bool:
        """Evaluate an OR specification with lazy evaluation.

        Args:
            spec: The OR specification to evaluate
            data: Nested dictionary structure containing the data

        Returns:
            True if either left or right is satisfied, False otherwise
        """
        logger.debug("Evaluating OR specification")
        left_result = await self._evaluate_spec(spec.left, data)
        logger.debug(f"OR left result: {left_result}")
        if left_result:
            logger.debug("OR short-circuit: left is True, skipping right evaluation")
            return True  # Short-circuit: don't evaluate right if left is True
        right_result = await self._evaluate_spec(spec.right, data)
        logger.debug(f"OR right result: {right_result}, final result: {right_result}")
        return right_result

    async def _evaluate_not_spec(
        self,
        spec: NotSpecification,
        data: dict[str, Any],
    ) -> bool:
        """Evaluate a NOT specification.

        Args:
            spec: The NOT specification to evaluate
            data: Nested dictionary structure containing the data

        Returns:
            True if child is not satisfied, False otherwise
        """
        logger.debug("Evaluating NOT specification")
        child_result = await self._evaluate_spec(spec.spec, data)
        result = not child_result
        logger.debug(f"NOT specification: child={child_result}, result={result}")
        return result

    def get_nested_value(self, data: dict[str, Any], path: str) -> Any:
        """Get a value from nested dictionary using dot-notation path.

        Args:
            data: Nested dictionary structure
            path: Dot-notation path (e.g., "user.id", "meta.size")

        Returns:
            The value at the specified path

        Raises:
            KeyError: If the path doesn't exist in data
        """
        logger.debug(f"Getting nested value for path: '{path}'")
        keys = path.split(".")
        current = data

        for key in keys:
            if not isinstance(current, dict):
                logger.error(f"Path '{path}' is invalid: '{key}' is not a dictionary")
                raise KeyError(f"Path '{path}' is invalid: '{key}' is not a dictionary")
            if key not in current:
                logger.error(f"Path '{path}' not found: key '{key}' doesn't exist")
                raise KeyError(f"Path '{path}' not found: key '{key}' doesn't exist")
            current = current[key]

        logger.debug(f"Successfully extracted value from path '{path}': {current}")
        return current

    def _get_parameter_value(
        self,
        param_value: ParameterValue,
        data: dict[str, Any],
    ) -> Any:
        """Get the value from a parameter definition (path or literal).

        Args:
            param_value: Parameter definition (either path or literal value)
            data: Nested dictionary structure containing the data

        Returns:
            The value (either extracted from data or literal)

        Raises:
            KeyError: If path doesn't exist in data
            ValueError: If parameter_type is invalid
        """
        parameter_type = param_value["parameter_type"]

        if parameter_type == "path":
            # Extract value from data using path
            path = param_value["value"]
            return self.get_nested_value(data, path)
        elif parameter_type == "value":
            # Use literal value
            return param_value["value"]
        else:
            raise ValueError(f"Invalid parameter_type: {parameter_type}. Must be 'path' or 'value'")

    def _extract_parameter_values(
        self,
        param_mapping: dict[str, ParameterValue],
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract values from data dictionary using parameter definitions.

        Args:
            param_mapping: Dictionary mapping parameter names to parameter definitions
                          (either path or literal value)
            data: Nested dictionary structure

        Returns:
            Dictionary with parameter names as keys and extracted/literal values as values

        Raises:
            KeyError: If a path doesn't exist in data
            ValueError: If parameter_type is invalid
        """
        extracted = {}

        for param_name, param_def in param_mapping.items():
            value = self._get_parameter_value(param_def, data)
            extracted[param_name] = value

        return extracted

    def _apply_operator(
        self,
        operator_name: str,
        left_value: Any,
        right_value: Any,
    ) -> bool:
        """Apply an operator to compare two values using the operator registry.

        Args:
            operator_name: Name of the operator (e.g., "equal", "greater_than")
            left_value: Left operand value
            right_value: Right operand value

        Returns:
            True if the comparison is satisfied, False otherwise

        Raises:
            ValueError: If operator is not found or not compatible with value types
        """
        logger.debug(f"Applying operator '{operator_name}' to values: {left_value} vs {right_value}")
        # Get operator from registry
        operator = get_operator(operator_name)
        if operator is None:
            logger.error(f"Operator '{operator_name}' not found in registry")
            raise ValueError(f"Operator '{operator_name}' not found in registry")

        # Determine the type of left_value for compatibility checking
        try:
            left_type = ParameterTypeEnum.from_type(type(left_value))
        except ValueError:
            # If type is not in enum, we can't validate compatibility
            # but we can still try to use the operator
            left_type = None
            logger.debug(f"Could not determine type for value {left_value}, skipping compatibility check")

        # Validate compatibility if we could determine the type
        if left_type is not None and not operator.is_compatible_with(left_type):
            compatible_types = [t.label for t in operator.compatible_types]
            logger.error(
                f"Operator '{operator_name}' is not compatible with type '{left_type.label}'. "
                f"Compatible types: {', '.join(compatible_types)}"
            )
            raise ValueError(
                f"Operator '{operator_name}' is not compatible with type '{left_type.label}'. "
                f"Compatible types: {', '.join(compatible_types)}"
            )

        # Use operator's compare method (sync)
        result = operator.compare(left_value, right_value)
        logger.debug(f"Operator '{operator_name}' comparison result: {result}")
        return result
