from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class LearningPathStatus(str, Enum):
    active = "active"
    paused = "paused"
    completed = "completed"


class LearningPathCreate(BaseModel):
    name: str
    status: LearningPathStatus = LearningPathStatus.active


class LearningPathUpdate(BaseModel):
    name: str | None = None
    status: LearningPathStatus | None = None


class LearningPath(BaseModel):
    id: str
    user_id: str
    name: str
    status: LearningPathStatus
    created_at: datetime


class EpubCreate(BaseModel):
    learning_path_id: str
    title: str


class EpubProgressUpdate(BaseModel):
    current_chapter: int = Field(ge=0)
    progress_percent: float = Field(ge=0, le=100)


class Epub(BaseModel):
    id: str
    user_id: str
    learning_path_id: str
    title: str
    file_path: str
    total_chapters: int
    current_chapter: int
    progress_percent: float
    uploaded_at: datetime


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct_index: int


class QuizSubmission(BaseModel):
    answers: list[int]


class Quiz(BaseModel):
    id: str
    epub_id: str
    chapter: int
    questions: list[QuizQuestion]
    answers: list[int] | None = None
    score: float | None = None
    taken_at: datetime | None = None


class Critique(BaseModel):
    id: str
    user_id: str
    period: str
    content: str
    created_at: datetime
