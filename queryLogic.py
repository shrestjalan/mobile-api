from models import ClientRegistrationModel
from fastapi import  HTTPException
from sqlalchemy.orm import Session


async def MaxclientId(db:Session)->int:
    try:
        result = db.query(ClientRegistrationModel).order_by(ClientRegistrationModel.clientId.desc()).first()
            # Return the highest clientId or 0 if the table is empty
        return result.clientId if result else 0
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error During registrartion.")
