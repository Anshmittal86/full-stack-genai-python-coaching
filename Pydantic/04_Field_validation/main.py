from typing import Optional
from typing_extensions import Self
from pydantic import BaseModel, Field, field_validator, model_validator

class Employee(BaseModel):
    id: int
    name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description='Name of user',
        examples=['John Doe']
    )
    department: Optional[str] = 'General'
    salary: float = Field(
        ...,
        ge=10_000 # gt, le, lt
    )


class User(BaseModel):
    email: str = Field(..., pattern=r'')
    phone: str = Field(..., pattern=r'')
    age: int = Field(
        ...,
        ge=0,
        le=150,
        description='Age in years',
    )
    discount: float = Field(
        ...,
        ge=0,
        le=100,
        description='Discount percentage',
    )

employee = Employee(
    id=1,
    name='Ansh Mittal',
    salary=20000,
)

class Person(BaseModel):
    username: str
    old_password: str
    new_password: str

    # Validation for single field [(model='after') default]
    @field_validator('username')
    @classmethod
    def validate_username(cls, v:str) -> str:
        if len(v) < 2:
            raise ValueError('Username must be at least 2 characters long')
        return v

    # Validation for multiple fields
    @model_validator(mode='after')
    def check_password_are_different(self) -> Self:
        if self.old_password == self.new_password:
            raise ValueError('New password must be different')
        return self

person = Person(
    username="om",
    old_password="123",
    new_password="12",
)

print(person)