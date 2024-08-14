from sqlalchemy import Boolean, Integer, String, Column
from database import Base, engine

class ClientRegistrationModel(Base):
    __tablename__ = "ClientRegistration"

    clientId = Column(Integer, primary_key=True, index=True)
    userName= Column(String(50))
    emailId = Column(String(50))
    mobileNumber = Column(String(20))
    firmName = Column(String(50))
    location =Column(String(50))
    state=Column(String(50))
    country=Column(String(50))
    password=Column(String(50))
    status=Column(Integer)

