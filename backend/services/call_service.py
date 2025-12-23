from sqlalchemy.orm import Session
from database.repositories.call_repo import CallRepository
from database.repositories.session_repo import SessionRepository
from database.models.call import Call as CallModel
from backend.error import NotFoundError, ConflictError

class CallService:
    def __init__(self, db: Session):
        self.db = db
        self.call_repo = CallRepository(db)
        self.session_repo = SessionRepository(db)

    def start_call(self, caller_id: str) -> CallModel:
        try :    
            call = self.call_repo.create(caller_id)
            session = self.session_repo.create(call.id)
            self.db.commit()
            self.db.refresh(call)
            self.db.refresh(session)
            return call
        except Exception:
            self.db.rollback()
            raise
        
    def end_call(self, call_id: str) -> CallModel:
        try :
            call = self.call_repo.get_by_id(call_id)
            if not call:
                raise NotFoundError("Call not found.")
            
            if call.ended_at is not None:
                raise ConflictError("Call has already ended.")
            
            self.call_repo.end_call(call)
            session = self.session_repo.get_active_by_call_id(call_id)
            if session:
                self.session_repo.end(session)
            self.db.commit()
            self.db.refresh(call)
            return call
        except Exception:
            self.db.rollback()
            raise