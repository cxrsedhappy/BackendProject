from fastapi import APIRouter
from datetime import datetime
from data.db_session import create_session
from data.items import Item
from models.models import m_Item, m_GetItem

router = APIRouter(prefix='/menu',
                   tags=['Menu Section'],
                   responses={404: {'description': 'Not found'}})  # initialize /menu router


@router.post('/', name='Create Item')
async def create_item(params: m_Item):
    connection = create_session()

    # TODO create sizes check code with prices
    # Whats the best way?
    # 1) price str (not int) param with 399/499/599 and sizes with the same way
    # 2) two new database tables with relationship to prices and params
    # (I prefer the first one)
    # if '/' not in params.sizes:
    #     return {'message': {'status': 'error',
    #                         'error_msg': 'sizes does not have /'}}

    item = Item()  # create Item object
    item.name = params.name  # add params
    item.price = params.price
    item.discount = 0
    item.purchased = 0
    # item.sizes = params.sizes
    item.description = item.description
    item.timestamp = datetime.now().replace(microsecond=0)

    connection.add(item)
    connection.commit()
    connection.close()

    return {'message': {'status': 'success'}}


@router.get('/', name='Get Item')
async def get_item(id: int = 0, name: str = None, price: int = None):
    connection = create_session()
    params = [id, name, price]
    results = []

    # Search by id
    if id is not None:
        query = connection.query(Item)
        results = query.all() if id == 0 else query.filter_by(id=id)  # if id == 0 then return all items in database

    # Search by name
    elif name is not None:
        results = connection.query(Item).filter_by(name=name).all()

    # Search by price
    elif price is not None:
        results = connection.query(Item).filter_by(price=price).all()

    connection.close()
    return {'message':
                {'status': 'success',
                 'items': [
                    {'id': f'{item.id}',
                     'name': f'{item.name}',
                     'price': f'{item.price}',
                     'description': f'{item.description}',
                     'discount': f'{item.discount}',
                     'purchased': f'{item.purchased}',
                     'timestamp': f'{item.timestamp}'} for item in results]}}


# Todo fix create item id
# Why do we need id in params when we create item if id is autoincrement?
# Do not know lol
# Todo add search by size
# I WANT MY BIG SAUSAGE PIZZA WHY THERE EVERYTHING IS SMALL
