"""Query Binding Context.

"""

from typing import Optional

from repraxis.nodes.base_types import INode


class QueryBindingContext:
    """Used internally to track bindings for a single sentence and the database."""

    __slots__ = ("_bindings", "_subtree")

    _bindings: dict[str, INode]
    _subtree: INode

    def __init__(
        self, sub_tree: INode, bindings: Optional[dict[str, INode]] = None
    ) -> None:
        self._subtree = sub_tree
        self._bindings = bindings if bindings else {}

    @property
    def bindings(self) -> dict[str, INode]:
        """Variable names mapped to their bound node values."""
        return self._bindings

    @property
    def sub_tree(self) -> INode:
        """The sub_tree of the database that these bindings apply to."""
        return self._subtree
