from urllib.error import HTTPError

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from sqlalchemy.exc import IntegrityError

from src.controllers import address_controllers, authantication, users_controllers

app = FastAPI(title='User Address API',
              version="1.0",
              description='User Address Api')

app.include_router(authantication.router)
app.include_router(users_controllers.router)
app.include_router(address_controllers.router)


@app.exception_handler(HTTPError)
async def https_exception_handler(request, exc):
    if exc.status_code == 422:
        return Response(status_code=status.HTTP_409_CONFLICT,
                        content=jsonable_encoder({
                            'message': 'Not Exist',
                            'error': str(exc)
                        }))
    if exc.status_code == 401:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED,
                        content=jsonable_encoder({
                            'message': 'Not UNAUTHORIZED',
                            'error': str(exc)
                        }))
    if exc.status_code == 409:
        return Response(status_code=status.HTTP_409_CONFLICT,
                        content=jsonable_encoder({
                            'message': 'Not Created',
                            'error': str(exc)
                        }))


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content=jsonable_encoder({
                            'message': 'violates constraint',
                            'error': str(exc)
                        }))
