from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Address(BaseModel):
    name: str = Field(regex=r'[A-Za-z]{5,50}')
    zip_code: str = Field(regex=r'[0-9]{5}')
    building_number: Optional[str] = Field(0, regex=r'[0-9]{0,4}')
    street_name: Optional[str] = Field('', regex=r'[A-Za-z]{10,50}')


class AddressRespons(BaseModel):
    name: str
    zip_code: str
    building_number: Optional[int] = 0
    street_name: Optional[str] = None

    class Config:
        orm_mode = True


class User(BaseModel):
    first_name: str = Field(regex=r'[A-Za-z]{5,50}')
    last_name: str = Field(regex=r'[A-Za-z]{5,50}')
    email: str = Field(regex=r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')
    address_id: UUID


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    name: str
    zip_code: str
    building_number: Optional[int] = 0
    street_name: Optional[str] = None

    class Config:
        orm_mode = True
