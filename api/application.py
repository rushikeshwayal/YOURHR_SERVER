from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from models.job_apply_application import JobApplyApplication
from schemas.application import ApplicationCreate, ApplicationOut
from sqlalchemy.future import select

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=ApplicationOut)
async def apply_job(application: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    # optional: verify job_id exists
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
