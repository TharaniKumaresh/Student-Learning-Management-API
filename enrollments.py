from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.deps import get_db, require_role, get_current_user
from app.models import Enrollment, Course, User
from app.schemas import EnrollmentOut

router = APIRouter()

@router.post("/enroll/{course_id}")
async def enroll(course_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(await require_role("student"))):
    res = await db.execute(select(Course).where(Course.id == course_id))
    course = res.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check existing enrollment
    res = await db.execute(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id))
    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already enrolled")

    enr = Enrollment(user_id=user.id, course_id=course_id)
    db.add(enr)
    await db.commit()
    return {"detail": "Enrolled successfully"}

@router.get("/enrollments/me", response_model=List[EnrollmentOut])
async def my_enrollments(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    res = await db.execute(select(Enrollment).where(Enrollment.user_id == user.id).join(Enrollment.course))
    return res.scalars().all()
