from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal
from Basic.models.job_apply_application import JobApplyApplication
from Basic.schemas.application import ApplicationCreate, ApplicationOut
from typing import List

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

# GET all job applications
@router.get("/", response_model=List[ApplicationOut])
async def get_applications(db: AsyncSession = Depends(get_db)):
    query = select(JobApplyApplication)
    result = await db.execute(query)
    applications = result.scalars().all()
    return applications

# ✨ NEW: GET job applications by job_id
@router.get("/job/{job_id}", response_model=List[ApplicationOut])
async def get_applications_by_job_id(job_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get all applications for a specific job ID.
    """
    query = select(JobApplyApplication).where(JobApplyApplication.job_id == job_id)
    result = await db.execute(query)
    applications = result.scalars().all()
    # This will correctly return an empty list [] if no applications are found
    return applications

# POST a new job application
@router.post("/post/", response_model=ApplicationOut)
async def apply_job(application: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    # Check if the user has already applied for this job
    result = await db.execute(
        select(JobApplyApplication).where(
            JobApplyApplication.email == application.email,
            JobApplyApplication.job_id == application.job_id
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this job")

    new_app = JobApplyApplication(**application.dict())
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)
    return new_app