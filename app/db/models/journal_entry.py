from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, Text, CheckConstraint
from datetime import datetime
from sqlalchemy.sql import func


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    entry_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    memo : Mapped[str] = mapped_column(Text, nullable=True)
    reference : Mapped[str] = mapped_column(String(100), nullable=True)
    source : Mapped[str] = mapped_column(String(64), nullable=True)
    status : Mapped[str] = mapped_column(String(100), default="draft")
    posted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=True)
    
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = CheckConstraint("status IN ('draft', 'posted')", name="ck_journal_entry_status")