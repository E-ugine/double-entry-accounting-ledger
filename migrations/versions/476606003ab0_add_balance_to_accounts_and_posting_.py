"""add balance to accounts and posting trigger

Revision ID: 476606003ab0
Revises: a80576538458
Create Date: 2026-09-26 12:36:01.982201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '476606003ab0'
down_revision: Union[str, None] = 'a80576538458'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "accounts",
        sa.Column("balance", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0"),
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION apply_journal_entry_posting() RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.status = 'posted' AND OLD.status IS DISTINCT FROM 'posted' THEN
                WITH line_sums AS (
                    SELECT
                        l.account_id,
                        SUM(CASE WHEN l.direction = 'debit' THEN l.amount ELSE 0 END) AS debit_sum,
                        SUM(CASE WHEN l.direction = 'credit' THEN l.amount ELSE 0 END) AS credit_sum
                    FROM lines l
                    WHERE l.journal_entry_id = NEW.id
                    GROUP BY l.account_id
                ),
                deltas AS (
                    SELECT
                        ls.account_id,
                        CASE
                            WHEN (CASE a.account_type
                                      WHEN 'asset' THEN 'debit'
                                      WHEN 'expense' THEN 'debit'
                                      ELSE 'credit'
                                  END) = 'debit'
                                THEN ls.debit_sum - ls.credit_sum
                            ELSE ls.credit_sum - ls.debit_sum
                        END AS delta
                    FROM line_sums ls
                    JOIN accounts a ON a.id = ls.account_id
                )
                UPDATE accounts acc
                SET balance = acc.balance + d.delta
                FROM deltas d
                WHERE acc.id = d.account_id;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.execute(
        """
        CREATE TRIGGER trg_apply_journal_entry_posting
        AFTER UPDATE ON journal_entries
        FOR EACH ROW
        EXECUTE FUNCTION apply_journal_entry_posting();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_apply_journal_entry_posting ON journal_entries;")
    op.execute("DROP FUNCTION IF EXISTS apply_journal_entry_posting();")
    op.drop_column("accounts", "balance")
