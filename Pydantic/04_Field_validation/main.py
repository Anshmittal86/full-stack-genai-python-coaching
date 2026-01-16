from pydantic import BaseModel, Field
from typing import Optional
import re

class Employee(BaseModel):
    id: int
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee Name",
        examples="Ansh Mittal"
    )
    department: Optional[str] = 'General'
    salary: float = Field(
        ...,
        ge=10_000, #gt, le and lt
        le=10_000_00,
        description="Annual Salary in usd"
    )

class User(BaseModel):
    email: str = Field(..., pattern=r'')
    phone: str = Field(..., pattern=r'')
    age: int = Field(
        ...,
        ge=0,
        le=150,
        description="Age in years."
    )
    discount: float = Field(
        ...,
        ge=0,
        le=100,
        description="Discount Percentage"
    )