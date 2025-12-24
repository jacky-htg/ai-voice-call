from sqlalchemy.orm import Session
from database.repositories.call_repo import CallRepository
from database.repositories.session_repo import SessionRepository
from database.models.call import Call as CallModel
from database.models.session import Session as SessionModel
from backend.error import NotFoundError, ConflictError
from backend.services.livekit_service import LiveKitService
from loguru import logger

class CallService:
    def __init__(self, db: Session):
        self.db = db
        self.call_repo = CallRepository(db)
        self.session_repo = SessionRepository(db)
        self.livekit = LiveKitService()

    def start_call(self, caller_id: str) -> CallModel:
        try :    
            call = self.call_repo.create(caller_id)
            session = SessionModel(call_id=call.id, user_id=caller_id, status="initiated")
            self.db.add(session)
            self.db.commit()
            self.db.refresh(call)
            self.db.refresh(session)

            room_name = f"call_{call.id}"
            identity = session.id
            token = self.livekit.create_token(room_name=room_name, identity=identity, name=f"user-{caller_id}")
            return {
                "call": call,
                "session": session,
                "livekit_token": token,
                "room_name": room_name
            }
        except Exception:
            self.db.rollback()
            raise

    def join_call(self, call_id: str, user_id: str) -> dict:
        call = self.call_repo.get_by_id(call_id)
        if not call or call.ended_at:
            raise NotFoundError("Call not active")

        session = self.session_repo.create(call_id=call_id, user_id=user_id)
        self.db.flush()

        room_name = f"call_{call.id}"
        identity = session.id
        token = self.livekit.create_token(
            room_name=room_name,
            identity=identity,
        )
        if not token:
            raise Exception("Failed to generate LiveKit token")
        
        self.db.commit()
        return {
            "call": call,
            "session": session,
            "room_name": room_name,
            "livekit_token": token,
        }
     
    def end_call(self, call_id: str, from_webhook: bool = False) :
        call = self.call_repo.get_by_id(call_id)
        if not call:
            return None, []
    
        if call.ended_at:
            return call, []
    
        try :
            room_name = f"call_{call.id}"
            
            self.call_repo.end_call(call)
            sessions = self.session_repo.get_active_by_call_id(call_id)
            for session in sessions: 
                self.session_repo.end(session)

            self.db.commit()
            self.db.refresh(call)

            if not from_webhook: 
                room_name = f"call_{call.id}"
                self.livekit.end_room(room_name)

            return call, session
        except Exception:
            self.db.rollback()
            raise

    def handle_webhook_event(self, event: str, payload: dict):
        if event == "participant_joined":
            identity = payload["participant"]["identity"]
            self.session_repo.set_active_by_id(identity)
            self.db.commit()

        elif event == "participant_left":
            identity = payload["participant"]["identity"]
            session = self.session_repo.get_by_id(identity)
            if session: self.session_repo.end(session)
            self.db.commit()

        elif event == "room_finished":
            room_name = payload["room"]["name"]
            call_id = room_name.replace("call_", "")
            self.end_call(call_id, from_webhook=True)
