import datetime
from typing import Optional
from pydantic import Field, BaseModel, field_validator 

class OrderModel(BaseModel):

    # =========================================
    # Converts the passed value "YYYY-MM-DD HH:MM:SS, YYYY-MM-DDTHH:MM:SS"
    # for the timestamp field to a value of the type 
    # datetime suitable for saving in Mongo     
    # =========================================
    @field_validator('timestamp', mode='before')
    @classmethod
    def parse_datetime_string(cls, v: str) -> datetime.datetime:

        try:
            if ' ' in v:
                return datetime.datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            elif 'T' in v:
                return datetime.datetime.fromisoformat(v.replace('Z', '+00:00'))
            else:
                return datetime.datetime.strptime(v, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Incorrect date format: {v}. Expected 'YYYY-MM-DD HH:MM:SS'")
        

    email: str = Field(..., description="email address for contacting the customer")

    organization: Optional[str] = Field(default=None, description="the name of the organization, if the order is from a legal entity") 

    phone: Optional[str] = Field(default=None, description="Contact number for communication") 

    timestamp: datetime.datetime = Field(..., description="date of sending the order request")

    product: str = Field(..., description="the category of the ordered product")
