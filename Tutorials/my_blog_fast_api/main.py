from fastapi import FastAPI
from data.blog_entries import posts
from fastapi.responses import HTMLResponse

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
"""
app = FastAPI()


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def home():
    # return {"message": "Welcome to my blog!"}
    return f"<h1> Welcome to my blog! </h1>"


@app.get("/api/posts")
def get_posts():
    return posts
