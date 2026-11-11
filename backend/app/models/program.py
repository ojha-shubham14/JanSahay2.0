from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Date, DateTime, ForeignKey, Index, Numeric, String, Text, func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Program(Base):
    __tablename__ = "programs"
    __table_args__ = (
        Index(
            "ix_programs_status_category_govt_state",
            "status", "category_id", "govt_level", "state_code",
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False
    )
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("admin_users.id", ondelete="RESTRICT"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    abbreviation: Mapped[str | None] = mapped_column(String(40), nullable=True)
    govt_level: Mapped[str] = mapped_column(String(10), nullable=False)
    state_code: Mapped[str | None] = mapped_column(String(5), nullable=True)
    primary_type: Mapped[str] = mapped_column(String(20), nullable=False)
    purpose: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    benefit_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    amount_min: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    amount_max: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    interest_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tenure_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    implementing_authority: Mapped[str | None] = mapped_column(String(255), nullable=True)
    operational_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="unclear"
    )
    application_window_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    scheme_version: Mapped[str | None] = mapped_column(String(40), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")
    last_verified_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )