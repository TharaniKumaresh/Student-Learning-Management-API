from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, courses, enrollments, users
from app.db.database import init_db

app = FastAPI(title="Student Learning Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, tags=["users"])
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(enrollments.router, tags=["enrollments"])

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the Student Learning Management API"}
