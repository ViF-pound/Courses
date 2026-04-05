import datetime

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.db import Base
if TYPE_CHECKING:
    from src.models.course_model import Course


class Lesson(Base):
    __tablename__ = "lessons_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    title:Mapped[str]
    summary:Mapped[str]
    position:Mapped[int]
    duration_minutes:Mapped[int]
    is_open:Mapped[bool]
    created_at:Mapped[datetime.date] = mapped_column(default=datetime.date.today())

    course_id:Mapped[int] = mapped_column(ForeignKey("courses_table.id", ondelete="CASCADE"))
    course:Mapped["Course"] = relationship(back_populates="lessons")