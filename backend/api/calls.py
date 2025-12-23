from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.services.call_service import CallService
from backend.schemas.call import StartCallRequest, CallResponse
from backend.deps import get_db

router = APIRouter(
    prefix="/calls",
    tags=["calls"],
)

@router.post("/", response_model=CallResponse)
def start_call(payload: StartCallRequest, db: Session = Depends(get_db)):
   service = CallService(db)
   return service.start_call(payload.caller_id)
   
@router.post("/{call_id}/end", response_model=CallResponse)
def end_call(call_id: str, db: Session = Depends(get_db)):
    service = CallService(db)
    return service.end_call(call_id)