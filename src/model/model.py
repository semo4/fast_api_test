import re
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ValidationError, validator


class Address(BaseModel):
    name: str
    zip_code: str
    building_number: Optional[str] = 0
    street_name: Optional[str] = ''

    # name: str = Query(min_length=10, max_length=50)
    # zip_code: str = Query(length=5)
    # building_number: Optional[int] = Query(None, min_length=1, max_length=4)
    # street_name: Optional[str] = Query(None, min_length=10, max_length=50)

    @validator('name')
    def check_name(cls, value):
        if not re.findall('[A-Za-z]{5,50}', value):
            raise ValueError(
                'Name must contain letter and it\'s length between 10 to 50 letters'
            )
        return value

    @validator('zip_code')
    def check_zip_code(cls, value):
        if len(value) != 5:
            raise ValueError('Zip Code must be number and it\'s length is 5')
        elif not re.findall('[0-9]{5}', value):
            raise ValueError('Zip Code must be number and it\'s length is 5')
        return value

    @validator('street_name')
    def check_street_name(cls, value):
        if not re.findall('[A-Za-z]{10,50}', value):
            raise ValueError(
                'Street name must contain letters and it\'s length between 10 to 50'
            )
        return value

    @validator('building_number')
    def check_building_number(cls, value):
        if not re.findall('[0-9]{0,4}', value):
            raise ValueError('Building number must contain numbers')
        elif not 0 < int(value) < 1000:
            raise ValueError(
                'Bulding number must be garter from 0 and less than 1000')
        return int(value)


class AddressRespons(BaseModel):
    name: str
    zip_code: str
    building_number: Optional[int] = 0
    street_name: Optional[str] = None

    class Config:
        orm_mode = True


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    address_id: UUID

    @validator('first_name')
    def check_first_name(cls, value):
        if not re.findall('[A-Za-z]{10,50}', value):
            raise ValidationError(
                'First Name must contain letter and it\'s length between 10 to 50 letters'
            )
        return value

    @validator('last_name')
    def check_last_name(cls, value):
        if not re.findall('[A-Za-z]{10,50}', value):
            raise ValidationError(
                'Last Name must contain letter and it\'s length between 10 to 50 letters'
            )
        return value

    @validator('email')
    def check_email(cls, value):
        if not re.findall('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',
                          value):
            raise ValidationError(
                'email must be like this format (example@example.com)')
        return value


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    name: Optional[str] = None
    zip_code: Optional[str] = None
    building_number: Optional[int] = None
    street_name: Optional[str] = None

    class Config:
        orm_mode = True
