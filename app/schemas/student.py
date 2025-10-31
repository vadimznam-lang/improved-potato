from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    name: str
    email: EmailStr
    interests: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    goals: List[str] = Field(default_factory=list)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    interests: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    goals: Optional[List[str]] = None


class LearningPathStep(BaseModel):
    title: str
    description: str
    resource: str


class LearningPath(BaseModel):
    overview: str
    steps: List[LearningPathStep]


class StudentProgressInfo(BaseModel):
    completed_courses: List[str] = Field(default_factory=list)
    current_step: str = ""
    progress_percent: int = 0
    last_feedback: Optional[str] = None


class StudentResponse(StudentBase):
    id: int
    learning_path: LearningPath
    recommended_professions: List[str]
    soft_skill_recommendations: List[str]
    points: int
    achievements: List[str]
    progress: Optional[StudentProgressInfo] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class StudentProgressUpdate(BaseModel):
    completed_courses: Optional[List[str]] = None
    current_step: Optional[str] = None
    progress_percent: Optional[int] = None
    last_feedback: Optional[str] = None
