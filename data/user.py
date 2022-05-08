import sqlalchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


class User(SqlAlchemyBase):
    __tablename__ = 'user'
    id = Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    nickname = Column(sqlalchemy.String, nullable=False)
    email = Column(sqlalchemy.String, nullable=False)
    password = Column(sqlalchemy.String, nullable=False)
    post = relationship("Post")
    timestamp = Column(sqlalchemy.DateTime, nullable=False)

    def to_dict(self):
        return {'id': self.id,
                'nickname': self.nickname,
                'email': self.email,
                'password': self.password,
                'post_ids': [post.id for post in self.post],
                'timestamp': str(self.timestamp)}


class Post(SqlAlchemyBase):
    __tablename__ = 'post'
    id = Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    author_id = Column(sqlalchemy.Integer, ForeignKey('user.id'))
    title = Column(sqlalchemy.String, nullable=False)
    content = Column(sqlalchemy.String, nullable=False)
    timestamp = Column(sqlalchemy.DateTime, nullable=False)
