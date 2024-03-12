"""Concrete Query Expression Types.

"""

from repraxis.database import RePraxisDatabase
from repraxis.helpers import bind_sentence, parse_sentence, sentence_has_variables
from repraxis.nodes.base_types import INode
from repraxis.query.base_types import IQueryExpression
from repraxis.query.helpers import unify_all
from repraxis.query.query_state import QueryState


class AssertExpression(IQueryExpression):
    """Asserts a given statement is in the database."""

    __slots__ = ("statement",)

    statement: str

    def __init__(self, statement: str) -> None:
        super().__init__()
        self.statement = statement

    def evaluate(self, database: RePraxisDatabase, state: QueryState) -> QueryState:
        if sentence_has_variables(self.statement):
            bindings = unify_all(database, state, [self.statement])

            if len(bindings) == 0:
                return QueryState(False)

            valid_bindings = [
                binding
                for binding in bindings
                if database.assert_statement(bind_sentence(self.statement, binding))
            ]

            if len(valid_bindings) == 0:
                return QueryState(False)

            return QueryState(True, valid_bindings)

        if not database.assert_statement(self.statement):
            return QueryState(False)

        return state


class EqualsExpression(IQueryExpression):
    """Evaluates if two values have the same value."""

    __slots__ = ("lh_value", "rh_value")

    lh_value: str
    rh_value: str

    def __init__(self, lh_value: str, rh_value: str) -> None:
        self.lh_value = lh_value
        self.rh_value = rh_value

    def evaluate(self, database: RePraxisDatabase, state: QueryState) -> QueryState:
        lh_nodes = parse_sentence(self.lh_value)
        rh_nodes = parse_sentence(self.rh_value)

        if len(lh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.lh_value} has too many parts."
            )

        if len(rh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.rh_value} has too many parts."
            )

        # If no bindings are found and at least one of the values is a variable,
        # then the query has failed.
        if len(state.bindings) == 0 and (
            sentence_has_variables(self.lh_value)
            or sentence_has_variables(self.rh_value)
        ):
            return QueryState(False)

        # Loop through the bindings and find those where the bound values
        # are equivalent.
        valid_bindings = [
            binding
            for binding in state.bindings
            if parse_sentence(bind_sentence(self.lh_value, binding))[0].equal_to(
                parse_sentence(bind_sentence(self.rh_value, binding))[0]
            )
        ]

        if not valid_bindings:
            return QueryState(False)

        return QueryState(True, valid_bindings)


class NotEqualExpression(IQueryExpression):
    """Evaluates if two values do not the same value."""

    __slots__ = ("lh_value", "rh_value")

    lh_value: str
    rh_value: str

    def __init__(self, lh_value: str, rh_value: str) -> None:
        self.lh_value = lh_value
        self.rh_value = rh_value

    def evaluate(self, database: RePraxisDatabase, state: QueryState) -> QueryState:
        lh_nodes = parse_sentence(self.lh_value)
        rh_nodes = parse_sentence(self.rh_value)

        if len(lh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.lh_value} has too many parts."
            )

        if len(rh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.rh_value} has too many parts."
            )

        # If no bindings are found and at least one of the values is a variable,
        # then the query has failed.
        if len(state.bindings) == 0 and (
            sentence_has_variables(self.lh_value)
            or sentence_has_variables(self.rh_value)
        ):
            return QueryState(False)

        # Loop through the bindings and find those where the bound values
        # are equivalent.
        valid_bindings = [
            binding
            for binding in state.bindings
            if parse_sentence(bind_sentence(self.lh_value, binding))[0].not_equal_to(
                parse_sentence(bind_sentence(self.rh_value, binding))[0]
            )
        ]

        if not valid_bindings:
            return QueryState(False)

        return QueryState(True, valid_bindings)


class GreaterThanEqualToExpression(IQueryExpression):
    """Check if one expression's value is greater than or equal to another's"""

    __slots__ = ("lh_value", "rh_value")

    lh_value: str
    rh_value: str

    def __init__(self, lh_value: str, rh_value: str) -> None:
        self.lh_value = lh_value
        self.rh_value = rh_value

    def evaluate(self, database: RePraxisDatabase, state: QueryState) -> QueryState:
        lh_nodes = parse_sentence(self.lh_value)
        rh_nodes = parse_sentence(self.rh_value)

        if len(lh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.lh_value} has too many parts."
            )

        if len(rh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.rh_value} has too many parts."
            )

        # If no bindings are found and at least one of the values is a variable,
        # then the query has failed.
        if len(state.bindings) == 0 and (
            sentence_has_variables(self.lh_value)
            or sentence_has_variables(self.rh_value)
        ):
            return QueryState(False)

        # Loop through the bindings and find those where the bound left value
        # is greater than or equal to the right.
        valid_bindings = [
            binding
            for binding in state.bindings
            if (
                parse_sentence(bind_sentence(self.lh_value, binding))[
                    0
                ].greater_than_equal_to(
                    parse_sentence(bind_sentence(self.rh_value, binding))[0]
                )
            )
        ]

        if not valid_bindings:
            return QueryState(False)

        return QueryState(True, valid_bindings)


class GreaterThanExpression(IQueryExpression):
    """Check if one expression's value is greater than another's"""

    __slots__ = ("lh_value", "rh_value")

    lh_value: str
    rh_value: str

    def __init__(self, lh_value: str, rh_value: str) -> None:
        self.lh_value = lh_value
        self.rh_value = rh_value

    def evaluate(self, database: RePraxisDatabase, state: QueryState) -> QueryState:
        lh_nodes = parse_sentence(self.lh_value)
        rh_nodes = parse_sentence(self.rh_value)

        if len(lh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.lh_value} has too many parts."
            )

        if len(rh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.rh_value} has too many parts."
            )

        # If no bindings are found and at least one of the values is a variable,
        # then the query has failed.
        if len(state.bindings) == 0 and (
            sentence_has_variables(self.lh_value)
            or sentence_has_variables(self.rh_value)
        ):
            return QueryState(False)

        # Loop through the bindings and find those where the bound left value
        # is greater than or equal to the right.
        valid_bindings = [
            binding
            for binding in state.bindings
            if (
                parse_sentence(bind_sentence(self.lh_value, binding))[0].greater_than(
                    parse_sentence(bind_sentence(self.rh_value, binding))[0]
                )
            )
        ]

        if not valid_bindings:
            return QueryState(False)

        return QueryState(True, valid_bindings)


class LessThanExpression(IQueryExpression):
    """Check if one expression's value is less than another's"""

    __slots__ = ("lh_value", "rh_value")

    lh_value: str
    rh_value: str

    def __init__(self, lh_value: str, rh_value: str) -> None:
        self.lh_value = lh_value
        self.rh_value = rh_value

    def evaluate(self, database: RePraxisDatabase, state: QueryState) -> QueryState:
        lh_nodes = parse_sentence(self.lh_value)
        rh_nodes = parse_sentence(self.rh_value)

        if len(lh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.lh_value} has too many parts."
            )

        if len(rh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.rh_value} has too many parts."
            )

        # If no bindings are found and at least one of the values is a variable,
        # then the query has failed.
        if len(state.bindings) == 0 and (
            sentence_has_variables(self.lh_value)
            or sentence_has_variables(self.rh_value)
        ):
            return QueryState(False)

        # Loop through the bindings and find those where the bound left value
        # is greater than or equal to the right.
        valid_bindings = [
            binding
            for binding in state.bindings
            if (
                parse_sentence(bind_sentence(self.lh_value, binding))[0].less_than(
                    parse_sentence(bind_sentence(self.rh_value, binding))[0]
                )
            )
        ]

        if not valid_bindings:
            return QueryState(False)

        return QueryState(True, valid_bindings)


class LessThanEqualToExpression(IQueryExpression):
    """Check if one expression's value is less than or equal to another's"""

    __slots__ = ("lh_value", "rh_value")

    lh_value: str
    rh_value: str

    def __init__(self, lh_value: str, rh_value: str) -> None:
        self.lh_value = lh_value
        self.rh_value = rh_value

    def evaluate(self, database: RePraxisDatabase, state: QueryState) -> QueryState:
        lh_nodes = parse_sentence(self.lh_value)
        rh_nodes = parse_sentence(self.rh_value)

        if len(lh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.lh_value} has too many parts."
            )

        if len(rh_nodes) > 1:
            raise ValueError(
                "Comparator expression may only be single variables, symbols, "
                f"or constants. {self.rh_value} has too many parts."
            )

        # If no bindings are found and at least one of the values is a variable,
        # then the query has failed.
        if len(state.bindings) == 0 and (
            sentence_has_variables(self.lh_value)
            or sentence_has_variables(self.rh_value)
        ):
            return QueryState(False)

        # Loop through the bindings and find those where the bound left value
        # is greater than or equal to the right.
        valid_bindings = [
            binding
            for binding in state.bindings
            if (
                parse_sentence(bind_sentence(self.lh_value, binding))[
                    0
                ].less_than_equal_to(
                    parse_sentence(bind_sentence(self.rh_value, binding))[0]
                )
            )
        ]

        if not valid_bindings:
            return QueryState(False)

        return QueryState(True, valid_bindings)


class NotExpression(IQueryExpression):
    """Perform a not expression"""

    __slots__ = ("statement",)

    def __init__(self, statement: str):
        self.statement = statement

    def evaluate(self, database: RePraxisDatabase, state: QueryState) -> QueryState:
        if sentence_has_variables(self.statement):
            # If there are no existing bindings, then this is the first statement in the query
            # or no previous statements contained variables.
            if len(state.bindings) == 0:
                # We need to find bindings for all of the variables in this expression
                bindings = unify_all(database, state, [self.statement])

                # If bindings for variables are found then we know this expression fails
                # because we want to ensure that the statement is never true
                if bindings:
                    return QueryState(False)

                # Continue the query.
                return state

            # If we have existing bindings, we need to filter the existing bindings
            valid_bindings = [
                binding
                for binding in state.bindings
                if self._evaluate_binding(database, binding)
            ]

            if not valid_bindings:
                return QueryState(False)

            return QueryState(True, valid_bindings)

        if database.assert_statement(self.statement):
            return QueryState(False)

        return state

    def _evaluate_binding(
        self, database: RePraxisDatabase, binding: dict[str, INode]
    ) -> bool:
        # Try to build a new sentence from the bindings and the expression's
        # statement.
        sentence = bind_sentence(self.statement, binding)

        if sentence_has_variables(sentence):
            # Treat the new sentence like it's the first in the query
            # and do a sub-unification, swapping out the state for an empty
            # one without existing bindings
            scoped_bindings = unify_all(database, QueryState(True), [sentence])

            # If any of the remaining variables are bound in the scoped
            # bindings, then the entire binding fails
            if scoped_bindings:
                return False

            return True

        return not database.assert_statement(sentence)
