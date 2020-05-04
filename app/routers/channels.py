from typing import List

from fastapi import APIRouter, HTTPException, Depends, Response, Query

from app.crud import channel, video
from app.db import channels
from app.schemas.channel import Channel
from app.schemas.video import Video

router = APIRouter()


async def find_channel(slug: str):
    db_channel = await channel.get_channel_by_slug(slug=slug)
    if db_channel:
        return db_channel
    else:
        raise HTTPException(status_code=404, detail='Канал не найден')


@router.get('/channels/', response_model=List[Channel], tags=['Каналы'], summary='Получить список каналов')
async def read_channels(response: Response, skip: int = 0, limit: int = Query(default=25, ge=1, le=50)):
    db_channels = await channel.get_channels(skip=skip, limit=limit)
    response.headers["X-Total-Count"] = str(await channel.get_channels_count())
    return db_channels


@router.get('/channels/{slug}', response_model=Channel, tags=['Каналы'], summary='Получить канал')
async def read_channel(db_channel: channels = Depends(find_channel)):
    return db_channel


@router.get('/channels/{slug}/videos',
            response_model=List[Video],
            tags=['Видео', 'Каналы'],
            summary='Получение списка видео для канала')
async def read_channel_videos(limit: int = 25, skip: int = 0, db_channel: channels = Depends(find_channel)):
    videos = await video.get_videos(skip=skip, limit=limit, parent=db_channel)
    return videos
