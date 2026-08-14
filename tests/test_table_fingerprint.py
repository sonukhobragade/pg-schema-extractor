"""
Fingerprint tests for TableExtractor._generate_table_definition.

The fingerprint decides whether a schema change gets reported at all, so a gap
in it is silent: the run says "no change" and everyone believes it. These cases
each correspond to something the fingerprint used to miss.

No database connection is needed; the definition is built from a Table model.
"""

from __future__ import annotations

from datetime import datetime

import pytest

from src.extractors.table_extractor import TableExtractor
from src.models.database_objects import Column, Table


@pytest.fixture
def extractor():
    # __init__ only stores connection settings; nothing connects until extract().
    return TableExtractor(
        host="localhost", port=5432, dbname="db", user="u", password="p"
    )


def make_table(**overrides) -> Table:
    fields = {
        "name": "orders",
        "schema": "public",
        "oid": 16384,
        "owner": "app",
        "created_at": datetime(2026, 1, 1),
        "modified_at": datetime(2026, 1, 1),
        "columns": [
            Column(name="id", position=1, data_type="integer", nullable=False),
            Column(name="total", position=2, data_type="numeric", nullable=True),
        ],
    }
    fields.update(overrides)
    return Table(**fields)


def definition(extractor, table) -> str:
    return extractor._generate_table_definition(table)


class TestColumns:
    def test_columns_appear(self, extractor):
        d = definition(extractor, make_table())
        assert "id integer NOT NULL" in d
        assert "total numeric" in d

    def test_changed_type_changes_the_definition(self, extractor):
        before = definition(extractor, make_table())
        after = definition(extractor, make_table(columns=[
            Column(name="id", position=1, data_type="bigint", nullable=False),
            Column(name="total", position=2, data_type="numeric", nullable=True),
        ]))
        assert before != after


class TestIndexes:
    """Dropping an index used to leave the fingerprint unchanged."""

    def test_index_is_part_of_the_definition(self, extractor):
        without = definition(extractor, make_table())
        with_index = definition(extractor, make_table(indexes=[
            {"index_name": "orders_total_idx", "definition": "(total)"},
        ]))
        assert without != with_index
        assert "orders_total_idx" in with_index

    def test_index_order_does_not_matter(self, extractor):
        a = definition(extractor, make_table(indexes=[
            {"index_name": "idx_a", "definition": "(id)"},
            {"index_name": "idx_b", "definition": "(total)"},
        ]))
        b = definition(extractor, make_table(indexes=[
            {"index_name": "idx_b", "definition": "(total)"},
            {"index_name": "idx_a", "definition": "(id)"},
        ]))
        assert a == b, "catalogue ordering must not change the fingerprint"


class TestComments:
    """hash_utils says a changed comment is a real change worth surfacing."""

    def test_table_comment_is_included(self, extractor):
        without = definition(extractor, make_table())
        with_comment = definition(extractor, make_table(comment="Customer orders"))
        assert without != with_comment

    def test_changed_table_comment_changes_the_definition(self, extractor):
        a = definition(extractor, make_table(comment="Customer orders"))
        b = definition(extractor, make_table(comment="Customer orders, incl. refunds"))
        assert a != b

    def test_column_comment_is_included(self, extractor):
        plain = make_table()
        annotated = make_table(columns=[
            Column(name="id", position=1, data_type="integer", nullable=False),
            Column(name="total", position=2, data_type="numeric", nullable=True,
                   comment="Gross, minor units"),
        ])
        assert definition(extractor, plain) != definition(extractor, annotated)


class TestNoCreationTime:
    def test_definition_does_not_depend_on_timestamps(self, extractor):
        """PostgreSQL does not record table creation time, so these values are
        not a schema property and must not move the fingerprint."""
        a = definition(extractor, make_table(created_at=datetime(2026, 1, 1)))
        b = definition(extractor, make_table(created_at=datetime(2020, 6, 30)))
        assert a == b
