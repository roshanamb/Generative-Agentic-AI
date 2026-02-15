from pydantic import BaseModel, Field, computed_field

class Product(BaseModel):
    price : float
    quantity : int

    @computed_field
    @property   ## This is a computed property, it will be calculated on the fly when accessed, and it won't be stored in the model's data.
    def total_price(self) -> float:
        return self.price * self.quantity
    

product = Product(price=10.0, quantity=5)
print(product.total_price)  # Output: 50.0
print(product.model_dump()) # Output: {'price': 10.0, 'quantity': 5, 'total_price': 50.0}

