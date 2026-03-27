from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarlettHTTPException


class BlogExceptionHandler:

    def __init__(self, app: FastAPI):
        self.app = app
        self.register_handlers()

    def register_handlers(self):

        @self.app.exception_handler(StarlettHTTPException)
        def general_http_exception_handler(
            self, request: Request, exception: StarlettHTTPException
        ):
            message = (
                exception.detail
                if exception.detail
                else "An error occurred. Please check your request and try again."
            )
            return message  # TODO: return template
