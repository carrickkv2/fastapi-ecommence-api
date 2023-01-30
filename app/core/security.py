from datetime import datetime
from datetime import timedelta
from typing import List
from typing import MutableMapping
from typing import Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.operations import get_user_by_email
from .config import Settings


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWTPayloadMapping = MutableMapping[str, Union[datetime, bool, str, List[str], List[int]]]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{Settings().API_VERSION}/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


async def authenticate(
    *,
    email: str,
    password: str,
    db_session: AsyncSession,
):
    """
    Authenticate a user by email and password.
    """
    user = await get_user_by_email(db_session, email=email)
    if not user:
        return None
    user = dict(user[0])
    if not verify_password(password, user["password"]):
        return None
    return user


def create_access_token(*, sub: str) -> str:
    """
    Create an access token.
    """
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)

    return jwt.encode(payload, Settings().JWT_SECRET, algorithm=Settings().ALGORITHM)
