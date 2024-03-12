"""Concrete Node Class Definitions.

"""

from typing import cast

from .base_types import INode, Node, NodeCardinality, NodeType


class IntNode(Node[int]):
    """A node containing an integer value."""

    def __init__(self, value: int, cardinality: NodeCardinality) -> None:
        super().__init__(str(value), value, cardinality)
        self._node_type = NodeType.INT

    def equal_to(self, other: INode) -> bool:

        if other.node_type != self.node_type:
            return False

        return self.value == other.get_value()

    def not_equal_to(self, other: INode) -> bool:

        if other.node_type != self.node_type:
            return True

        return self.value != other.get_value()

    def greater_than_equal_to(self, other: INode) -> bool:

        if other.node_type != NodeType.INT and other.node_type != NodeType.FLOAT:

            raise TypeError(
                ">= not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        if other.node_type == NodeType.FLOAT:
            return self.value >= cast(FloatNode, other).value

        return self.value >= cast(IntNode, other).value

    def less_than_equal_to(self, other: INode) -> bool:

        if other.node_type != NodeType.INT and other.node_type != NodeType.FLOAT:

            raise TypeError(
                "<= not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        if other.node_type == NodeType.FLOAT:
            return self.value <= cast(FloatNode, other).value

        return self.value <= cast(IntNode, other).value

    def greater_than(self, other: INode) -> bool:

        if other.node_type != NodeType.INT and other.node_type != NodeType.FLOAT:

            raise TypeError(
                "> not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        if other.node_type == NodeType.FLOAT:
            return self.value > cast(FloatNode, other).value

        return self.value > cast(IntNode, other).value

    def less_than(self, other: INode) -> bool:

        if other.node_type != NodeType.INT and other.node_type != NodeType.FLOAT:

            raise TypeError(
                ">= not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        if other.node_type == NodeType.FLOAT:
            return self.value < cast(FloatNode, other).value

        return self.value < cast(IntNode, other).value

    def copy(self) -> INode:
        return IntNode(self.value, self.cardinality)


class FloatNode(Node[float]):
    """A node containing a floating point value."""

    def __init__(self, value: float, cardinality: NodeCardinality) -> None:
        super().__init__(f"{value:.3E}", value, cardinality)
        self._node_type = NodeType.FLOAT

    def equal_to(self, other: INode) -> bool:

        if other.node_type != self.node_type:
            return False

        return self.value == other.get_value()

    def not_equal_to(self, other: INode) -> bool:

        if other.node_type != self.node_type:
            return True

        return self.value != other.get_value()

    def greater_than_equal_to(self, other: INode) -> bool:

        if other.node_type != NodeType.INT and other.node_type != NodeType.FLOAT:

            raise TypeError(
                ">= not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        if other.node_type == NodeType.FLOAT:
            return self.value >= cast(FloatNode, other).value

        return self.value >= cast(IntNode, other).value

    def less_than_equal_to(self, other: INode) -> bool:

        if other.node_type != NodeType.INT and other.node_type != NodeType.FLOAT:

            raise TypeError(
                "<= not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        if other.node_type == NodeType.FLOAT:
            return self.value <= cast(FloatNode, other).value

        return self.value <= cast(IntNode, other).value

    def greater_than(self, other: INode) -> bool:

        if other.node_type != NodeType.INT and other.node_type != NodeType.FLOAT:

            raise TypeError(
                "> not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        if other.node_type == NodeType.FLOAT:
            return self.value > cast(FloatNode, other).value

        return self.value > cast(IntNode, other).value

    def less_than(self, other: INode) -> bool:

        if other.node_type != NodeType.INT and other.node_type != NodeType.FLOAT:

            raise TypeError(
                ">= not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        if other.node_type == NodeType.FLOAT:
            return self.value < cast(FloatNode, other).value

        return self.value < cast(IntNode, other).value

    def copy(self) -> INode:
        return FloatNode(self.value, self.cardinality)


class SymbolNode(Node[str]):
    """A node containing a string/symbolic value."""

    def __init__(self, value: str, cardinality: NodeCardinality) -> None:
        super().__init__(value, value, cardinality)
        self._node_type = NodeType.SYMBOL

    def equal_to(self, other: INode) -> bool:

        if other.node_type != self.node_type:
            return False

        return self.value == other.get_value()

    def not_equal_to(self, other: INode) -> bool:

        if other.node_type != self.node_type:
            return True

        return self.value != other.get_value()

    def greater_than_equal_to(self, other: INode) -> bool:
        if other.node_type != self.node_type:
            raise TypeError(
                ">= not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        return self.value >= cast(SymbolNode, other).value

    def less_than_equal_to(self, other: INode) -> bool:
        if other.node_type != self.node_type:
            raise TypeError(
                "<= not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        return self.value <= cast(SymbolNode, other).value

    def greater_than(self, other: INode) -> bool:
        if other.node_type != self.node_type:
            raise TypeError(
                "> not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        return self.value > cast(SymbolNode, other).value

    def less_than(self, other: INode) -> bool:
        if other.node_type != self.node_type:
            raise TypeError(
                "< not defined between nodes of type "
                f"{self.node_type} and {other.node_type}"
            )

        return self.value < cast(SymbolNode, other).value

    def copy(self) -> INode:
        return SymbolNode(self.value, self.cardinality)


class VariableNode(Node[str]):
    """A node containing a variable."""

    def __init__(self, value: str, cardinality: NodeCardinality) -> None:
        super().__init__(value, value, cardinality)
        self._node_type = NodeType.VARIABLE

    def equal_to(self, other: INode) -> bool:

        if other.node_type != self.node_type:
            return False

        return self.value == other.get_value()

    def not_equal_to(self, other: INode) -> bool:

        if other.node_type != self.node_type:
            return True

        return self.value != other.get_value()

    def greater_than_equal_to(self, other: INode) -> bool:
        raise TypeError(
            ">= not defined between nodes of type "
            f"{self.node_type} and {other.node_type}"
        )

    def less_than_equal_to(self, other: INode) -> bool:
        raise TypeError(
            "<= not defined between nodes of type "
            f"{self.node_type} and {other.node_type}"
        )

    def greater_than(self, other: INode) -> bool:
        raise TypeError(
            "> not defined between nodes of type "
            f"{self.node_type} and {other.node_type}"
        )

    def less_than(self, other: INode) -> bool:
        raise TypeError(
            "< not defined between nodes of type "
            f"{self.node_type} and {other.node_type}"
        )

    def copy(self) -> INode:
        return VariableNode(self.value, self.cardinality)
