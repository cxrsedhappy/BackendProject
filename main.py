import uvicorn
from fastapi import FastAPI

from data.db_session import global_init

from routers import user, post


app = FastAPI()


# adding routers to FastAPI
app.include_router(user.router)
app.include_router(post.router)


if __name__ == '__main__':
    global_init('db/SuperDatabase.db')  # initialize database for whole project
    uvicorn.run('main:app', host='127.0.0.1', port=8000)
