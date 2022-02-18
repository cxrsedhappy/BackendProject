from fastapi import APIRouter
from datetime import datetime
from data.db_session import create_session
from data.items import Item
from models.models import m_Item

router = APIRouter(prefix='/menu',
                   tags=['Menu Section'],
                   responses={404: {'description': 'Not found'}})  # initialize /menu router


@router.post('/', name='create item')
async def create_item(params: m_Item):
    connection = create_session()

    item = Item()  # create Item object
    item.name = params.name  # add params
    item.price = params.price
    item.discount = 0
    item.purchased = 0
    item.description = item.description
    item.timestamp = datetime.now().replace(microsecond=0)

    connection.add(item)
    connection.commit()
    connection.close()

    return {'status': 'item added'}


@router.get('/', name='get item')
async def get_item(id: int = 1, name: str = ''):
    connection = create_session()
    connection.close()
    return {'status': f'id: {id}, name:{name} '}
