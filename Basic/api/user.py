from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from Basic.models.user_detail import UserDetail
from Basic.schemas.user import UserCreate, UserOut, GoogleUserCreate
from sqlalchemy.future import select

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserDetail))
    users = result.scalars().all()
    return [
        UserOut(
            id=user.id,
            user_id=str(user.user_id),
            full_name=user.full_name,
            phone_number=user.phone_number,
            email_address=user.email_address,
            password=user.password
        )
        for user in users
    ]

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
    
    # Return with proper formatting
    return UserOut(
        id=new_user.id,
        user_id=str(new_user.user_id),
        full_name=new_user.full_name,
        phone_number=new_user.phone_number,
        email_address=new_user.email_address,
        password=new_user.password
    )

@router.post("/google", response_model=UserOut)
async def create_or_get_google_user(google_user: GoogleUserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Check if user already exists
        result = await db.execute(
            select(UserDetail).where(UserDetail.email_address == google_user.email_address)
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            # User exists, return existing user with proper formatting
            print(f"Google user already exists: {existing.email_address}")
            return UserOut(
                id=existing.id,
                user_id=str(existing.user_id),
                full_name=existing.full_name,
                phone_number=existing.phone_number,
                email_address=existing.email_address,
                password=existing.password
            )
        
        # User doesn't exist, create new user
        print(f"Creating new Google user: {google_user.email_address}")
        new_user = UserDetail(
            full_name=google_user.full_name,
            email_address=google_user.email_address,
            phone_number=google_user.phone_number,
            password=None  # No password for Google users
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        print(f"Successfully created Google user: {new_user.email_address}")
        
        # Return with proper formatting
        return UserOut(
            id=new_user.id,
            user_id=str(new_user.user_id),
            full_name=new_user.full_name,
            phone_number=new_user.phone_number,
            email_address=new_user.email_address,
            password=new_user.password
        )
    except Exception as e:
        print(f"Error in create_or_get_google_user: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating Google user: {str(e)}")

@router.get("/check/{email}")
async def check_user_exists(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UserDetail).where(UserDetail.email_address == email)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        return {
            "exists": True, 
            "user": {
                "id": existing.id,
                "user_id": str(existing.user_id),
                "full_name": existing.full_name,
                "phone_number": existing.phone_number,
                "email_address": existing.email_address,
                "password": existing.password
            }
        }
    else:
        return {"exists": False, "user": None}

@router.get("/email/{email}", response_model=UserOut)
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UserDetail).where(UserDetail.email_address == email)
    )
    user = result.scalar_one_or_none()
    if user:
        return UserOut(
            id=user.id,
            user_id=str(user.user_id),
            full_name=user.full_name,
            phone_number=user.phone_number,
            email_address=user.email_address,
            password=user.password
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")