class ResourceNotFoundError(Exception):
    """Raised when an entity is not found in the database (Maps to 404)."""
    pass

class DatabaseError(Exception):
    """Raised when a database operations fails unexpectedly (Maps to 500)."""
    pass