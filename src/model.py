from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Address(BaseModel):
    name: str = Field(regex=r'[A-Za-z]{5,50}')
    zip_code: str = Field(regex=r'[0-9]{5}')
    building_number: Optional[str] = Field(0, regex=r'[0-9]{0,4}')
    street_name: Optional[str] = Field('', regex=r'[A-Za-z]{10,50}')


class AddressRespons(BaseModel):
    id: UUID
    name: str
    zip_code: str
    building_number: Optional[int]
    street_name: Optional[str]
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class User(BaseModel):
    first_name: str = Field(regex=r'[A-Za-z]{5,50}',
                            description='Last Name must be all character at least with length of 5')
    last_name: str = Field(
        regex=r'[A-Za-z]{5,50}',
        description='Last Name must be all character at least with length of 5'
    )
    email: str = Field(
        regex=r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',
        validate_email=True,
        description='Email must by like exmple@example.com')
    address_id: UUID
    password: str = Field(
        regex=r'[A-Za-z0-9]{8,}$',
        description='the password should contain Letters(Lower and Upper),'
        + 'special characters and numbers at least with length 8'
    )
    # @validate_email('email')
    # def check_email(cls, email):
    #     if not re.findall('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', email):
    #         raise ValidationError('message': 'Email must by like exmple@example.com')
    #     return email


class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    created_at: datetime = None
    updated_at: datetime = None
    address: dict = {}

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
