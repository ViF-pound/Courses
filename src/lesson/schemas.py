from pydantic import BaseModel


class DataLesson(BaseModel):

    title: str
    summary: str
    position: int
    duration_minutes: int
    is_open: bool = False
    course_id: int


class NewDataLesson(BaseModel):

    title: str | None
    summary: str | None
    position: int | None
    duration_minutes: int | None
    is_open: bool = False