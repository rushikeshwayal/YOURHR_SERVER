from fastapi import FastAPI
from Basic.api.application import router as application
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from Basic.api.job import router as job
from Basic.api.user import router as user
from InterviewQus.router import router as interview_router
from SkillGap.router import router as skillgap_router
# Import Resume model to register it with SQLAlchemy
from Resume.model.model import Resume
from Resume.api.resume import router as resume
from Community.api.api import router as community_router
from CareerPath.router import router as careerpath_router
from Company.api.api import router as company_router
from Company_Job.api.api import router as company_job_router
from Company_job_application.api.api import router as company_application_router


app = FastAPI()
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://your-hr-client.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(job, prefix="/jobs", tags=["Jobs"])
app.include_router(application, prefix="/applications", tags=["Applications"])
app.include_router(user, prefix="/users", tags=["Users"])
app.include_router(resume, prefix="/resumes", tags=["Resumes"])
app.include_router(interview_router, prefix="/jobs", tags=["Interview Questions"])
app.include_router(skillgap_router, prefix="/jobs", tags=["Skill Gaps"])
app.include_router(community_router, prefix="/community", tags=["Community"])
app.include_router(careerpath_router, prefix="/career-path", tags=["Career Path"])
app.include_router(company_router, prefix="/companies", tags=["Companies"])
app.include_router(company_job_router, prefix="/company-jobs", tags=["Company Jobs"])
app.include_router(company_application_router, prefix="/company-applications", tags=["Company Job Applications"])