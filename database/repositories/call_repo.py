from sqlalchemy import func
from database.models.call import Call as CallModel
from .base import BaseRepository

class CallRepository(BaseRepository):
    def create(self, caller_id: str) -> CallModel:
        new_call = CallModel(caller_id=caller_id)
        new_call.status = "initiated"
        self.db.add(new_call)
        return new_call

    def end_call(self, call: CallModel) -> CallModel:
        call.status = "ended"
        call.ended_at = func.now()
        return call
    
    def get_by_id(self, call_id: str) -> CallModel | None:
        return (
            self.db
            .query(CallModel)
            .filter(CallModel.id == call_id)
            .first()
        )
