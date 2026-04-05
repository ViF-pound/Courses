from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.course_model import Course
from src.course.schemas import DataCourse, FiltersCourse, UpdateDataCourse
from src.db import get_session
from src.lesson.lesson_router import return_lessons


course_router = APIRouter(prefix="/courses", tags=["Courses"])


@course_router.post("/create")
async def create_course(data: DataCourse, session: AsyncSession = Depends(get_session)):

    course_data = data.model_dump()

    course = Course(**course_data)

    session.add(course)
    await session.commit()

    return {"status_ code": 200, "detail": "courses created", "detail": course_data}
    

@course_router.post("/filtration")
async def return_course(filters: FiltersCourse, session: AsyncSession = Depends(get_session)):

    query = select(Course)
    
    if filters.category:
        query = query.where(Course.category == filters.category)

    if filters.level:
        query = query.where(Course.level == filters.level)

    if filters.is_published != None:
        query = query.where(Course.is_published == filters.is_published)

    if filters.search:
        query = query.where(Course.title.ilike(f"%{filters.search}%"))

    if filters.sort_by:
        if filters.sort_by == "title":
            if filters.sort_order == "asc":
                query = query.order_by(Course.title.asc())
            elif filters.sort_order == "desc":
                query = query.order_by(Course.title.desc())
        elif filters.sort_by == "created_at":
            if filters.sort_order == "asc":
                query = query.order_by(Course.created_at.asc())
            elif filters.sort_order == "desc":
                query = query.order_by(Course.created_at.desc())

    if filters.limit:
        query = query.limit(filters.limit)

    if filters.offset:
        query = query.offset(filters.offset)

    courses = await session.scalars(query)

    return courses.all()


@course_router.put("/update")
async def update_course(new_data: UpdateDataCourse, session: AsyncSession = Depends(get_session)):

    course = await session.scalar(select(Course).where(Course.id == new_data.id))
    if not course:
        raise HTTPException(status_code=404, detail="not found")

    if new_data.title:
        course.title = new_data.title

    if new_data.description:
        course.description = new_data.description

    if new_data.category:
        course.category = new_data.category

    if new_data.level:
        course.level = new_data.level

    if new_data.is_published:
        course.is_published = new_data.is_published

    await session.commit()
    await session.refresh(course)

    return {"status_code": 200, "detail": "update successful", "data": course}


@course_router.get("/return/{id}")
async def return_course(id: int, session: AsyncSession = Depends(get_session)):

    course = await session.scalar(select(Course).where(Course.id == id))
    if not course:
        raise HTTPException(status_code=404, detail="not found")

    lessons = await return_lessons(id, session)

    lessons_count = len(lessons)
    open_lessons_count = 0
    total_duration_minutes = 0
    for lesson in lessons:
        if lesson.is_open:
            open_lessons_count += 1
        total_duration_minutes += lesson.duration_minutes
    
    return {"course": course,
            "lessons": lessons,
            "stat": {
                "lessons_count": lessons_count,
                "open_lessons_count": open_lessons_count,
                "total_duration_minutes": total_duration_minutes
            }}


@course_router.delete("/delete")
async def delete_course(id: int, session: AsyncSession = Depends(get_session)):

    course = await session.scalar(select(Course).where(Course.id == id))
    if not course:
        raise HTTPException(status_code=404, detail="not found")

    await session.delete(course)
    await session.commit()

    return {"status_code": 200, "detail": "delete successful"}
