class AppError(Exception):
    """Base class untuk semua application errors"""

class NotFoundError(AppError):
    pass

class ConflictError(AppError):
    pass

class ValidationError(AppError):
    pass

class UnauthorizedError(AppError):
    pass

