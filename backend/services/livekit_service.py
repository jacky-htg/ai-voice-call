from livekit import api
import os

class LiveKitService:
    def __init__(self):
        self.api_key = os.getenv("LIVEKIT_API_KEY")
        self.api_secret = os.getenv("LIVEKIT_API_SECRET")
        self.url = os.getenv("LIVEKIT_URL")

        self.room_service = api.RoomServiceClient(
            self.url,
            self.api_key,
            self.api_secret,
        )


    def create_token(self, room_name: str, identity: str, name: str):
        token = (
            api.AccessToken(self.api_key, self.api_secret)
            .with_identity(identity)
            .with_name(name)
            .with_grants(
                api.VideoGrants(
                    room_join=True,
                    room=room_name
                )
            )
        )
        return token.to_jwt()

    def end_room(self, room_name: str):
        self.room_service.delete_room(room_name)