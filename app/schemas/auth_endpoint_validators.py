from __future__ import annotations

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Extra
from pydantic import Field


class UserBaseSchema(BaseModel):
    """
    Pydantic validator (schema) for a new user.
    """

    class Config:
        extra = Extra.forbid  # forbid extra fields

    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)


class UserSignupSchema(UserBaseSchema):
    """
    Pydantic validator (schema) for the signup of a new user.
    Defines a data validation model for the signup endpoint.
    This makes sure that we receive the data is what we expect.
    """

    class Config:
        extra = Extra.forbid  # forbid extra fields

    password: str = Field(..., min_length=8, max_length=300)
    password_confirmation: str = Field(..., min_length=3, max_length=50)


class UserSignupDB(UserBaseSchema):
    user_id: int
    message: str

    class Config:
        orm_mode = True  # tell pydantic to read the data as if from an ORM, not a dict


class UserLoginDB(BaseModel):
    message: str
    access_token: str
    token_type: str
