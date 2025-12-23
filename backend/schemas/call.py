from pydantic import BaseModel

class StartCallRequest(BaseModel):
    caller_id: str

class CallResponse(BaseModel):
    call_id: str
    caller_id: str
    session_id: str 
    started_at: str 
    ended_at: str | None = None