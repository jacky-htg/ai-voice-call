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
   result = service.start_call(payload.caller_id)
   call = result["call"]
   session = result["session"]
   return CallResponse(
       call_id=call.id,
       caller_id=call.caller_id,
       session_id=session.id,
       started_at=call.started_at.isoformat(), 
       ended_at=call.ended_at.isoformat() if call.ended_at else None,
       livekit_token=result["livekit_token"],
       room_name=result["room_name"]
   )

@router.post("/{call_id}/join/{user_id}", response_model=CallResponse)
def start_call(call_id: str, user_id: str, db: Session = Depends(get_db)):
   service = CallService(db)
   result = service.join_call(call_id=call_id, user_id=user_id)
   call = result["call"]
   session = result["session"]
   return CallResponse(
       call_id=call.id,
       caller_id=call.caller_id,
       session_id=session.id,
       started_at=call.started_at.isoformat(), 
       ended_at=call.ended_at.isoformat() if call.ended_at else None,
       livekit_token=result["livekit_token"],
       room_name=result["room_name"]
   )

@router.post("/{call_id}/end", response_model=CallResponse)
def end_call(call_id: str, db: Session = Depends(get_db)):
    service = CallService(db)
    call, sessions = service.end_call(call_id)
    
    return CallResponse(
        call_id=call.id,
        caller_id=call.caller_id,
        session_id=sessions[0].id if sessions else "",
        started_at=call.started_at.isoformat(), 
        ended_at=call.ended_at.isoformat() if call.ended_at else None,
        livekit_token="",
        room_name=f"call_{call.id}"
    )