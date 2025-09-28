from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal
from Resume.model.model import Resume
from Resume.schema.schema import ResumeCreate, ResumeUpdate, ResumeOut
from uuid import UUID

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


# @router.post("/", response_model=ResumeOut)
# async def create_resume(resume: ResumeCreate, db: AsyncSession = Depends(get_db)):
#     """Create a new resume"""
#     db_resume = Resume(
#         user_id=resume.user_id,
#         resume_data=resume.resume_data,
#         status=resume.status
#     )
#     db.add(db_resume)
#     await db.commit()
#     await db.refresh(db_resume)
#     return db_resume

@router.post("/", response_model=ResumeOut)
async def create_or_update_resume(resume: ResumeCreate, db: AsyncSession = Depends(get_db)):
    """Create a new resume or update existing one for the user"""
    # check if user already has a resume (latest one)
    existing_result = await db.execute(
        select(Resume)
        .where(Resume.user_id == resume.user_id)
        .order_by(desc(Resume.created_at))
        .limit(1)
    )
    existing_resume = existing_result.scalar_one_or_none()

    if existing_resume:
        # update the existing record
        existing_resume.resume_data = resume.resume_data
        existing_resume.status = resume.status
        await db.commit()
        await db.refresh(existing_resume)
        return existing_resume
    else:
        # create a new record
        db_resume = Resume(
            user_id=resume.user_id,
            resume_data=resume.resume_data,
            status=resume.status
        )
        db.add(db_resume)
        await db.commit()
        await db.refresh(db_resume)
        return db_resume


@router.get("/{resume_id}", response_model=ResumeOut)
async def get_resume(resume_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a resume by ID"""
    result = await db.execute(select(Resume).where(Resume.resume_id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.get("/user/{user_id}", response_model=list[ResumeOut])
async def get_user_resumes(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get all resumes for a specific user"""
    result = await db.execute(select(Resume).where(Resume.user_id == user_id))
    resumes = result.scalars().all()
    return resumes


@router.put("/{resume_id}", response_model=ResumeOut)
async def update_resume(resume_id: UUID, resume_update: ResumeUpdate, db: AsyncSession = Depends(get_db)):
    """Update a resume"""
    result = await db.execute(select(Resume).where(Resume.resume_id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if resume_update.resume_data is not None:
        resume.resume_data = resume_update.resume_data
    if resume_update.status is not None:
        resume.status = resume_update.status
    
    await db.commit()
    await db.refresh(resume)
    return resume


@router.delete("/{resume_id}")
async def delete_resume(resume_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a resume"""
    result = await db.execute(select(Resume).where(Resume.resume_id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    await db.delete(resume)
    await db.commit()
    return {"message": "Resume deleted successfully"}

@router.get("/resumes/user/{user_id}", response_model=list[ResumeOut])
async def get_resumes_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Resume).where(Resume.user_id == user_id)
    )
    resumes = result.scalars().all()        
    return resumes

