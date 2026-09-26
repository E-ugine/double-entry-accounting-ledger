"""prevent posted journal entries from being unposted

Revision ID: fc5e6daaef57
Revises: 476606003ab0
Create Date: 2026-09-26 12:46:38.363570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc5e6daaef57'
down_revision: Union[str, None] = '476606003ab0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION prevent_unposting_journal_entry() RETURNS TRIGGER AS $$
        BEGIN
            IF OLD.status = 'posted' AND NEW.status IS DISTINCT FROM 'posted' THEN
                RAISE EXCEPTION 'journal_entries.status cannot change away from posted (entry id %)', OLD.id;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.execute(
        """
        CREATE TRIGGER trg_prevent_unposting_journal_entry
        BEFORE UPDATE ON journal_entries
        FOR EACH ROW
        EXECUTE FUNCTION prevent_unposting_journal_entry();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_prevent_unposting_journal_entry ON journal_entries;")
    op.execute("DROP FUNCTION IF EXISTS prevent_unposting_journal_entry();")
