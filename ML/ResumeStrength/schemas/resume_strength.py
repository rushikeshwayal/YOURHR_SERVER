from pydantic import BaseModel, Field
from typing import Literal

class ResumeStrengthRequest(BaseModel):
    years_experience: float = Field(..., ge=0, example=5)
    skills_match_score: float = Field(..., ge=0, le=100, example=82.5)

    education_level: Literal[
        "High School",
        "Bachelors",
        "Masters",
        "PhD"
    ]

    project_count: int = Field(..., ge=0, example=6)
    github_activity: int = Field(..., ge=0, example=200)
