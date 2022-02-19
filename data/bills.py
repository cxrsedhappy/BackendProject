import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from data.db_session import SqlAlchemyBase


class Bill(SqlAlchemyBase):
    __tablename__ = 'Bills'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    # items = relationship()
    pay = Column(Boolean)
    timestamp = Column(DateTime)

    def __repr__(self):
        return f'Bill: id:{self.id} price:{self.price}'


# Todo add relationship to items and bills
# bill = Bill()
# for item in bill.items:
#     print(item.id, item.name, item.price)
