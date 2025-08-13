from fastapi import APIRouter, Depends
from app.deps import get_current_user
from app.schemas import UserOut

router = APIRouter()

@router.get("/users/me", response_model=UserOut)
async def read_me(user=Depends(get_current_user)):
    return user
