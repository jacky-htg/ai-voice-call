from sqlalchemy import func
from database.models.session import Session as SessionModel
from .base import BaseRepository

class SessionRepository(BaseRepository):
    def get_active_by_call_id(self, call_id: str) -> SessionModel | None:
        return self.db.query(SessionModel).filter(SessionModel.call_id == call_id, SessionModel.status == "active", SessionModel.ended_at == None).first()

    def end(self, session: SessionModel) -> SessionModel: 
        session.status = "ended"
        session.ended_at = func.now()
        return session

    def create(self, call_id: str) -> SessionModel:
        new_session = SessionModel(call_id=call_id)
        self.db.add(new_session)
        return new_session