from pydantic import BaseModel, Field

class StartCallRequest(BaseModel):
    caller_id: str = Field (..., min_length=1, description="caller_id can not be empty")

class CallResponse(BaseModel):
    call_id: str
    caller_id: str
    session_id: str 
    started_at: str 
    ended_at: str | None = None