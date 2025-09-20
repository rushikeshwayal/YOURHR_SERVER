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

@router.get("/", response_model=list[JobOut])
async def get_jobs(
    job_id: int = Query(None),
    sort_by: str = Query("salary_range"),
    order: str = Query("ASC"),
    employment_type: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    async with db.begin():  # ensure proper transaction scope
        query = select(JobVacancy)
        if job_id:
            query = query.where(JobVacancy.job_id == job_id)
        if employment_type:
            query = query.where(JobVacancy.employment_type == employment_type)

        order_column = getattr(JobVacancy, sort_by, None)
        if not order_column:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if order.upper() == "DESC":
            query = query.order_by(desc(order_column))
        else:
            query = query.order_by(asc(order_column))

        result = await db.execute(query)
        jobs = result.scalars().all()  # ok here, inside single await context

    return jobs

@router.post("/post/", response_model=JobOut)
async def post_job(job: JobCreate, db: AsyncSession = Depends(get_db)):
    new_job = JobVacancy(**job.dict())
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job
