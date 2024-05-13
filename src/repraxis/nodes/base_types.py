"""Database node abstract base class definitions.

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Generic, Mapping, Optional, Protocol, TypeVar


class NodeType(Enum):
    """Indicator of what kind of data an node holds."""

    VARIABLE = auto()
    SYMBOL = auto()
    INT = auto()
    FLOAT = auto()


class NodeCardinality(Enum):
    """The number of children a node is allowed to have."""

    NONE = auto()
    ONE = auto()
    MANY = auto()


class INode(Protocol):
    """The interface for all nodes in the database."""

    @property
    @abstractmethod
    def node_type(self) -> NodeType:
        """The type of data held in the node."""

        raise NotImplementedError()

    @property
    @abstractmethod
    def symbol(self) -> str:
        """Get the symbol associated with the node in the database."""

        raise NotImplementedError()

    @property
    @abstractmethod
    def cardinality(self) -> NodeCardinality:
        """How many children is the node allowed to have at one time."""

        raise NotImplementedError()

    @property
    @abstractmethod
    def children(self) -> Mapping[str, INode]:
        """The children of the node."""

        raise NotImplementedError()

    @property
    @abstractmethod
    def parent(self) -> Optional[INode]:
        """A reference to the node's parent node."""

        raise NotImplementedError()

    @abstractmethod
    def set_parent(self, node: Optional[INode]) -> None:
        """Set parent node reference"""

        raise NotImplementedError()

    @abstractmethod
    def get_value(self) -> object:
        """Get the value associated with this node."""

        raise NotADirectoryError()

    @abstractmethod
    def equal_to(self, other: INode) -> bool:
        """Check if the node's value is equal to another."""

        raise NotImplementedError()

    @abstractmethod
    def not_equal_to(self, other: INode) -> bool:
        """Check if the node's value is not equal to another."""

        raise NotImplementedError()

    @abstractmethod
    def less_than_equal_to(self, other: INode) -> bool:
        """Check if the node's value is less than or equal to another."""

        raise NotImplementedError()

    @abstractmethod
    def greater_than_equal_to(self, other: INode) -> bool:
        """Check if the node's value is greater than or equal to another."""

        raise NotImplementedError()

    @abstractmethod
    def less_than(self, other: INode) -> bool:
        """Check if the node's value is less than another."""

        raise NotImplementedError()

    @abstractmethod
    def greater_than(self, other: INode) -> bool:
        """Check if the node's value is greater than another."""

        raise NotImplementedError()

    @abstractmethod
    def add_child(self, node: INode) -> None:
        """Add a child node to the node."""

        raise NotImplementedError()

    @abstractmethod
    def remove_child(self, symbol: str) -> bool:
        """Removes a child node from the node."""

        raise NotImplementedError()

    @abstractmethod
    def get_child(self, symbol: str) -> INode:
        """Get a child node."""

        raise NotImplementedError()

    @abstractmethod
    def has_child(self, symbol: str) -> bool:
        """Check if the node has a child."""

        raise NotImplementedError()

    @abstractmethod
    def clear_children(self) -> None:
        """Remove all children and from this node."""

        raise NotImplementedError()

    @abstractmethod
    def get_path(self) -> str:
        """Get the database sentence this node represents."""

        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> INode:
        """Create a copy of the node."""

        raise NotImplementedError()


_T = TypeVar("_T")


class Node(ABC, Generic[_T]):
    """A templated abstract baseclass inherited by all nodes."""

    __slots__ = (
        "_children",
        "_symbol",
        "_cardinality",
        "_node_type",
        "_parent",
        "_value",
    )

    _children: dict[str, INode]
    _symbol: str
    _cardinality: NodeCardinality
    _node_type: NodeType
    _parent: Optional[INode]
    _value: _T

    def __init__(self, symbol: str, value: _T, cardinality: NodeCardinality) -> None:
        super().__init__()
        self._symbol = symbol
        self._value = value
        self._cardinality = cardinality
        self._children = {}
        self._parent = None

    @property
    def node_type(self) -> NodeType:
        """The type of data held in the node."""

        return self._node_type

    @property
    def symbol(self) -> str:
        """Get the symbol associated with the node in the database."""

        return self._symbol

    @property
    def cardinality(self) -> NodeCardinality:
        """How many children is the node allowed to have at one time."""

        return self._cardinality

    @property
    def children(self) -> Mapping[str, INode]:
        """The children of the node."""

        return self._children

    @property
    def parent(self) -> Optional[INode]:
        """A reference to the node's parent node."""

        return self._parent

    def set_parent(self, node: Optional[INode]) -> None:
        """Set parent node reference"""

        self._parent = node

    @property
    def value(self) -> _T:
        """The value associated with this node."""

        return self._value

    def get_value(self) -> object:
        """Get the value associated with this node."""

        return self._value

    @abstractmethod
    def equal_to(self, other: INode) -> bool:
        """Check if the node's value is equal to another."""

        raise NotImplementedError()

    @abstractmethod
    def not_equal_to(self, other: INode) -> bool:
        """Check if the node's value is not equal to another."""

        raise NotImplementedError()

    @abstractmethod
    def less_than_equal_to(self, other: INode) -> bool:
        """Check if the node's value is less than or equal to another."""

        raise NotImplementedError()

    @abstractmethod
    def greater_than_equal_to(self, other: INode) -> bool:
        """Check if the node's value is greater than or equal to another."""

        raise NotImplementedError()

    @abstractmethod
    def less_than(self, other: INode) -> bool:
        """Check if the node's value is less than another."""

        raise NotImplementedError()

    @abstractmethod
    def greater_than(self, other: INode) -> bool:
        """Check if the node's value is greater than another."""

        raise NotImplementedError()

    def add_child(self, node: INode) -> None:
        """Add a child node to the node."""

        if self._cardinality == NodeCardinality.NONE:
            raise TypeError("Cannot add child to node with cardinality NONE.")

        if self._cardinality == NodeCardinality.ONE and len(self._children) >= 1:
            raise TypeError("Cannot add additional child to node with cardinality ONE.")

        self._children[node.symbol] = node
        node.set_parent(self)

    def remove_child(self, symbol: str) -> bool:
        """Removes a child node from the node."""

        if symbol in self._children:
            child = self._children[symbol]
            child.set_parent(None)
            del self._children[symbol]
            return True

        return False

    def get_child(self, symbol: str) -> INode:
        """Get a child node."""

        return self._children[symbol]

    def has_child(self, symbol: str) -> bool:
        """Check if the node has a child."""

        return symbol in self._children

    def clear_children(self) -> None:
        """Remove all children and from this node."""

        for _, child in self._children.items():
            child.clear_children()
            child.set_parent(None)

        self._children.clear()

    def get_path(self) -> str:
        """Get the database sentence this node represents."""

        if self._parent is None or self._parent.symbol == "root":
            return self._symbol

        parent_cardinality_op = (
            "!" if self._parent.cardinality == NodeCardinality.ONE else "."
        )

        return self._parent.get_path() + parent_cardinality_op + self._symbol

    @abstractmethod
    def copy(self) -> INode:
        """Create a copy of the node."""

        raise NotImplementedError()
