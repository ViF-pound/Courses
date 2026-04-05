from binascii import Error
from fastapi import FastAPI

from src.course.course_router import course_router
from src.lesson.lesson_router import lesson_router
from src.db import Base, engine


app = FastAPI()
app.include_router(course_router)
app.include_router(lesson_router)

@app.get("/init")
async def create_db():
    
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except Error as e:
            print(e)
        await conn.run_sync(Base.metadata.create_all)

    return "database created"