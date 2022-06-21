
from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from database import cursor, conn
from schemas import CreatePost
import oath2

router = APIRouter()
@router.post('/posts', status_code=status.HTTP_201_CREATED)
def createPost(post: CreatePost = Body(...), current_user: int = Depends(oath2.get_current_user)):
    print(current_user['iduser'])
    cursor.execute(""" INSERT INTO posts(title, content, id_user) VALUES(%s, %s, %s) returning *""",(post.title, post.content, current_user['iduser']) )
    new_post = cursor.fetchone()
    print(post)
    conn.commit()
    return {"data": new_post}

@router.get('/posts')
def getPosts(current_user: int = Depends(oath2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]=""):
    #print(limit)
    #print(skip)
    #print(search)
    #print(current_user)
    cursor.execute("""select posts.*, count(votes.post_id) as votes from posts left join votes on posts.id=votes.post_id
     group by posts.id having title like %s or title=%s order by created_at desc LIMIT %s OFFSET %s rows""", ("%"+ search+"%", search, limit,skip))
    posts = cursor.fetchall()
    return {'data': posts}

@router.get('/posts/{id}')
def getPostid(id, current_user: int = Depends(oath2.get_current_user)):
    cursor.execute(""" select posts.*, count(votes.post_id) as votes from posts left join votes on posts.id=votes.post_id
     group by posts.id having posts.id = %s """,(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {'detail' :post}

@router.put('/posts/{id}')
def updatePost(id, post: CreatePost=Body(...), current_user: int = Depends(oath2.get_current_user) ):
    cursor.execute(""" update posts SET title=%s, content=%s, published=%s where id=%s returning *""",(post.title, post.content, post.published, id))
    updatedPost = cursor.fetchone()
    if not updatedPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    id_owner = updatedPost['id_user']
    if id_owner != current_user['iduser']:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    conn.commit()
    return {'data': updatedPost}

@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id, current_user: int = Depends(oath2.get_current_user)):
    
    cursor.execute(""" delete from posts where id = %s returning *""", (id,))
    deletedPost = cursor.fetchone()
    
    if deletedPost is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    id_owner =deletedPost['id_user']
    #print("id owner", id_owner)
    #print("id current user",current_user['iduser'])
    if id_owner != current_user['iduser']:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)