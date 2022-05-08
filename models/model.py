from pydantic import BaseModel


class mUser(BaseModel):
    nickname: str
    email: str
    password: str


class mPost(BaseModel):
    title: str
    content: str

