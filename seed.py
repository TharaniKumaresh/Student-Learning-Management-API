import asyncio
from app.db.database import async_engine, get_session
from app.models import Base, User, Course
from app.utils.security import get_password_hash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

async def seed():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for session in get_session():
        try:
            admin_email = "admin@example.com"
            student_email = "student@example.com"

            # Create admin
            res = await session.execute(select(User).where(User.email == admin_email))
            if not res.scalar_one_or_none():
                admin = User(
                    email=admin_email,
                    hashed_password=get_password_hash("Admin@123"),
                    full_name="Admin User",
                    role="admin",
                )
                session.add(admin)

            # Create student
            res = await session.execute(select(User).where(User.email == student_email))
            if not res.scalar_one_or_none():
                student = User(
                    email=student_email,
                    hashed_password=get_password_hash("Student@123"),
                    full_name="Student User",
                    role="student",
                )
                session.add(student)

            # Add sample courses
            sample_courses = [
                Course(title="Python for Data Science", description="Numpy, Pandas, ML basics", published=True),
                Course(title="Flutter for Beginners", description="Widgets, layouts, state management", published=True),
                Course(title="FastAPI Crash Course", description="Async APIs with PostgreSQL", published=True),
            ]
            for c in sample_courses:
                session.add(c)

            await session.commit()
            print("Seed completed.")
        except IntegrityError:
            await session.rollback()
            print("Seed rolled back due to integrity error.")

if __name__ == "__main__":
    asyncio.run(seed())
