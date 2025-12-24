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
   call = service.start_call(payload.caller_id)
   active_session = next((s for s in call.sessions if s.ended_at is None), None)
   return CallResponse(
       call_id=call.id,
       caller_id=call.caller_id,
       session_id=active_session.id if active_session else None,
       started_at=call.started_at.isoformat(), 
       ended_at=call.ended_at.isoformat() if call.ended_at else None
   )
   
@router.post("/{call_id}/end", response_model=CallResponse)
def end_call(call_id: str, db: Session = Depends(get_db)):
    service = CallService(db)
    call = service.end_call(call_id)
    last_session = (call.sessions[-1] if call.sessions else None)

    return CallResponse(
        call_id=call.id,
        caller_id=call.caller_id,
        session_id=last_session.id if last_session else None,
        started_at=call.started_at.isoformat(), 
        ended_at=call.ended_at.isoformat() if call.ended_at else None
    )