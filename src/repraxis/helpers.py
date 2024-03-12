"""Various helper functions used by the database and query engine.

"""

from typing import Optional

from repraxis.nodes.base_types import INode, NodeCardinality, NodeType
from repraxis.nodes.nodes import FloatNode, IntNode, SymbolNode, VariableNode


def sentence_has_variables(sentence: str) -> bool:
    """Return True if the sentence contains any variables."""

    nodes = parse_sentence(sentence)
    return any(n.node_type == NodeType.VARIABLE for n in nodes)


def bind_sentence(sentence: str, bindings: dict[str, INode]) -> str:
    """Replace variables in the sentence using the given bindings."""

    nodes = parse_sentence(sentence)
    final_sentence: str = ""

    for i, node in enumerate(nodes):
        if node.node_type == NodeType.VARIABLE:
            if node.symbol in bindings:
                final_sentence += bindings[node.symbol].symbol
            else:
                final_sentence += node.symbol
        else:
            final_sentence += node.symbol

        if i < len(nodes) - 1:
            final_sentence += "!" if node.cardinality == NodeCardinality.ONE else "."

    return final_sentence


def create_sentence(nodes: list[INode]) -> str:
    """Create a new sentence from a collection of nodes."""
    sentence = ""

    for i, node in enumerate(nodes):
        sentence += node.symbol

        if i != len(nodes) - 1:
            sentence += "!" if node.cardinality == NodeCardinality.ONE else "."

    return sentence


def parse_sentence(sentence: str) -> list[INode]:
    """Breakup a database sentence into a series of nodes."""

    nodes: list[INode] = []

    current_token: str = ""

    for char in sentence:
        if char == "!" or char == ".":
            cardinality = NodeCardinality.ONE if char == "!" else NodeCardinality.MANY

            nodes.append(node_from_token(current_token, cardinality))

            current_token = ""
        else:
            current_token += char

    nodes.append(node_from_token(current_token, NodeCardinality.MANY))

    return nodes


def node_from_token(token: str, cardinality: NodeCardinality) -> INode:
    """Create a new node from a given string token."""

    def try_parse_int(token: str) -> Optional[int]:
        """Try to parse a string to an integer."""
        try:
            return int(token)
        except ValueError:
            return None

    def try_parse_float(token: str) -> Optional[float]:
        """Try to parse a string to a float."""
        try:
            return float(token)
        except ValueError:
            return None

    if token[0] == "?":
        return VariableNode(token, cardinality)

    if isinstance(value := try_parse_int(token), int):
        return IntNode(value, cardinality)

    if isinstance(value := try_parse_float(token), float):
        return FloatNode(value, cardinality)

    return SymbolNode(token, cardinality)


def node_from_object(obj: object) -> INode:
    """Create a new node from a given string token."""

    if isinstance(obj, int):
        return IntNode(obj, NodeCardinality.NONE)

    if isinstance(obj, float):
        return FloatNode(obj, NodeCardinality.NONE)

    if isinstance(obj, str):
        return SymbolNode(obj, NodeCardinality.NONE)

    raise TypeError(f"Cannot convert object of type {type(obj)} into a node.")
