from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class SuccessResponseData(BaseModel):

    email: EmailStr = Field(
        ...,
        description="Email customer's address",
        examples=["some@mail.com", "contact@organization.com"]
    )
    
    organization: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Name organization",
        examples=["Name organization", "Tech Corp"]
    )
    
    phone: Optional[str] = Field(
        None,
        description="Phone number in international format",
        examples=["+90-532-454-64-96", "+7-495-123-45-67", "+1-212-555-1234"]
    )
    
    product: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Product Name",
        examples=["Sensor", "Gateway", "Controller", "Software License"]
    )
    
    createdAt: str = Field(
        ...,
        description="Date and time when the record was created in the format 'YYYY-MM-DD HH:MM:SS'",
        examples=["2026-03-12 10:10:10", "2026-03-15 14:30:00"]
    )

    class Config:

        json_schema_extra = {
            "example": {
                "email": "some@mail.com",
                "organization": "Tech Corp",
                "phone": "+90-532-454-64-96",
                "product": "Sensor",
                "createdAt": "2026-03-12 10:10:10"
            }
        }


class SuccessResponse(BaseModel):

    data: SuccessResponseData = Field(
        ...,
        description="The object with the successful response data"
    )

    class Config:

        json_schema_extra = {
            "example": {
                "data": {
                    "email": "some@mail.com",
                    "organization": "Tech Corp",
                    "phone": "+90-532-454-64-96",
                    "product": "Sensor",
                    "createdAt": "2026-03-12 10:10:10"
                }
            }
        }