import uvicorn
from fastapi import FastAPI
from data.db_session import global_init
from routers import menu

app = FastAPI()
app.include_router(menu.router)  # adding routers to FastAPI


@app.get('/', tags=['Main'])
async def index():
    return {'message': {'status': 'success'}}


if __name__ == '__main__':
    global_init('db/SuperDatabase.db')  # initialize database for whole project
    uvicorn.run('main:app', host='localhost', port=8000)


# v0.0.3 features
# Main json scheme of the project
# {'message': {'status': 'success/error',               <- status of request
#              'error_msg': 'something wrong buddy',    <- if you got any errors
#              'items/users': []}}                      <- if you got successful request
