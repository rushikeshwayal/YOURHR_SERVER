from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from models.user_detail import UserDetail
from schemas.user import UserCreate, UserOut
from sqlalchemy.future import select

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # check for duplicate email
    result = await db.execute(
        select(UserDetail).where(UserDetail.email_address == user.email_address)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = UserDetail(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
