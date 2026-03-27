from fastapi import FastAPI, Request, HTTPException, status
from data.blog_entries import posts, blog_name
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarlettHTTPException
import exception_handler as Blog_exception

""" 
FastAPI Supports sync and async functions

fastapi dev main.py -> converts my functions to json (or HTML if needed)
 - dev: better for debugging, re starst server after changes
 - run: optimized for production
 
 Automatic route documentation generation in http://127.0.0.1:8000/doc or ../redoc
 
 Recommendation:
  - Have separation between API routes (json response: for programmatic purposes) 
    and HTML routes (for human readability) -> Use include in schema to hide from documentation HTML responses
  - Decorator stacking, in the example, to give many routes to the same function
  - python string for HTML is not optima, use templates instead (Jinja 2 is template engine used by FastAPI and Flask)
  
  - Template inheritance important for maintanability and avoid repeated code:
    - Have main structure in parent with blocks
    - Templated inherits from parent and implement blocks
    
 - Add path parameters to endpoint
"""


class PostNotFoundError(Exception):
    pass


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")  # templates object


""" 
First example of api route with HTML response
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def home():
    # return {"message": "Welcome to my blog!"}
    return f"<h1> Welcome to my blog! </h1>" 
"""

data = {"posts": posts, "title": blog_name}


# -------------------------------- API Routes --------------------------------


@app.get("/api/posts")
def get_posts():
    return posts


@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        # get returns None if key doesnt exist
        # ["id"] return error is key doesnt exist
        if post.get("id") == post_id:
            return post

    # Custome exception
    # raise PostNotFoundError(f"Post {post_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


# -------------------------------- HTML Routes --------------------------------


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", data)


@app.get("/posts/{post_id}", include_in_schema=False, name="post_detail")
def get_post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return templates.TemplateResponse(
                request, "post.html", {"post": post, "title": data["title"]}
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
