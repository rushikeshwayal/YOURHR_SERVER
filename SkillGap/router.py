# SkillGap/router.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from database import SessionLocal
from Basic.models.job_vacancy import JobVacancy
from Resume.model.model import Resume
from SkillGap.prompt import Prompts
from Agent.config import CustomAgent

router = APIRouter()
prompt = Prompts()
agent = CustomAgent()

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session


@router.get("/skill-gaps/{job_id}/{user_id}")
async def generate_skill_gaps(job_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    # get job vacancy
    result = await db.execute(select(JobVacancy).where(JobVacancy.job_id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    user_result = await db.execute(select(Resume).where(Resume.user_id == user_id))
    if not user_result:
        raise HTTPException(status_code=404, detail="User resume not found")
    print(user_result)
    user_resume = user_result.scalar_one_or_none()
    if not user_resume:
        raise HTTPException(status_code=404, detail="User resume not found")
    resume_data = user_resume.resume_data or {}
    print(resume_data["certifications"])
    user_skills = resume_data["skills"]  or ""
    user_summary = resume_data.get("summary", "")
    user_experience = str(resume_data.get("experience", "")).replace("{", " ").replace("}", " ")
    user_certifications = str(resume_data.get("certifications", "")).replace("{", " ").replace("}", " ")

    data = {
        "job_title": job.job_title,
        "company_name": job.company_name,
        "job_description": job.job_description,
        "skills_required": job.skills_required or "N/A",
        "experience_required": job.experience_required or "N/A",
        "user_skills": user_skills,
        "user_summary": user_summary,
        "user_experience": user_experience,
        "user_certifications": user_certifications
    }

    # create prompt for the agent
    user_prompt = prompt.user_prompt(data=data)

    # call our simplified agent
    response = agent.invoke_agent(
        system_input=prompt.system_prompt(),
        user_input=user_prompt,
        model_name="google",
        model_variant="gemini-2.5-flash",
        output_parser="json",
    )

    # response should be already parsed JSON list from the agent
    return response
