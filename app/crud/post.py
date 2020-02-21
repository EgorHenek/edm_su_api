from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import Post
from app.models import User
from app.schemas.post import BasePost


def create_post(db: Session, post: BasePost, user: User):
    db_post = Post(**post.dict(), user=user)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post_by_slug(db: Session, slug: str):
    db_post = db.query(Post).filter_by(slug=slug).first()
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 12):
    return db.query(Post).filter(Post.published_at <= datetime.now()) \
        .order_by(desc(Post.published_at)).offset(skip).limit(limit).all()
