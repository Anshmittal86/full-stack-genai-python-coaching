from pydantic import BaseModel
from typing import Optional, List, Dict

class Cart(BaseModel):
    id: int
    user_id: int
    items: List[str]
    quantities: Dict[str, int]
    total_price: float = 0.0
    currency: Optional[str] = 'INR'

cart = Cart(
    id=1,
    user_id=1,
    items=['Mouse', 'Keyboard'],
    quantities={
        'Mouse':1,
        'Keyboard':2
    }
)

print(cart)

