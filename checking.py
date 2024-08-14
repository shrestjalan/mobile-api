from models import ClientRegistrationModel
from fastapi import  HTTPException
from sqlalchemy.orm import Session

async def loginverification(mobileNumber:str,password:str,db:Session):
    try:
        db_user = db.query(ClientRegistrationModel).filter( ClientRegistrationModel.mobileNumber == mobileNumber).first()
        if db_user:
            customer=db_user.status

            if db_user.password==password:
                return {"status": 1,"message":"verifiedSuccessfully","isCustomer":customer}
            else:
                return {"status": 0,"message":"wrongPassword","isCustomer":customer}
        else:
            return {"status": -1,"message":"notRegistered","isCustomer":0}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during verification.")
    
async def mobileVerification(mobileNumber:str,db:Session):
    try:
        db_user = db.query(ClientRegistrationModel).filter( ClientRegistrationModel.mobileNumber == mobileNumber).first()
        if db_user:
            return 1
        else:
            return 0
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during mobile Verification.")
