from sqlalchemy import Column, Integer, String, LargeBinary

from app.database import Base


class Secret(Base):
    __tablename__ = 'secret'

    id = Column(Integer, primary_key=True)
    body = Column(LargeBinary)
    phrase = Column(LargeBinary)
    secret_key = Column(String)

    def __str__(self):
        return self.body
