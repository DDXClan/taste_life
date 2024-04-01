import os
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

image_path = './img'

async def add_img(img: UploadFile):
    os.makedirs(image_path, exist_ok=True)
    img_path = os.path.join(image_path, img.filename)
    with open(img_path, 'wb') as file:
        content = await img.read()
        file.write(content)

async def delete(session: AsyncSession, item):
    if not item:
        return None
    await session.delete(item)
    await session.commit()
    return True

async def create(session: AsyncSession, item):
    session.add(item)
    await session.commit()
    return item