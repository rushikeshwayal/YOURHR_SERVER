from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import async_session
from Basic.models.job_vacancy import JobVacancy
from Basic.schemas.job import JobOut, JobCreate
from typing import List, Optional # Import Optional for Pydantic updates

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.get("/", response_model=List[JobOut])
async def get_all_jobs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobVacancy))
    jobs = result.scalars().all()
    return jobs

@router.get("/{job_id}", response_model=JobOut)
async def get_job_by_id(job_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobVacancy).where(JobVacancy.job_id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/user/{contact_email}", response_model=List[JobOut])
async def get_jobs_by_contact_email(contact_email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(JobVacancy).where(JobVacancy.contact_email == contact_email)
    )
    jobs = result.scalars().all()
    
    if not jobs:
        raise HTTPException(
            status_code=404,
            detail=f"No jobs found posted by the email: {contact_email}"
        )
        
    return jobs

@router.post("/post/", response_model=JobOut, status_code=status.HTTP_201_CREATED)
async def post_job(job: JobCreate, db: AsyncSession = Depends(get_db)):
    new_job = JobVacancy(**job.dict())
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job

# ✨ NEW: PUT endpoint for updating an existing job
@router.put("/{job_id}", response_model=JobOut)
async def update_job(job_id: int, job_update: JobCreate, db: AsyncSession = Depends(get_db)):
    """
    Updates an existing job vacancy.
    """
    result = await db.execute(select(JobVacancy).where(JobVacancy.job_id == job_id))
    existing_job = result.scalar_one_or_none()

    if not existing_job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Update fields from the incoming job_update schema
    for field, value in job_update.dict(exclude_unset=True).items():
        setattr(existing_job, field, value)

    await db.commit()
    await db.refresh(existing_job)
    return existing_job

