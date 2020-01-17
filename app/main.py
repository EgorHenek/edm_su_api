from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.db.session import Session
from app.routers import channels, events, djs, videos, users, comments

app = FastAPI()

origins = [
    "http://edm.su",
    "https://edm.su",
    "http://localhost:3000"
]

app.include_router(channels.router)
app.include_router(events.router)
app.include_router(djs.router)
app.include_router(videos.router)
app.include_router(users.router)
app.include_router(comments.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware('http')
async def db_session_middleware(requiest: Request, call_next):
    requiest.state.db = Session()
    response = await call_next(requiest)
    requiest.state.db.close()
    return response
