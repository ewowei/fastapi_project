from fastapi import Response,APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema, oauth2

from sqlalchemy import func

from typing import List, Optional

router = APIRouter(prefix="/posts", tags=['Posts'])


#1. GET POSTS
@router.get("/", response_model= List[schema.PostOut])
def  get_posts(db: Session = Depends(get_db), 
               current_user: int = Depends(oauth2.get_current_user)
               , limit: int = 10, skip: int = 0, search: Optional[str]= ""): 
     
     
    #  posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
      
     posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
         models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
         models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # To get all posts from a specific owner_id(posts)
    #  posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # type: ignore
   
     return posts


# 2. GET A SINGLE POST WITH {id}
@router.get("/{id}", response_model=schema.PostOut)
def get_singlepost(id: int, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
  
    # post = db.query(models.Post).filter(models.Post.id==id).first()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
         models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id==id).first()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return posts


# 3. CREATE POSTS 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # print(current_user.email) # type: ignore
    print(current_user)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # type: ignore
    print(new_post.title)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
   

# 4. DELETING A POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
  
    post_query = db.query(models.Post).filter(models.Post.id==id)
    
    print('hello', post_query)
    post = post_query.first()
    print('hmmm', post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this operation")
    
    post_query.delete(synchronize_session=False)
    print(post)
    db.commit()
   
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# 5. UPDATE A POST
@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
 
     post_query = db.query(models.Post).filter(models.Post.id == id)

     post = post_query.first()

     if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
     
     if post.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this operation")
     post_query.update(updated_post.dict(), synchronize_session=False) # type: ignore

     db.commit()
   
     return post_query.first()