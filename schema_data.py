from pydantic import BaseModel

class ClientRegistration(BaseModel):
    userName : str
    emailId  : str
    mobileNumber : str
    firmName : str
    location  : str
    password  : str
    state:str
    country:str


class ClientLogin(BaseModel):
    mobileNumber : str
    password     : str


