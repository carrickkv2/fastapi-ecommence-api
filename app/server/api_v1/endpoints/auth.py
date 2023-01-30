import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.common import get_current_user
from ....core.security import authenticate
from ....core.security import create_access_token
from ....core.security import get_password_hash
from ....db import operations
from ....db.connect import get_session
from ....schemas.auth_endpoint_validators import UserLoginDB
from ....schemas.auth_endpoint_validators import UserSignupDB
from ....schemas.auth_endpoint_validators import UserSignupSchema


log = logging.getLogger("uvicorn")
router = APIRouter()


@router.post(
    "/signup",
    response_model=UserSignupDB,
    status_code=201,
)
async def create_new_user(user: UserSignupSchema, session: AsyncSession = Depends(get_session)):
    """
    An endpoint to create(signup) a new user using a POST request.
    """

    if user.password != user.password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The password and password confirmation do not match.",
        )

    if await operations.get_user_by_email(session, user.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )

    if await operations.get_user_by_phone_number(session, user.phone_number) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this phone number already exists.",
        )

    try:

        user = dict(user)
        password = user.pop("password")

        # Hash the password
        user["password"] = get_password_hash(password)

        # Convert the dict back to a pydantic model.
        user = UserSignupSchema(**user)

        db_response = await operations.add_new_user_to_db(session, user)
        db_response = dict(db_response)

        response_object = {
            "user_id": db_response["id"],
            "message": "Created a new user successfully",
            "email": user.email,
            "phone_number": user.phone_number,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        return response_object

    except Exception as e:
        log.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error : [{e}] occurred while creating a new user.",
        )


@router.post(
    "/login",
    response_model=UserLoginDB,
    status_code=200,
)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)
):
    """
    An endpoint to login a user using form data from OAuth2.
    """

    user = await authenticate(email=form_data.username, password=form_data.password, db_session=session)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username(email) or password")

    access_token = create_access_token(sub=user["id"])

    return {
        "message": "Logged in user successfully",
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
def read_users_me(current_user=Depends(get_current_user)):
    """
    Fetch the current logged in user.
    """
    user = current_user
    return user
