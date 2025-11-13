from fastapi import status

class CustomAPIError(Exception):

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "BAD_REQUEST",
        details: dict | None = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self) -> dict:
        return {
            "success": False,
            "error": {
                "message": self.message,
                "code": self.error_code,
                "details": self.details
            }
        }
