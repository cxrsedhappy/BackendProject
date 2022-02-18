import uvicorn
from fastapi import FastAPI
from data.db_session import global_init

app = FastAPI()


@app.get('/')
async def index():
    return {'status': 'Setup completed'}


if __name__ == '__main__':
    global_init('db/Database.db')
    uvicorn.run('main:app', host='localhost', port=8000)  # Start server on localhost:8000
