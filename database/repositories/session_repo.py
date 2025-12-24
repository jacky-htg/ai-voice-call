from sqlalchemy import func
from database.models.session import Session as SessionModel
from .base import BaseRepository

class SessionRepository(BaseRepository):
    def get_active_by_call_id(self, call_id: str) -> list[SessionModel]:
        return self.db.query(SessionModel).filter(SessionModel.call_id == call_id, SessionModel.status == "active", SessionModel.ended_at.is_(None)).all()

    def get_by_id(self, session_id: str) -> SessionModel | None:
        return (
            self.db
            .query(SessionModel)
            .filter(SessionModel.id == session_id)
            .first()
        )
    
    def set_active_by_id(self, session_id: str) -> SessionModel | None:
        session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if session:
            session.status = "active"
        return session
    
    def end(self, session: SessionModel) -> SessionModel: 
        session.status = "ended"
        session.ended_at = func.now()
        return session

    def create(self, call_id: str, user_id: str) -> SessionModel:
        new_session = SessionModel(call_id=call_id, user_id=user_id, status="initiated")
        self.db.add(new_session)
        return new_session