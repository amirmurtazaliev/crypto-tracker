import json
from redis.asyncio import Redis

class RedisClient:
    async def get_listings(self):
        async with Redis() as redis:
            try:
                result = {}
                async for key in redis.scan_iter(match="*", count=100):
                    value = await redis.get(key)
                    if value is not None:
                        result[key] = json.loads(value)
                
                return result
            finally:
                await redis.close()
    
    async def set_listing(self, cmc_id: int, name: str, price: float):
        async with Redis() as redis_client:
            return await redis_client.set(str(cmc_id), json.dumps([name, price]))
    
    async def get_listing_by_id(self, id: int):
        async with Redis() as redis:
            try:
                return await redis.get(id)
            finally:
                await redis.close()