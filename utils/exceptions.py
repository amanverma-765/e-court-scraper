class NotFoundException(Exception):
    """Raised when a requested resource is not found."""
    pass

class ValidationException(Exception):
    """Raised when validation of input fails."""
    pass

class UnauthorizedException(Exception):
    """Raised when authentication fails."""
    pass

class ConflictException(Exception):
    """Raised when a conflict occurs (e.g., duplicate resource)."""
    pass

class BadRequestException(Exception):
    """Raised when the request is malformed or invalid."""
    pass

class InternalServerErrorException(Exception):
    """Raised when an internal server error occurs."""
    pass
