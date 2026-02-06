from pydantic import BaseModel

class ATSRequest(BaseModel):
    job_id: int
    user_id: int
