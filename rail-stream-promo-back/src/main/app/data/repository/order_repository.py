from typing import Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId

from data.models.order_model import OrderModel


# ==========================
# A class for working with order 
# collections
# ==========================
class OrderRepository:
    
    def __init__(self, mongo_collection: AsyncIOMotorCollection):
        self.collection: AsyncIOMotorCollection = mongo_collection

    async def post_order_info(self, order_document: OrderModel) -> Optional[ObjectId]:
        try:
            result: InsertOneResult = await self.collection.insert_one(order_document.model_dump())
            return result.inserted_id
        except Exception as e:
            print(f"Error inserting user: {e}")
            return None