# No ones here
from pydantic import BaseModel


class m_Item(BaseModel):
    id: int | None
    name: str
    price: str
    size: str
    description: str | None


class m_GetItem(BaseModel):
    id: int
    name: str
    price: str


class m_Bill(BaseModel):
    customer_name: str
    ready: bool = False
    pay: bool = False

