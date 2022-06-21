
from fastapi import APIRouter, Body, HTTPException, status, Form
from database import cursor
import cryptpwd
import schemas
import oath2
router = APIRouter()

@router.post('/login')
def login(email: str = Form(...), password: str = Form(...), response_model=schemas.Token):
    cursor.execute(""" select * from users where email = %s""", (email,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credential")

    if not cryptpwd.verify(password, user['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credential")

    access_token = oath2.create_access_token(data= {"userID": user['iduser']})

    return {"access_token": access_token, "token type": 'bearer'}