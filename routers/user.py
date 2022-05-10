import datetime
import jwt

from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse

from data.db_session import create_session
from data.user import User, Hasher

from models.model import mUser

from starlette import status


JWT_SECRET = 'secret'

oauth_scheme = OAuth2PasswordBearer(tokenUrl='api/user/auth')

router = APIRouter(prefix='/api/user',
                   tags=['user section'],
                   responses={404: {'description': 'Not found'}})  # initialize /user router


async def get_current_user(tkn: str = Depends(oauth_scheme)):
    try:
        print(tkn)
        payload = jwt.decode(tkn, JWT_SECRET, algorithms=['HS256'])
        connection = create_session()
        user = connection.query(User).where(User.id == payload.get('id')).first()
        return user

    except ValueError as e:
        print(e)
        return False


async def auth_user(nickname: str, password: str):
    connection = create_session()
    user = connection.query(User).where(User.nickname == nickname).first()

    if not user:
        return False, None

    if not Hasher.verify_password(password, user.password):
        return False, None

    return True, user


@router.post('/auth', name='Auth user')
async def token(req: Request, username: str = Form(...), password: str = Form(...)):
    user = await auth_user(username, password)
    if not user[0]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    token = jwt.encode(user[1].to_dict(), JWT_SECRET)
    return {'token': token,
            'token_type': 'bearer'}

# USER PART
# <---------------------------------------------------------->


@router.post('/', name='Create user')
async def create_user(body: mUser):
    connection = create_session()
    # create a new user
    user = User()
    user.nickname = body.nickname
    user.email = body.email
    user.password = Hasher.get_password_hash(body.password)  # hash his password
    user.timestamp = datetime.datetime.now().replace(microsecond=0)

    connection.add(user)
    connection.commit()
    connection.close()
    return {'message': f'user created'}


@router.get('/', name='Get user')
async def get_user(uid: int):
    connection = create_session()
    user = connection.query(User).where(User.id == uid).first()
    if user:
        return {'id': user.id,
                'nickname': user.nickname,
                'total_post': len(user.post),
                'posts': [{"author": post.author.nickname,
                           "title": post.title,
                           "content": post.content} for post in user.post],
                'created_at': user.timestamp}
    return {}


@router.get('/me', name='Me')
async def me(tkn: str = Depends(oauth_scheme)):
    user = await get_current_user(tkn)
    return {'id': user.id,
            'nickname': user.nickname,
            'email': user.email,
            'password': user.password,
            'total_post': len(user.post),
            'post_ids': [post.id for post in user.post],
            'created_at': user.timestamp}
