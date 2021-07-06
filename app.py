from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from src.controller import address, users
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(version="1.0", description='User Address Api')
app.include_router(users.router)
app.include_router(address.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(status_code=exc.status_code,
                             detail={'message': exc.detail})


@app.exception_handler(ValueError)
async def value_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content=jsonable_encoder({'message': str(exc)}))


@app.exception_handler(StarletteHTTPException)
async def https_exception_handler(request, exc):
    return await http_exception_handler(request, exc)
