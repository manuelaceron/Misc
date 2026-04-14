from fastapi import FastAPI, Request, status
from starlette.exceptions import HTTPException as StarlettHTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError

""" 
Exception handlers are not called through the routing system like routes
They are called by Starlett layer
No inspection of parameter depedency, only sends request and exception, no dependency injection 

"""


class BlogExceptionHandler:

    def __init__(
        self,
        app: FastAPI,
        template: Jinja2Templates,
    ):
        self.app = app
        self.template = template
        self.register_handlers()

    def register_handlers(self):
        # decorator registers exception handler to the app
        # exception handler only receives request and exception, must match Starlett signature
        @self.app.exception_handler(StarlettHTTPException)
        def general_http_exception_handler(
            request: Request,
            exception: StarlettHTTPException,
        ):
            message = (
                exception.detail
                if exception.detail
                else "An error occurred. Please check your request and try again."
            )

            if request.url.path.startswith("/api"):
                return JSONResponse(
                    status_code=exception.status_code, content={"detail": message}
                )
            return self.template.TemplateResponse(
                request,
                "error.html",
                {
                    "status_code": exception.status_code,
                    "title": exception.status_code,
                    "message": message,
                },
            )

        @self.app.exception_handler(RequestValidationError)
        def validation_exception_handler(
            request: Request,
            exception: RequestValidationError,
        ):
            if request.url.path.startswith("/api"):
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    content={"detail": exception.errors()},
                )
            return self.template.TemplateResponse(
                request,
                "error.html",
                {
                    "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
                    "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
                    "message": "Invalid request. Please check your input and try again.",
                },
            )
