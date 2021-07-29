from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.database import users
from src.hashpass import Hash
from src.model import Token
from src.token import create_access_token

router = APIRouter(prefix='/login', tags=['Authantication'])


@router.post('/')
async def login(request: OAuth2PasswordRequestForm = Depends()):
    result = users.select().where(
        users.c.email == request.username).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Incorrect username or password')
    if not Hash.verify(result.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Incorrect username or password')
    access_token = create_access_token(data={"sub": result.email})
    return Token(access_token=access_token, token_type='bearer')
