from fastapi import Request, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip webhook
        if request.url.path.startswith("/webhooks"):
            return await call_next(request)

        auth = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(auth)

        if scheme.lower() != "bearer" or not token:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # TODO: validate JWT properly
        user_id = self.verify_token(token)

        # inject user_id ke request.state
        request.state.user_id = user_id

        return await call_next(request)

    def verify_token(self, token: str) -> str:
        """
        return user_id
        raise exception if invalid
        """
        # sementara mock
        if token == "invalid":
            raise HTTPException(status_code=401, detail="Invalid token")

        return token  # misal token = user_id

class LiveKitWebhookAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith("/webhooks/livekit"):
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if auth != f"Bearer {os.getenv('LIVEKIT_WEBHOOK_SECRET')}":
            raise HTTPException(status_code=401, detail="Invalid webhook signature")

        return await call_next(request)
