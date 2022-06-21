from fastapi import APIRouter, Body, HTTPException, status
from database import cursor, conn
from schemas import CreateUser
import cryptpwd

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED)
def createUser(user: CreateUser = Body(...)):
    password = cryptpwd.hash(user.password)
    try:
        cursor.execute(""" insert into users(email, password) values(%s, %s) returning (iduser, email, created_at)""",(user.email, password))
        newUser = cursor.fetchone()
        conn.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"there already exists an acount registred with {user.email}")
    return {'new user':newUser}

@router.get('/users/{id}', status_code=status.HTTP_200_OK)
def getUser(id):
    cursor.execute(""" select iduser, email, created_at from users where iduser = %s """,(id))
    user = cursor.fetchone()
    return {'data': user}


