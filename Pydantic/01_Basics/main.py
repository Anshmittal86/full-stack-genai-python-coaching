from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int
    gender: str

user_one = {
    "id":1,
    "name":"John",
    "age":18,
    "gender":"Male"
}

# Pydantic always tries to convert values into the given annotated types
user_two = {
    "id":'1',
    "name":"John",
    "age":'18',
    "gender":"Male"
}


first_user = User(**user_one)
second_user = User(**user_two)

print(first_user)
print(second_user)