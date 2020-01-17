from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.crud import video
from app.schemas.user import MyUser
from app.schemas.video import Video, VideoList
from app.utils import get_db, get_current_admin

router = APIRouter()


@router.get('/videos/', response_model=VideoList, tags=['Видео'], summary='Получить список видео')
def read_videos(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    videos = video.get_videos(db, skip, limit)
    count = video.get_videos_count(db)
    return {'total_count': count, 'videos': videos}


@router.get('/videos/{slug}', response_model=Video, tags=['Видео'], summary='Получить видео')
def read_video(slug: str, db: Session = Depends(get_db)):
    video_db = find_video(slug, db)
    return video_db


@router.delete('/videos/{slug}', tags=['Видео'], summary='Удаление видео', status_code=204)
def delete_video(slug: str, db: Session = Depends(get_db), admin: MyUser = Depends(get_current_admin)):
    video_db = find_video(slug, db)
    if video.delete_video(db, video_db):
        return {}
    else:
        raise HTTPException(400, 'При удалении произошла ошибка')


@router.get('/videos/{slug}/related', response_model=List[Video], tags=['Видео'],
            summary='Получить похожие видео')
def read_related_videos(slug: str, db: Session = Depends(get_db), limit: int = 15):
    video_db = find_video(slug, db)
    related_videos = video.get_related_videos(video_db.title, db, limit)
    return related_videos


def find_video(slug: str, db: Session):
    video_db = video.get_video_by_slug(db, slug)
    if video_db:
        return video_db
    else:
        raise HTTPException(status_code=404, detail='Видео не найдено')
