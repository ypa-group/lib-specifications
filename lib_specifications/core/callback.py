import inspect
from abc import ABC
from typing import Literal

from ..logging_config import get_logger
from .base import BaseSpecification
from .parameters import ParameterValue, SignatureSchema, generate_signature_from_callable

logger = get_logger(__name__)


class CallbackSpecification(BaseSpecification):
    """Specification for callback evaluation.

    Parameters:
        callback_name: Name of the callback
        signature: SignatureSchema extracted from the callback
        params: Dictionary mapping callback parameter names to ParameterValue

    Example:
        >>> callback_spec = CallbackSpecification(
        >>>     callback_name="is_weekend",
        >>>     signature=SignatureSchema(parameters=[ParameterSchema(name="date", data_type="date")]),
        >>>     params={"date": ParameterPathValue(parameter_type="path", data_type="date", value="user.birthday")}
        >>> )
    """

    def __init__(
        self,
        callback_name: str,
        signature: SignatureSchema,
        params: dict[str, ParameterValue],
    ):
        """Initialize callback specification.

        Args:
            callback_name: Name of the callback
            signature: SignatureSchema extracted from the callback
            params: Dictionary mapping callback parameter names to ParameterValue
        """
        self.callback_name = callback_name
        self.signature = signature
        self.params = params

    def describe(self) -> str:
        """Return human-readable description."""
        if self.signature.parameters:
            param_descriptions = []
            for param_schema in self.signature.parameters.values():
                param_name = param_schema.name
                data_type = param_schema.data_type.label

                # Get the actual parameter value from self.params
                if param_name in self.params:
                    param_value = self.params[param_name]
                    # Format the value: show path or literal value
                    if param_value["parameter_type"] == "path":
                        value_str = param_value["value"]
                    else:  # literal value
                        value_str = repr(param_value["value"])
                    param_descriptions.append(f"{param_name}: {data_type}={value_str}")
                else:
                    # Fallback if parameter not found (shouldn't happen in practice)
                    param_descriptions.append(f"{param_name}: {data_type}")

            params_str = ", ".join(param_descriptions)
            return f"{self.callback_name}({params_str})"
        return f"{self.callback_name}()"


class BaseCallback(ABC):
    """Base class for all callbacks.

    This class ensures that all callbacks implement either a synchronous or asynchronous __call__ method.
    __init__ should take all parameters (signature extracted from here)
    """

    qualname: str
    run_type: Literal["sync", "async"]

    def __call__(self) -> bool:
        """At this point sync one - but may be overridden in a subclass.
        Returns:
            bool: True if the callback returns True, False otherwise
        """
        raise NotImplementedError("Subclasses must implement this method")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Check if the class defines a __call__ method
        call_attribute = getattr(cls, "__call__", None)  # noqa: B004
        if call_attribute is None:
            raise TypeError(
                f"Class {cls.__name__} must implement either a synchronous or asynchronous a __call__ method."
            )

        # Check if __call__ is a method
        if not callable(call_attribute):
            raise TypeError(f"Class {cls.__name__} must implement a __call__ method.")

        # Check if __call__ is async
        is_async = inspect.iscoroutinefunction(call_attribute)
        cls.run_type = "async" if is_async else "sync"


class CallbackRegistry:
    """Registry for managing callbacks.

    Stores callbacks with their extracted signatures.
    For UI/service: use abstract callbacks (with NotImplemented __call__)
    For evaluator: use concrete implementations with real __call__ methods.

    Abstract callbacks can be overridden with concrete implementations using
    the override() method, but only if the signature matches.
    """

    def __init__(self, callbacks: list[type[BaseCallback]] | None = None):
        """Initialize the callback registry."""
        self._callbacks: dict[str, type[BaseCallback]] = {}
        self._signatures: dict[str, SignatureSchema] = {}
        if callbacks:
            for callback_class in callbacks:
                self.register(callback_class)
        logger.debug("Initialized CallbackRegistry")

    def register(self, callback_class: type[BaseCallback]) -> None:
        """Register a callback class.

        Extracts signature from the callback's __init__ method.

        Args:
            callback_class: Callback class (must inherit from BaseCallback)

        Raises:
            ValueError: If callback doesn't inherit from BaseCallback, or if callback
                       is already registered (use override() instead)
        """
        if not issubclass(callback_class, BaseCallback):
            raise ValueError("Callback class must inherit from BaseCallback")

        logger.debug(f"Registering callback '{callback_class.qualname}' with class {callback_class.__name__}")

        # Check if already registered
        if callback_class.qualname in self._callbacks:
            logger.error(f"Attempted to register already registered callback '{callback_class.qualname}'")
            raise ValueError(
                f"Callback '{callback_class.qualname}' is already registered. Use override() to replace an existing callback."
            )

        # Extract signature from __init__
        signature = generate_signature_from_callable(callback_class.__init__)
        logger.debug(
            f"Extracted signature for callback '{callback_class.qualname}': {len(signature.parameters)} parameters"
        )

        self._callbacks[callback_class.qualname] = callback_class
        self._signatures[callback_class.qualname] = signature
        logger.info(f"Successfully registered callback '{callback_class.qualname}'")

    def override(self, callback_class: type[BaseCallback]) -> None:
        """Override an already registered callback with a new implementation.

        The signature must match the existing callback.

        Args:
            callback_class: New callback class (must inherit from BaseCallback)

        Raises:
            ValueError: If callback doesn't inherit from BaseCallback, if callback
                       is not registered, or if signature doesn't match
        """
        if not issubclass(callback_class, BaseCallback):
            raise ValueError("Callback class must inherit from BaseCallback")

        logger.debug(
            f"Attempting to override callback '{callback_class.qualname}' with class {callback_class.__name__}"
        )

        # Check if callback is registered
        if callback_class.qualname not in self._callbacks:
            logger.error(f"Attempted to override non-registered callback '{callback_class.qualname}'")
            raise ValueError(
                f"Callback '{callback_class.qualname}' is not registered. Use register() to register a new callback."
            )

        # Extract signature from __init__
        signature = generate_signature_from_callable(callback_class.__init__)
        logger.debug(
            f"Extracted signature for override callback '{callback_class.qualname}': {len(signature.parameters)} parameters"
        )

        # Validate signature consistency
        existing_signature = self._signatures[callback_class.qualname]
        if not self._signatures_match(existing_signature, signature):
            logger.error(f"Signature mismatch for callback '{callback_class.qualname}' during override")
            raise ValueError(
                f"Signature mismatch for callback '{callback_class.qualname}'. Existing signature does not match new signature."
            )

        # Override with concrete implementation
        self._callbacks[callback_class.qualname] = callback_class
        self._signatures[callback_class.qualname] = signature
        logger.info(f"Successfully overridden callback '{callback_class.qualname}'")

    def _signatures_match(self, sig1: SignatureSchema, sig2: SignatureSchema) -> bool:
        """Check if two signatures match.

        Args:
            sig1: First signature
            sig2: Second signature

        Returns:
            True if signatures match, False otherwise
        """
        # Compare parameter names
        if set(sig1.parameters.keys()) != set(sig2.parameters.keys()):
            return False

        # Compare each parameter
        for param_name in sig1.parameters.keys():
            param1 = sig1.parameters[param_name]
            param2 = sig2.parameters[param_name]

            # Compare data type
            if param1.data_type != param2.data_type:
                return False

            # Compare required flag
            if param1.required != param2.required:
                return False

            # Compare default values (if both have defaults)
            if param1.default is not None and param2.default is not None:
                if param1.default != param2.default:
                    return False
            elif param1.default is not None or param2.default is not None:
                # One has default, other doesn't
                return False

        return True

    def get(self, name: str) -> type[BaseCallback]:
        """Get callback class by name.

        Args:
            name: Name of the callback

        Returns:
            Callback class or None if not found
        """
        callback = self._callbacks.get(name)
        if callback is None:
            raise ValueError(f"Callback '{name}' not found in registry.")
        return callback

    def get_signature(self, name: str) -> SignatureSchema | None:
        """Get signature for a callback by name.

        Args:
            name: Name of the callback

        Returns:
            SignatureSchema or None if callback not found
        """
        signature = self._signatures.get(name)
        if signature is None:
            raise ValueError(f"Signature for callback '{name}' not found in registry.")
        return signature

    def has(self, name: str) -> bool:
        """Check if callback is registered.

        Args:
            name: Name of the callback

        Returns:
            True if registered
        """
        return name in self._callbacks

    def list_names(self) -> list[str]:
        """List all registered callback names.

        Returns:
            List of callback names
        """
        return list(self._callbacks.keys())

    def __getattr__(self, name: str) -> type[BaseCallback]:
        """Get a callback by name."""
        if name not in self._callbacks:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'. "
                f"Available callbacks: {', '.join(sorted(self._callbacks.keys()))}"
            )
        return self._callbacks[name]

    def __dir__(self) -> list[str]:
        """Return list of available attributes including all callback names."""
        return sorted(set(super().__dir__()) | set(self._callbacks.keys()))
