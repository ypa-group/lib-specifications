from typing import Literal, TypedDict

from .parameters import ParameterValue

# Type definitions
SpecType = Literal["leaf", "and", "or", "not"]
SpecSubtype = Literal["field", "callback"]


class SpecificationNode(TypedDict):
    """Base node in specification tree."""

    type: SpecType


class BaseSpecificationLeafNode(SpecificationNode):
    """Base leaf node representing a single specification.

    Can be either:
    - Field comparison: Compare a context field to a value or another field
    - Callback: External function call
    """

    type: Literal["leaf"]
    subtype: SpecSubtype  # "field" or "callback"
    name: str  # For field: operator name (e.g., "equal"), For callback: callback name (e.g., "isWeekend")


class SpecificationFieldLeafNode(BaseSpecificationLeafNode):
    """Field comparison leaf node.

    Compares a field (always a path) against either another field (path) or a literal value.
    """

    subtype: Literal["field"]
    field: str  # Field name (path), supports dot notation (e.g., "user.profile.age")
    compare_to: ParameterValue  # What to compare against - can be path or literal value


class SpecificationCallbackLeafNode(BaseSpecificationLeafNode):
    """Callback leaf node.

    Each parameter can be either a path (to extract from data) or a literal value.
    """

    subtype: Literal["callback"]
    params: dict[
        str, ParameterValue
    ]  # Parameters for callback function, key is the parameter name, value is either path or literal value


SpecificationLeafNode = SpecificationFieldLeafNode | SpecificationCallbackLeafNode


class SpecificationAndNode(SpecificationNode):
    """AND combinator node.

    Both left and right must be satisfied.
    """

    type: Literal["and"]
    left: "SpecificationTree"
    right: "SpecificationTree"


class SpecificationOrNode(SpecificationNode):
    """OR combinator node.

    Either left or right must be satisfied.
    """

    type: Literal["or"]
    left: "SpecificationTree"
    right: "SpecificationTree"


class SpecificationNotNode(SpecificationNode):
    """NOT combinator node.

    Negates the child specification.
    """

    type: Literal["not"]
    child: "SpecificationTree"


SpecificationTree = SpecificationLeafNode | SpecificationAndNode | SpecificationOrNode | SpecificationNotNode
