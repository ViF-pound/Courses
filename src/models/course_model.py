import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base
from src.models.lesson_model import Lesson


class Course(Base):
    __tablename__ = "courses_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    title:Mapped[str]
    description:Mapped[str]
    category:Mapped[str]
    level:Mapped[str]
    is_published:Mapped[bool] = mapped_column(default=False)
    created_at:Mapped[datetime.date] = mapped_column(default=datetime.date.today())

    lessons:Mapped["Lesson"] = relationship(back_populates="course", uselist=True)
