import json
from fastapi import FastAPI, HTTPException,Depends,status
from pydantic import BaseModel
import models
from database import engine, sessionLocal
from sqlalchemy.orm import Session
from schema_data import ClientRegistration,ClientLogin
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from models import ClientRegistrationModel
from checking import loginverification,mobileVerification
import logging
from queryLogic import MaxclientId

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally: 
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=FileResponse)
def loginPage():
    return FileResponse("static/login.html")

@app.post("/loginSubmit",status_code=status.HTTP_201_CREATED)
async def user_post(post : ClientLogin,db:Session = Depends(get_db)):
    post = post.dict()
    mobileNumber=str(post['mobileNumber'])
    password=post['password']
    verificationStatus=await loginverification( mobileNumber,password,db)
    verificationStatus['mobileNumber']=  mobileNumber
    #jsonVerificationStatus = json.dumps(verificationStatus)
    #return jsonVerificationStatus
    return verificationStatus
    #return FileResponse("static/login.html")


@app.post("/registerSubmit",status_code=status.HTTP_201_CREATED)
async def user_post(post : ClientRegistration,db:Session = Depends(get_db)):
    post = post.dict()
    mobileNumber = post['mobileNumber']
    result= await mobileVerification( mobileNumber,db)
    if result:
        jsonRegistrationstatus={"status":0,"message":"Already registered with this number"}
    else:
        try:
            clientId=await MaxclientId(db)
            print(type(clientId))
            clientId=clientId+1
            status=0
            post['clientId']=clientId
            post['status']=status
            db_user =ClientRegistrationModel(**post)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            jsonRegistrationstatus={"status":1,"message":"Resgistration done successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occurred in Registration while commiting the data.")

    #jsonRegistrationstatus = json.dumps(jsonRegistrationstatus)
    return jsonRegistrationstatus
    #return FileResponse("static/login.html")


    
    