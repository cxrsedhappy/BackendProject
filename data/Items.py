from sqlalchemy import Column, Integer, String
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    purchased = Column(Integer)

    def __repr__(self):
        return f'Items: {self.id} {self.cash} {self.price}'
