from pydantic import BaseModel


class DataCourse(BaseModel):

    title: str
    description: str
    category: str
    level: str


class FiltersCourse(BaseModel):

    category: str = ""
    level: str = ""
    is_published: bool | None
    search: str = ""
    sort_by: str = "created_at"
    sort_order: str = "asc"
    limit: int = 0
    offset: int = 0


class UpdateDataCourse(BaseModel):

    id: int
    title: str | None
    description: str | None
    category: str | None
    level: str | None
    is_published: bool = False