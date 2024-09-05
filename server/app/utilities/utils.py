from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.schemas.token import TokenData
from passlib.hash import bcrypt
import logging

logger = logging.getLogger(__name__)


def hash_password(password: str):
    return bcrypt.hash(password)


def verify_hash(password, hash):
    return bcrypt.verify(password, hash)


# generate access token
def create_access_token(data: dict):
    logger.debug("Creating access token for user: %s", data.get("sub"))
    expiry_time = datetime.now() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode = data.copy()
    to_encode.update({"expiry": expiry_time})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGO)

# Generate Refresh Token


def create_refresh_token(data: dict):
    logger.debug("Creating refresh token for user: %s", data.get("sub"))
    expire = datetime.now() + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGO)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithm=[settings.JWT_ALGO])
        email: str = payload.get("sub")

        if email is None:
            return None
        return email
    except jwt.JWTError:
        return None

# Create access token from refresh token


def refresh_access_token(refresh_token: str):
    email = decode_access_token(refresh_token)
    if email:
        return create_access_token({"sub": email})

    return None
