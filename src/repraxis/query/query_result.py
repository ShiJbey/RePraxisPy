"""RePraxis Query Result.

"""

from __future__ import annotations

from typing import Optional


class QueryResult:
    """Returned by queries indicating if it passed and what bindings it found."""

    __slots__ = ("_success", "_bindings")

    _success: bool
    _bindings: list[dict[str, object]]

    def __init__(
        self, success: bool, bindings: Optional[list[dict[str, object]]] = None
    ) -> None:
        self._success = success
        self._bindings = bindings if bindings else []

    @property
    def success(self) -> bool:
        """Did the query pass."""
        return self._success

    @property
    def bindings(self) -> list[dict[str, object]]:
        """Bindings for any variables present in the query."""
        return self._bindings

    def limit_to_vars(self, *args: str) -> QueryResult:
        """Filter the results to only include the given variables."""

        if self._success is False:
            return QueryResult(False)

        if len(args) == 0:
            return QueryResult(True)

        filtered_results: list[dict[str, object]] = []

        for result in self._bindings:
            filtered_results.append({k: v for (k, v) in result.items() if k in args})

        return QueryResult(True, filtered_results)
