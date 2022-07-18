from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{'title': 'My first post', 'content': 'This is my first post', "id": 1}, {'title': 'My second post', 'content': 'This is my second post', "id": 2}]

@app.get("/")
# async is not required here
async def root():
     my_message = {"message": "FastAPI / Python Demo Project"}
     return my_message["message"]

@app.get("/posts")
def get_posts():
     return {"posts": my_posts}
     
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
     post_dict = post.dict()
     post_dict['id'] = randrange(0, 10000000)
     my_posts.append(post_dict)

     return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
     for post in my_posts:
          if post['id'] == id:
               return {"post_details": post}
     raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
     for post in my_posts:
          if post['id'] == id:
               my_posts.pop(my_posts.index(post))
               return Response(status_code=status.HTTP_204_NO_CONTENT)
     raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
     for post_dict in my_posts:
          if post_dict['id'] == id:
               post_dict['title'] = post.title
               post_dict['content'] = post.content
               post_dict['published'] = post.published
               post_dict['rating'] = post.rating
               return {"data": post_dict}
     raise HTTPException(status_code=404, detail=f"Post with id {id} not found")