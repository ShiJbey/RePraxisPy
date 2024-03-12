"""Query Helper Functions.

"""

from typing import Iterable

from repraxis.database import RePraxisDatabase
from repraxis.helpers import parse_sentence
from repraxis.nodes.base_types import INode, NodeType
from repraxis.query.query_binding_context import QueryBindingContext
from repraxis.query.query_state import QueryState


def unify(database: RePraxisDatabase, sentence: str) -> list[dict[str, INode]]:
    """Generate potential bindings from the database for a single sentence."""

    unified = [QueryBindingContext(database.root)]

    tokens = parse_sentence(sentence)

    for token in tokens:
        next_unified: list[QueryBindingContext] = []

        for entry in unified:
            for child in entry.sub_tree.children:
                if token.node_type == NodeType.VARIABLE:
                    unification = QueryBindingContext(
                        child, {key: value for key, value in entry.bindings.items()}
                    )
                    unification.bindings[token.symbol] = child
                    next_unified.append(unification)
                else:
                    if token.symbol == child.symbol:
                        next_unified.append(QueryBindingContext(child, entry.bindings))

        unified = next_unified

    return [
        unification.bindings for unification in unified if len(unification.bindings) > 0
    ]


def unify_all(
    database: RePraxisDatabase, state: QueryState, sentences: Iterable[str]
) -> list[dict[str, INode]]:
    """Generate potential bindings from the database unifying across all given sentences."""

    possible_bindings = [binding.copy() for binding in state.bindings]

    for sentence in sentences:
        iterative_bindings: list[dict[str, INode]] = []

        new_bindings = unify(database, sentence)

        if not possible_bindings:
            # Copy the new bindings to the iterative bindings list
            for binding in new_bindings:
                iterative_bindings.append(binding.copy())
        else:
            for old_binding in possible_bindings:
                for binding in new_bindings:
                    new_keys = [k for k in binding.keys() if k not in old_binding]
                    old_keys = [k for k in binding.keys() if k in old_binding]
                    exists_incompatible_key = any(
                        k for k in old_keys if not old_binding[k].equal_to(binding[k])
                    )

                    if exists_incompatible_key:
                        continue
                    else:
                        next_unification = old_binding.copy()

                        for k in new_keys:
                            next_unification[k] = binding[k]

                        iterative_bindings.append(next_unification)

        possible_bindings = iterative_bindings

    return [bindings for bindings in possible_bindings if len(bindings) > 0]
