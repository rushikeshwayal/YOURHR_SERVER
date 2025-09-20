from fastapi import FastAPI
from api.application import  router as application
from api.job import router as job
from api.user import router as user

app = FastAPI()

app.include_router(job, prefix="/jobs", tags=["Jobs"])
app.include_router(application, prefix="/applications", tags=["Applications"])
app.include_router(user, prefix="/users", tags=["Users"])
