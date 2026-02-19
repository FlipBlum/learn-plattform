from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, critique, epub, learning_paths, news, videos

app = FastAPI(title="Learn Plattform API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(learning_paths.router, prefix="/api/learning-paths", tags=["learning-paths"])
app.include_router(epub.router, prefix="/api/epub", tags=["epub"])
app.include_router(critique.router, prefix="/api/critique", tags=["critique"])


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
