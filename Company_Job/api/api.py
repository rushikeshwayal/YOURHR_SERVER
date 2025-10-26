from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Company_Job.model.model import Job
from Company_Job.schema.schema import JobCreate, JobUpdate, JobResponse
from database import get_db
import uuid

router = APIRouter()


# ✅ Create Job
@router.post("/post/jobs", response_model=JobResponse)
async def create_job(job: JobCreate, db: AsyncSession = Depends(get_db)):
    new_job = Job(
        job_id=str(uuid.uuid4()),
        company_id=job.company_id,
        title=job.title,
        role=job.role,
        location=job.location,
        job_type=job.job_type,
        salary_range=job.salary_range,
        experience_required=job.experience_required,
        skills_required=job.skills_required,
        description=job.description,
        responsibilities=job.responsibilities,
        benefits=job.benefits,
        application_deadline=job.application_deadline,
        status=job.status,
        apply_link=str(job.apply_link) if job.apply_link else None,
    )

    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job



# ✅ Get All Jobs
@router.get("/get/jobs", response_model=list[JobResponse])
async def get_all_jobs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job))
    return result.scalars().all()


# ✅ Get Job by ID
@router.get("/get/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.job_id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


# ✅ Get Jobs by Company
@router.get("/get/company/{company_id}", response_model=list[JobResponse])
async def get_jobs_by_company(company_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.company_id == company_id))
    return result.scalars().all()


# ✅ Update Job
@router.put("/put/jobs/{job_id}", response_model=JobResponse)
async def update_job(job_id: str, updates: JobUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.job_id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(job, key, value)

    await db.commit()
    await db.refresh(job)
    return job


# ✅ Delete Job
@router.delete("/delete/jobs/{job_id}")
async def delete_job(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.job_id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    await db.delete(job)
    await db.commit()
    return {"message": "Job deleted successfully"}
