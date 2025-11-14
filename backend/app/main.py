from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import setup_logger
from app.core.errors import CustomAPIError
from app.core.exception_handler import (
    custom_api_error_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from app.controllers import document_routes, chat_routes

logger = setup_logger()

app = FastAPI()

origins = [
    "https://jv-pharma-gouransh.vercel.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.add_exception_handler(CustomAPIError, custom_api_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(document_routes.router, prefix="/api/docs", tags=["Documents"])
app.include_router(chat_routes.router, prefix="/api/chat", tags=["Chat"])
@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "GenAI backend is running"}

@app.get("/checkup")
async def health_check():
    return {"status": "ok"}