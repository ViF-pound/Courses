import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.lesson_model import Lesson
from src.lesson.schemas import DataLesson, NewDataLesson
from src.db import get_session
from src.models.course_model import Course


lesson_router = APIRouter(prefix="/lessons", tags=["Lessons"])


async def return_lessons(course_id: int, session: AsyncSession):

    lessons = await session.scalars(select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.position))

    return lessons.all()


@lesson_router.post("/create")
async def create_lesson(data: DataLesson, session: AsyncSession = Depends(get_session)):

    course = await session.scalar(select(Course).where(Course.id == data.course_id))
    if not course:
        raise HTTPException(status_code=404, detail="not found")

    lesson_data = data.model_dump()

    lesson = Lesson(**lesson_data)

    session.add(lesson)
    await session.commit()
    await session.refresh(lesson)

    return {"status_code": 200, "detail": "lesson created", "lesson": lesson_data}


@lesson_router.get("/return")
async def return_lessons_course(course_id: int, session: AsyncSession = Depends(get_session)):

    course = await session.scalar(select(Course).where(Course.id == course_id))
    if not course:
        raise HTTPException(status_code=404, detail="not found")

    lessons = await return_lessons(course_id, session)

    return lessons


@lesson_router.put("/update")
async def update_lesson(new_data: NewDataLesson, course_id: int, lesson_id: int, session: AsyncSession = Depends(get_session)):

    course = await session.scalar(select(Course).where(Course.id == course_id))
    if not course:
        raise HTTPException(status_code=404, detail="not found")

    lesson = await session.scalar(select(Lesson).where(Lesson.course_id == course_id, Lesson.id == lesson_id))
    if not lesson:
        raise HTTPException(status_code=404, detail="not found")

    if new_data.title:
        lesson.title = new_data.title

    if new_data.summary:
        lesson.summary = new_data.summary

    if new_data.position:
        lesson.position = new_data.position

    if new_data.duration_minutes:
        lesson.duration_minutes = new_data.duration_minutes

    if new_data.is_open:
        lesson.is_open = new_data.is_open

    await session.commit()
    await session.refresh(lesson)

    return {"status_code": 200, "detail": "update successful", "data": lesson}


@lesson_router.delete("/delete")
async def delete_lesson(course_id: int, lesson_id: int, session: AsyncSession = Depends(get_session)):

    course = await session.scalar(select(Course).where(Course.id == course_id))
    if not course:
        raise HTTPException(status_code=404, detail="not found")

    lesson = await session.scalar(select(Lesson).where(Lesson.course_id == course_id, Lesson.id == lesson_id))
    if not lesson:
        raise HTTPException(status_code=404, detail="not found")

    await session.delete(lesson)
    await session.commit()

    return {"status_code": 200, "detail": "delete successful"}