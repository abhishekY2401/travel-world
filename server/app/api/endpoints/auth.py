from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.schemas.token import Token
from app.models.user import User
from app.utilities.utils import verify_hash, hash_password, create_access_token, create_refresh_token
from app.database.session import mongodb
import logging

router = APIRouter()

logger = logging.getLogger(__name__)  # Get a logger for this file


@router.post("/register", response_model=UserCreate)
async def register_user(user: UserCreate):
    logger.info("Attempting to register user: %s", user.email)

    user_collection = mongodb.get_user_collection()
    print(user_collection)

    try:
        # Check if user already exists in the MongoDB collection
        existing_user = await user_collection.find_one({"email": user.email})
        if existing_user:
            logger.error(
                "Registration failed - Email already registered: %s", user.email)
            raise HTTPException(
                status_code=400, detail="Email already registered")

        # Hash the user's password
        hashed_password = hash_password(user.password)

        # Insert the new user into MongoDB
        new_user = {
            "email": user.email,
            "password": hashed_password
        }
        # Insert user into the MongoDB collection
        result = await user_collection.insert_one(new_user)
        if result.inserted_id:
            logger.info("User successfully registered: %s", user.email)
            return {"email": user.email}

    except Exception as e:
        logger.error("An error occurred during registration: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/login", response_model=Token)
async def login_user(user: UserCreate):
    logger.info("Attempting to log in user: %s", user.email)

    user_collection = mongodb.get_user_collection()

    try:
        # Check if the user exists in the MongoDB collection
        db_user = await user_collection.find_one({"email": user.email})
        if not db_user:
            logger.error("Login failed - Invalid email: %s", user.email)
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Verify the password
        if not verify_hash(user.password, db_user["password"]):
            logger.error(
                "Login failed - Incorrect password for email: %s", user.email)
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Generate access and refresh tokens
        access_token = create_access_token(data={"sub": db_user["email"]})
        refresh_token = create_refresh_token(data={"sub": db_user["email"]})

        logger.info("User successfully logged in: %s", user.email)

        # Store refresh token in the database if needed
        await user_collection.update_one(
            {"email": db_user["email"]},
            {"$set": {"refresh_token": refresh_token}}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token
        }

    except Exception as e:
        logger.error("An error occurred during login: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post('/refresh-token', response_model=Token)
def refresh_token(refresh_token: str):
    new_access_token = create_access_token(refresh_token)
    if not new_access_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_token_data = {
        "access_token": new_access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

    return new_token_data
