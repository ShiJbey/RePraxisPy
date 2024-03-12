"""Database Implementation.

"""

from repraxis.helpers import parse_sentence
from repraxis.nodes.base_types import INode, NodeCardinality, NodeType
from repraxis.nodes.nodes import SymbolNode


class RePraxisDatabase:
    """A database that manages a tree of data nodes to be queried."""

    __slots__ = ("_root",)

    _root: INode

    def __init__(self) -> None:
        self._root = SymbolNode("root", NodeCardinality.MANY)

    @property
    def root(self) -> INode:
        """The root node of the database."""
        return self._root

    def insert(self, sentence: str) -> None:
        """Insert a statement into the database."""

        nodes = parse_sentence(sentence)

        sub_tree: INode = self._root

        for node in nodes:
            if node.node_type == NodeType.VARIABLE:
                raise TypeError(
                    f"Found variable {node.symbol} in sentence '({sentence})'. "
                    "Sentence cannot contain variables when inserting a value."
                )

            if not sub_tree.has_child(node.symbol):
                if sub_tree.cardinality == NodeCardinality.ONE:
                    sub_tree.clear_children()

                sub_tree.add_child(node)
                sub_tree = node

            else:

                existing_node = sub_tree.get_child(node.symbol)

                if existing_node.cardinality != node.cardinality:
                    raise TypeError(
                        f"Cardinality mismatch on {node.symbol} in '{sentence}'."
                    )

                sub_tree = existing_node

    def assert_statement(self, sentence: str) -> bool:
        """Check if a given sentence exists within the database."""

        nodes = parse_sentence(sentence)

        current_node = self._root

        for i, node in enumerate(nodes):

            if node.node_type == NodeType.VARIABLE:
                raise TypeError(
                    f"Found variable {node.symbol} in sentence '({sentence})'. "
                    "Sentence cannot contain variables when asserting a value."
                )

            if not current_node.has_child(node.symbol):
                return False

            if i == len(nodes) - 1:
                return True

            current_node = current_node.get_child(node.symbol)

            if current_node.cardinality != node.cardinality:
                return False

        return True

    def delete(self, sentence: str) -> bool:
        """Delete a sentence from the database and any data in its sub_tree."""

        if sentence == "":
            return False

        nodes = parse_sentence(sentence)

        current_node = self._root

        for i, node in enumerate(nodes):

            if not current_node.has_child(node.symbol):
                return False

            current_node = current_node.get_child(node.symbol)

            if i == len(nodes) - 2:
                break

        last_node = nodes[-1]

        return current_node.remove_child(last_node.symbol)

    def clear(self) -> None:
        """Clear the contents of the database."""
        self._root.clear_children()

    def __contains__(self, key: str) -> bool:
        return self.assert_statement(key)
