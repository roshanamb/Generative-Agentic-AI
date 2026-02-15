from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class User(BaseModel):
    id: int
    name: str
    email: str
    addresses: Address,
    tags: List[str] = []]

address = Address(street="123 Main St", city="Anytown", state="CA", zip_code="12345")
user = User(id=1, name="John Doe", email="john.doe@example.com", addresses=address, tags=["admin", "user"])
print(user) # Output: id=1 name='John Doe' email='john.doe@example.com' addresses=Address(street='123 Main St', city='Anytown', state='CA', zip_code='12345') tags=['admin', 'user']
print(user.addresses.city) # Output: Anytown
print(user.model_dump_json()) # Output: {"id": 1, "name": "John Doe", "email": "john.doe@example.com", "addresses": {"street": "123 Main St", "city": "Anytown", "state": "CA", "zip_code": "12345"}, "tags": []}
