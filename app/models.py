from sqlalchemy import Column, Integer, String

from app.database import Base


class Secret(Base):
    __tablename__ = 'secret'

    id = Column(Integer, primary_key=True)
    body = Column(String)
    phrase = Column(String)
    secret_key = Column(String)
