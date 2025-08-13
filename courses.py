from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.deps import get_db, require_role
from app.models import Course
from app.schemas import CourseCreate, CourseOut, CourseUpdate
from typing import List

router = APIRouter()

@router.post("", response_model=CourseOut)
async def create_course(data: CourseCreate, db: AsyncSession = Depends(get_db), admin=Depends(await require_role("admin"))):
    course = Course(**data.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course

@router.get("", response_model=List[CourseOut])
async def list_courses(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course))
    return res.scalars().all()

@router.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course).where(Course.id == course_id))
    course = res.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=CourseOut)
async def update_course(course_id: int, data: CourseUpdate, db: AsyncSession = Depends(get_db), admin=Depends(await require_role("admin"))):
    res = await db.execute(select(Course).where(Course.id == course_id))
    course = res.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(course, k, v)
    await db.commit()
    await db.refresh(course)
    return course

@router.delete("/{course_id}")
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db), admin=Depends(await require_role("admin"))):
    res = await db.execute(select(Course).where(Course.id == course_id))
    course = res.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    await db.delete(course)
    await db.commit()
    return {"detail": "Course deleted"}
