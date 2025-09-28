from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal
from Basic.models.job_vacancy import JobVacancy
from Agent.config import CustomAgent
from InterviewQus.prompts import Prompts

router = APIRouter()
prompt = Prompts()
agent = CustomAgent()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/interview-questions/{job_id}")
async def generate_interview_questions(job_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobVacancy).where(JobVacancy.job_id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    user_prompt = prompt.user_prompt(
        job_title=job.job_title,
        company_name=job.company_name,
        job_description=job.job_description,
        skills_required=job.skills_required or "N/A",
        experience_required=job.experience_required or "N/A"
    )

    # now call our simplified agent
    response = agent.invoke_agent(
        system_input=prompt.system_prompt(),
        user_input=user_prompt,
        model_name="google",
        model_variant="gemini-2.5-flash",
        output_parser="json"
    )

    # response is already parsed JSON list
    return response
