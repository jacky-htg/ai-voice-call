from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from backend.deps import get_db
from backend.services.call_service import CallService

router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"],
)

@router.post("/livekit")
async def livekit_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    event = payload.get("event")
    service = CallService(db)
    service.handle_webhook_event(event, payload)

    return {"status": "ok"}