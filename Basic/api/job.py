from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import async_session
from Basic.models.job_vacancy import JobVacancy
from Basic.schemas.job import JobOut, JobCreate

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.get("/", response_model=list[JobOut])
async def get_all_jobs(db: AsyncSession = Depends(get_db)):
    async with db:  # optional, ensures proper context
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

@router.post("/post/", response_model=JobOut)
async def post_job(job: JobCreate, db: AsyncSession = Depends(get_db)):
    new_job = JobVacancy(**job.dict())
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job
