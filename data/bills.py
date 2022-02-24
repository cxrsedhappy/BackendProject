import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase
from data.items import Item


class Bill(SqlAlchemyBase):
    __tablename__ = 'Bill'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String)

    item = relationship("ItemBill", backref="items")

    ready = Column(Boolean)
    pay = Column(Boolean)
    timestamp = Column(DateTime)

    def __repr__(self):
        return f'Bill: id:{self.id} price:{self.price}'


class ItemBill(SqlAlchemyBase):
    __tablename__ = 'ItemBill'
    id = Column(Integer, primary_key=True, autoincrement=True)

    bill_id = Column(Integer, ForeignKey('Bill.id'))
    item_id = Column(Integer)
    # count = Column(Integer)
    # size = Column(Integer)
    # price = Column(Integer)
    timestamp = Column(DateTime)

    def __repr__(self):
        return f'BillItem: id:{self.id} price:{self.price}'


# Todo add relationship to items and bills
# bill = Bill()
# for item in bill.items:
#     print(item.id, item.name, item.price)
