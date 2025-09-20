from fastapi import FastAPI
from api.application import router as application
from fastapi.middleware.cors import CORSMiddleware
from api.job import router as job
from api.user import router as user
from mangum import Mangum

app = FastAPI()

# Allow all origins for CORS (for dev and serverless)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(job, prefix="/jobs", tags=["Jobs"])
app.include_router(application, prefix="/applications", tags=["Applications"])
app.include_router(user, prefix="/users", tags=["Users"])

# Mangum handler for Vercel/AWS Lambda


