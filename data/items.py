from sqlalchemy import Column, Integer, String, DateTime
from data.db_session import SqlAlchemyBase


class Item(SqlAlchemyBase):
    __tablename__ = 'Items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    price = Column(String)
    size = Column(String)
    description = Column(String, nullable=True)
    discount = Column(Integer)
    purchased = Column(Integer)
    timestamp = Column(DateTime)

    def __repr__(self):
        return f'Item: id:{self.id} name:{self.name}'
