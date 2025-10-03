from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database import SessionLocal
from Resume.model.model import Resume
from Basic.models.user_detail import UserDetail # ✨ ADDED: Missing import
from CareerPath.prompts import Prompts
from CareerPath.model import RoadMap
from CareerPath.schema import RoadMapCreate, RoadMapOut
from Agent.career_config import CustomAgentWithSearch
import os
import uuid
from typing import List

# Define the prefix and tags for the entire router once.
router = APIRouter(
    prefix="/career-path",
    tags=["Career Path"]
)
prompt = Prompts()
agent = CustomAgentWithSearch(serpapi_key=os.getenv("SERPAPI_KEY"))

async def get_db():
    async with SessionLocal() as session:
        yield session

# Path is relative to the router's prefix ("/career-path")
@router.get("/generate/{user_id}", response_model=List[dict])
async def generate_career_path(
    user_id: int,
    job_title: str,
    company_name: str = "N/A",
    db: AsyncSession = Depends(get_db),
    use_search: bool = False
):
    """
    Generates a new career path roadmap based on user's resume data.
    """
    user_result = await db.execute(select(Resume).where(Resume.user_id == user_id))
    user_resume = user_result.scalar_one_or_none()

    if not user_resume:
        raise HTTPException(status_code=404, detail="User resume not found")

    resume_data = user_resume.resume_data or {}
    data = {
        "job_title": job_title,
        "company_name": company_name,
        "user_skills": resume_data.get("skills", ""),
        "user_summary": resume_data.get("summary", ""),
        "user_experience": str(resume_data.get("experience", "")).replace("{", " ").replace("}", " "),
        "user_certifications": str(resume_data.get("certifications", "")).replace("{", " ").replace("}", " ")
    }
    user_prompt = prompt.user_prompt(data=data)
    response = agent.invoke_agent(
        system_input=prompt.system_prompt(),
        user_input=user_prompt,
        model_name="google",
        output_parser="json",
        use_tools=False
    )
    return response

# Path is now relative, just "/"
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoadMapOut)
async def save_career_path(
    roadmap: RoadMapCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Saves a generated career path roadmap to the database.
    """
    new_roadmap = RoadMap(
        user_email=roadmap.user_email,
        job_title=roadmap.job_title,      
        company_name=roadmap.company_name, 
        roadmap_data=roadmap.roadmap_data,
        status="saved"
    )
    db.add(new_roadmap)
    await db.commit()
    await db.refresh(new_roadmap)
    return new_roadmap

# Path is now relative
@router.get("/user/{user_email}", response_model=List[RoadMapOut])
async def get_saved_roadmaps_by_email(
    user_email: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves all saved career path roadmaps for a user by email.
    """
    result = await db.execute(select(RoadMap).where(RoadMap.user_email == user_email))
    roadmaps = result.scalars().all()
    if not roadmaps:
        raise HTTPException(status_code=404, detail="No saved roadmaps found for this user.")
    return roadmaps

# Path is now relative.
@router.delete("/{roadmap_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_roadmap(
    roadmap_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Deletes a specific roadmap by its ID.
    """
    roadmap_to_delete = await db.get(RoadMap, roadmap_id)
    if not roadmap_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found")
    
    await db.delete(roadmap_to_delete)
    await db.commit()
    return