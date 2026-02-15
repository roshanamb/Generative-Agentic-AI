from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Employee(BaseModel):
    id: int
    name: str = Field(
        ..., ## Mandatory field, must be provided when creating an instance
        min_length=10,
        max_length=50,
        description="The full name of the employee",
        example="John Doe"
    )
    department: Optional[str] = "General"
    salary: float = Field(
        ...,
        gt=10000, ## Salary must be greater than 10000
        le=200000, ## Salary must be less than or equal to 200000
        description="The salary of the employee",
        example=50000.00
    )

class User(BaseModel):
    email: str = Field(..., regex=r'^\S+@\S+\.\S+$')
    phone: str = Field(..., regex=r'^\+?1?-?\.?\s?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})$')