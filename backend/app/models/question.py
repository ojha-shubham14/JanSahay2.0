from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (
        Index("ix_questions_category_id_display_order", "category_id", "display_order"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=True
    )
    field_key: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    help_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    why_we_ask: Mapped[str | None] = mapped_column(Text, nullable=True)
    answer_type: Mapped[str] = mapped_column(String(20), nullable=False)
    options_json: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    depends_on_key: Mapped[str | None] = mapped_column(String(60), nullable=True)
    depends_on_value: Mapped[str | None] = mapped_column(String(100), nullable=True)