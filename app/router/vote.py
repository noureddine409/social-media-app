from fastapi import APIRouter, Body, Depends, HTTPException, status
from schemas import vote
from database import cursor, conn
import oath2

router = APIRouter()

@router.post('/votes', status_code=status.HTTP_201_CREATED)
def vote(vote: vote=Body(...), current_user: int = Depends(oath2.get_current_user) ):
    cursor.execute(""" SELECT * FROM posts where id = %s """, (vote.post_id,))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {vote.post_id} does not exist")
    cursor.execute(""" SELECT * FROM votes WHERE post_id=%s and user_id=%s """, (vote.post_id, current_user['iduser']))
    vote_found = cursor.fetchone()
    if vote.dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already added")
        else:
            cursor.execute(""" insert into votes values(%s, %s)""", (vote.post_id, current_user['iduser']))
            conn.commit()
            return {"message": "successfully added vote"}
    if vote.dir == 0:
        if vote_found is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already removed")
        else:
            cursor.execute(""" delete from votes where post_id = %s and user_id = %s """, (vote.post_id, current_user['iduser']))
            conn.commit()
            return {"message": "successfully removed vote"}

    else:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)