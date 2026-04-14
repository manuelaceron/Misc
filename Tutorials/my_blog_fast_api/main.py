from fastapi import FastAPI
from config import templates
from routes.api import router as api_router
from routes.web import router as web_router
from fastapi.staticfiles import StaticFiles
from exceptions.exception_handler import (
    BlogExceptionHandler,
)

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


app = FastAPI()
app.include_router(api_router)
app.include_router(web_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
BlogExceptionHandler(app, templates)
