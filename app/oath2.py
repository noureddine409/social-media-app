from fastapi import Depends, HTTPException, status
from jose import ExpiredSignatureError, JWSError, jwt 
from datetime import datetime, timedelta
import schemas
from fastapi.security import OAuth2PasswordBearer
from database import cursor, conn
from config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data: dict):
    d = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    d.update({'exp': expire})

    encoded_jwt = jwt.encode(d, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str =payload.get("userID")
        if id is None:
            raise credentials_exception
        token_data = schemas.Token_data(id=id)
    except JWSError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="could not validate credentials", 
    headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    
    cursor.execute(""" select * from users where iduser = %s; """,(token.id,))
    user = cursor.fetchone()
    conn.commit()
    return user




