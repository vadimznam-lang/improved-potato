from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr

from app.schemas.student import StudentProgressInfo


class TeacherBase(BaseModel):
    name: str
    email: EmailStr


class TeacherCreate(TeacherBase):
    pass


class TeacherResponse(TeacherBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TeacherCommentCreate(BaseModel):
    student_id: int
    comment: str


class TeacherDashboardStudent(BaseModel):
    id: int
    name: str
    email: EmailStr
    progress: StudentProgressInfo | None = None
    points: int
    achievements: List[str]


class TeacherDashboardResponse(BaseModel):
    students: List[TeacherDashboardStudent]
    total_students: int
    average_progress: float
