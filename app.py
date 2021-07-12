from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.controller import address, authantication, users

app = FastAPI(version="1.0", description='User Address Api')
app.include_router(authantication.router)
app.include_router(users.router)
app.include_router(address.router)


@app.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail={'message': 'Not Exist'})


@app.exception_handler(ValueError)
async def value_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content=jsonable_encoder({'message': str(exc)}))


@app.exception_handler(HTTPException)
async def https_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content=jsonable_encoder({'message': 'Not Exist'}))


@app.exception_handler(HTTPException)
async def unauthorized_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                        content=jsonable_encoder({'message': 'Not UNAUTHORIZED'}))


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({
            'message':
            'violates constraint', 'error': str(exc)
        }))
