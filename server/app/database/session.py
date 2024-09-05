from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging


class MongoDB:
    def __init__(self):
        try:
            # Connect to MongoDB using the URI
            self.client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
            # Make sure you use the correct database name
            self.db = self.client[settings.MONGO_DATABASE]
            logging.info("MongoDB connected successfully.")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise Exception("MongoDB connection failed")

    def get_user_collection(self):
        # Return the 'users' collection from the database
        return self.db["users"]


# Initialize MongoDB instance
mongodb = MongoDB()
