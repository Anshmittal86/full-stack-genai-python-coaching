from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True

product_one = Product(
    name="Mouse",
    price=5.00,
    in_stock=False
)

# Not throw error because in_stock has default value
product_two = Product(
    name="keyboard",
    price=10.00
)

print(product_one)
print(product_two)
