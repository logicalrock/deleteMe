from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

class UserProfile(BaseModel):
    name: str

@router.post("/create")
def create_user(profile: UserProfile):
    return {"message": f"Welcome {profile.name}!", "status": "ok"}

