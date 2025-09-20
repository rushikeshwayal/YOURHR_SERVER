from fastapi import FastAPI
from api.application import  router as application
from fastapi.middleware.cors import CORSMiddleware
from api.job import router as job
from api.user import router as user
from mangum import Mangum

app = FastAPI()
app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://your-frontend-domain.com",  # add your deployed frontend too
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] for all origins (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(job, prefix="/jobs", tags=["Jobs"])
app.include_router(application, prefix="/applications", tags=["Applications"])
app.include_router(user, prefix="/users", tags=["Users"])

handler = Mangum(app)