from fastapi import FastAPI, Request
from data.blog_entries import posts
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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
"""
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


@app.get("/", include_in_schema=False)
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "The 6AM Journal"}
    )


@app.get("/api/posts")
def get_posts():
    return posts
