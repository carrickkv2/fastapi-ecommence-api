from typing import Optional
from uuid import uuid4

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from jose import jwt
from jose import JWTError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.connect import get_session
from ..db.operations import get_user_by_id
from .config import Settings
from .security import oauth2_scheme


class TokenData(BaseModel):
    username: Optional[int] = None


settings = Settings()


async def get_current_user(session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    """
    Get's the current logged in user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        username: int | None = payload.get("sub", None)
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(session, id=token_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def generate_unique_reference_code() -> str:
    """
    Generates a unique reference code.
    """
    return str(uuid4())
