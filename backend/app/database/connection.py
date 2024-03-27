from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from redis import asyncio as aioredis
import os
async_engine = create_async_engine(f'mysql+aiomysql://{os.getenv('database_url')}')

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def operation_session(op):
    try:
        async with async_session() as session: 
            result = await op(session)
            return result
    except Exception:
        return None
    
redis = aioredis.from_url('redis://localhost')
