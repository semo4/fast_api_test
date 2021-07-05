from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Address(BaseModel):
    name: Optional[str] = None
    zip_code: Optional[str] = None
    street_name: Optional[str] = None
    building_number: Optional[int] = 0


class User(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    address_id: Optional[UUID] = None
    name: Optional[str] = None
    zip_code: Optional[str] = None
    street_name: Optional[str] = None
    building_number: Optional[int] = 0
