# pylint: disable=C0116,W0621

"""Test the repraxis package.

"""

import pytest

from repraxis import RePraxisDatabase
from repraxis.query import DBQuery


@pytest.fixture
def db():
    database = RePraxisDatabase()

    database.insert("astrid.relationships.jordan.reputation!30")
    database.insert("astrid.relationships.jordan.tags.rivalry")
    database.insert("astrid.relationships.britt.reputation!-10")
    database.insert("astrid.relationships.britt.tags.ex_lover")
    database.insert("astrid.relationships.lee.reputation!20")
    database.insert("astrid.relationships.lee.tags.friend")
    database.insert("britt.relationships.player.tags.spouse")
    database.insert("player.relationships.jordan.reputation!-20")
    database.insert("player.relationships.jordan.tags.enemy")
    database.insert("player.relationships.britt.tags.spouse")

    return database


def test_insert_sentence():

    db = RePraxisDatabase()

    db.insert("A.relationships.B.reputation!10")
    db.insert("A.relationships.B.type!rivalry")

    assert not db.assert_statement("A.relationships.B.reputation!19")
    assert db.assert_statement("A.relationships.B.type")
    assert db.assert_statement("A")


def test_delete_sentence():

    db = RePraxisDatabase()

    db.insert("A.relationships.B.reputation!10")
    db.delete("A.relationships.B.reputation")

    assert db.assert_statement("A.relationships.B.reputation") is False


def test_update_sentence():

    db = RePraxisDatabase()

    db.insert("A.relationships.B.reputation!10")
    db.insert("A.relationships.B.reputation!-99")

    assert db.assert_statement("A.relationships.B.reputation!-99")
    assert not db.assert_statement("A.relationships.B.reputation.-99")


def test_assert_expression_no_vars(db: RePraxisDatabase):
    query = DBQuery().where("astrid.relationships.britt")
    result = query.run(db)

    assert result.success
    assert len(result.bindings) == 0


def test_failing_assert_expression_no_vars(db: RePraxisDatabase):
    query = DBQuery().where("astrid.relationships.haley")
    result = query.run(db)

    assert not result.success
    assert len(result.bindings) == 0


def test_gte_expression(db: RePraxisDatabase):
    query = (
        DBQuery().where("astrid.relationships.?other.reputation!?r").where("gte ?r 10")
    )
    result = query.run(db)

    assert result.success is True
    assert len(result.bindings) == 2


def test_gte_expression_with_bindings(db: RePraxisDatabase):
    query = (
        DBQuery().where("astrid.relationships.?other.reputation!?r").where("gte ?r 10")
    )
    result = query.run(db, [{"?other": "lee"}])

    assert result.success is True
    assert len(result.bindings) == 1


def test_lte_with_multiple_vars(db: RePraxisDatabase):
    # Relational expression with multiple variables
    query = DBQuery().where("?A.relationships.?other.reputation!?r").where("lte ?r 0")
    result = query.run(db)

    assert result.success is True
    assert len(result.bindings) == 2


def test_not_expression(db: RePraxisDatabase):
    # Check that a sentence without variables is not true within the database
    query = DBQuery().where("not player.relationships.jordan.reputation!30")
    result = query.run(db)

    assert result.success is True


def test_not_expression_with_vars(db: RePraxisDatabase):
    query = DBQuery().where("not astrid.relationships.?other.reputation!15")
    result = query.run(db)
    assert result.success is True


def test_neq_expression_with_vars(db: RePraxisDatabase):
    query = (
        DBQuery()
        .where("astrid.relationships.?other.reputation!?rep")
        .where("neq ?rep 30")
    )
    result = query.run(db)
    assert result.success is True
    assert len(result.bindings) == 2  # britt and lee


def test_not_expression_with_bindings(db: RePraxisDatabase):
    query = DBQuery().where("not player.relationships.?other.reputation!30")
    result = query.run(db, [{"?other": "jordan"}])
    assert result.success is True


def test_compound_not_queries(db: RePraxisDatabase):
    # For all relationships astrid has with an ?other
    # filter for those where reputation is not 30
    query = (
        DBQuery()
        .where("astrid.relationships.?other")
        .where("not astrid.relationships.?other.reputation!30")
    )
    result = query.run(db)
    assert result.success is True
    assert len(result.bindings) == 2  # britt and lee

    # For all relationships astrid has with an ?other
    # filter for those where reputation from astrid to ?other is not 30
    # and ?other does not have a relationship with a spouse tag
    query = (
        DBQuery()
        .where("astrid.relationships.?other")
        .where("not astrid.relationships.?other.reputation!30")
        .where("not ?other.relationships.?others_spouse.tags.spouse")
    )
    result = query.run(db)
    assert result.success is True
    assert len(result.bindings) == 1  # lee

    # For all relationships astrid has with an ?other
    # filter for those where reputation from astrid to ?other is not 30.
    # Also ensure that the player does not have a spouse
    query = (
        DBQuery()
        .where("astrid.relationships.?other")
        .where("not astrid.relationships.?other.reputation!30")
        .where("not player.relationships.?x.tags.spouse")
    )
    result = query.run(db)
    assert result.success is False

    # For all relationships astrid has with an ?other
    # filter for those where reputation from astrid to ?other is not 30.
    # Also ensure that the player does not have any friends
    query = (
        DBQuery()
        .where("astrid.relationships.?other")
        .where("not astrid.relationships.?other.reputation!30")
        .where("not player.relationships.?x.tags.friend")
    )
    result = query.run(db)
    assert result.success is True


def test_compound_query_with_vars(db: RePraxisDatabase):
    # Compound query with multiple variables
    query = (
        DBQuery()
        .where("?speaker.relationships.?other.reputation!?r0")
        .where("gt ?r0 10")
        .where("player.relationships.?other.reputation!?r1")
        .where("lt ?r1 0")
        .where("neq ?speaker player")
    )

    result = query.run(db)

    assert result.success is True
    assert len(result.bindings) == 1


def test_results_data_types(db: RePraxisDatabase):
    # Compound query with multiple variables
    query = (
        DBQuery()
        .where("?speaker.relationships.?other.reputation!?r0")
        .where("gt ?r0 10")
        .where("player.relationships.?other.reputation!?r1")
        .where("lt ?r1 0")
        .where("neq ?speaker player")
    )

    result = query.run(db)

    assert result.success is True
    assert len(result.bindings) == 1
    assert isinstance(result.bindings[0]["?speaker"], str)
    assert isinstance(result.bindings[0]["?other"], str)
    assert isinstance(result.bindings[0]["?r0"], int)
    assert isinstance(result.bindings[0]["?r1"], int)


def test_remove_nonexistent_data():
    db = RePraxisDatabase()

    result = db.delete("katara")

    assert result is False


def test_empty_query(db: RePraxisDatabase):
    result = DBQuery().run(db)

    assert result.success is True
