from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Company_job_application.model.model import JobApplication
from Company_job_application.schema.schema import JobApplicationCreate, JobApplicationResponse
from Company_job_application.model.model import JobApplication
from database import get_db

router = APIRouter()


# ✅ Apply for a Job
@router.post("/post/applications", response_model=JobApplicationResponse)
async def apply_for_job(application: JobApplicationCreate, db: AsyncSession = Depends(get_db)):
    new_application = JobApplication(
        email=application.email,
        resume_link=str(application.resume_link),
        why_hired=application.why_hired,
        company_job_id=application.company_job_id,
    )

    db.add(new_application)
    await db.commit()
    await db.refresh(new_application)
    return new_application



# ✅ Get all applications
@router.get("/get/applications", response_model=list[JobApplicationResponse])
async def get_all_applications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobApplication))
    return result.scalars().all()


# ✅ Get applications for a specific job
@router.get("/get/applications/job/{job_id}", response_model=list[JobApplicationResponse])
async def get_applications_by_job(job_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobApplication).where(JobApplication.company_job_id == job_id))
    return result.scalars().all()


# ✅ Get applications by user email
@router.get("/get/applications/user/{email}", response_model=list[JobApplicationResponse])
async def get_applications_by_user(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobApplication).where(JobApplication.email == email))
    return result.scalars().all()


# ✅ Delete an application
@router.delete("/delete/applications/{id}")
async def delete_application(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobApplication).where(JobApplication.id == id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    await db.delete(application)
    await db.commit()
    return {"message": "Application deleted successfully"}