from fastapi import APIRouter
from .redis_client import RedisClient 

router = APIRouter()
redis_client = RedisClient()

@router.get("/redis/get_all_listings")
async def get_all_listings():
    return await redis_client.get_listings()
    
@router.get("/redis/get_listing_by_id")
async def get_listing_by_id(id: int):
    ...
@router.post("/redis/set_listing")
async def set_listing(id: int, name: str, price: float):
    return await redis_client.set_listing(id, name, price)
    