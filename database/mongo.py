from typing import List

from pymongo import AsyncMongoClient

from config import *


class MongoDB:
    def __init__(self) -> None:
        self.mongo = AsyncMongoClient(
            config.MONGO_DB_URI,
        )
        self.db = self.mongo.Star

        self.nks = self.db.nokos


    async def add_nokos(
        self,
        _id: int,
        price: str,
        session: str,
    ):
        return await self.nks.update_one(
            {"_id": _id}, {
                "$set": {
                    "price": price,
                    "session": session,
                }
            }, upsert=True
        )

    async def delete_nokos(self, _id: int):
        return await self.nks.delete_one(
            {"_id": _id}
        )

    async def get_nokos(self):
        result = []
        cursor = self.nks.find(
            {"_id": {"$exists": True}}
        )
        async for data in cursor:
            result.append(data)
        return result 
    async def get_nokos_by_id(self, _id: int):
        return await self.nks.find_one({"_id": int(_id)})


db = MongoDB()
