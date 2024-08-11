from typing import Union

from motor.motor_asyncio import AsyncIOMotorCollection
from app.database import Clients


class MongoCollection(AsyncIOMotorCollection):
    def __init__(self, name, database=None, *args, **kwargs):
        """
        Args:
            name: str - name of the collection
            database: (AsyncIOMotorDatabase), defaults to clients.mongo.get_database(MONGO_DATABASE)
        """

    def __new__(cls, name, database: Union[str, None] = None, *args, **kwargs):
        if database is not None:
            collection = AsyncIOMotorCollection(
                database=database, name=name, *args, **kwargs
            )

            collection.__class__ = MongoCollection
            return collection

        else:
            collection = AsyncIOMotorCollection(
                database=Clients.mongodb.get_database(),
                name=name,
                *args,
                **kwargs
            )
            collection.__class__ = MongoCollection
            return collection
