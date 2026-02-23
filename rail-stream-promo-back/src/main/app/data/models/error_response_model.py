from typing import Any, Dict, Optional
from pydantic import Field, BaseModel


class ErrorResponse(BaseModel):

    type: str = Field(
        default="about:blank",
        description="URI link to the description of the error type",
        examples=["https://api.example.com/errors/database-error"]
    )
    title: str = Field(
        ...,  
        description="The short name of the error",
        examples=["Database Error", "Validation Failed", "Not Found"]
    )
    status: int = Field(
        ...,  
        ge=100, le=599,
        description="HTTP status error code",
        examples=[500, 400, 404]
    )
    detail: Optional[str] = Field(
        None,
        description="Detailed error description",
        examples=["The order data could not be saved. Try again later"]
    )
    instance: Optional[str] = Field(
        None,
        description="The path to the endpoint' that caused the error",
        examples=["/api/save/form/order", "/api/users/123"]
    )
    

    extensions: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional information about the error"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "type": "https://api.example.com/errors/database-error",
                "title": "Database Error",
                "status": 500,
                "detail": "The order data could not be saved. Try again later",
                "instance": "/api/save/form/order",
                "extensions": {
                    "timestamp": "2024-01-01T12:00:00Z",
                    "request_id": "abc-123-def"
                }
            }
        }