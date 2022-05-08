import datetime

from fastapi import APIRouter, Depends

from data.user import Post
from data.db_session import create_session
from routers.user import oauth_scheme, get_current_user
from models.model import mPost

router = APIRouter(prefix='/api/post',
                   tags=['post section'],
                   responses={404: {'description': 'not found'}})  # initialize /post router


@router.post('/', name='Create post')
async def create_post(body: mPost, tkn: str = Depends(oauth_scheme)):
    current_user = await get_current_user(tkn)

    if current_user is False:
        return {'message': 'auth required'}

    connection = create_session()
    post = Post()
    post.author_id = current_user.id
    post.title = body.title
    post.content = body.content
    post.timestamp = datetime.datetime.now().replace(microsecond=0)

    connection.add(post)
    connection.commit()
    connection.close()

    return {'message': 'post created'}


@router.get('/', name='Get post')
async def get_post(pid: int):
    connection = create_session()
    post = connection.query(Post).where(Post.id == pid).first()

    if post is None:
        return {'message': 'not found'}

    return {'id': post.id,
            'author_id': post.author_id,
            'title': post.title,
            'content': post.content,
            'timestamp': post.timestamp}

