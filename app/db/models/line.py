from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, Text, Numeric, Integer, ForeignKey, CheckConstraint
from datetime import datetime
from sqlalchemy.sql import func
from decimal import Decimal

class Line(Base):
    __tablename__ = "lines"

    id : Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18,2))
    direction: Mapped[str] = mapped_column(String(100),nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    line_no : Mapped[int] = mapped_column(Integer(), nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    journal_entry_id : Mapped[int] = mapped_column(ForeignKey("journal_entries.id"))
    account_id : Mapped[int] = mapped_column(ForeignKey("accounts.id"))

    __table_args__ = (
    CheckConstraint("direction IN ('debit', 'credit')", name="ck_line_direction"),
    CheckConstraint("amount > 0", name="ck_line_amount"),
)

