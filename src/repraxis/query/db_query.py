"""RePraxis Database Query.

"""

from __future__ import annotations

from typing import Iterable, Optional

from repraxis.database import RePraxisDatabase
from repraxis.query.expressions import (
    AssertExpression,
    EqualsExpression,
    GreaterThanEqualToExpression,
    GreaterThanExpression,
    LessThanEqualToExpression,
    LessThanExpression,
    NotEqualExpression,
    NotExpression,
)
from repraxis.query.query_result import QueryResult
from repraxis.query.query_state import QueryState


class DBQuery:
    """A query to run against a database.

    Queries are immutable. Adding additional expressions creates a new query
    instance.
    """

    __slots__ = ("_expressions",)

    _expressions: list[str]

    def __init__(self, expressions: Optional[Iterable[str]] = None) -> None:
        self._expressions = list(expressions) if expressions else []

    def where(self, expression: str) -> DBQuery:
        """Add an expression to the query"""
        return DBQuery([*self._expressions, expression])

    def run(
        self,
        db: RePraxisDatabase,
        bindings: Optional[Iterable[dict[str, object]]] = None,
    ) -> QueryResult:
        """Run the query against the database."""

        state = QueryState.from_object_bindings(True, bindings if bindings else [])

        for expression_str in self._expressions:

            expression_parts = [part.strip() for part in expression_str.split(" ")]

            if len(expression_parts) == 1:
                state = AssertExpression(expression_parts[0]).evaluate(db, state)

            elif len(expression_parts) == 2:
                if expression_parts[0] == "not":
                    state = NotExpression(expression_parts[1]).evaluate(db, state)
                else:
                    raise ValueError(f"Unrecognized query expression: {expression_str}")

            elif len(expression_parts) == 3:
                comparison_op = expression_parts[0]

                if comparison_op == "eq":
                    state = EqualsExpression(
                        expression_parts[1], expression_parts[2]
                    ).evaluate(db, state)
                elif comparison_op == "neq":
                    state = NotEqualExpression(
                        expression_parts[1], expression_parts[2]
                    ).evaluate(db, state)
                elif comparison_op == "lt":
                    state = LessThanExpression(
                        expression_parts[1], expression_parts[2]
                    ).evaluate(db, state)
                elif comparison_op == "gt":
                    state = GreaterThanExpression(
                        expression_parts[1], expression_parts[2]
                    ).evaluate(db, state)
                elif comparison_op == "lte":
                    state = LessThanEqualToExpression(
                        expression_parts[1], expression_parts[2]
                    ).evaluate(db, state)
                elif comparison_op == "gte":
                    state = GreaterThanEqualToExpression(
                        expression_parts[1], expression_parts[2]
                    ).evaluate(db, state)
                else:
                    raise ValueError(f"Unrecognized query expression: {expression_str}")
            else:
                raise ValueError(f"Unrecognized query expression: {expression_str}")

        return state.to_result()
