from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from models.job_vacancy import JobVacancy
from schemas.job import JobCreate, JobOut

from sqlalchemy.future import select
from sqlalchemy import asc, desc

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import async_session
from models.job_vacancy import JobVacancy
from schemas.job import JobOut

router = APIRouter()

# Dependency for async session
async def get_db():
    async with async_session() as session:
        yield session

# GET all jobs
@router.get("/", response_model=list[JobOut])
async def get_all_jobs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobVacancy))
    jobs = result.scalars().all()
    return jobs

# GET job by ID
@router.get("/{job_id}", response_model=JobOut)
async def get_job_by_id(job_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobVacancy).where(JobVacancy.job_id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/post/", response_model=JobOut)
async def post_job(job: JobCreate, db: AsyncSession = Depends(get_db)):
    new_job = JobVacancy(**job.dict())
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job
