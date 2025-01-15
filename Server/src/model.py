from pymongo import MongoClient
from loguru import logger

from src.config import server_config
from src.schema import Record, Filters
from src.security import get_now

# Create a new client and connect to the server
# Send a ping to confirm a successful connection
try:
    client = MongoClient(server_config.mongo.MONGO_URI)
    client.admin.command("ping")
except Exception as e:
    logger.error(e)


# Get the database and collection
db = client[server_config.mongo.MONGO_DB]
collection = db[server_config.mongo.MONGO_COLLECTION]


def test_connection():
    try:
        client.admin.command("ping")
        logger.info("Connected to MongoDB")
        return True
    except Exception as e:
        logger.error(e)
        return False


def get_service():
    return Service()


class Service:
    def backfill_records(self, records: list[Record]):
        created_records = collection.insert_many(
            [record.model_dump() for record in records]
        )
        return collection.find({"_id": {"$in": created_records.inserted_ids}})

    def insert(self):
        return self.create_record(Record(seen=False, created_at=get_now()))

    async def watch_collection(self):
        async with collection.watch(full_document="updateLookup") as stream:
            async for change in stream:
                yield change

    def create_record(self, record: Record):
        new_record = collection.insert_one(record.model_dump())
        created_record = collection.find_one({"_id": new_record.inserted_id})
        return created_record

    def read_record_by_id(self, id):
        return collection.find_one({"_id": id})

    def read_records(self, filters: Filters):
        query = {}
        if filters.seen is not None:
            query["seen"] = filters.seen
        if filters.created_at_start is not None:
            query["created_at"] = {"$gte": filters.created_at_start}
        if filters.created_at_end is not None:
            query["created_at"] = {"$lte": filters.created_at_end}
        return collection.find(query)

    def read_heat_maps(self, filters: Filters):
        query = {}
        if filters.seen is not None:
            query["seen"] = filters.seen
        if filters.created_at_start is not None:
            query["created_at"] = {"$gte": filters.created_at_start}
        if filters.created_at_end is not None:
            query["created_at"] = {"$lte": filters.created_at_end}

        # aggregate the data by date
        return collection.aggregate(
            [
                {"$match": query},
                {"$group": {"_id": {"$toLong": "$created_at"}, "value": {"$sum": 1}}},
            ]
        )

    def update_record(self, id, record: Record):
        update_result = collection.update_one(
            {"_id": id}, {"$set": record.model_dump()}
        )
        return collection.find_one({"_id": id})

    def delete_record(self, id):
        return collection.delete_one({"_id": id})
