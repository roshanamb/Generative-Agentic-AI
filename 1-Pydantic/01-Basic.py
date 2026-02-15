from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

input_data = {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
}
print(input_data)
user = User(**input_data)
print(user)
# Output:id=1 name='John Doe' email='john.doe@example.com'  
