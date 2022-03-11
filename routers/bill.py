from fastapi import APIRouter
from datetime import datetime
from data.bills import Bill, ItemBill
from data.items import Item
from models.models import m_Bill
from data.db_session import create_session

router = APIRouter(prefix='/bill',
                   tags=['Bill section'],
                   responses={404: {'description': 'Not found'}})


@router.post('/', name='Create bill')
async def create_bill(customer_name: str):
    """
    creates bill

    :param customer_name: str
    :return: status with bill scheme
    """
    connection = create_session()

    bill = Bill()
    bill.customer_name = customer_name
    bill.ready = False
    bill.pay = False
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


@router.post('/{bill_id}', name='Add item to bill')
async def add_items_to_bill(bill_id, item_id: int):
    connection = create_session()

    bill = connection.query(Bill).filter_by(id=bill_id).first()
    item = connection.query(Item).filter_by(id=item_id).first()

    adding_item = ItemBill()
    adding_item.item_id = item_id
    adding_item.timestamp = datetime.now().replace(microsecond=0)

    bill.item.append(adding_item)
    connection.commit()

    return {'message': {'status': 'success',
                        'msg': f'{bill_id}'}}

    # choice = 1/2/3
    # price = 399/499/599


@router.delete('/{bill_id}', name='Delete item from bill')
async def add_items_to_bill(bill_id, item_id: int):
    connection = create_session()
    bill = connection.query(Bill).filter_by(id=bill_id).first()
    item = connection.query(Item).filter_by(id=item_id).first()

    print(bill.item)
    print(item)


@router.get('/{bill_id}', name='Get bill info')
async def get_bill(bill_id):
    connection = create_session()
    bill = connection.query(Bill).filter_by(id=bill_id).first()
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