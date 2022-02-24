from fastapi import APIRouter
from datetime import datetime
from data.bills import Bill, ItemBill
from data.items import Item
from models.models import m_Bill
from data.db_session import create_session

router = APIRouter(prefix='/bill',
                   tags=['Bill section'],
                   responses={404: {'description': 'Not found'}})


"""
Bills section

ItemBill - Item which used only in bill
Item - Item which used to show pizzeria menu

"""


@router.post('/', name='Create bill')
async def create_bill(customer_name: str):
    connection = create_session()

    bill = Bill()
    bill.customer_name = customer_name
    bill.timestamp = datetime.now().replace(microsecond=0)

    connection.add(bill)
    connection.commit()
    return {'message': {'status': 'success',
                        'bill': {
                            'id': bill.id,
                            'customer_name': bill.customer_name,
                            'items': [item.id for item in bill.item],
                            'ready': bill.ready,
                            'pay': bill.pay,
                            'timestamp': bill.timestamp
                        }}}


@router.post('/{id}', name='Add items to bill')
async def add_items_to_bill(id, item_id: int):
    connection = create_session()

    bill = connection.query(Bill).filter_by(id=id).first()
    item = connection.query(Item).filter_by(id=item_id).first()

    adding_item = ItemBill()
    adding_item.item_id = item_id
    adding_item.timestamp = datetime.now().replace(microsecond=0)

    bill.item.append(adding_item)
    connection.commit()

    return {'message': {'status': 'success',
                        'msg': f'{id}'}}

    # choice = 1/2/3
    # price = 399/499/599


@router.get('/{id}', name='Get bill info')
async def get_bill(id):
    connection = create_session()
    bill = connection.query(Bill).filter_by(id=id).first()
    return {'message': {'status': 'success',
                        'bill': {
                            'id': bill.id,
                            'customer_name': bill.customer_name,
                            'items': [{'id': item.id,
                                       'timestamp': item.timestamp} for item in bill.item],
                            'ready': bill.ready,
                            'pay': bill.pay,
                            'timestamp': bill.timestamp
                        }}}