"""Builder for constructing specifications from specification trees."""

from ..logging_config import get_logger
from .base import (
    AndSpecification,
    BaseSpecification,
    NotSpecification,
    OrSpecification,
)
from .callback import CallbackRegistry, CallbackSpecification
from .field import FieldSpecification
from .parameters import ParameterPathValue, ParameterValue
from .tree import (
    SpecificationCallbackLeafNode,
    SpecificationFieldLeafNode,
    SpecificationTree,
)

logger = get_logger(__name__)


class SpecificationBuilder:
    """Builder for constructing specifications from trees.

    Converts specification tree structures (TypedDict/JSON) into
    Specification instances.
    """

    def __init__(
        self,
        callback_registry: CallbackRegistry,
    ):
        """Initialize builder.

        Args:
            callback_registry: Callback registry. Required for building callback specs.
        """
        self.callback_registry = callback_registry
        logger.debug("Initialized SpecificationBuilder")

    def build(self, spec_tree: SpecificationTree) -> BaseSpecification:
        """Build specification from tree.

        Args:
            spec_tree: The specification tree to build from

        Returns:
            Specification instance

        Raises:
            ValueError: If tree structure is invalid
            KeyError: If referenced specification type or callback is not registered
        """
        logger.debug("Starting to build specification from tree")
        try:
            result = self._build_branch(spec_tree)
            logger.info(f"Successfully built specification: {type(result).__name__}")
            return result
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to build specification: {e}")
            raise

    def _build_branch(self, spec_tree: SpecificationTree) -> BaseSpecification:
        """Recursively build specification from tree branch.

        Args:
            spec_tree: Current tree node to build

        Returns:
            BaseSpecification instance for this branch

        Raises:
            ValueError: If node type is invalid
        """
        node_type = spec_tree.get("type")
        logger.debug(f"Building branch with type: {node_type}")

        if node_type == "leaf":
            return self._build_leaf(spec_tree)
        elif node_type == "and":
            logger.debug("Building AND specification")
            and_node = spec_tree
            left = self._build_branch(and_node["left"])
            right = self._build_branch(and_node["right"])
            return AndSpecification(left, right)
        elif node_type == "or":
            logger.debug("Building OR specification")
            or_node = spec_tree
            left = self._build_branch(or_node["left"])
            right = self._build_branch(or_node["right"])
            return OrSpecification(left, right)
        elif node_type == "not":
            logger.debug("Building NOT specification")
            not_node = spec_tree
            child = self._build_branch(not_node["child"])
            return NotSpecification(child)
        else:
            logger.error(f"Unknown specification type: {node_type}")
            raise ValueError(f"Unknown specification type: {node_type}")

    def _build_leaf(self, node: dict) -> FieldSpecification | CallbackSpecification:
        """Build leaf node specification.

        Args:
            node: Leaf node dictionary

        Returns:
            FieldSpecification or CallbackSpecification instance

        Raises:
            ValueError: If leaf structure is invalid
        """
        subtype = node.get("subtype")
        logger.debug(f"Building leaf node with subtype: {subtype}")

        if subtype == "field":
            return self._build_field_spec(node)
        elif subtype == "callback":
            return self._build_callback_spec(node)
        else:
            logger.error(f"Unknown leaf subtype: {subtype}")
            raise ValueError(f"Unknown leaf subtype: {subtype}")

    def _build_field_spec(self, node: SpecificationFieldLeafNode) -> FieldSpecification:
        """Build field specification.

        Args:
            node: Field node dictionary

        Returns:
            FieldSpecification instance

        Raises:
            ValueError: If field structure is invalid
        """
        field_path = node.get("field")
        operator_name = node.get("name")
        compare_to: ParameterValue = node.get("compare_to")

        logger.debug(f"Building field specification: field='{field_path}', operator='{operator_name}'")

        if not field_path:
            logger.error("Field specification missing 'field'")
            raise ValueError("Field specification requires 'field'")
        if not operator_name:
            logger.error("Field specification missing 'name' (operator)")
            raise ValueError("Field specification requires 'name' (operator)")
        if not compare_to:
            logger.error("Field specification missing 'compare_to'")
            raise ValueError("Field specification requires 'compare_to'")

        # Convert field string to ParameterPathValue
        field_param: ParameterPathValue = {
            "parameter_type": "path",
            "data_type": "str",  # Path is always a string
            "value": field_path,
        }

        logger.debug("Successfully built field specification")
        return FieldSpecification(
            field=field_param,
            operator=operator_name,
            compare_to=compare_to,
        )

    def _build_callback_spec(self, node: SpecificationCallbackLeafNode) -> CallbackSpecification:
        """Build callback specification.

        Args:
            node: Callback node dictionary

        Returns:
            CallbackSpecification instance

        Raises:
            ValueError: If callback structure is invalid
            KeyError: If callback is not registered
        """
        callback_name = node.get("name")
        params = node.get("params", {})

        logger.debug(f"Building callback specification: name='{callback_name}', params={list(params.keys())}")

        if not callback_name:
            logger.error("Callback specification missing 'name'")
            raise ValueError("Callback specification requires 'name'")

        # Get callback signature from registry
        signature = self.callback_registry.get_signature(callback_name)
        if signature is None:
            logger.error(f"Callback '{callback_name}' not found in callback registry")
            raise KeyError(f"Callback '{callback_name}' not found in callback registry")

        logger.debug(f"Successfully built callback specification for '{callback_name}'")
        return CallbackSpecification(
            callback_name=callback_name,
            signature=signature,
            params=params,
        )
