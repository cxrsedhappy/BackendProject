# No ones here
from pydantic import BaseModel


class m_Item(BaseModel):
    id: int | None
    name: str
    price: int
    # sizes: str
    description: str | None


class m_GetItem(BaseModel):
    id: int
    name: str
    price: int

