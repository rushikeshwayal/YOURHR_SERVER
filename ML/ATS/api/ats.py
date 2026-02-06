from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from database import get_db
from Basic.models.job_vacancy import JobVacancy 
from Resume.model.model import Resume
from ML.ATS.schemas.ats import ATSRequest
from ML.ATS.preprocess import clean_text
from ML.ATS.ats_score import calculate_ats_score

log = logging.getLogger(__name__)

router = APIRouter(prefix="/ats", tags=["ATS"])

def build_job_text(job: JobVacancy) -> str:
    fields = [
        job.job_title,
        job.skills_required,
        job.experience_required,
        job.education_required,
    ]
    return " ".join([f for f in fields if f])



def build_resume_text(resume_data: dict) -> str:
    parts = []

    parts.append(resume_data.get("summary", ""))

    skills = resume_data.get("skills", [])
    if isinstance(skills, list):
        parts.append(" ".join(skills))

    for project in resume_data.get("projects", []):
        parts.append(project.get("description", ""))

    for exp in resume_data.get("work_experience", []):
        parts.append(exp.get("title", ""))
        desc = exp.get("description", [])
        if isinstance(desc, list):
            parts.append(" ".join(desc))

    for cert in resume_data.get("certifications", []):
        parts.append(cert.get("name", ""))

    return " ".join(parts)



@router.post("/score")
async def calculate_ats(
    payload: ATSRequest,
    db: AsyncSession = Depends(get_db)
):
    # Fetch Job
    job_result = await db.execute(
        select(JobVacancy).where(JobVacancy.job_id == payload.job_id)
    )
    job = job_result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Fetch Resume
    resume_result = await db.execute(
        select(Resume)
        .where(Resume.user_id == payload.user_id)
        .order_by(Resume.created_at.desc())
    )
    resume = resume_result.scalars().first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Build text
    job_text = build_job_text(job)
    resume_text = build_resume_text(resume.resume_data)

    # Clean text
    job_clean = clean_text(job_text)
    resume_clean = clean_text(resume_text)

    # ✅ IMPROVED ATS SCORE
    ats_score = calculate_ats_score(
        resume_clean,
        job_clean,
        resume.resume_data,
        job
    )

    return {
        "job_id": payload.job_id,
        "user_id": payload.user_id,
        "ats_score": ats_score
    }
    