from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.controllers import address_controllers, authantication, users_controllers

app = FastAPI(title='User Address API',
              version="1.0",
              description='User Address Api')

app.include_router(authantication.router)
app.include_router(users_controllers.router)
app.include_router(address_controllers.router)


@app.exception_handler(HTTPException)
async def https_exception_handler(request, exc):
    if exc.status_code == 409:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=jsonable_encoder({
                                'message': 'Not Created',
                                'error': str(exc)
                            }))
    elif exc.status_code == 401:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=jsonable_encoder({
                                'message': 'Not UNAUTHORIZED',
                                'error': str(exc)
                            }))


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content=jsonable_encoder({
                            'message': 'violates constraint',
                            'error': str(exc)
                        }))
