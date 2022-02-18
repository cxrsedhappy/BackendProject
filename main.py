import uvicorn
from fastapi import FastAPI
from data.db_session import global_init
from routers import menu

app = FastAPI()
app.include_router(menu.router)  # adding routers to FastAPI


@app.get('/', tags=['Main'])
async def index():
    return {'status': 'Setup completed'}


if __name__ == '__main__':
    global_init('db/SuperDatabase.db')  # initialize database for whole project
    uvicorn.run('main:app', host='localhost', port=8000)
