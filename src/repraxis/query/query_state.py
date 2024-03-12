"""Query State.

"""

from __future__ import annotations

from typing import Iterable, Optional

from repraxis.helpers import node_from_object
from repraxis.nodes.base_types import INode
from repraxis.query.query_result import QueryResult


class QueryState:
    """The intermediate state of a query while processing expressions."""

    __slots__ = ("success", "bindings")

    success: bool
    bindings: list[dict[str, INode]]

    def __init__(
        self, success: bool, bindings: Optional[Iterable[dict[str, INode]]] = None
    ) -> None:
        self.success = success
        self.bindings = list(bindings) if bindings else []

    def to_result(self) -> QueryResult:
        """Convert the state to a result."""

        if self.success is False:
            return QueryResult(False)

        results: list[dict[str, object]] = []

        for entry in self.bindings:
            results.append({k: v.get_value() for k, v in entry.items()})

        return QueryResult(True, results)

    @classmethod
    def from_object_bindings(
        cls, success: bool, bindings: Iterable[dict[str, object]]
    ) -> QueryState:
        """Create a new QueryState using bindings of strings to objects."""

        new_bindings: list[dict[str, INode]] = []
        for entry in bindings:
            new_bindings.append({k: node_from_object(v) for k, v in entry.items()})

        return cls(success, new_bindings)
