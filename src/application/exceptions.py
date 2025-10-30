from typing import Optional


class ApplicationException(Exception):
    """Base class for application-specific exceptions."""
    def __init__(self, message: str = "An application error occurred"):
        self.message = message
        super().__init__(self.message)

class NotFoundException(ApplicationException):
    """Exception raised when a requested resource is not found."""
    def __init__(self, resource_name: str = "Resource", identifier = None, message: Optional[str] = None):
        if message is None:
            if identifier:
                self.message = f"{resource_name} with ID/NIM '{identifier}' not found."
            else:
                self.message = f"{resource_name} not found."
        else:
            self.message = message
        super().__init__(self.message)

class DuplicateEntryException(ApplicationException):
    """Exception raised when an attempt is made to create a duplicate resource."""
    def __init__(self, resource_name: str = "Resource", field_name: Optional[str] = None, field_value = None, message: Optional[str] = None):
        if message is None:
            if field_name and field_value:
                self.message = f"{resource_name} with {field_name} '{field_value}' already exists."
            else:
                self.message = f"Duplicate {resource_name} entry."
        else:
            self.message = message
        super().__init__(self.message)

class InvalidInputException(ApplicationException):
    """Exception raised for invalid input data."""
    def __init__(self, message: str = "Invalid input provided."):
        super().__init__(message)

class UnauthorizedException(ApplicationException):
    """Exception raised when a user is not authorized to perform an action."""
    def __init__(self, message: str = "Authentication required or invalid credentials."):
        super().__init__(message)

class ForbiddenException(ApplicationException):
    """Exception raised when a user is authenticated but not allowed to perform an action."""
    def __init__(self, message: str = "You do not have permission to perform this action."):
        super().__init__(message)

class RepositoryException(ApplicationException):
    """Base class for repository-specific exceptions."""
    def __init__(self, message: str = "A repository error occurred"):
        super().__init__(message)

class DatabaseException(RepositoryException):
    """Exception raised for database-related errors (e.g., connection, integrity)."""
    def __init__(self, message: str = "A database operation failed."):
        super().__init__(message)
