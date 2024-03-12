"""Query Expression Abstract Base Types.

"""

from abc import ABC, abstractmethod

from repraxis.database import RePraxisDatabase
from repraxis.query.query_state import QueryState


class IQueryExpression(ABC):
    """An expression evaluated as part of a database query."""

    @abstractmethod
    def evaluate(self, database: RePraxisDatabase, state: QueryState) -> QueryState:
        """Evaluate the expression and return a new query state."""

        raise NotImplementedError()
