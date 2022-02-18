# No ones here
from pydantic import BaseModel


class m_Item(BaseModel):
    id: int | None
    name: str
    price: int
    description: str | None

