from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from backend.error import NotFoundError, ConflictError, ValidationError
from backend.api import calls

app = FastAPI()

app.include_router(calls.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Voice Call API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.exception_handler(NotFoundError)
def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": str(exc)}
    )

@app.exception_handler(ConflictError)
def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(
        status_code=409,
        content={"error": str(exc)}
    )

@app.exception_handler(ValidationError)
def validation_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )

@app.exception_handler(Exception)
def internal_error_handler(request: Request, exc: Exception):
    # log exc here
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )