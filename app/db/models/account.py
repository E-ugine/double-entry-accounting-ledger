from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, CheckConstraint
from datetime import datetime
from sqlalchemy.sql import func



class Account(Base):
    __tablename__ = "accounts"

    id : Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name : Mapped[str] = mapped_column(String(100), nullable=False)
    account_type: Mapped[str] = mapped_column(String(100), nullable=False,)
    currency : Mapped[str] = mapped_column(String(3), nullable=False)
    is_active : Mapped[bool] = mapped_column(default=True)

    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(), nullable=False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (CheckConstraint("account_type IN ('asset', 'liability', 'equity', 'revenue', 'expense')",name="ck_account_type"),)




