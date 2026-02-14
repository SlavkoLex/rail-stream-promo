from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

class AsyncMongoDBCollection:

    @classmethod
    def client_init(cls, 
                    host: str, 
                    port: int, 
                    user_name: str, 
                    pwd: str, 
                    authSource: str,
                    authMechanism: str,
                    db_name: str, 
                    collection_name: str) -> AsyncIOMotorClient:
        
        client_mongo = AsyncIOMotorClient(
            host=host, 
            port=port, 
            username=user_name, 
            password=pwd, 
            authSource=authSource,
            authMechanism=authMechanism)
        
        
        db = client_mongo[db_name]
        collection = db[collection_name]
        
        return cls(db,collection)


    def __init__(self, db: AsyncIOMotorDatabase, collection_name: AsyncIOMotorCollection):
        self.db: AsyncIOMotorDatabase = db
        self.collection: AsyncIOMotorCollection = collection_name
        self.client: AsyncIOMotorClient = db.client
    
    def get_current_collection(self) -> AsyncIOMotorCollection:
        return self.collection
        
    def close_current_connect(self) -> None:
        if self.client:
            print("==============================")
            print("Сonnection to mongo is closed!")
            print("==============================")
            self.client.close()

    async def test_connect(self) ->Optional[dict[str, float]]:
        res: dict[str, float] = None
        try:
            res = await self.client.admin.command('ping')
        except Exception as e:
            print(f"Error: {e}")
        return res
